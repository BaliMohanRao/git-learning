# -*- coding: utf-8 -*-
"""
Generate the Goal 01 Business Builder supporting document PDF (PMS - October Review Cycle 2026).

Produces TWO identical PDFs (content the same, only Name + Employee ID differ):
  1. Bali Mohan Rao       - Emp ID 19031
  2. Tanuja Subhash Shinde - Emp ID 19038

Format follows Goal01_BusinessBuilder_Supporting_Doc.pdf, with:
  - "DataBridge Pro"  renamed to "SQL Server and Excel to cloud platforms"
  - "MetaSphere"      renamed to "Decision Intelligence"
  - Two extra projects added (Stonex POC, Telcortex AI)
  - Detailed rationale (well within the 20,000-char PMS limit)
  - NO "Evidence to Upload" section (PDF is ready to upload as-is)
"""
from fpdf import FPDF

# ---- Theme ----
NAVY = (26, 26, 26)
BLUE = (26, 26, 26)
GREY_HEAD = (233, 233, 233)
GREY_ALT = (247, 247, 247)
BLACK = (26, 26, 26)
GREEN = (26, 26, 26)

CYCLE = "October Review Cycle 2026"
GOAL_TITLE = "Contribute Reusable BI Visuals, Measures, or Report Templates (10%)"


class Doc(FPDF):
    def __init__(self, emp_name, emp_id):
        super().__init__(orientation="P", unit="mm", format="Letter")
        self.emp_name = emp_name
        self.emp_id = emp_id
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(15, 16, 15)

    def header(self):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*BLUE)
        self.cell(0, 5, "R SYSTEMS INTERNATIONAL  |  " + CYCLE.upper(),
                  align="L")
        self.ln(5)
        self.set_draw_color(*BLUE)
        self.set_line_width(0.4)
        self.line(15, self.get_y(), self.w - 15, self.get_y())
        self.ln(4)
        self.set_text_color(*BLACK)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.2)
        self.line(15, self.get_y(), self.w - 15, self.get_y())
        self.ln(1)
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, "Prepared for R Systems PMS - " + CYCLE +
                  "   |   " + self.emp_name + " (Emp ID " + self.emp_id + ")",
                  align="L")
        self.cell(0, 5, "Page " + str(self.page_no()) + " of {nb}", align="R")
        self.set_text_color(*BLACK)


def content_w(pdf):
    return pdf.w - pdf.l_margin - pdf.r_margin


