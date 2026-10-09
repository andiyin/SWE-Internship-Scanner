# SWE Internship Scanner

**Live: https://swe-internship-scanner.vercel.app/**

I keep a list of interesting companies and check their career pages for software / AI internships. Scrolling through a CSV with 150+ rows got annoying, so I built a small dashboard for it.

It shows which companies currently have open internships and links straight to the postings. Every company has a tier (S+ to B) and every posting a location priority (Munich first, then the rest of Germany, then other places in Europe). The UI is in German, with an English version you can switch to in the top right (or open the link with `#en` at the end).

## What it can do

- filter by location, tier and internship / working student (you can pick several at once)
- search, and sort by location, tier or name
- see what's new since the last scan and what disappeared
- mark postings as saved or applied (stored in your browser only)
- light and dark mode

## Run it locally

You only need Python 3, no packages.

```bash
./start.sh
```

This starts a local server on http://localhost:8765 and opens the dashboard. Stop it with `Ctrl + C`.

## Updating the data

The dashboard is built from `career_pages_full.csv`. Replace the file and reload the page, the local server notices the change and rebuilds.

If your CSV lives in another folder, put the path into a file called `.csv-source` in this folder (it's gitignored) or set `CSV_PATH`. The build then reads from there and keeps the copy in this repo in sync.

The hosted site is rebuilt by Vercel on every push. To publish new data:

```bash
./publish.sh
```

It commits the CSV if it changed and pushes it.

On macOS this can run by itself. This installs a small background job that watches the CSV and runs `publish.sh` as soon as the file is changed or replaced:

```bash
./install-watcher.sh
```

`./install-watcher.sh remove` turns it off again.

The CSV needs these columns:

`Tier, Company, Status, Position Title, Location, Location Tier, Direct Job URL, Career/Board URL, All Current Matches (count), Last Checked, Notes`

## Files

- `career_pages_full.csv` – the data (one row per company)
- `template.html` – the dashboard itself (HTML, CSS and JS in one file)
- `build.py` – reads the CSV and writes `dashboard.html`
- `serve.py` – local server that rebuilds when the CSV changes
- `start.sh` / `publish.sh` – start locally / push new data
- `install-watcher.sh` – publish automatically when the CSV changes (macOS)
- `vercel.json` – build settings for Vercel

## Notes

The CSV only stores one posting per company. If a company has more matches, the dashboard shows the count and links to their career page for the rest.

The data is a snapshot from the last time I ran the scan, so postings might be gone by the time you look at them.
