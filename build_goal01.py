# -*- coding: utf-8 -*-
"""
Generate the Goal 01 (Business Builder) supporting document PDF for the
R Systems October Review Cycle 2026 PMS self-assessment.

Matches the visual style of Goal01_BusinessBuilder_Supporting_Doc.pdf:
 - purple header band on every page
 - purple section bars (numbered)
 - purple-header two-column tables
 - dark-purple deliverable sub-bars
 - green-bordered rationale box
 - italic centred footer with "x of y" page numbering

Produces one identical PDF per employee (only Employee + Employee ID differ).
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, KeepTogether,
)
from reportlab.pdfgen import canvas

# ------------------------------------------------------------------ palette
PURPLE       = HexColor("#5A2D82")   # header band / table header / sub-bars
PURPLE_TEXT  = HexColor("#5A2D82")   # purple labels & headings
BAND_LIGHT   = HexColor("#ECE3F3")   # light purple section bars
CELL_LIGHT   = HexColor("#F4EFF8")   # light lavender left cells
GREY_LINE    = HexColor("#BBBBBB")
GREEN_BORDER = HexColor("#4C9A2A")
GREEN_FILL   = HexColor("#F2F8EC")
ITALIC_GREY  = HexColor("#666666")

PAGE_W, PAGE_H = A4
LM = RM = 40
TOPM = 66
BOTM = 46
CONTENT_W = PAGE_W - LM - RM

# ------------------------------------------------------------------ styles
styles = getSampleStyleSheet()

def _s(name, **kw):
    base = kw.pop("parent", styles["Normal"])
    return ParagraphStyle(name, parent=base, **kw)

st_title    = _s("gtitle", fontName="Helvetica-Bold", fontSize=17,
                 textColor=PURPLE_TEXT, spaceAfter=2, leading=20)
st_subtitle = _s("gsub", fontName="Helvetica-Bold", fontSize=11.5,
                 textColor=HexColor("#222222"), spaceAfter=8, leading=14)
st_label    = _s("glabel", fontName="Helvetica-Bold", fontSize=9.5,
                 textColor=PURPLE_TEXT, leading=13)
st_value    = _s("gvalue", fontName="Helvetica", fontSize=9.5,
                 textColor=HexColor("#111111"), leading=13)
st_sect     = _s("gsect", fontName="Helvetica-Bold", fontSize=11,
                 textColor=PURPLE_TEXT, leading=14)
st_subbar   = _s("gsubbar", fontName="Helvetica-Bold", fontSize=9.5,
                 textColor=white, leading=13)
st_thead    = _s("gthead", fontName="Helvetica-Bold", fontSize=9.5,
                 textColor=white, leading=12)
st_tkey     = _s("gtkey", fontName="Helvetica-Bold", fontSize=9,
                 textColor=HexColor("#1a1a1a"), leading=12)
st_tval     = _s("gtval", fontName="Helvetica", fontSize=9,
                 textColor=HexColor("#111111"), leading=12, alignment=TA_JUSTIFY)
st_bullet   = _s("gbul", fontName="Helvetica", fontSize=9.2,
                 textColor=HexColor("#111111"), leading=12.5,
                 alignment=TA_JUSTIFY, leftIndent=14, bulletIndent=3,
                 spaceAfter=1.5)
st_stack    = _s("gstack", fontName="Helvetica-Oblique", fontSize=8.6,
                 textColor=HexColor("#444444"), leading=11, leftIndent=14,
                 spaceBefore=1, spaceAfter=2)
st_rationale= _s("grat", fontName="Helvetica", fontSize=9.1,
                 textColor=HexColor("#0f0f0f"), leading=12.6,
                 alignment=TA_JUSTIFY)
st_tip      = _s("gtip", fontName="Helvetica-Oblique", fontSize=8.4,
                 textColor=HexColor("#8a6d00"), leading=11, spaceBefore=4)


# ------------------------------------------------------------------ helpers
def section_bar(number, title):
    """Light purple full-width bar with purple numbered heading."""
    p = Paragraph(f"{number}.&nbsp;&nbsp;{title}", st_sect)
    t = Table([[p]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BAND_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def sub_bar(text):
    """Dark purple full-width sub-bar (2.1, 2.2 ...) with white bold text."""
    p = Paragraph(text, st_subbar)
    t = Table([[p]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PURPLE),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def kv_table(rows, key_w=150):
    """Two-column table with purple header row + alternating light key cells."""
    data = [[Paragraph(rows[0][0], st_thead), Paragraph(rows[0][1], st_thead)]]
    for k, v in rows[1:]:
        data.append([Paragraph(k, st_tkey), Paragraph(v, st_tval)])
    t = Table(data, colWidths=[key_w, CONTENT_W - key_w], repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, GREY_LINE),
        ("BACKGROUND", (0, 1), (0, -1), CELL_LIGHT),
    ]
    t.setStyle(TableStyle(style))
    return t


def bullets(items):
    return [Paragraph(x, st_bullet, bulletText="-") for x in items]


def stack(text):
    return Paragraph(f"<b>Stack:</b> {text}", st_stack)


def deliverable(title, items, stack_text):
    """Return a list of flowables. The sub-bar is kept together with the first
    bullet to avoid an orphaned header at the bottom of a page, while the rest
    is allowed to flow so pages fill naturally."""
    body = bullets(items)
    flow = [KeepTogether([sub_bar(title), Spacer(1, 3), body[0]])]
    flow += body[1:]
    flow.append(stack(stack_text))
    flow.append(Spacer(1, 7))
    return flow


def rationale_box(paragraphs):
    cell = []
    for i, para in enumerate(paragraphs):
        cell.append(Paragraph(para, st_rationale))
        if i != len(paragraphs) - 1:
            cell.append(Spacer(1, 4))
    t = Table([[cell]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, GREEN_BORDER),
        ("BACKGROUND", (0, 0), (-1, -1), GREEN_FILL),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


# ------------------------------------------------------------------ canvas
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved)
        for state in self._saved:
            self.__dict__.update(state)
            self._draw_header()
            self._draw_footer(total)
            super().showPage()
        super().save()

    def _draw_header(self):
        self.saveState()
        self.setFillColor(PURPLE)
        self.rect(0, PAGE_H - 40, PAGE_W, 40, stroke=0, fill=1)
        self.setFillColor(white)
        self.setFont("Helvetica-Bold", 11)
        self.drawCentredString(
            PAGE_W / 2, PAGE_H - 26,
            "R SYSTEMS INTERNATIONAL   |   OCTOBER REVIEW CYCLE 2026")
        self.restoreState()

    def _draw_footer(self, total):
        self.saveState()
        self.setFillColor(ITALIC_GREY)
        self.setFont("Helvetica-Oblique", 8.5)
        self.drawCentredString(
            PAGE_W / 2, 26,
            f"Prepared for R Systems PMS - October Review Cycle 2026   |   "
            f"{self._pageNumber} of {total}")
        self.restoreState()


# ------------------------------------------------------------------ content
def build_story(name, emp_id):
    story = []

    story.append(Paragraph("Supporting Document - Goal 01", st_title))
    story.append(Paragraph(
        "Contribute Reusable BI Visuals, Measures, or Report Templates (10%)",
        st_subtitle))

    info = [
        ("Employee:", name),
        ("Employee ID:", emp_id),
        ("Review cycle:", "October Review Cycle 2026"),
        ("Self-rating:", "Business Builder"),
        ("Goal metric:", ">= 2 AI-reviewed assets (DAX measures, Power Query "
                          "snippets, report templates) added to team library; "
                          "each reused on >= 1 subsequent report"),
    ]
    info_tbl = Table(
        [[Paragraph(k, st_label), Paragraph(v, st_value)] for k, v in info],
        colWidths=[95, CONTENT_W - 95])
    info_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(info_tbl)
    story.append(Spacer(1, 12))

    # ---- 1. Goal Alignment
    story.append(section_bar(1, "Goal Alignment"))
    story.append(Spacer(1, 6))
    story.append(kv_table([
        ("Goal element", "How addressed"),
        ("Reusable DAX measures",
         "Auto-generated 100+ DAX measures via MetricAI DAX Enrichment Engine "
         "(KPI scoring, time-intelligence, dependency analysis); exported as "
         "reusable Power BI semantic model JSON."),
        ("Reusable visual components",
         "Built a shared visual-component library (KPI bars, metric charts, "
         "severity / priority / confidence badges, shared data-table wrapper) "
         "reused across 10+ Telcortex AI dashboards - the direct equivalent of "
         "shared Power BI themes and custom visuals."),
        ("Report templates",
         "Report Rebinder converts Import-mode PBIX to DirectQuery PBIP models; "
         "template reusable for all future AAS-to-Power BI migrations."),
        ("Power Query / TMDL assets",
         "TMDL Extractor auto-exports Power BI semantic model definitions "
         "(TMDL) from Azure Analysis Services; removes 100% of manual export "
         "effort."),
        ("Excel-to-PBI templates",
         "SQL Server and Excel to cloud platforms provides an Excel-to-DAX "
         "formula converter and chart-to-Power BI visual mapper that convert "
         "Excel KPI sheets into reusable Power BI templates."),
        ("Reusable measure modules",
         "Shared formula modules (CSSR, TCH drop, MOS and availability with RAG "
         "grading; ARPU -> annualized revenue exposure) reused across multiple "
         "reports - the analog of a central DAX measure table."),
        ("AI review before library add",
         "Every asset passes a human approval / stakeholder review gate before "
         "entering the library; the R Systems SPOT Award confirms the quality "
         "standard."),
        ("Reused on > 1 report",
         "MetricAI tools reused across Novigo Phase 1 and Phase 2; "
         "cloud-migration templates reused across SQL Server and Excel targets; "
         "Telcortex components reused across 10+ dashboards."),
    ]))
    story.append(Spacer(1, 12))

    # ---- 2. Key Deliverables
    story.append(section_bar(2, "Key Deliverables"))
    story.append(Spacer(1, 6))

    story.extend(deliverable(
        "2.1  MetricAI - AAS to Power BI Semantic Migration Accelerator",
        [
            "TMDL Extractor - auto-exports Power BI semantic model definitions "
            "(.tmdl) from Azure Analysis Services via SSMS; eliminates 100% of "
            "manual export effort.",
            "DAX Enrichment Engine - LLM-assisted pipeline reads AAS measure "
            "metadata, enriches with KPI categories and business-friendly "
            "names, and generates reusable Power BI semantic model JSON "
            "artefacts.",
            "Report Rebinder - converts Import-mode PBIX to DirectQuery PBIP "
            "models connected to Databricks SQL Warehouse; the rebinding logic "
            "is reusable for all future AAS migrations.",
            "Delivered to Novigo client; R Systems SPOT Award received for "
            "Outstanding Performance.",
            "100+ DAX measures, TMDL exports, PBIP templates - all "
            "peer-reviewed before production use.",
        ],
        "Python | Flask | Azure Analysis Services | Databricks SQL Warehouse | "
        "Power BI TMDL | PBIP | DAX"))

    story.extend(deliverable(
        "2.2  SQL Server and Excel to cloud platforms - Excel & SQL Server to "
        "Cloud Migration Platform",
        [
            "Excel-to-DAX formula converter: maps Excel calculation formulas to "
            "equivalent Power BI DAX measures.",
            "Chart-to-Power BI visual mapper: converts Excel KPI chart "
            "definitions to Power BI visual configs - reusable Power BI report "
            "template JSON output.",
            "9-stage Excel pre-migration assessment pipeline produces a Power "
            "BI readiness report before publish.",
            "Reused across SQL Server -> Snowflake, SQL Server -> Microsoft "
            "Fabric Lakehouse, and Excel -> Power BI.",
        ],
        "Python | pandas | openpyxl | Snowflake SQL | Microsoft Fabric | "
        "Azure Data Factory | Power BI"))

    story.extend(deliverable(
        "2.3  Telcortex AI - Real-Time Telecom Intelligence Platform "
        "(BeEXIQO Code-AI-Thon 2026, 1st Place)",
        [
            "Reusable visual-component library reused across 10+ dashboards: "
            "TelecomKPIBar, MetricsCharts, ImpactLedger, SeverityBadge, "
            "PriorityTierBadge, ConfidenceBar, and a shared data-table wrapper "
            "- the analog of shared Power BI themes and custom visuals.",
            "Reusable 'measures' as shared formula modules: a KPI service "
            "(CSSR, TCH drop, MOS, availability with RAG grading) and a "
            "revenue-exposure estimator (ARPU -> annualized revenue), mirrored "
            "on the frontend - the analog of a central DAX measure table.",
            "Shared time-range selector and a common utility library "
            "(risk-score, duration and severity-colour formatters) - the "
            "reusable date-table / common-KPI / page-layout pattern the goal "
            "asks for.",
        ],
        "Python | Flask | Next.js | TypeScript | Groq (Llama 3.1) | Redis | "
        "PostgreSQL"))

    story.extend(deliverable(
        "2.4  Stonex POC - Reusable BI Repair & Data-Contract Assets",
        [
            "Contributed reusable, parameterized engineering assets: a "
            "schema-diff and rename-detection module, a SAFE / RISKY "
            "repair-classification module, and a table-agnostic data-freshness "
            "/ gap-check harness that works against any source-target pair by "
            "configuration.",
            "Established two repeatable patterns: a 'contract layer' "
            "(compatibility view) that keeps existing report visuals and "
            "measures working during upstream schema changes, and a DDL "
            "allow-list safety guard that constrains blast radius.",
            "Every change flows through a human approval gate - nothing is "
            "applied until the exact SQL is reviewed and approved - and all "
            "assets are documented so others can reuse them without "
            "reverse-engineering the code.",
        ],
        "Python | SQL | Databricks / Delta | Power BI | Model Context Protocol"))

    story.extend(deliverable(
        "2.5  Domo -> Snowflake + Power BI Migration - LambWeston "
        "(Fortune 500)",
        [
            "Automated Power BI workspace publishing with semantic model JSON "
            "generation - consistent naming conventions, correct measure "
            "aggregations, and slicers mapped from Domo filter definitions.",
            "All Power BI visuals mapped from Domo card types to semantically "
            "equivalent Power BI visual types.",
            "Semantic model JSON published and verified end-to-end before "
            "client sign-off.",
        ],
        "Python | Snowflake | Power BI REST API | Semantic Model JSON | "
        "Domo API"))

    story.extend(deliverable(
        "2.6  Decision Intelligence - Enterprise AI Data Intelligence Platform",
        [
            "Built reusable analytical building blocks: shared metric / measure "
            "definitions and multi-source query templates that run directly at "
            "the source across SQL Server, PostgreSQL, Snowflake and Databricks "
            "without moving data.",
            "Reusable front-end component set (result tables, query panels, "
            "review views) and a governed tool-routing layer reused across "
            "every question type.",
            "A multi-stage answer-quality review applied consistently so "
            "reusable outputs meet a trust bar before they are displayed.",
        ],
        "React | TypeScript | Node.js | PostgreSQL | Neo4j | Snowflake | "
        "OpenAI / Anthropic"))

    # ---- 3. Metrics & Evidence
    story.append(section_bar(3, "Metrics & Evidence"))
    story.append(Spacer(1, 6))
    story.append(kv_table([
        ("Metric / Deliverable", "Evidence"),
        (">= 2 reviewed AI assets",
         "MetricAI alone delivers 3 distinct reusable artefact types; across "
         "projects 6+ reusable asset families were delivered - far exceeds the "
         "minimum of 2."),
        ("Peer-reviewed before library",
         "Novigo stakeholder review + SPOT Award (external and internal "
         "review); Stonex applies a human approval gate on every change."),
        ("Reused on >= 1 report",
         "TMDL + DAX artefacts reused across Novigo Phase 1 and Phase 2; "
         "cloud-migration templates reused across SQL Server and Excel targets; "
         "Telcortex components reused across 10+ dashboards."),
        ("100+ DAX measures generated",
         "DAX Enrichment Engine: KPI-scoring, time-intelligence and "
         "dependency-analysis measure library."),
        ("Reusable visual library",
         "Telcortex shared components (KPI bar, charts, badges, table wrapper) "
         "reused across 10+ dashboards."),
        ("Fortune 500 delivery",
         "LambWeston - Power BI semantic model JSON published and verified "
         "end-to-end."),
        ("SPOT Award received",
         "R Systems SPOT Award for Outstanding Performance on MetricAI - "
         "validates BI quality."),
    ]))
    story.append(Spacer(1, 12))

    # ---- 4. Rationale
    story.append(section_bar(4, 'Rationale  (copy-paste into PMS "Add '
                               'Rationale" box)'))
    story.append(Spacer(1, 6))
    story.append(rationale_box(RATIONALE))
    story.append(Paragraph(
        'Tip: Copy the text above into the PMS "Add Rationale" box. '
        "Max 20,000 characters.", st_tip))

    return story


# ------------------------------------------------------------------ rationale
RATIONALE = [
    "This cycle my central contribution against Goal 01 was building "
    "reusable BI assets - measures, visuals, and report templates - that the "
    "team can apply across many reports instead of rebuilding them each time. "
    "Rather than shipping one-off dashboards, I engineered libraries and "
    "repeatable patterns, put every asset through a review gate before it "
    "entered the library, and then reused them on subsequent reports. Across "
    "the projects below I delivered six distinct families of reusable assets, "
    "comfortably exceeding the goal minimum of two AI-reviewed assets each "
    "reused on at least one further report.",

    "MetricAI (AAS to Power BI Semantic Migration Accelerator) is my "
    "strongest evidence. It produced three distinct reusable artefact types "
    "that output production-ready Power BI semantic model artefacts directly "
    "from Azure Analysis Services source models. The TMDL Extractor "
    "auto-exports Power BI semantic model definitions (.tmdl) and removed 100% "
    "of the manual export effort; the DAX Enrichment Engine is an LLM-assisted "
    "pipeline that reads AAS measure metadata and generated 100+ reusable DAX "
    "measures enriched with KPI categories, time-intelligence and "
    "dependency-analysis, exported as reusable semantic model JSON; and the "
    "Report Rebinder converts Import-mode PBIX into DirectQuery PBIP templates "
    "connected to Databricks SQL Warehouse, with rebinding logic reusable for "
    "all future AAS migrations. These assets were peer-reviewed before "
    "production use and reused across two Novigo delivery phases, and the "
    "delivery earned the R Systems SPOT Award for Outstanding Performance, "
    "confirming the reusable assets met client and leadership quality "
    "standards.",

    "SQL Server and Excel to cloud platforms added two further reusable "
    "templates: an Excel-to-DAX formula converter that maps Excel calculation "
    "formulas to equivalent Power BI DAX measures, and a chart-to-Power BI "
    "visual mapper that converts Excel KPI chart definitions into Power BI "
    "visual configs and emits reusable Power BI report-template JSON. A "
    "9-stage pre-migration assessment produces a Power BI readiness report "
    "before publish. These templates were validated and reused across SQL "
    "Server -> Snowflake, SQL Server -> Microsoft Fabric Lakehouse, and "
    "Excel -> Power BI targets, so the same assets served multiple downstream "
    "reports rather than a single deliverable.",

    "Telcortex AI is a genuine reusable-component strength area. I built a "
    "library of reusable visual components - TelecomKPIBar, MetricsCharts, "
    "ImpactLedger, SeverityBadge, PriorityTierBadge, ConfidenceBar and a "
    "shared data-table wrapper - that were reused across 10+ dashboards, the "
    "direct equivalent of shared Power BI themes and custom visuals. I also "
    "created reusable 'measures' as shared formula modules: a KPI service "
    "computing CSSR, TCH drop, MOS and availability with RAG grading, and a "
    "revenue-exposure estimator turning ARPU into annualized revenue, mirrored "
    "on the frontend so the same logic is reused everywhere - the analog of a "
    "central DAX measure table. A shared time-range selector and a common "
    "utility library (risk-score, duration and severity-colour formatters) "
    "provided the reusable date-table / common-KPI / page-layout pattern the "
    "goal describes. This work won 1st place at the BeEXIQO Code-AI-Thon 2026.",

    "Stonex POC extended the same discipline to reusable data-repair and "
    "data-contract assets: a schema-diff and rename-detection module, a "
    "SAFE / RISKY repair-classification module, and a table-agnostic "
    "data-freshness / gap-check harness that works against any source-target "
    "pair purely by configuration. I established two repeatable patterns that "
    "protect BI reports directly - a 'contract layer' (compatibility view) "
    "that keeps existing report visuals and measures working during upstream "
    "schema changes, and a DDL allow-list safety guard that constrains blast "
    "radius. Every change flows through a human approval gate: nothing is "
    "applied until the exact SQL is reviewed and approved, and each asset is "
    "documented so others can reuse it without reverse-engineering the code.",

    "Two further deliveries reinforce the goal. On the Domo -> Snowflake + "
    "Power BI migration for LambWeston (Fortune 500) I automated Power BI "
    "workspace publishing with semantic model JSON generation - consistent "
    "naming conventions, correct measure aggregations, and slicers mapped from "
    "Domo filter definitions - mapping all visuals from Domo card types to "
    "semantically equivalent Power BI visual types and verifying the JSON "
    "end-to-end before client sign-off. On Decision Intelligence I built "
    "reusable analytical building blocks - shared metric / measure definitions "
    "and multi-source query templates that run directly at the source across "
    "SQL Server, PostgreSQL, Snowflake and Databricks - plus a reusable "
    "front-end component set and a governed tool-routing layer reused across "
    "every question type.",

    "Taken together, every asset above cleared the goal bar: at least two "
    "AI-reviewed reusable assets - in practice six distinct families - each "
    "passed a review or approval gate before entering the library, and each "
    "was reused on more than one subsequent report or dashboard. The "
    "consistent theme is engineering for reuse and review rather than one-off "
    "output, which is exactly what a Business Builder rating recognises.",
]


# ------------------------------------------------------------------ build
def build_pdf(name, emp_id, out_path):
    doc = BaseDocTemplate(
        out_path, pagesize=A4,
        leftMargin=LM, rightMargin=RM, topMargin=TOPM, bottomMargin=BOTM,
        title=f"Supporting Document - Goal 01 - {name}",
        author=name)
    frame = Frame(LM, BOTM, CONTENT_W, PAGE_H - TOPM - BOTM, id="main",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="tmpl", frames=[frame])])
    doc.build(build_story(name, emp_id), canvasmaker=NumberedCanvas)
    print("SAVED:", out_path)


if __name__ == "__main__":
    base = r"C:\Users\bali\Desktop\Mohan\CVs"
    build_pdf("Bali Mohan Rao", "19031",
              base + r"\Goal01_BusinessBuilder_BaliMohanRao_19031.pdf")
    build_pdf("Tanuja Subhash Shinde", "19038",
              base + r"\Goal01_BusinessBuilder_TanujaSubhashShinde_19038.pdf")
    # character count sanity check for the rationale
    total = sum(len(p) for p in RATIONALE)
    print("Rationale characters:", total)
