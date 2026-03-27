#!/usr/bin/env python3
"""Build a spreadsheet workbook for blog-consolidation monitoring.

The workbook is dependency-free and writes a minimal XLSX file with four tabs:
- Redirect Verification
- Cannibalization Monitor
- Broken Link Audit
- Content Calendar
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import zipfile
from dataclasses import dataclass
from pathlib import Path


DEFAULT_OUTPUT = Path("ops/seo/dresslikemommy-blog-consolidation-monitoring-checklist.xlsx")
SITE_ROOT = "https://www.dresslikemommy.com"


@dataclass(frozen=True)
class SheetSpec:
    name: str
    headers: tuple[str, ...]
    widths: tuple[float, ...]
    rows: tuple[tuple[str, ...], ...]


SEASONAL_TOPICS = (
    (
        "Mommy and me Valentine's Day outfits",
        f"{SITE_ROOT}/blogs/news/mommy-and-me-valentines-day-outfits",
        "mommy and me valentines day outfit ideas",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ),
    (
        "Mother-daughter matching dresses for Easter",
        f"{SITE_ROOT}/blogs/news/mother-daughter-matching-dresses-for-easter",
        "mother daughter matching dresses for easter",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ),
    (
        "Mommy and me Easter dresses",
        f"{SITE_ROOT}/blogs/news/mommy-and-me-easter-dresses-2026",
        "mommy and me easter dresses",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ),
    (
        "Family matching outfits for spring photos",
        f"{SITE_ROOT}/blogs/news/family-matching-outfits-spring-photos",
        "family matching outfits for spring photos",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ),
    (
        "Daddy and me outfit ideas for Father's Day",
        f"{SITE_ROOT}/blogs/news/daddy-and-me-outfit-ideas-for-fathers-day",
        "daddy and me outfit ideas for father's day",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ),
    (
        "Family vacation outfits",
        f"{SITE_ROOT}/blogs/news/family-vacation-outfits-beach-cruise-resort",
        "matching family vacation outfits",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ),
    (
        "Mommy and me beach dresses",
        f"{SITE_ROOT}/blogs/news/mommy-and-me-beach-dresses-vacation-photos",
        "mommy and me beach dresses",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ),
    (
        "Best family swimsuits",
        f"{SITE_ROOT}/blogs/news/best-family-swimsuits-for-beach-vacations-and-pool-days",
        "family matching swimsuits",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ),
    (
        "Mother-daughter matching swimsuits",
        f"{SITE_ROOT}/blogs/news/mother-daughter-matching-swimsuits-complete-guide-for-summer-2026",
        "mother daughter matching swimsuits",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ),
    (
        "Daddy and me matching shirts",
        f"{SITE_ROOT}/blogs/news/daddy-and-me-matching-shirts-summer-photos",
        "daddy and me matching shirts",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ),
    (
        "Family reunion matching shirts",
        f"{SITE_ROOT}/blogs/news/family-reunion-matching-shirts-outfit-ideas",
        "family reunion matching shirts",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ),
    (
        "Matching family outfits for Disney trips",
        f"{SITE_ROOT}/blogs/news/matching-family-outfits-for-disney-trips",
        "matching family outfits for disney trips",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ),
    (
        "Matching family cruise outfits",
        f"{SITE_ROOT}/blogs/news/matching-family-cruise-outfits-what-to-pack",
        "matching family cruise outfits",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ),
    (
        "Family matching pajamas ideas",
        f"{SITE_ROOT}/blogs/news/family-matching-pajamas-our-top-picks-for-cozy-nights",
        "family matching pajamas ideas",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ),
)


CONTENT_CALENDAR_ROWS = (
    (
        f"{SITE_ROOT}/blogs/news/mommy-and-me-valentines-day-outfits",
        "Mommy and me Valentine's Day outfits",
        "Valentine's Day",
        "",
        "",
        "",
        "",
    ),
    (
        f"{SITE_ROOT}/blogs/news/mother-daughter-matching-dresses-for-easter",
        "Mother-daughter matching dresses for Easter",
        "Easter",
        "",
        "",
        "",
        "",
    ),
    (
        f"{SITE_ROOT}/blogs/news/mommy-and-me-easter-dresses-2026",
        "Mommy and me Easter dresses",
        "Easter",
        "",
        "",
        "",
        "",
    ),
    (
        f"{SITE_ROOT}/blogs/news/family-matching-outfits-spring-photos",
        "Family matching outfits for spring photos",
        "Spring",
        "",
        "",
        "",
        "",
    ),
    (
        f"{SITE_ROOT}/blogs/news/daddy-and-me-outfit-ideas-for-fathers-day",
        "Daddy and me outfit ideas for Father's Day",
        "Father's Day",
        "",
        "",
        "",
        "",
    ),
    (
        f"{SITE_ROOT}/blogs/news/family-vacation-outfits-beach-cruise-resort",
        "Family vacation outfits",
        "Summer vacation",
        "",
        "",
        "",
        "",
    ),
    (
        f"{SITE_ROOT}/blogs/news/mommy-and-me-beach-dresses-vacation-photos",
        "Mommy and me beach dresses",
        "Summer vacation",
        "",
        "",
        "",
        "",
    ),
    (
        f"{SITE_ROOT}/blogs/news/best-family-swimsuits-for-beach-vacations-and-pool-days",
        "Best family swimsuits",
        "Summer",
        "",
        "",
        "",
        "",
    ),
    (
        f"{SITE_ROOT}/blogs/news/mother-daughter-matching-swimsuits-complete-guide-for-summer-2026",
        "Mother-daughter matching swimsuits",
        "Summer",
        "",
        "",
        "",
        "",
    ),
    (
        f"{SITE_ROOT}/blogs/news/daddy-and-me-matching-shirts-summer-photos",
        "Daddy and me matching shirts",
        "Summer",
        "",
        "",
        "",
        "",
    ),
    (
        f"{SITE_ROOT}/blogs/news/family-reunion-matching-shirts-outfit-ideas",
        "Family reunion matching shirts",
        "Summer events",
        "",
        "",
        "",
        "",
    ),
    (
        f"{SITE_ROOT}/blogs/news/matching-family-outfits-for-disney-trips",
        "Matching family outfits for Disney trips",
        "Summer travel",
        "",
        "",
        "",
        "",
    ),
    (
        f"{SITE_ROOT}/blogs/news/matching-family-cruise-outfits-what-to-pack",
        "Matching family cruise outfits",
        "Cruise travel",
        "",
        "",
        "",
        "",
    ),
    (
        f"{SITE_ROOT}/blogs/news/family-matching-pajamas-our-top-picks-for-cozy-nights",
        "Family matching pajamas ideas",
        "Christmas and holiday pajamas",
        "",
        "",
        "",
        "",
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="XLSX output path")
    return parser.parse_args()


def column_name(index: int) -> str:
    value = index
    label = []
    while value > 0:
        value, remainder = divmod(value - 1, 26)
        label.append(chr(65 + remainder))
    return "".join(reversed(label))


def escape_inline(value: str) -> str:
    return html.escape(value, quote=False)


def build_cell(cell_ref: str, value: str, *, header: bool = False) -> str:
    style = ' s="1"' if header else ""
    return (
        f'<c r="{cell_ref}" t="inlineStr"{style}>'
        f"<is><t>{escape_inline(value)}</t></is>"
        "</c>"
    )


def build_sheet_xml(spec: SheetSpec) -> str:
    all_rows = [spec.headers, *spec.rows]
    max_row = len(all_rows)
    max_col = len(spec.headers)
    dimension = f"A1:{column_name(max_col)}{max_row}"
    cols_xml = []
    for index, width in enumerate(spec.widths, start=1):
        cols_xml.append(
            f'<col min="{index}" max="{index}" width="{width}" customWidth="1"/>'
        )

    row_xml = []
    for row_index, row in enumerate(all_rows, start=1):
        cells = []
        for col_index, value in enumerate(row, start=1):
            if value == "":
                continue
            cells.append(
                build_cell(
                    f"{column_name(col_index)}{row_index}",
                    value,
                    header=row_index == 1,
                )
            )
        row_xml.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    auto_filter_ref = f"A1:{column_name(max_col)}1"
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<dimension ref="{dimension}"/>'
        '<sheetViews><sheetView workbookViewId="0">'
        '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
        '<selection pane="bottomLeft" activeCell="A2" sqref="A2"/>'
        '</sheetView></sheetViews>'
        '<sheetFormatPr defaultRowHeight="15"/>'
        f'<cols>{"".join(cols_xml)}</cols>'
        f'<sheetData>{"".join(row_xml)}</sheetData>'
        f'<autoFilter ref="{auto_filter_ref}"/>'
        '</worksheet>'
    )


def build_sheets() -> tuple[SheetSpec, ...]:
    return (
        SheetSpec(
            name="Redirect Verification",
            headers=(
                "old_url",
                "new_canonical_url",
                "redirect_created_date",
                "redirect_verified (Y/N)",
                "GSC_old_url_removed_from_index (Y/N)",
                "GSC_canonical_indexed (Y/N)",
                "check_date",
            ),
            widths=(42, 42, 22, 22, 32, 26, 18),
            rows=(),
        ),
        SheetSpec(
            name="Cannibalization Monitor",
            headers=(
                "topic",
                "canonical_url",
                "query (from GSC)",
                "impressions_before",
                "clicks_before",
                "position_before",
                "impressions_after_30d",
                "clicks_after_30d",
                "position_after_30d",
                "competing_urls_count_before",
                "competing_urls_count_after",
            ),
            widths=(34, 48, 28, 18, 14, 16, 20, 18, 18, 28, 28),
            rows=SEASONAL_TOPICS,
        ),
        SheetSpec(
            name="Broken Link Audit",
            headers=(
                "source_url",
                "broken_link_url",
                "status_code",
                "found_date",
                "fixed_date",
                "fixed_by",
            ),
            widths=(42, 42, 14, 18, 18, 18),
            rows=(),
        ),
        SheetSpec(
            name="Content Calendar",
            headers=(
                "canonical_url",
                "topic",
                "season",
                "last_refreshed_date",
                "next_refresh_due",
                "products_updated (Y/N)",
                "refresh_assignee",
            ),
            widths=(48, 34, 24, 20, 20, 22, 22),
            rows=CONTENT_CALENDAR_ROWS,
        ),
    )


def write_workbook(output_path: Path, sheets: tuple[SheetSpec, ...]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    created = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as workbook:
        workbook.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/styles.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
            '<Override PartName="/docProps/core.xml" '
            'ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
            '<Override PartName="/docProps/app.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
            + "".join(
                f'<Override PartName="/xl/worksheets/sheet{index}.xml" '
                'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                for index in range(1, len(sheets) + 1)
            )
            + "</Types>",
        )
        workbook.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="xl/workbook.xml"/>'
            '<Relationship Id="rId2" '
            'Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" '
            'Target="docProps/core.xml"/>'
            '<Relationship Id="rId3" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" '
            'Target="docProps/app.xml"/>'
            "</Relationships>",
        )
        workbook.writestr(
            "docProps/core.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties '
            'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>Dress Like Mommy Blog Consolidation Monitoring Checklist</dc:title>'
            '<dc:creator>Codex</dc:creator>'
            '<cp:lastModifiedBy>Codex</cp:lastModifiedBy>'
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{created}</dcterms:created>'
            f'<dcterms:modified xsi:type="dcterms:W3CDTF">{created}</dcterms:modified>'
            "</cp:coreProperties>",
        )
        workbook.writestr(
            "docProps/app.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            '<Application>Codex</Application>'
            '</Properties>',
        )
        workbook.writestr(
            "xl/workbook.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<bookViews><workbookView xWindow="0" yWindow="0" windowWidth="24000" windowHeight="14000"/></bookViews>'
            "<sheets>"
            + "".join(
                f'<sheet name="{escape_inline(sheet.name)}" sheetId="{index}" r:id="rId{index}"/>'
                for index, sheet in enumerate(sheets, start=1)
            )
            + "</sheets>"
            "</workbook>",
        )
        workbook.writestr(
            "xl/_rels/workbook.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(
                f'<Relationship Id="rId{index}" '
                'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
                f'Target="worksheets/sheet{index}.xml"/>'
                for index in range(1, len(sheets) + 1)
            )
            + f'<Relationship Id="rId{len(sheets) + 1}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
            'Target="styles.xml"/>'
            "</Relationships>",
        )
        workbook.writestr(
            "xl/styles.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<fonts count="2">'
            '<font><sz val="11"/><name val="Aptos"/></font>'
            '<font><b/><sz val="11"/><name val="Aptos"/></font>'
            '</fonts>'
            '<fills count="2">'
            '<fill><patternFill patternType="none"/></fill>'
            '<fill><patternFill patternType="gray125"/></fill>'
            '</fills>'
            '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
            '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
            '<cellXfs count="2">'
            '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
            '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>'
            '</cellXfs>'
            '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
            '</styleSheet>',
        )
        for index, sheet in enumerate(sheets, start=1):
            workbook.writestr(f"xl/worksheets/sheet{index}.xml", build_sheet_xml(sheet))


def main() -> None:
    args = parse_args()
    sheets = build_sheets()
    write_workbook(args.output, sheets)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
