# Grind Office compatibility corpus

Build fictional Word and Excel compatibility files with WordCraft and GridCraft, import them through Grind into ODT/ODS, and save Grind's JSON conversion reports beside each imported file. The container installs pinned, checksum-verified WordCraft and GridCraft packages and builds Grind, so no local Craft CLI installation is needed.

```sh
docker build -t grind-sample-corpus .
docker run --rm -v "$PWD/samples:/workspace/samples" grind-sample-corpus
```

The corpus is written to `samples/compatibility/`. To write elsewhere, pass the output directory after the image name:

```sh
docker run --rm -v "$PWD/output:/output" grind-sample-corpus /output
```

The generator can also run directly with `wordcraft-cli`, `gridcraft-cli`, and a Grind build with DOCX/XLSX import enabled:

```sh
GRIND_BIN=/path/to/grind bash scripts/create_samples.sh
```

The corpus includes fictional memos, proposals, invoices, reviews, and workbooks with headings, tables, lists, hyperlinks, tracked changes and comments, formulas, multiple sheets, filters, charts, validation, conditional formatting, and defined names. Names, contacts, dates, and figures are fabricated; `.test` email addresses and `FICTIONAL TEST DATA` labels make that explicit. Generated files are overwritten on each run.

The GitHub Actions workflow builds the same image, generates and imports the corpus, and uploads `samples/compatibility/` as an artifact. Reports may record intentional conversion losses, especially for spreadsheet charts and validation.