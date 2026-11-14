#!/usr/bin/env python3
"""Build fictional Office files with the Craft CLIs and import them in Grind."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

OUTPUT = Path(sys.argv[1] if len(sys.argv) > 1 else "samples/compatibility")
GRIND = os.environ.get("GRIND_BIN", "grind")
WORDCRAFT = shutil.which("wordcraft-cli")
GRIDCRAFT = shutil.which("gridcraft-cli")
os.environ.setdefault("WORDCRAFT_REGION", "en-US")
if not WORDCRAFT or not GRIDCRAFT:
    raise SystemExit("wordcraft-cli and gridcraft-cli must be on PATH")
if shutil.which(GRIND):
    GRIND = shutil.which(GRIND) or GRIND
elif not Path(GRIND).is_file():
    raise SystemExit(f"Grind executable not found: {GRIND}; set GRIND_BIN")

for folder in ("docx", "xlsx", "imported/docx", "imported/xlsx", "reports/docx", "reports/xlsx"):
    (OUTPUT / folder).mkdir(parents=True, exist_ok=True)


def command(name, params=None):
    result = {"command": name}
    if params is not None:
        result["params"] = params
    return result


def paragraph(commands, value, style=None):
    if style:
        commands.append(command("para.style", {"style": style}))
    commands.extend((command("text.insert", {"text": value}), command("text.newParagraph")))


def bullet_list(commands, items):
    commands.append(command("para.bullets", {"kind": "bullet"}))
    for item in items:
        commands.extend((command("text.insert", {"text": item}), command("text.newParagraph")))
    commands.append(command("para.bullets", {"off": True}))


def paragraph_with_footnote(commands, value, note):
    commands.extend((command("text.insert", {"text": value}), command("references.footnote", {"text": note}), command("text.newParagraph")))


def paragraph_with_link(commands, prefix, url, label):
    commands.extend((command("text.insert", {"text": prefix}), command("insert.link", {"url": url, "text": label}), command("text.newParagraph")))


def word_table(commands, rows):
    commands.append(command("insert.table", {"rows": len(rows), "cols": len(rows[0]), "style": "Table Grid"}))
    for row_number, row in enumerate(rows):
        for column_number, value in enumerate(row):
            commands.append(command("text.insert", {"text": str(value)}))
            if row_number != len(rows) - 1 or column_number != len(row) - 1:
                commands.append(command("text.tab"))


def make_docx(name, commands):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", encoding="utf-8") as script:
        json.dump({"template": "blank", "commands": commands}, script)
        script.flush()
        subprocess.run([WORDCRAFT, "run", "--script", script.name, "--save", str(OUTPUT / "docx" / f"{name}.docx"), "--author", "Compatibility Test Fixture"], check=True)


def make_xlsx(name, commands):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", encoding="utf-8") as script:
        for item in commands:
            script.write(json.dumps(item) + "\n")
        script.flush()
        subprocess.run([GRIDCRAFT, "run", "--script", script.name, "--out", str(OUTPUT / "xlsx" / f"{name}.xlsx")], check=True)


def word_page_furniture(commands, header):
    commands.extend((
        command("insert.header", {"text": header}),
        command("insert.pageNumber", {"position": "bottom", "align": "right", "format": "x of y"}),
    ))


memo = []
paragraph(memo, "FICTIONAL TEST DOCUMENT - Monthly Operations Memo", "Title")
paragraph(memo, "Example Works Ltd. | All people, dates, figures, and events in this file are fabricated.")
paragraph(memo, "To: Department Leads    From: Morgan Sample, Operations    Date: 14 November 2026    Subject: December service readiness")
paragraph(memo, "Decision requested", "Heading 1")
paragraph(memo, "Approve the proposed support rota and reserve two training afternoons before the seasonal release. This planning example is not an instruction for a real operation.")
paragraph(memo, "Readiness actions", "Heading 1")
word_table(memo, [
    ["Workstream", "Action", "Owner", "Due"],
    ["Support", "Publish rota", "R. Example", "20 Nov"],
    ["Training", "Book two sessions", "J. Placeholder", "24 Nov"],
    ["Facilities", "Check meeting room", "A. Fiction", "26 Nov"],
    ["Communications", "Send staff notice", "C. Sample", "27 Nov"],
])
paragraph(memo, "Distribution: internal demo only | Contact: ops@example.test")
word_page_furniture(memo, "EXAMPLE WORKS LTD. | FICTIONAL TEST DATA")
make_docx("01-operations-memo", memo)

proposal = []
paragraph(proposal, "FICTIONAL TEST DOCUMENT - Service Proposal", "Title")
paragraph(proposal, "Prepared for Example Works Ltd. by Northstar Office Services (fictional vendor) | Proposal Q-26041 | 14 November 2026")
paragraph(proposal, "1. Executive summary", "Heading 1")
paragraph(proposal, "Northstar proposes a twelve-week records-modernization pilot using invented systems and sample records. No real customer or employee data is included.")
paragraph(proposal, "2. Scope and deliverables", "Heading 1")
paragraph(proposal, "The pilot covers a discovery workshop, sample-data migration, quality review, staff handover, and a close-out report. Production access and live credentials are out of scope.")
paragraph(proposal, "The vendor will provide:", "Heading 2")
bullet_list(proposal, ["A process map based on fictional workflows.", "A migration prototype containing synthetic records only.", "A validation log and a short staff handover."])
word_table(proposal, [
    ["Phase", "Weeks", "Output", "Acceptance evidence"],
    ["Discovery", "1-2", "Process map", "Approved sample map"],
    ["Prototype", "3-6", "Import workflow", "Ten fabricated records"],
    ["Validation", "7-9", "Test report", "Issues reviewed"],
    ["Handover", "10-12", "Runbook", "Materials delivered"],
])
paragraph(proposal, "3. Assumptions and exclusions", "Heading 1")
paragraph(proposal, "The client will nominate one fictional contact and provide only the synthetic files bundled with this test. Any scope change requires a written change note. This proposal has no commercial force.")
paragraph(proposal, "Commercial schedule", "Heading 2")
word_table(proposal, [
    ["Milestone", "Fee (USD)", "Invoice trigger"],
    ["Discovery complete", "4,800", "Acceptance of map"],
    ["Prototype review", "9,600", "Pilot review"],
    ["Handover", "4,800", "Runbook delivered"],
])
paragraph(proposal, "Questions: proposal@example.test | 100 Placeholder Lane, Example City")
word_page_furniture(proposal, "NORTHSTAR OFFICE SERVICES | PROPOSAL Q-26041 | FICTIONAL")
make_docx("02-service-proposal", proposal)

invoice = []
paragraph(invoice, "FICTIONAL TEST DOCUMENT - Tax Invoice", "Title")
paragraph(invoice, "EXAMPLE WORKS LTD. | Invoice EW-2026-041 | Issued 14 November 2026 | Due 14 December 2026")
paragraph(invoice, "Supplier: Northstar Office Services, 100 Placeholder Lane, Example City, ZZ 00000, tax ID 00-0000000")
paragraph(invoice, "Bill to: Example Works Ltd., Accounts Payable, 42 Fiction Road, Sampletown, ZZ 00000 | ap@example.test")
paragraph(invoice, "Services supplied", "Heading 1")
word_table(invoice, [
    ["Code", "Description", "Qty", "Rate", "Amount"],
    ["DISC-01", "Discovery workshop", "2", "850.00", "1,700.00"],
    ["DATA-02", "Sample data preparation", "12", "125.00", "1,500.00"],
    ["MIG-03", "Migration prototype setup", "18", "150.00", "2,700.00"],
    ["QA-04", "Validation and issue log", "10", "135.00", "1,350.00"],
    ["DOC-05", "Runbook and handover", "6", "140.00", "840.00"],
    ["SUP-06", "Post-pilot support sample", "4", "110.00", "440.00"],
])
paragraph(invoice, "Subtotal: USD 8,530.00    Tax (8.25%): USD 703.73    Total due: USD 9,233.73")
paragraph(invoice, "Payment and remittance", "Heading 1")
paragraph(invoice, "Payment terms: 30 days. Remittance details are intentionally nonfunctional: Example Bank, routing 000000000, account 0000000000. Reference EW-2026-041 on any test remittance.")
word_page_furniture(invoice, "EXAMPLE WORKS LTD. | INVOICE EW-2026-041 | FICTIONAL")
make_docx("03-vendor-invoice", invoice)

review = []
paragraph(review, "FICTIONAL TEST DOCUMENT - Quarterly Service Review", "Title")
paragraph(review, "Example Works Ltd. | Reporting period: Q3 2026 | Prepared by: Service Enablement | Internal demo only")
paragraph(review, "Executive overview", "Heading 1")
paragraph_with_footnote(review, "This review summarizes an invented support service. These are illustrative values, not measurements of a real company, system, or person.", "All organizations, people, survey results, and service measurements in this document are fabricated.")
paragraph(review, "The team recommends retaining the current service window and improving the self-service guide.")
paragraph_with_link(review, "Reference material: ", "https://portal.example.test/guide", "fictional service guide")
paragraph(review, "Quarterly indicators", "Heading 1")
word_table(review, [
    ["Indicator", "Target", "Actual", "Comment"],
    ["Availability", "99.5%", "99.7%", "Synthetic monthly average"],
    ["First response", "4 hours", "3.2 hours", "Sample queue data"],
    ["Resolution", "2 days", "1.6 days", "No real tickets included"],
    ["Satisfaction", "4.2 / 5", "4.4 / 5", "Invented survey responses"],
])
review.append(command("text.pageBreak"))
paragraph(review, "Risks and follow-up", "Heading 1")
paragraph(review, "The largest modeled risk is inconsistent terminology in older help articles. The proposed response is an editorial pass followed by review with fictional pilot participants.")
paragraph(review, "Action register", "Heading 2")
word_table(review, [
    ["ID", "Action", "Owner", "Review date"],
    ["R-01", "Consolidate duplicate help pages", "T. Example", "02 Dec 2026"],
    ["R-02", "Add a sample escalation flow", "M. Sample", "09 Dec 2026"],
    ["R-03", "Recheck response target", "J. Placeholder", "16 Dec 2026"],
    ["R-04", "Publish revised guide", "A. Fiction", "18 Dec 2026"],
])
paragraph(review, "Prepared for compatibility testing. Contact: service-review@example.test")
word_page_furniture(review, "EXAMPLE WORKS LTD. | QUARTERLY REVIEW | FICTIONAL")
make_docx("04-quarterly-review", review)

markup = []
paragraph(markup, "FICTIONAL TEST DOCUMENT - Draft Review Notes", "Title")
paragraph(markup, "Example Works Ltd. | Draft 0.3 | Reviewer: Compatibility Test Fixture | No real parties or project data")
paragraph(markup, "Summary", "Heading 1")
paragraph(markup, "The sample audit group verified 14 fictional records against the agreed test checklist.")
markup.append(command("review.trackChanges", {"value": True}))
markup.extend((command("select.text", {"text": "sample audit group"}), command("text.insert", {"text": "fictional QA group"})))
markup.extend((command("select.text", {"text": "14 fictional records"}), command("review.newComment", {"text": "This count is synthetic and exists only to exercise comment import."})))
paragraph(markup, "Open items", "Heading 1")
paragraph(markup, "Confirm that the generated workbook totals match the fixed test data before comparing imported ODS output.")
word_page_furniture(markup, "EXAMPLE WORKS LTD. | REVIEW DRAFT | FICTIONAL")
make_docx("05-review-markup", markup)


def values(address, rows):
    return command("range.setValues", {"range": address, "values": rows})


budget = [
    command("file.new", {}), command("sheet.rename", {"name": "Monthly Budget"}),
    values("A1:G15", [
        ["FICTIONAL TEST DATA - Example Works Ltd. Operating Budget", None, None, None, None, None, None],
        ["Month", "Payroll", "Facilities", "Software", "Travel", "Other", "Total"],
        ["Jan", 48200, 8400, 3100, 1250, 900, "=SUM(B3:F3)"],
        ["Feb", 47900, 8400, 3100, 980, 1100, "=SUM(B4:F4)"],
        ["Mar", 49100, 8400, 3250, 1420, 875, "=SUM(B5:F5)"],
        ["Apr", 48800, 8400, 3250, 1100, 950, "=SUM(B6:F6)"],
        ["May", 50200, 8400, 3250, 1675, 1200, "=SUM(B7:F7)"],
        ["Jun", 49700, 8400, 3400, 1450, 980, "=SUM(B8:F8)"],
        ["Jul", 51100, 8600, 3400, 1890, 1300, "=SUM(B9:F9)"],
        ["Aug", 50800, 8600, 3400, 1225, 1050, "=SUM(B10:F10)"],
        ["Sep", 51900, 8600, 3550, 1550, 975, "=SUM(B11:F11)"],
        ["Oct", 52300, 8600, 3550, 1780, 1250, "=SUM(B12:F12)"],
        ["Nov", 51800, 8600, 3550, 1325, 1100, "=SUM(B13:F13)"],
        ["Dec", 53400, 8600, 3650, 2100, 1400, "=SUM(B14:F14)"],
        ["Annual total", "=SUM(B3:B14)", "=SUM(C3:C14)", "=SUM(D3:D14)", "=SUM(E3:E14)", "=SUM(F3:F14)", "=SUM(G3:G14)"],
    ]),
    command("insert.table", {"range": "A2:G14", "header": True, "style": "TableStyleMedium2", "name": "MonthlyBudget"}),
    command("home.numberFormat", {"range": "B3:G15", "format": "Currency"}),
    command("home.conditionalFormat", {"range": "G3:G14", "rule": {"type": "dataBar", "color": "#5B9BD5"}}),
    command("view.freezePanes", {"cell": "B3"}), command("home.insertSheet", {"name": "Assumptions"}),
    values("A1:B5", [["FICTIONAL TEST DATA - Assumption", "Value"], ["Organization", "Example Works Ltd."], ["Currency", "USD"], ["Period", "Calendar year 2026"], ["Contact", "finance@example.test"]]),
]
make_xlsx("01-operating-budget", budget)

order_rows = [
    ["Order", "Date", "Customer", "Region", "Item", "Units", "Net sales"],
    ["EW-26001", "2026-01-08", "Acme Example", "North", "Desk lamp", 12, "=F3*42.5"],
    ["EW-26002", "2026-01-13", "Blue Sample Co", "West", "Notebook set", 35, "=F4*18"],
    ["EW-26003", "2026-01-22", "Fable Supply", "East", "Storage box", 18, "=F5*27.25"],
    ["EW-26004", "2026-02-02", "Northwind Demo", "South", "Desk lamp", 9, "=F6*42.5"],
    ["EW-26005", "2026-02-11", "Cedar Placeholder", "North", "Cable organizer", 42, "=F7*8.75"],
    ["EW-26006", "2026-02-19", "Acme Example", "East", "Notebook set", 28, "=F8*18"],
    ["EW-26007", "2026-03-04", "Blue Sample Co", "West", "Storage box", 21, "=F9*27.25"],
    ["EW-26008", "2026-03-16", "Fable Supply", "South", "Cable organizer", 31, "=F10*8.75"],
    ["EW-26009", "2026-04-03", "Northwind Demo", "North", "Notebook set", 44, "=F11*18"],
    ["EW-26010", "2026-04-18", "Cedar Placeholder", "East", "Desk lamp", 15, "=F12*42.5"],
    ["EW-26011", "2026-05-06", "Acme Example", "West", "Storage box", 26, "=F13*27.25"],
    ["EW-26012", "2026-05-21", "Blue Sample Co", "South", "Cable organizer", 55, "=F14*8.75"],
    ["EW-26013", "2026-06-02", "Fable Supply", "North", "Desk lamp", 11, "=F15*42.5"],
    ["EW-26014", "2026-06-14", "Northwind Demo", "East", "Notebook set", 39, "=F16*18"],
]
sales = [
    command("file.new", {}), command("sheet.rename", {"name": "Orders"}),
    values("A1:G16", [["FICTIONAL TEST DATA - Example Works Ltd. Sales Ledger", None, None, None, None, None, None], *order_rows]),
    command("insert.table", {"range": "A2:G16", "header": True, "style": "TableStyleMedium4", "name": "ExampleOrders"}),
    command("home.numberFormat", {"range": "G3:G16", "format": "Currency"}), command("data.filter", {"range": "A2:G16"}),
    command("view.freezeTopRow", {}), command("home.insertSheet", {"name": "By Region"}),
    values("A1:C6", [["FICTIONAL TEST DATA - Region", "Orders", "Net sales"], ["North", "=COUNTIF(Orders!D3:D16,A2)", "=SUMIF(Orders!D3:D16,A2,Orders!G3:G16)"], ["South", "=COUNTIF(Orders!D3:D16,A3)", "=SUMIF(Orders!D3:D16,A3,Orders!G3:G16)"], ["East", "=COUNTIF(Orders!D3:D16,A4)", "=SUMIF(Orders!D3:D16,A4,Orders!G3:G16)"], ["West", "=COUNTIF(Orders!D3:D16,A5)", "=SUMIF(Orders!D3:D16,A5,Orders!G3:G16)"], ["All regions", "=SUM(B2:B5)", "=SUM(C2:C5)"]]),
    command("home.numberFormat", {"range": "C2:C6", "format": "Currency"}),
    command("insert.chart", {"range": "A1:B5", "type": "column", "title": "Orders by region", "at": "E2"}),
]
make_xlsx("02-sales-ledger", sales)

inventory = [
    command("file.new", {}), command("sheet.rename", {"name": "Stock"}),
    values("A1:H10", [
        ["FICTIONAL TEST DATA - Example Works Ltd. Inventory Plan", None, None, None, None, None, None, None],
        ["SKU", "Description", "Supplier", "On hand", "Reorder at", "Unit cost", "Reorder qty", "Stock value"],
        ["EX-1001", "Desk lamp", "Cedar Placeholder", 42, 18, 42.5, "=MAX(0,E3-D3)", "=D3*F3"],
        ["EX-1002", "Notebook set", "Blue Sample Co", 16, 24, 18, "=MAX(0,E4-D4)", "=D4*F4"],
        ["EX-1003", "Storage box", "Fable Supply", 31, 15, 27.25, "=MAX(0,E5-D5)", "=D5*F5"],
        ["EX-1004", "Cable organizer", "Northwind Demo", 9, 30, 8.75, "=MAX(0,E6-D6)", "=D6*F6"],
        ["EX-1005", "Monitor riser", "Cedar Placeholder", 14, 12, 54, "=MAX(0,E7-D7)", "=D7*F7"],
        ["EX-1006", "Label roll", "Blue Sample Co", 7, 20, 6.4, "=MAX(0,E8-D8)", "=D8*F8"],
        ["EX-1007", "Shipping sleeve", "Fable Supply", 85, 40, 1.25, "=MAX(0,E9-D9)", "=D9*F9"],
        ["EX-1008", "Whiteboard kit", "Northwind Demo", 11, 10, 33.8, "=MAX(0,E10-D10)", "=D10*F10"],
    ]),
    command("insert.table", {"range": "A2:H10", "header": True, "style": "TableStyleMedium2", "name": "ExampleInventory"}),
    command("home.numberFormat", {"range": "F3:F10", "format": "Currency"}), command("home.numberFormat", {"range": "H3:H10", "format": "Currency"}),
    command("home.conditionalFormat", {"range": "D3:D10", "rule": {"type": "cellIs", "operator": "less", "value": 20, "preset": "lightRedFill"}}),
    command("data.validation", {"range": "E3:E10", "type": "whole", "operator": "greaterOrEqual", "formula1": "0", "errorTitle": "Invalid reorder point", "errorMessage": "Enter a non-negative whole number."}),
    command("view.freezePanes", {"cell": "A3"}), command("home.insertSheet", {"name": "Suppliers"}),
    values("A1:D5", [["FICTIONAL TEST DATA - Supplier Directory", "Contact", "Email", "Terms"], ["Cedar Placeholder", "R. Example", "cedar@example.test", "Net 30"], ["Blue Sample Co", "T. Sample", "blue@example.test", "Net 45"], ["Fable Supply", "J. Fiction", "fable@example.test", "Net 30"], ["Northwind Demo", "A. Placeholder", "northwind@example.test", "Net 15"]]),
    command("insert.table", {"range": "A1:D5", "header": True, "style": "TableStyleMedium4", "name": "ExampleSuppliers"}),
]
make_xlsx("03-inventory-plan", inventory)

portfolio = [
    command("file.new", {}), command("sheet.rename", {"name": "Projects"}),
    values("A1:G10", [
        ["FICTIONAL TEST DATA - Example Works Ltd. Project Portfolio", None, None, None, None, None, None],
        ["Project ID", "Project", "Lead", "Budget", "Actual", "Variance", "Status"],
        ["PX-101", "Archive refresh", "A. Example", 18000, 14200, "=D3-E3", "Active"],
        ["PX-102", "Access audit", "B. Sample", 12000, 8900, "=D4-E4", "New"],
        ["PX-103", "Search refresh", "C. Placeholder", 25000, 27100, "=D5-E5", "Paused"],
        ["PX-104", "Help center", "D. Fiction", 9000, 6400, "=D6-E6", "Done"],
        ["PX-105", "Form redesign", "E. Example", 14500, 9600, "=D7-E7", "Active"],
        ["PX-106", "Data dictionary", "F. Sample", 7800, 5200, "=D8-E8", "New"],
        ["PX-107", "Export review", "G. Placeholder", 11000, 11800, "=D9-E9", "Active"],
        ["PX-108", "Onboarding kit", "H. Fiction", 6200, 4100, "=D10-E10", "Done"],
    ]),
    command("insert.table", {"range": "A2:G10", "header": True, "style": "TableStyleMedium4", "name": "ExamplePortfolio"}),
    command("home.numberFormat", {"range": "D3:F10", "format": "Currency"}),
    command("home.conditionalFormat", {"range": "F3:F10", "rule": {"type": "colorScale", "colors": ["#F8696B", "#FFEB84", "#63BE7B"]}}),
    command("data.validation", {"range": "G3:G10", "type": "list", "formula1": "\"New,Active,Paused,Done\""}),
    command("view.freezeTopRow", {}), command("insert.chart", {"range": "B2:E10", "type": "bar", "title": "Project budget and actual", "at": "I2"}),
    command("formulas.defineName", {"name": "PortfolioBudget", "refersTo": "=Projects!$D$3:$D$10", "comment": "Fictional project budgets"}),
    command("home.insertSheet", {"name": "Status Guide"}),
    values("A1:B5", [["FICTIONAL TEST DATA - Status", "Meaning"], ["New", "Not started"], ["Active", "In progress"], ["Paused", "Waiting for a decision"], ["Done", "Complete in this sample"]]),
    command("insert.table", {"range": "A1:B5", "header": True, "style": "TableStyleMedium2", "name": "StatusDefinitions"}),
]
make_xlsx("04-project-portfolio", portfolio)

subprocess.run([GRIDCRAFT, "check", str(OUTPUT / "xlsx")], check=True)


def import_with_grind(kind, extension, verb, output_extension):
    for source in sorted((OUTPUT / kind).glob(f"*.{extension}")):
        name = source.stem
        imported = OUTPUT / "imported" / kind / f"{name}.{output_extension}"
        report = OUTPUT / "reports" / kind / f"{name}.json"
        info = OUTPUT / "reports" / kind / f"{name}-info.json"
        with report.open("w", encoding="utf-8") as stream:
            subprocess.run([GRIND, *verb, str(source), str(imported), "--force", "--format", "json"], check=True, stdout=stream)
        with info.open("w", encoding="utf-8") as stream:
            subprocess.run([GRIND, "info", str(imported), "--format", "json"], check=True, stdout=stream)


import_with_grind("docx", "docx", ["text", "import"], "odt")
import_with_grind("xlsx", "xlsx", ["sheet", "import"], "ods")
print(f"Created 5 DOCX, 4 XLSX, and Grind imports/reports in {OUTPUT}")