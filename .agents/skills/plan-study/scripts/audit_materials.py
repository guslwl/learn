#!/usr/bin/env python3
"""Inventory course PDFs and flag likely extraction or completeness problems.

The script is deliberately read-only: it prints Markdown or JSON to stdout and
does not modify the topic directory.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import statistics
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path


SEQUENCE_RE = re.compile(
    r"^(?P<prefix>aula|lecture|lesson|unit|module|modulo|módulo)[ _.-]*(?P<number>\d+)$",
    re.IGNORECASE,
)
WORD_RE = re.compile(r"[^\W\d_]{4,}", re.UNICODE)


@dataclass
class PdfRecord:
    path: str
    pages: int | None
    title: str
    author: str
    creation_date: str
    sampled_pages: int
    sample_characters: int
    flags: list[str] = field(default_factory=list)


def require_program(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(
            f"Required program '{name}' was not found. Install Poppler tools "
            "or audit the PDFs manually."
        )


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors="replace",
    )


def read_pdf_info(pdf: Path) -> tuple[dict[str, str], str | None]:
    result = run(["pdfinfo", str(pdf)])
    if result.returncode != 0:
        message = result.stderr.strip() or f"pdfinfo exited with {result.returncode}"
        return {}, message

    fields: dict[str, str] = {}
    for line in result.stdout.splitlines():
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip()
    return fields, None


def sample_pdf_text(pdf: Path, pages: int | None) -> tuple[int, int, str | None]:
    sample_pages = min(pages, 3) if pages and pages > 0 else 1
    result = run(
        ["pdftotext", "-f", "1", "-l", str(sample_pages), str(pdf), "-"]
    )
    if result.returncode != 0:
        message = result.stderr.strip() or f"pdftotext exited with {result.returncode}"
        return sample_pages, 0, message

    characters = len(re.sub(r"\s+", "", result.stdout))
    return sample_pages, characters, None


def inspect_pdf(pdf: Path, topic_root: Path) -> PdfRecord:
    fields, info_error = read_pdf_info(pdf)
    raw_pages = fields.get("Pages", "")
    pages = int(raw_pages) if raw_pages.isdigit() else None
    sampled_pages, characters, text_error = sample_pdf_text(pdf, pages)

    record = PdfRecord(
        path=pdf.relative_to(topic_root).as_posix(),
        pages=pages,
        title=fields.get("Title", ""),
        author=fields.get("Author", ""),
        creation_date=fields.get("CreationDate", ""),
        sampled_pages=sampled_pages,
        sample_characters=characters,
    )

    if info_error:
        record.flags.append(f"metadata-failed: {info_error}")
    if text_error:
        record.flags.append(f"text-extraction-failed: {text_error}")
    elif sampled_pages and characters / sampled_pages < 80:
        record.flags.append("little-extractable-text")
    if pages is not None and pages <= 2:
        record.flags.append("very-short-pdf")
    filename_words = {word.casefold() for word in WORD_RE.findall(pdf.stem)}
    title_words = {word.casefold() for word in WORD_RE.findall(record.title)}
    if filename_words and title_words and filename_words.isdisjoint(title_words):
        record.flags.append("filename-title-metadata-mismatch")
    return record


def flag_sequence_outliers(records: list[PdfRecord]) -> None:
    groups: dict[tuple[str, str], list[PdfRecord]] = {}

    for record in records:
        relative = Path(record.path)
        match = SEQUENCE_RE.match(relative.stem)
        if match and record.pages is not None:
            key = (relative.parent.as_posix(), match.group("prefix").casefold())
            groups.setdefault(key, []).append(record)

    for group in groups.values():
        page_counts = [record.pages for record in group if record.pages is not None]
        if len(page_counts) < 3:
            continue
        median_pages = statistics.median(page_counts)
        threshold = max(3.0, median_pages * 0.35)
        for record in group:
            if record.pages is not None and record.pages < threshold:
                record.flags.append(
                    f"sequence-page-outlier: {record.pages} pages vs median {median_pages:g}"
                )


def markdown_cell(value: object) -> str:
    if value is None or value == "":
        return "—"
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(topic_root: Path, records: list[PdfRecord]) -> str:
    lines = [
        "# PDF material audit",
        "",
        f"Topic: `{topic_root}`",
        "",
        "| PDF | Pages | Sample text chars | Title | Flags |",
        "|---|---:|---:|---|---|",
    ]
    for record in records:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{markdown_cell(record.path)}`",
                    markdown_cell(record.pages),
                    markdown_cell(record.sample_characters),
                    markdown_cell(record.title),
                    markdown_cell("; ".join(record.flags)),
                ]
            )
            + " |"
        )

    flagged = sum(bool(record.flags) for record in records)
    lines.extend(
        [
            "",
            f"PDFs found: {len(records)}. PDFs with warnings: {flagged}.",
            "",
            "Warnings are review prompts, not proof that a document is invalid.",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory PDFs below a course topic without modifying them."
    )
    parser.add_argument("topic_root", type=Path)
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        dest="output_format",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    topic_root = args.topic_root.expanduser().resolve()
    if not topic_root.is_dir():
        print(f"Topic root is not a directory: {topic_root}", file=sys.stderr)
        return 2

    require_program("pdfinfo")
    require_program("pdftotext")

    pdfs = sorted(
        (
            path
            for path in topic_root.rglob("*")
            if path.is_file() and path.suffix.lower() == ".pdf"
        ),
        key=lambda path: path.relative_to(topic_root).as_posix().casefold(),
    )
    records = [inspect_pdf(pdf, topic_root) for pdf in pdfs]
    flag_sequence_outliers(records)

    if args.output_format == "json":
        payload = {
            "topic_root": str(topic_root),
            "pdf_count": len(records),
            "warning_count": sum(bool(record.flags) for record in records),
            "pdfs": [asdict(record) for record in records],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(topic_root, records))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
