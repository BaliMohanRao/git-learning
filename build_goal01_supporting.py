# -*- coding: utf-8 -*-
"""
Generate the Goal 01 Supporting Document PDF (Contribute Reusable BI Visuals,
Measures, or Report Templates) - Business Builder rating.

Produces two IDENTICAL PDFs that differ only in Employee name + Employee ID:
  - Bali Mohan Rao      | 19031
  - Tanuja Subhash Shinde | 19038

Format mirrors: Goal01_BusinessBuilder_Supporting_Doc.pdf
The "Evidence to Upload" section is intentionally EXCLUDED so the PDF is
ready to upload as-is.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, KeepTogether,
)

# ---------------------------------------------------------------- palette
NAVY = colors.HexColor("#1F3864")
BLUE = colors.HexColor("#2E74B5")
LIGHT = colors.HexColor("#EAF0F7")
SILVER = colors.HexColor("#C0C0C0")
GREEN = colors.HexColor("#1E6B3A")

HEADER_TEXT = "R SYSTEMS INTERNATIONAL  |  OCTOBER REVIEW CYCLE 2026"
FOOTER_TEXT = "Prepared for R Systems PMS - October Review Cycle 2026"

# ---------------------------------------------------------------- styles
styles = getSampleStyleSheet()


def S(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)


st_title = S("t_title", fontName="Helvetica-Bold", fontSize=15, textColor=NAVY,
             spaceAfter=2, leading=18)
st_sub = S("t_sub", fontName="Helvetica-Bold", fontSize=11, textColor=BLUE,
           spaceAfter=8, leading=14)
st_meta = S("t_meta", fontName="Helvetica", fontSize=9.5, textColor=colors.black,
            leading=13)
st_h = S("t_h", fontName="Helvetica-Bold", fontSize=11.5, textColor=BLUE,
         spaceBefore=10, spaceAfter=5, leading=14)
st_sh = S("t_sh", fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
          spaceBefore=6, spaceAfter=2, leading=13)
st_body = S("t_body", fontName="Helvetica", fontSize=9.3, alignment=TA_JUSTIFY,
            leading=13, spaceAfter=3)
st_bul = S("t_bul", fontName="Helvetica", fontSize=9.3, alignment=TA_LEFT,
           leading=12.5, leftIndent=12, bulletIndent=2, spaceAfter=2)
st_stack = S("t_stack", fontName="Helvetica-Oblique", fontSize=8.8,
             textColor=colors.HexColor("#333333"), leading=12, spaceAfter=2)
st_rat = S("t_rat", fontName="Helvetica", fontSize=9.3, alignment=TA_JUSTIFY,
           textColor=GREEN, leading=13.5, spaceAfter=6)
st_cell = S("t_cell", fontName="Helvetica", fontSize=8.8, leading=11.5)
st_cellb = S("t_cellb", fontName="Helvetica-Bold", fontSize=8.8, leading=11.5,
             textColor=NAVY)
st_tip = S("t_tip", fontName="Helvetica-Oblique", fontSize=8.5,
           textColor=colors.HexColor("#555555"), leading=11, spaceBefore=4)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def bullet(text):
    return Paragraph("&bull;&nbsp;&nbsp;" + text, st_bul)


# ---------------------------------------------------------------- header/footer
def make_decorator(employee, empid):
    def deco(canvas, doc):
        canvas.saveState()
        w, h = letter
        # top band
        canvas.setFillColor(NAVY)
        canvas.rect(0, h - 0.55 * inch, w, 0.55 * inch, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawString(0.7 * inch, h - 0.36 * inch, HEADER_TEXT)
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(w - 0.7 * inch, h - 0.36 * inch,
                               employee + "  |  Emp ID: " + empid)
        # footer line
        canvas.setStrokeColor(SILVER)
        canvas.setLineWidth(0.6)
        canvas.line(0.7 * inch, 0.62 * inch, w - 0.7 * inch, 0.62 * inch)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.setFont("Helvetica", 7.8)
        canvas.drawString(0.7 * inch, 0.45 * inch, FOOTER_TEXT)
        canvas.drawRightString(w - 0.7 * inch, 0.45 * inch,
                               "Page %d" % doc.page)
        canvas.restoreState()
    return deco


# ---------------------------------------------------------------- content
def two_col_table(rows, w1, w2, header=("", "")):
    data = []
    if header[0]:
        data.append([Paragraph(esc(header[0]), st_cellb),
                     Paragraph(esc(header[1]), st_cellb)])
    for a, b in rows:
        data.append([Paragraph(a, st_cellb), Paragraph(b, st_cell)])
    t = Table(data, colWidths=[w1, w2])
    ts = [
        ("GRID", (0, 0), (-1, -1), 0.5, SILVER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT]),
    ]
    if header[0]:
        ts.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D6E1F0")))
    t.setStyle(TableStyle(ts))
    return t


def build(employee, empid, out_path):
    doc = BaseDocTemplate(
        out_path, pagesize=letter,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.72 * inch, bottomMargin=0.78 * inch,
        title="Supporting Document - Goal 01 - " + employee,
        author=employee,
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height, id="main")
    deco = make_decorator(employee, empid)
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=deco)])

    e = []

    # ---- title block
    e.append(Paragraph("Supporting Document &mdash; Goal 01", st_title))
    e.append(Paragraph("Contribute Reusable BI Visuals, Measures, or Report "
                       "Templates (10%)", st_sub))
    meta = ("<b>Employee:</b> %s&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;"
            "<b>Employee ID:</b> %s<br/>"
            "<b>Review cycle:</b> October Review Cycle 2026&nbsp;&nbsp;&nbsp;"
            "|&nbsp;&nbsp;&nbsp;<b>Self-rating:</b> Business Builder<br/>"
            "<b>Goal metric:</b> &gt;= 2 AI-reviewed assets (DAX measures, "
            "Power Query snippets, report templates) added to team library; "
            "each reused on &gt;= 1 subsequent report.") % (esc(employee), esc(empid))
    e.append(Paragraph(meta, st_meta))
    e.append(Spacer(1, 6))

    # ---- Section 1: Goal alignment
    e.append(Paragraph("1.&nbsp;&nbsp;Goal Alignment", st_h))
    align_rows = [
        ("Reusable DAX measures",
         "Auto-generated 100+ DAX measures via the MetricAI DAX Enrichment "
         "Engine (KPI scoring, time-intelligence, dependency analysis); "
         "exported as a reusable Power BI semantic model JSON."),
        ("Report templates",
         "MetricAI Report Rebinder converts Import-mode PBIX to DirectQuery "
         "PBIP models; the rebinding template is reusable for all future "
         "AAS-to-Power BI migrations."),
        ("Power Query / TMDL assets",
         "MetricAI TMDL Extractor auto-exports Power BI semantic model "
         "definitions (.tmdl) from Azure Analysis Services; removes 100% of "
         "manual export effort."),
        ("Excel-to-PBI templates",
         "SQL Server and Excel to cloud platforms provides an Excel-to-DAX "
         "formula converter and a chart-to-Power BI visual mapper that turn "
         "Excel KPI sheets into reusable Power BI report templates (JSON)."),
        ("Reusable visual library",
         "Telcortex AI shared visual components (TelecomKPIBar, MetricsCharts, "
         "ImpactLedger, SeverityBadge, PriorityTierBadge, ConfidenceBar) "
         "reused across 10+ dashboards - the equivalent of shared Power BI "
         "themes/visuals."),
        ("Reusable measure modules",
         "Telcortex kpi_service (CSSR, TCH drop, MOS, availability with RAG "
         "grading) and revenue-exposure-estimate (ARPU -&gt; annualized "
         "revenue), reused across multiple reports - the analog of a central "
         "DAX measure table."),
        ("Reusable engineering assets",
         "StoneX POC schema-diff / rename-detection, SAFE/RISKY repair-"
         "classification, and a table-agnostic freshness/gap-check harness "
         "that work against any source-target pair purely by configuration, "
         "plus a reusable 'contract layer' compatibility view."),
        ("AI/human review before library add",
         "All assets passed a review gate: Novigo stakeholder review, and "
         "StoneX human approval before any SQL is applied. The R Systems SPOT "
         "Award confirms the quality standard."),
        ("Reused on &gt; 1 report",
         "MetricAI tools reused across Novigo Phase 1 and Phase 2; SQL Server "
         "and Excel to cloud platforms templates reused across SQL Server and "
         "Excel targets; Telcortex components reused across 10+ dashboards."),
    ]
    e.append(two_col_table(align_rows, 1.55 * inch, 5.55 * inch,
                           header=("Goal element", "How addressed")))
    e.append(Spacer(1, 4))

    # ---- Section 2: Key deliverables
    e.append(Paragraph("2.&nbsp;&nbsp;Key Deliverables", st_h))

    def deliverable(title, bullets, stack):
        blk = [Paragraph(esc(title), st_sh)]
        for b in bullets:
            blk.append(bullet(b))
        blk.append(Paragraph("<b>Stack:</b> " + esc(stack), st_stack))
        return KeepTogether(blk)

    e.append(deliverable(
        "2.1  MetricAI - AAS to Power BI Semantic Migration Accelerator",
        [
            "TMDL Extractor - auto-exports Power BI semantic model definitions "
            "(.tmdl) from Azure Analysis Services via SSMS; eliminates 100% of "
            "manual export effort.",
            "DAX Enrichment Engine - LLM-assisted pipeline that reads AAS "
            "measure metadata, enriches it with KPI categories and business-"
            "friendly names, and generates 100+ reusable DAX measures as a "
            "Power BI semantic model JSON artefact.",
            "Report Rebinder - converts Import-mode PBIX to DirectQuery PBIP "
            "models connected to a Databricks SQL Warehouse; the rebinding "
            "logic is reusable for all future AAS migrations.",
            "Delivered to the Novigo client and reused across Phase 1 and "
            "Phase 2; earned the R Systems SPOT Award for Outstanding "
            "Performance. All 100+ DAX measures, TMDL exports, and PBIP "
            "templates were peer-reviewed before production use.",
        ],
        "Python | Flask | Azure Analysis Services | Databricks SQL Warehouse | "
        "Power BI TMDL | PBIP | DAX"))

    e.append(deliverable(
        "2.2  SQL Server and Excel to cloud platforms - Excel & SQL Server to "
        "Cloud Migration Platform",
        [
            "Excel-to-DAX formula converter: maps Excel calculation formulas "
            "to equivalent Power BI DAX measures.",
            "Chart-to-Power BI visual mapper: converts Excel KPI chart "
            "definitions into Power BI visual configs - a reusable Power BI "
            "report template (JSON output).",
            "9-stage Excel pre-migration assessment pipeline produces a "
            "standard Power BI readiness report before publish.",
            "Reused across SQL Server -&gt; Snowflake, SQL Server -&gt; "
            "Microsoft Fabric Lakehouse, and Excel -&gt; Power BI targets.",
        ],
        "Python | pandas | openpyxl | Snowflake SQL | Microsoft Fabric | "
        "Azure Data Factory | Power BI"))

    e.append(deliverable(
        "2.3  Telcortex AI - Reusable Telecom BI Visual & Measure Library",
        [
            "Library of reusable visual components (TelecomKPIBar, "
            "MetricsCharts, ImpactLedger, SeverityBadge, PriorityTierBadge, "
            "ConfidenceBar, shared data-table wrapper) reused across 10+ "
            "dashboards - the direct equivalent of shared Power BI "
            "themes/visuals.",
            "Reusable 'measures' as shared formula modules: kpi_service (CSSR, "
            "TCH drop, MOS, availability with RAG grading) and revenue-"
            "exposure-estimate (ARPU -&gt; annualized revenue), mirrored on "
            "the frontend - the analog of a central DAX measure table used in "
            "multiple reports.",
            "Shared time-range selector and common utility library "
            "(formatRiskScore, formatDuration, severityColor) - the date-table "
            "/ common-KPI / page-layout pattern the goal asks for.",
            "Recognised with 1st Place at the BeEXIQO Code-AI-Thon 2026.",
        ],
        "Python | Flask | Next.js | TypeScript | Groq (Llama 3.1) | Docker"))

    e.append(deliverable(
        "2.4  Domo -> Snowflake + Power BI Migration - LambWeston "
        "(Fortune 500)",
        [
            "Automated Power BI workspace publishing with semantic model JSON "
            "generation - consistent naming conventions, correct measure "
            "aggregations, and slicers mapped from Domo filter definitions.",
            "All Power BI visuals mapped from Domo card types to semantically "
            "equivalent Power BI visual types - a reusable publishing template "
            "for future Domo-to-Power BI rebuilds.",
            "Semantic model JSON published and verified end-to-end before "
            "client sign-off.",
        ],
        "Python | Snowflake | Power BI REST API | Semantic Model JSON | "
        "Domo API"))

    e.append(deliverable(
        "2.5  StoneX POC - Reusable BI Engineering Modules & Report Contract "
        "Layer",
        [
            "Parameterized, table-agnostic modules the team can apply across "
            "reports instead of rebuilding: a schema-diff and rename-detection "
            "module, a SAFE/RISKY repair-classification module, and a "
            "data-freshness / gap-check harness driven purely by configuration.",
            "Two repeatable patterns: a 'contract layer' (compatibility view) "
            "that keeps existing report visuals and measures working during "
            "upstream schema changes, and a DDL allow-list safety guard that "
            "constrains blast radius.",
            "Every change flows through a human approval gate - nothing is "
            "applied until the exact SQL is reviewed and approved - and each "
            "module is documented so others can reuse it without reverse-"
            "engineering the code.",
        ],
        "Python | SQL | Databricks / Delta | Power BI | Model Context "
        "Protocol"))

    e.append(deliverable(
        "2.6  Decision Intelligence - Enterprise AI Data Intelligence Platform",
        [
            "Reusable connectors and a central orchestration layer that plug "
            "into SQL Server, PostgreSQL, Snowflake, and Databricks - the same "
            "building blocks are reused across data sources instead of rebuilt "
            "per integration.",
            "Reusable governance components (role-based access levels, full "
            "audit trail) and a multi-stage answer-quality review process "
            "packaged for reuse across reports and datasets.",
        ],
        "React | TypeScript | Node.js | PostgreSQL | Neo4j | Snowflake | "
        "SQL Server | Docker"))

    # ---- Section 3: Metrics & evidence
    e.append(Paragraph("3.&nbsp;&nbsp;Metrics &amp; Evidence", st_h))
    metric_rows = [
        ("&gt;= 2 reviewed AI assets",
         "MetricAI delivers 3 distinct reusable artefact types (TMDL "
         "Extractor, DAX Enrichment Engine, Report Rebinder) - exceeds the "
         "minimum of 2."),
        ("100+ DAX measures generated",
         "DAX Enrichment Engine produces a KPI-scoring, time-intelligence, and "
         "dependency-analysis measure library."),
        ("Reusable visual library",
         "Telcortex AI: 7 shared visual components reused across 10+ "
         "dashboards; kpi_service + revenue-exposure-estimate measure modules "
         "reused across multiple reports."),
        ("Reusable templates reused",
         "SQL Server and Excel to cloud platforms Excel-to-DAX converter and "
         "chart mapper reused across SQL Server -&gt; Snowflake, SQL Server "
         "-&gt; Fabric, and Excel -&gt; Power BI."),
        ("Peer/human-reviewed before library",
         "Novigo stakeholder review + StoneX human approval gate + SPOT Award "
         "= external and internal review passed."),
        ("Reused on &gt;= 1 report",
         "MetricAI reused across Novigo Phase 1 and Phase 2; templates reused "
         "across 3 targets; Telcortex components across 10+ dashboards."),
        ("Fortune 500 delivery",
         "LambWeston - Power BI semantic model JSON published and verified "
         "end-to-end before client sign-off."),
        ("Recognition",
         "R Systems SPOT Award for Outstanding Performance (MetricAI) and 1st "
         "Place at the BeEXIQO Code-AI-Thon 2026 (Telcortex AI)."),
    ]
    e.append(two_col_table(metric_rows, 2.0 * inch, 5.1 * inch,
                           header=("Metric / Deliverable", "Evidence")))
    e.append(Spacer(1, 4))

    # ---- Section 4: Rationale
    e.append(Paragraph("4.&nbsp;&nbsp;Rationale (copy-paste into the PMS "
                       "\"Add Rationale\" box)", st_h))
    for para in RATIONALE:
        e.append(Paragraph(para, st_rat))
    e.append(Paragraph("Tip: copy the green text above into the PMS "
                       "\"Add Rationale\" box. Max 20,000 characters.", st_tip))

    doc.build(e)
    return out_path


# ---------------------------------------------------------------- rationale
RATIONALE = [
    "In the October review cycle my strongest and most repeatable contribution "
    "was building reusable BI assets - semantic-model measures, report "
    "templates, and shared visual/measure libraries - that the wider team can "
    "apply across reports instead of rebuilding them from scratch each time. "
    "Across six projects I produced far more than the goal minimum of two "
    "AI-reviewed, reused assets, and every asset passed a human or stakeholder "
    "review gate before it was allowed into production or a shared library.",

    "On MetricAI (the AAS to Power BI Semantic Migration Accelerator) I "
    "delivered three distinct reusable automation tools, each of which emits "
    "production-ready Power BI artefacts from Azure Analysis Services source "
    "models. The TMDL Extractor auto-exports Power BI semantic model "
    "definitions (.tmdl) directly from Azure Analysis Services, removing 100% "
    "of the manual export effort the team previously did by hand. The DAX "
    "Enrichment Engine is an LLM-assisted pipeline that reads AAS measure "
    "metadata and generates 100+ reusable DAX measures enriched with KPI "
    "categories, time-intelligence patterns, dependency analysis, and "
    "business-friendly names, exported as a reusable Power BI semantic model "
    "JSON. The Report Rebinder converts Import-mode PBIX reports into "
    "DirectQuery PBIP models connected to a Databricks SQL Warehouse, and that "
    "rebinding logic is a reusable template for every future AAS-to-Power BI "
    "migration. These artefacts were peer-reviewed and reused across both "
    "Novigo delivery phases, and the delivery earned an R Systems SPOT Award "
    "for Outstanding Performance - external and internal confirmation that the "
    "reusable assets met client and leadership quality bars.",

    "On the SQL Server and Excel to cloud platforms project I added two more "
    "reusable templates to the BI toolkit: an Excel-to-DAX formula converter "
    "that maps Excel calculation formulas to equivalent Power BI DAX measures, "
    "and a chart-to-Power BI visual mapper that converts Excel KPI chart "
    "definitions into Power BI visual configurations, emitting a reusable "
    "Power BI report template JSON. A 9-stage Excel pre-migration assessment "
    "pipeline produces a standard Power BI readiness report before publish. "
    "These templates were validated and reused across SQL Server -&gt; "
    "Snowflake, SQL Server -&gt; Microsoft Fabric Lakehouse, and Excel -&gt; "
    "Power BI targets, proving reuse on more than one downstream report or "
    "pipeline.",

    "On Telcortex AI I built a genuine reusable BI visual and measure library "
    "- the closest analog to shared Power BI themes, visuals, and a central "
    "DAX measure table. I created a library of reusable visual components "
    "(TelecomKPIBar, MetricsCharts, ImpactLedger, SeverityBadge, "
    "PriorityTierBadge, ConfidenceBar, and a shared data-table wrapper) that "
    "are reused across 10+ dashboards. I also built reusable measures as "
    "shared formula modules - kpi_service (CSSR, TCH drop, MOS, availability "
    "with RAG grading) and revenue-exposure-estimate (ARPU -&gt; annualized "
    "revenue), mirrored on the frontend as a shared TypeScript module - used "
    "consistently across multiple reports. A shared time-range selector and a "
    "common utility library (formatRiskScore, formatDuration, severityColor) "
    "provide the date-table, common-KPI, and page-layout patterns the goal "
    "asks for. This work was recognised with 1st Place at the BeEXIQO "
    "Code-AI-Thon 2026.",

    "On the Domo -&gt; Snowflake + Power BI migration for LambWeston (a "
    "Fortune 500 client) I automated Power BI workspace publishing with "
    "semantic model JSON generation using consistent naming conventions, "
    "correct measure aggregations, and slicers mapped from Domo filter "
    "definitions. All Power BI visuals were mapped from Domo card types to "
    "semantically equivalent Power BI visual types, and the semantic model "
    "JSON was published and verified end-to-end before client sign-off - a "
    "reusable publishing template that standardises how future Domo dashboards "
    "are rebuilt in Power BI.",

    "On the StoneX POC I contributed reusable, parameterized engineering "
    "assets rather than one-off code: a schema-diff and rename-detection "
    "module, a SAFE/RISKY repair-classification module, and a table-agnostic "
    "data-freshness / gap-check harness that works against any source-target "
    "pair purely by configuration. I also established two repeatable patterns "
    "the team can adopt - a 'contract layer' (a compatibility view) that keeps "
    "existing report visuals and measures working during upstream schema "
    "changes, and a DDL allow-list safety guard that constrains blast radius. "
    "In line with the requirement that assets be reviewed before entering the "
    "library, every change flows through a human approval gate: nothing is "
    "applied until the exact SQL is reviewed and approved, and each module is "
    "documented so others can reuse it without reverse-engineering the code.",

    "On Decision Intelligence (the enterprise AI data-intelligence platform) I "
    "built shared, reusable components as well - a central orchestration "
    "layer, reusable connectors to SQL Server, PostgreSQL, Snowflake, and "
    "Databricks, role-based access levels, and a multi-stage review process "
    "for answer quality - packaged so the same building blocks can be reused "
    "across data sources instead of rebuilt per integration.",

    "Taken together, these deliverables comfortably exceed the goal's "
    "requirement of two or more AI-reviewed assets each reused on at least one "
    "subsequent report. MetricAI alone contributes three distinct reusable "
    "artefact types reused across two Novigo phases; the SQL Server and Excel "
    "to cloud platforms templates are reused across three migration targets; "
    "and the Telcortex component and measure libraries are reused across 10+ "
    "dashboards. Every asset was human-reviewed before entering production or "
    "a shared library, and the MetricAI SPOT Award and the Code-AI-Thon win "
    "independently validate the quality of the reusable work. Because these "
    "assets are documented and parameterized, the team's per-report build "
    "effort drops significantly and future BI migrations start from a proven, "
    "review-approved baseline rather than a blank page.",
]


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    base = r"C:\Users\bali\Desktop\Mohan\CVs"
    targets = [
        ("Bali Mohan Rao", "19031",
         base + r"\Goal01_BusinessBuilder_Supporting_Doc_BaliMohanRao.pdf"),
        ("Tanuja Subhash Shinde", "19038",
         base + r"\Goal01_BusinessBuilder_Supporting_Doc_TanujaSubhashShinde.pdf"),
    ]
    for name, eid, path in targets:
        build(name, eid, path)
        print("SAVED:", path)
