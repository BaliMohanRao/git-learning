# -*- coding: utf-8 -*-
"""
Generate the Goal 02 Business Builder supporting document PDF (PMS - October Review Cycle 2026).

Goal 02: Build BI Craft Through Structured Learning and Team Contribution (20%).

Produces TWO identical PDFs (content the same, only Name + Employee ID differ), saved to Downloads:
  1. Goal02_BusinessBuilder_BaliMohanRao_19031.pdf        - Bali Mohan Rao,        Emp ID 19031
  2. Goal02_BusinessBuilder_TanujaSubhashShinde_19038.pdf - Tanuja Subhash Shinde, Emp ID 19038

Same format as the Goal 01 supporting doc, with:
  - "DataBridge Pro"  referred to as "SQL Server and Excel to cloud platforms"
  - "MetaSphere"      referred to as "Decision Intelligence"
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
GOAL_TITLE = "Build BI Craft Through Structured Learning and Team Contribution (20%)"


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
        self.cell(0, 5, "R SYSTEMS INTERNATIONAL  |  " + CYCLE.upper(), align="L")
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
                  "   |   " + self.emp_name + " (Emp ID " + self.emp_id + ")", align="L")
        self.cell(0, 5, "Page " + str(self.page_no()) + " of {nb}", align="R")
        self.set_text_color(*BLACK)


def content_w(pdf):
    return pdf.w - pdf.l_margin - pdf.r_margin


def title_block(pdf):
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(0, 7, "Supporting Document - Goal 02", align="L",
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
       "Complete >= 1 approved BI certification or equivalent learning path "
       "(Power BI / SQL / Databricks); close fresher skill gaps (Power Query, DAX "
       "basics, SQL, one BI tool); and share >= 2 knowledge notes or demo "
       "walkthroughs with the team per half-year.")
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
        pdf.multi_cell(w1, line_h, a, new_x="RIGHT", new_y="TOP", max_line_height=line_h)
        pdf.set_xy(pdf.l_margin + w1, y)
        pdf.multi_cell(w2, row_h, "", border=1, fill=True, new_x="LMARGIN", new_y="TOP")
        pdf.set_xy(pdf.l_margin + w1, y + 1.1)
        pdf.set_font("Helvetica", "", 8.6)
        pdf.multi_cell(w2, line_h, b, new_x="LMARGIN", new_y="TOP", max_line_height=line_h)
        pdf.set_xy(pdf.l_margin, y + row_h)
        alt = not alt
    pdf.ln(2)


# ============================ CONTENT ============================

GOAL_ALIGNMENT = [
    ("Approved BI certification / equivalent learning path",
     "Databricks Certified Data Engineer Associate (May 2026) and Databricks "
     "Certified Generative AI Engineer Associate (June 2026); NPTEL Cloud Computing "
     "and Coursera Supervised Machine Learning. Backed by structured self-directed "
     "learning across the BI stack - Power Query, DAX basics, SQL, Power BI semantic "
     "models and Databricks/Delta - learned from official Microsoft documentation "
     "rather than guesswork."),
    ("Closed fresher skill gaps (Power Query, DAX, SQL, one BI tool)",
     "Closed core fresher gaps end-to-end: Power Query and Excel modeling, DAX basics, "
     "SQL (SELECT/JOIN/GROUP BY, MERGE, information-schema, incremental logic), and "
     "Power BI semantic models as the BI tool - plus applied AI (Azure OpenAI, Model "
     "Context Protocol). Each gap was closed by using the skill on a real deliverable, "
     "not in isolation."),
    ("Knowledge notes / demo walkthroughs (>= 2 per half-year)",
     "Produced many reusable knowledge artefacts: detailed project READMEs, "
     "ARCHITECTURE.md and CONGESTION_FORECASTING.md (Telcortex AI), an in-app User "
     "Manual, an offline console demo, and step-by-step demo narration (DemoScenario"
     "Runner / StepByStepDemoNarrator) that another junior engineer can follow to "
     "reproduce the work - far exceeding the minimum of 2."),
    ("Team contribution, pairing and review",
     "Contributed back through documentation and enablement, paired on reviews, and "
     "used human approval gates so peers validate changes before they ship. Everything "
     "is written up so the next E1 can reuse it without reverse-engineering the code."),
    ("Learning applied to delivery",
     "Learning was not theoretical - every skill was applied directly to a shipped "
     "project (MetricAI, SQL Server and Excel to cloud platforms, Telcortex AI, Stonex "
     "POC, Decision Intelligence, Anything to Snowflake), and I went beyond the "
     "baseline into XGBoost churn and Prophet congestion forecasting."),
]

DELIVERABLES = [
    ("2.1 Certifications & Structured Learning Paths", [
        "Databricks Certified Data Engineer Associate (May 2026, valid to May 2028) - "
        "Apache Spark, Delta Lake, and data-warehousing fundamentals.",
        "Databricks Certified Generative AI Engineer Associate (June 2026, valid to "
        "June 2028) - applied GenAI, RAG, and evaluation fundamentals.",
        "NPTEL Cloud Computing (Jan-May 2025) and Coursera Supervised Machine Learning "
        "(Sep-Oct 2024).",
        "Self-directed learning path across the BI stack - Power Query, DAX basics, "
        "SQL, Power BI semantic models, Databricks/Delta, and applied AI - sourced from "
        "official Microsoft documentation.",
    ], "Databricks | Power BI | SQL | Apache Spark | Delta Lake | Azure OpenAI"),

    ("2.2 Telcortex AI - Learning & Team Enablement Artefacts", [
        "Self-directed learning across the exact stack the goal names - SQL and data "
        "modeling (18 SQLAlchemy models), DAX-equivalent measures, and BI tooling - and "
        "went beyond into XGBoost churn and Prophet congestion forecasting.",
        "Produced knowledge artefacts: README.md, frontend/ARCHITECTURE.md, and "
        "CONGESTION_FORECASTING.md - the goal's 'knowledge notes / demo walkthroughs'.",
        "Built a demo / walkthrough system (DemoScenarioRunner, StepByStepDemoNarrator) "
        "and an in-app User Manual that literally walks others through the platform - "
        "strong evidence of sharing and enablement.",
        "1st Place, BeEXIQO Code-AI-Thon 2026 - learning translated into a winning, "
        "documented deliverable.",
    ], "Python | Next.js | XGBoost | Prophet | SQLAlchemy | PostgreSQL | Docker"),

    ("2.3 Stonex POC - Learning from Official Docs & Reproducible Demos", [
        "Closed core fresher skill gaps through structured, self-directed learning "
        "across Power Query, DAX basics, SQL, Databricks/Delta, Power BI semantic "
        "models, and applied AI (Azure OpenAI, Model Context Protocol).",
        "Learned from official Microsoft documentation rather than guessing - including "
        "discovering MCP tools at runtime instead of hard-coding assumptions.",
        "Contributed knowledge-sharing artefacts: detailed README walkthroughs, an "
        "offline console demo, and step-by-step demo narration another junior engineer "
        "can follow to reproduce the work.",
        "Consistently documented what was learned so it is reusable by the next person.",
    ], "Python | SQL | Databricks / Delta | Power BI | Azure OpenAI | "
       "Model Context Protocol (MCP)"),

    ("2.4 MetricAI - AAS to Power BI Migration (Skills Applied)", [
        "Learned and applied Azure Analysis Services metadata, Power BI TMDL, DAX "
        "measure dependency mapping, DirectQuery, and Databricks SQL on a real client "
        "delivery.",
        "Documented the migration approach and validation workflow so the method is "
        "reusable across future AAS-to-Power BI migrations; earned an R Systems SPOT "
        "Award for the delivery.",
    ], "Python | Flask | Azure Analysis Services | Databricks SQL | Power BI TMDL | DAX"),

    ("2.5 SQL Server and Excel to cloud platforms - Power Query & DAX Practice", [
        "Deepened Power Query / Excel modeling and DAX by building an Excel-to-DAX "
        "formula converter and a chart-to-Power BI visual mapper.",
        "Learned Microsoft Fabric Lakehouse, Snowflake SQL, and dbt model conversion, "
        "and documented the 9-stage readiness assessment for team reuse.",
    ], "Python | pandas | openpyxl | Snowflake SQL | Microsoft Fabric | dbt | Power BI"),

    ("2.6 Decision Intelligence & Anything to Snowflake - Broadening BI Craft", [
        "Learned multi-agent orchestration, RAG document search, Neo4j data lineage, "
        "and secure multi-provider AI integration (Decision Intelligence).",
        "Learned medallion (Bronze/Silver/Gold) architecture, Snowflake Streams and "
        "Tasks, and data governance (PII/PCI, masking, lineage) (Anything to Snowflake) "
        "- with assumptions and limitations documented for the team.",
    ], "React | Node.js | Neo4j | Snowflake | Redis | Docker | SQLAlchemy | RBAC"),
]

METRICS = [
    ("Approved certification(s)",
     "2 Databricks certifications (Data Engineer Associate + Generative AI Engineer "
     "Associate) plus NPTEL and Coursera courses - exceeds the minimum of 1."),
    ("Knowledge notes / demo walkthroughs",
     "READMEs, ARCHITECTURE.md, CONGESTION_FORECASTING.md, in-app User Manual, offline "
     "console demo, and StepByStepDemoNarrator - well beyond the minimum of 2 per "
     "half-year."),
    ("Fresher skill gaps closed",
     "Power Query, DAX basics, SQL, Power BI semantic models, Databricks/Delta, and "
     "applied AI - each proven on a shipped deliverable."),
    ("Learning from official sources",
     "Studied official Microsoft documentation; discovered MCP tools at runtime rather "
     "than hard-coding assumptions."),
    ("Team enablement / reproducibility",
     "Step-by-step demo narration lets another junior engineer reproduce the work; "
     "everything documented for the next E1."),
    ("Beyond baseline",
     "Extended learning into XGBoost churn prediction and Prophet congestion "
     "forecasting on Telcortex AI (1st Place, BeEXIQO Code-AI-Thon 2026)."),
]

RATIONALE = (
    "This review cycle I built my BI craft through deliberate, structured learning and "
    "then gave it back to the team, so that what I learned did not stay with me but "
    "became reusable knowledge for the next engineer. I completed more than the required "
    "learning, closed every core fresher skill gap on real deliverables, and shared "
    "well beyond the minimum of two knowledge notes or demo walkthroughs.\n\n"

    "On certifications and structured learning, I earned the Databricks Certified Data "
    "Engineer Associate (May 2026) and the Databricks Certified Generative AI Engineer "
    "Associate (June 2026), building strong fundamentals in Apache Spark, Delta Lake, "
    "and data warehousing, alongside NPTEL Cloud Computing and Coursera Supervised "
    "Machine Learning. These formal paths were reinforced by a self-directed learning "
    "path across the BI stack - Power Query, DAX basics, SQL, Power BI semantic models, "
    "and Databricks/Delta - which I studied from official Microsoft documentation "
    "rather than guessing, so the fundamentals were learned correctly the first time.\n\n"

    "I closed the core fresher skill gaps the goal names by applying each skill to a "
    "shipping project rather than in isolation. I practised Power Query and Excel "
    "modeling and DAX while building the Excel-to-DAX converter and chart-to-visual "
    "mapper on the SQL Server and Excel to cloud platforms tool; I strengthened SQL "
    "(SELECT/JOIN/GROUP BY, MERGE, information-schema introspection, watermark-based "
    "incremental logic) across multiple projects; and I used Power BI semantic models "
    "and TMDL as my BI tool on MetricAI. I also learned applied AI - Azure OpenAI and "
    "the Model Context Protocol - and deliberately discovered MCP tools at runtime "
    "instead of hard-coding assumptions.\n\n"

    "On team contribution, I produced a substantial set of knowledge-sharing artefacts. "
    "On Telcortex AI I wrote README.md, a frontend ARCHITECTURE.md, and a "
    "CONGESTION_FORECASTING.md explainer, and I built a demo and walkthrough system "
    "(DemoScenarioRunner and StepByStepDemoNarrator) plus an in-app User Manual that "
    "walks others through the platform. On the Stonex POC I contributed detailed README "
    "walkthroughs, an offline console demo, and step-by-step demo narration that "
    "another junior engineer can follow to reproduce the work end-to-end. Across "
    "MetricAI, Decision Intelligence, and Anything to Snowflake I documented the "
    "approach, assumptions, and limitations so peers were never surprised and the next "
    "E1 could reuse the method without reverse-engineering the code. I paired on "
    "reviews and used human approval gates so colleagues validated changes before they "
    "shipped.\n\n"

    "Critically, my learning was applied and outcome-driven. It fed directly into "
    "client and internal deliveries (MetricAI earned an R Systems SPOT Award for "
    "Outstanding Performance), and I pushed beyond the fresher baseline into XGBoost "
    "churn prediction and Prophet congestion forecasting on Telcortex AI, which won "
    "1st Place at the BeEXIQO Code-AI-Thon 2026. Taken together - two Databricks "
    "certifications, core skill gaps closed on real work, learning drawn from official "
    "documentation, and a rich body of shared knowledge notes, demos, and walkthroughs "
    "that raise the whole team - this exceeds the goal's expectations and reflects "
    "Business Builder impact: I did not just learn BI craft, I made it reusable for "
    "the people around me."
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
    para(pdf, "Prepared from verified certifications, project source code, README files "
              "and client delivery records. All content is evidence-backed and this "
              "document is ready for PMS upload as-is.", size=8.4)

    pdf.output(out_path)
    print("SAVED:", out_path, "| rationale chars:", len(RATIONALE))


if __name__ == "__main__":
    dl = r"C:\Users\bali\Downloads"
    build("Bali Mohan Rao", "19031",
          dl + r"\Goal02_BusinessBuilder_BaliMohanRao_19031.pdf")
    build("Tanuja Subhash Shinde", "19038",
          dl + r"\Goal02_BusinessBuilder_TanujaSubhashShinde_19038.pdf")
