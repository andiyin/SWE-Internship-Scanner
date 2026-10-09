# SWE Internship Scanner

I keep a list of companies I'd like to intern at and check their career pages for software / AI internships. Scrolling through a CSV with a few hundred rows got annoying, so I built a small dashboard for it.

It shows which companies currently have open internships, groups them by how much I like the location (Munich first, then the rest of Germany, then other places in Europe) and links straight to the postings. The UI is in German.

## Run it

You only need Python 3, no packages.

```bash
./start.sh
```

This starts a local server on http://localhost:8765 and opens the dashboard in your browser. Stop it with `Ctrl + C`.

To use a different CSV:

```bash
./start.sh path/to/other.csv
```

## Updating the data

Just replace `career_pages_full.csv` and reload the page. The server checks the file's modification time on every page load and rebuilds the dashboard if it changed.

The CSV needs these columns:

`Company, Status, Position Title, Location, Location Tier, Direct Job URL, Career/Board URL, All Current Matches (count), Last Checked, Notes`

## Files

- `career_pages_full.csv` – the data (one row per company)
- `template.html` – the dashboard itself (HTML, CSS and JS in one file)
- `build.py` – reads the CSV and writes `dashboard.html`
- `serve.py` – local server that rebuilds when the CSV changes
- `start.sh` – starts everything

## Notes

The CSV only stores one posting per company. If a company has more matches, the dashboard shows the count and links to their career page for the rest.

The data is a snapshot from the last time I ran the scan, so postings might be gone by the time you look at them.
