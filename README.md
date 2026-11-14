# Grind Office compatibility corpus

Build realistic, explicitly fictional Word and Excel files with WordCraft and GridCraft, then import them through Grind into ODT/ODS. Grind's JSON conversion reports are saved beside each imported file so unsupported Office constructs are visible.

```sh
bash scripts/create_samples.sh
```

By default, this writes to `samples/compatibility/`. Set `GRIND_BIN` if Grind is not at the development-build path, or pass an output directory as the first argument:

```sh
GRIND_BIN=/path/to/grind bash scripts/create_samples.sh /tmp/office-compatibility
```

The corpus includes an operations memo, service proposal, vendor invoice, quarterly review, annual operating budget, sales ledger, inventory plan, and project portfolio. Names, contacts, account details, dates, and figures are fabricated; `.test` email addresses and `FICTIONAL TEST DATA` labels make that explicit. The files cover headings, tables, lists, footnotes, hyperlinks, tracked changes and comments, multi-page layout, formulas, dates, multiple sheets, filters, charts, validation, conditional formatting, and defined names.

Requirements: `wordcraft-cli`, `gridcraft-cli`, and a Grind build with DOCX/XLSX import enabled. The script overwrites its generated files on each run. Compatibility reports may show intentional losses, especially for spreadsheet charts and validation; those are test results, not generation failures.

```sh
grind info samples/compatibility/imported/docx/04-quarterly-review.odt
grind info samples/compatibility/imported/xlsx/04-project-portfolio.ods
cat samples/compatibility/reports/docx/04-quarterly-review.json
cat samples/compatibility/reports/xlsx/04-project-portfolio.json
gridcraft-cli check samples/compatibility/xlsx
```