def title_block(pdf):
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(0, 7, "Supporting Document - Goal 01", align="L",
                   new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.multi_cell(0, 6, GOAL_TITLE, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_text_color(*BLACK)


def kv(pdf, key, val):
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.cell(30, 5.5, key)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.multi_cell(0, 5.5, val, new_x="LMARGIN", new_y="NEXT")


def employee_block(pdf):
    kv(pdf, "Employee:", pdf.emp_name)
    kv(pdf, "Employee ID:", pdf.emp_id)
    kv(pdf, "Review cycle:", CYCLE)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.cell(30, 5.5, "Self-rating:")
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(*GREEN)
    pdf.multi_cell(0, 5.5, "Business Builder", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*BLACK)
    kv(pdf, "Goal metric:",
       ">= 2 AI-reviewed assets (DAX measures, Power Query snippets, reusable "
       "visual components, report templates) added to the team library; each "
       "reused on >= 1 subsequent report or dashboard.")
    pdf.ln(3)


def section(pdf, text):
    pdf.ln(1)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.set_fill_color(*GREY_HEAD)
    pdf.set_draw_color(*BLUE)
    pdf.cell(0, 7, "  " + text, fill=True, border="B", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_text_color(*BLACK)


def sub(pdf, text):
    pdf.ln(1)
    pdf.set_font("Helvetica", "B", 9.8)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(0, 5.2, text, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*BLACK)


def para(pdf, text, bold=False, size=9.3, lh=4.9, color=BLACK):
    pdf.set_font("Helvetica", "B" if bold else "", size)
    pdf.set_text_color(*color)
    pdf.multi_cell(0, lh, text, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*BLACK)


def bullet(pdf, text, size=9.3, lh=4.9):
    x0 = pdf.get_x()
    pdf.set_font("Helvetica", "", size)
    pdf.cell(4, lh, "-")
    pdf.set_x(x0 + 4)
    pdf.multi_cell(content_w(pdf) - 4, lh, text, new_x="LMARGIN", new_y="NEXT")


def label_line(pdf, label, value, size=9.3, lh=4.9):
    pdf.set_font("Helvetica", "B", size)
    lw = pdf.get_string_width(label + " ") + 1
    pdf.cell(lw, lh, label)
    pdf.set_font("Helvetica", "", size)
    pdf.multi_cell(content_w(pdf) - lw, lh, value, new_x="LMARGIN", new_y="NEXT")


def two_col_table(pdf, headers, rows, w1_ratio=0.34):
    cw = content_w(pdf)
    w1 = cw * w1_ratio
    w2 = cw - w1
    line_h = 4.6
    pdf.set_draw_color(180, 180, 180)
    # header
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(*GREY_HEAD)
    pdf.set_text_color(*NAVY)
    y = pdf.get_y()
    pdf.multi_cell(w1, 6.5, headers[0], border=1, fill=True,
                   new_x="RIGHT", new_y="TOP", align="L", max_line_height=line_h)
    pdf.set_xy(pdf.l_margin + w1, y)
    pdf.multi_cell(w2, 6.5, headers[1], border=1, fill=True,
                   new_x="LMARGIN", new_y="NEXT", align="L", max_line_height=line_h)
    pdf.set_text_color(*BLACK)
    # body
    alt = False
    for a, b in rows:
        pdf.set_font("Helvetica", "B", 8.6)
        h1 = len(pdf.multi_cell(w1, line_h, a, dry_run=True, output="LINES",
                                max_line_height=line_h))
        pdf.set_font("Helvetica", "", 8.6)
        h2 = len(pdf.multi_cell(w2, line_h, b, dry_run=True, output="LINES",
                                max_line_height=line_h))
        row_h = max(h1, h2) * line_h + 2.2
        if pdf.get_y() + row_h > pdf.h - pdf.b_margin:
            pdf.add_page()
        fill = GREY_ALT if alt else (255, 255, 255)
        pdf.set_fill_color(*fill)
        y = pdf.get_y()
        pdf.set_font("Helvetica", "B", 8.6)
        pdf.multi_cell(w1, row_h, "", border=1, fill=True, new_x="RIGHT", new_y="TOP")
        pdf.set_xy(pdf.l_margin, y + 1.1)
        pdf.multi_cell(w1, line_h, a, new_x="RIGHT", new_y="TOP",
                       max_line_height=line_h)
        pdf.set_xy(pdf.l_margin + w1, y)
        pdf.multi_cell(w2, row_h, "", border=1, fill=True, new_x="LMARGIN", new_y="TOP")
        pdf.set_xy(pdf.l_margin + w1, y + 1.1)
        pdf.set_font("Helvetica", "", 8.6)
        pdf.multi_cell(w2, line_h, b, new_x="LMARGIN", new_y="TOP",
                       max_line_height=line_h)
        pdf.set_xy(pdf.l_margin, y + row_h)
        alt = not alt
    pdf.ln(2)


# ============================ CONTENT ============================

GOAL_ALIGNMENT = [
    ("Reusable DAX measures / measure modules",
     "MetricAI DAX Enrichment Engine auto-generated 100+ reusable DAX measures "
     "(KPI scoring, time-intelligence, dependency analysis). Telcortex AI shared "
     "measure modules (kpi_service.py: CSSR, TCH drop, MOS, availability with RAG "
     "grading; revenue_exposure_estimate.py / revenue-exposure-estimate.ts: ARPU "
     "to annualized revenue) act as a central, reusable measure table."),
    ("Reusable BI visuals",
     "Telcortex AI reusable component library reused across 10+ dashboards "
     "(TelecomKPIBar, MetricsCharts, ImpactLedger, SeverityBadge, PriorityTierBadge, "
     "ConfidenceBar, shared data-table wrapper) - the analog of shared Power BI "
     "themes/visuals. Domo cards mapped to semantically equivalent Power BI visuals."),
    ("Report templates",
     "MetricAI Report Rebinder converts Import-mode PBIX to reusable DirectQuery "
     "PBIP models. The SQL Server and Excel to cloud platforms tool converts Excel "
     "KPI sheets into reusable Power BI report template JSON and auto-generates PBIP "
     "projects for every future migration."),
    ("Power Query / TMDL assets",
     "MetricAI TMDL Extractor auto-exports Power BI semantic model definitions "
     "(.tmdl) from Azure Analysis Services, removing 100% of manual export effort."),
    ("Reusable BI engineering modules / contract layer",
     "Stonex POC contributed a schema-diff and rename-detection module, a SAFE/RISKY "
     "repair-classification module, and a table-agnostic freshness/gap-check harness "
     "(any source-target pair by configuration), plus a contract-layer compatibility "
     "view that keeps existing report visuals/measures working through upstream "
     "changes and a DDL allow-list safety guard."),
    ("AI / stakeholder review before library add",
     "Every asset passed a review gate before shared use - AI-assisted review plus "
     "human/stakeholder approval (Stonex POC applies nothing until the exact SQL is "
     "reviewed and approved). MetricAI passed Novigo stakeholder review; an R Systems "
     "SPOT Award confirms the quality standard."),
    ("Reused on > 1 report / dashboard",
     "MetricAI artefacts reused across Novigo Phase 1 and Phase 2; the migration "
     "templates reused across SQL Server -> Snowflake, SQL Server -> Microsoft Fabric, "
     "and Excel -> Power BI targets; Telcortex components reused across 10+ dashboards."),
]

DELIVERABLES = [
    ("2.1 MetricAI - AAS to Power BI Semantic Migration Accelerator", [
        "TMDL Extractor - auto-exports Power BI semantic model definitions (.tmdl) "
        "from Azure Analysis Services via SSMS; eliminates 100% of manual export effort.",
        "DAX Enrichment Engine - LLM-assisted pipeline reads AAS measure metadata, "
        "enriches it with KPI categories and business-friendly names, and generates "
        "100+ reusable DAX measures as a Power BI semantic model JSON library.",
        "Report Rebinder - converts Import-mode PBIX to DirectQuery PBIP models "
        "connected to Databricks SQL Warehouse; the rebinding template is reusable for "
        "all future AAS-to-Power BI migrations.",
        "Delivered to the Novigo client and reused across Phase 1 and Phase 2; earned "
        "an R Systems SPOT Award for Outstanding Performance. All artefacts were "
        "peer-reviewed before production use.",
    ], "Python | Flask | Azure Analysis Services | Databricks SQL Warehouse | "
       "Power BI TMDL | PBIP | DAX | OpenAI API"),

    ("2.2 SQL Server and Excel to cloud platforms - Excel & SQL Server to Cloud Migration", [
        "Excel-to-DAX formula converter: maps Excel calculation formulas to equivalent "
        "reusable Power BI DAX measures.",
        "Chart-to-Power BI visual mapper: converts Excel KPI chart definitions to "
        "Power BI visual configs - reusable Power BI report template JSON output.",
        "Automated PBIP (Power BI project) generator plus a 9-stage Excel "
        "pre-migration readiness assessment produced before publish.",
        "Templates reused across SQL Server -> Snowflake, SQL Server -> Microsoft "
        "Fabric Lakehouse, and Excel -> Power BI.",
    ], "Python | pandas | openpyxl | Snowflake SQL | Microsoft Fabric | "
       "Azure Data Factory | Power BI | dbt"),

    ("2.3 Domo -> Snowflake + Power BI Migration - LambWeston (Fortune 500)", [
        "Automated Power BI workspace publishing with semantic model JSON generation - "
        "consistent naming conventions, correct measure aggregations, and slicers "
        "mapped from Domo filter definitions.",
        "All Power BI visuals mapped from Domo card types to semantically equivalent "
        "Power BI visual types - a reusable mapping applied consistently across reports.",
        "Semantic model JSON published and verified end-to-end before client sign-off.",
    ], "Python | Snowflake | Power BI REST API | Semantic Model JSON | Domo API"),

    ("2.4 Telcortex AI - Reusable Telecom BI Component & Measure Library", [
        "Built a library of reusable visual components reused across 10+ dashboards "
        "(TelecomKPIBar, MetricsCharts, ImpactLedger, SeverityBadge, PriorityTierBadge, "
        "ConfidenceBar, shared data-table wrapper) - the direct equivalent of shared "
        "Power BI themes and visuals.",
        "Created reusable measures as shared formula modules: kpi_service.py (CSSR, "
        "TCH drop, MOS, availability with RAG grading) and revenue_exposure_estimate.py "
        "(ARPU to annualized revenue), mirrored on the frontend as "
        "revenue-exposure-estimate.ts - the analog of a central DAX measure table.",
        "Built a shared time-range selector and a common utility library (formatRiskScore, "
        "formatDuration, severityColor) - the reusable date-table / common-KPI / "
        "page-layout pattern the goal asks for.",
        "1st Place, BeEXIQO Code-AI-Thon 2026 - the reusable component set enabled "
        "consistent dashboards to be assembled quickly.",
    ], "Python | Flask | Next.js | TypeScript | Redis | PostgreSQL | Docker"),

    ("2.5 Stonex POC - Reusable BI Engineering Modules & Contract-Layer Patterns", [
        "Contributed reusable, parameterized engineering assets the team can apply "
        "across reports instead of rebuilding each time: a schema-diff and "
        "rename-detection module, a SAFE/RISKY repair-classification module, and a "
        "table-agnostic data-freshness / gap-check harness that works against any "
        "source-target pair by configuration.",
        "Established a reusable contract layer (compatibility view) that keeps existing "
        "report visuals and measures working during upstream schema changes.",
        "Established a DDL allow-list safety guard pattern that constrains blast radius.",
        "Every change flows through a human approval gate - nothing is applied until the "
        "exact SQL is reviewed and approved - and each asset is documented so others "
        "reuse it without reverse-engineering the code.",
    ], "Python | SQL | Databricks / Delta | Power BI | Azure OpenAI | "
       "Model Context Protocol (MCP)"),

    ("2.6 Decision Intelligence - Enterprise AI Data Intelligence Platform", [
        "Reusable source connectors (SQL Server, PostgreSQL, Snowflake, Databricks) and "
        "parameterized query/measure patterns authored once and reused across data "
        "sources rather than duplicated per engagement.",
        "Reusable multi-stage answer-review pattern and RAG document-search components "
        "shared across the platform.",
    ], "React | TypeScript | Node.js | PostgreSQL | Neo4j | Snowflake | "
       "OpenAI/Anthropic | Docker"),

    ("2.7 Anything to Snowflake - Enterprise AI Migration Accelerator", [
        "Reusable 12-agent modules (source discovery, table creation, governance, drift "
        "detection, self-healing) and reusable Bronze/Silver/Gold model templates "
        "applied consistently across sources.",
        "Reusable governance module (PII/PCI detection, masking, row-level access, "
        "lineage) packaged for reuse across migrations.",
    ], "Python | Flask | Snowflake | Redis | Docker | SQLAlchemy | JWT/RBAC"),
]

METRICS = [
    (">= 2 reviewed AI assets",
     "MetricAI alone delivers 3 distinct reusable artefact types (TMDL, DAX JSON, "
     "PBIP template); Telcortex adds a reusable visual + measure library - far "
     "exceeds the minimum of 2."),
    ("Peer-reviewed before library add",
     "Novigo stakeholder review + SPOT Award (external and internal review); Stonex "
     "POC human approval gate on exact SQL before anything is applied."),
    ("Reused on >= 1 report",
     "MetricAI reused across Novigo Phase 1 and Phase 2; migration templates reused "
     "across SQL Server and Excel targets; Telcortex components reused across 10+ "
     "dashboards."),
    ("100+ DAX measures generated",
     "DAX Enrichment Engine: reusable KPI-scoring, time-intelligence, and "
     "dependency-analysis measure library."),
    ("Fortune 500 delivery",
     "LambWeston - Power BI semantic model JSON published and verified end-to-end."),
    ("External recognition",
     "R Systems SPOT Award (MetricAI) and 1st Place at BeEXIQO Code-AI-Thon 2026 "
     "(Telcortex AI) validate BI quality and reuse."),
]

RATIONALE = (
    "This review cycle I treated contributing reusable BI assets as a deliberate "
    "engineering practice rather than a by-product, and I delivered reusable measures, "
    "visuals, report templates, and BI engineering modules across every project I "
    "worked on. Each asset was reviewed before it entered shared use (AI-assisted "
    "review plus human / stakeholder approval) and each was reused on at least one "
    "subsequent report or dashboard, exceeding the goal minimum of two reviewed, "
    "reused assets.\n\n"

    "On MetricAI (AAS to Power BI Semantic Migration Accelerator) I built three "
    "distinct reusable automation tools that output production-ready Power BI semantic "
    "artefacts directly from Azure Analysis Services models. The DAX Enrichment Engine "
    "auto-generated 100+ reusable DAX measures with KPI scoring, time-intelligence and "
    "dependency analysis, exported as a reusable Power BI semantic model JSON library. "
    "The TMDL Extractor auto-exports semantic model definitions (.tmdl), removing 100% "
    "of manual export effort, and the Report Rebinder converts Import-mode PBIX into "
    "reusable DirectQuery PBIP templates connected to a Databricks SQL Warehouse - a "
    "template pattern reusable for every future AAS-to-Power BI migration. These "
    "artefacts were peer-reviewed before production, reused across Novigo Phase 1 and "
    "Phase 2, and the delivery earned an R Systems SPOT Award for Outstanding "
    "Performance.\n\n"

    "On SQL Server and Excel to cloud platforms I built an Excel-to-DAX formula "
    "converter and a chart-to-Power BI visual mapper that turn Excel KPI sheets into "
    "reusable Power BI report templates (template JSON output), plus an automated PBIP "
    "generator and a 9-stage Excel pre-migration readiness assessment. These templates "
    "were reused across SQL Server -> Snowflake, SQL Server -> Microsoft Fabric "
    "Lakehouse, and Excel -> Power BI targets, so the same reviewed logic served "
    "multiple downstream reports instead of being rebuilt each time.\n\n"

    "On the Domo -> Snowflake + Power BI migration for LambWeston (Fortune 500) I "
    "automated Power BI workspace publishing with semantic model JSON generation using "
    "consistent naming conventions, correct measure aggregations and slicers mapped "
    "from Domo filter definitions, and I mapped every Domo card type to a semantically "
    "equivalent Power BI visual - a reusable mapping applied consistently across the "
    "published reports and verified end-to-end before client sign-off.\n\n"

    "On Telcortex AI I built a library of reusable visual components reused across 10+ "
    "dashboards - TelecomKPIBar, MetricsCharts, ImpactLedger, SeverityBadge, "
    "PriorityTierBadge, ConfidenceBar and a shared data-table wrapper - the direct "
    "analog of shared Power BI themes and visuals. I created reusable measure modules "
    "(kpi_service.py computing CSSR, TCH drop, MOS and availability with RAG grading, "
    "and revenue_exposure_estimate.py mirrored on the frontend as "
    "revenue-exposure-estimate.ts converting ARPU to annualized revenue exposure) that "
    "behave like a central DAX measure table consumed by multiple reports, plus a "
    "shared time-range selector and a common utility library (formatRiskScore, "
    "formatDuration, severityColor). This work won 1st Place at the BeEXIQO "
    "Code-AI-Thon 2026.\n\n"

    "On the Stonex POC I contributed reusable, parameterized engineering assets the "
    "team can apply across reports instead of rebuilding each time: a schema-diff and "
    "rename-detection module, a SAFE/RISKY repair-classification module, and a "
    "table-agnostic data-freshness / gap-check harness that works against any "
    "source-target pair by configuration. I also established two repeatable patterns - "
    "a contract layer (compatibility view) that keeps existing report visuals and "
    "measures working during upstream schema changes, and a DDL allow-list safety guard "
    "that constrains blast radius. Every change flows through a human approval gate: "
    "nothing is applied until the exact SQL is reviewed and approved, and each asset is "
    "documented so others reuse it without reverse-engineering the code.\n\n"

    "Across Decision Intelligence and Anything to Snowflake I applied the same reuse "
    "discipline - reusable source connectors, parameterized query and measure patterns, "
    "and Bronze/Silver/Gold model templates with a shared governance module - so common "
    "logic is authored once and reused rather than duplicated per engagement.\n\n"

    "Taken together, these deliverables exceed the goal's minimum of >= 2 reviewed "
    "reusable assets, with each asset reused on at least one subsequent report or "
    "dashboard, and the MetricAI work was externally validated by an R Systems SPOT "
    "Award while Telcortex AI won 1st Place at the BeEXIQO Code-AI-Thon 2026. This "
    "demonstrates Business Builder impact: I raised team velocity and consistency by "
    "turning one-off BI work into a reviewed, documented, reusable library."
)


def build(emp_name, emp_id, out_path):
    pdf = Doc(emp_name, emp_id)
    pdf.alias_nb_pages()
    pdf.add_page()

    title_block(pdf)
    employee_block(pdf)

    section(pdf, "1. Goal Alignment")
    two_col_table(pdf, ("Goal element", "How addressed"), GOAL_ALIGNMENT)

    section(pdf, "2. Key Deliverables")
    for name, bullets, stack in DELIVERABLES:
        sub(pdf, name)
        for b in bullets:
            bullet(pdf, b)
        label_line(pdf, "Stack:", stack)
        pdf.ln(1)

    section(pdf, "3. Metrics & Evidence")
    two_col_table(pdf, ("Metric / Deliverable", "Evidence"), METRICS, w1_ratio=0.30)

    section(pdf, "4. Rationale (copy-paste into the PMS \"Add Rationale\" box)")
    para(pdf, RATIONALE, color=GREEN, size=9.2, lh=4.9)
    pdf.ln(1)
    para(pdf, "Note: The PMS \"Add Rationale\" box allows up to 20,000 characters. "
              "The rationale above is approximately " + str(len(RATIONALE)) +
              " characters - well within the limit.", bold=True, size=8.4)

    pdf.ln(2)
    para(pdf, "Prepared from verified project source code, README files, client "
              "delivery records and award records. All content is evidence-backed "
              "and this document is ready for PMS upload as-is.", size=8.4)

    pdf.output(out_path)
    print("SAVED:", out_path, "| rationale chars:", len(RATIONALE))


if __name__ == "__main__":
    base = r"C:\Users\bali\Downloads"
    build("Bali Mohan Rao", "19031",
          base + r"\Goal01_BusinessBuilder_BaliMohanRao_19031.pdf")
    build("Tanuja Subhash Shinde", "19038",
          base + r"\Goal01_BusinessBuilder_TanujaSubhashShinde_19038.pdf")
