# 🚇 TTC Ridership Analysis

An exploratory data analysis of **Toronto Transit Commission ridership from 2003 to 2026**, built on open data published by the City of Toronto. The project traces two decades of growth, the COVID-19 collapse and the still-incomplete recovery, measured across four indicators: monthly ridership, average weekday ridership, and annual peak / non-peak passenger rides.

This is a portfolio project: every number and chart in the notebook is reproducible from the public data source documented below.

> 📍 Data source: [City of Toronto Open Data Portal — Toronto's Dashboard Key Indicators](https://open.toronto.ca/dataset/toronto-s-dashboard-key-indicators/)

---

## 📁 Project Structure

```
TTC/
│
├── Data_source/
│   └── TorontoMeasureData.csv          # committed — 508 rows × 4 columns (23 KB)
│
├── visualizations/                     # charts exported from the notebook
│
├── ttc_analysis.ipynb                  # EDA notebook
├── requirements.txt                    # pinned dependencies
├── .venv/                              # local virtual environment (not committed)
│
└── README.md
```

---

## 📊 Dataset Overview

| Property | Detail |
|---|---|
| Total Rows | 508 observations |
| Columns | 4 (`Measure Name`, `Year`, `Period`, `Value`) |
| Years | 2003 – 2026 (monthly series start in 2007 / 2008) |
| Measures | 4 |
| Format | Tidy / long — one observation per row |
| Missing Values | 46 nulls in `Period`, all structural (annual measures) |
| Duplicates | None |
| File Size | 23,132 bytes (~23 KB) |
| Committed | Yes — included in the repo, so clone → Run All needs no setup |
| Source Format | Filtered export of a 1.8 MB multi-indicator CSV |

### Columns

| Column | Type | Description |
|---|---|---|
| `Measure Name` | str | One of four TTC indicators (see below) |
| `Year` | int64 | Calendar year of the observation |
| `Period` | str | Month abbreviation (`Jan`–`Dec`); **null** for annual measures |
| `Value` | int64 | Ridership count — monthly figures are raw rides, annual figures are in thousands |

### Measures

| Measure Name | Rows | Granularity | Coverage |
|---|---|---|---|
| `TTC Average Weekday Ridership` | 237 | Monthly | 2007 – 2026 (2026 partial) |
| `TTC Monthly Ridership` | 225 | Monthly | 2008 – 2026 (2026 partial) |
| `TTC Annual Passenger Rides Peak (000s)` | 23 | Annual | 2003 – 2025 |
| `TTC Annual Passenger Rides Non-Peak (000s)` | 23 | Annual | 2003 – 2025 |

> ⚠️ **2026 is incomplete** — it contains January through September only. Any year-over-year comparison against 2026 must be YTD-matched (same months), otherwise the partial year reads as a false ~25% collapse.

---

## 🧪 Data Quality Checks (already verified)

- **No duplicate keys** — `Measure Name` + `Year` + `Period` is unique across all 508 rows.
- **No missing values** in `Measure Name`, `Year` or `Value`.
- **The 46 null `Period` values are structural**, not dirty data — the two annual measures have no month dimension.
- **Series reconcile internally** — summed monthly ridership reproduces the annual peak + non-peak total within 100.0% for every year from 2008 to 2025.
- **Consistent ratio** — monthly ridership ÷ average weekday ridership sits at ~26.5 every year, confirming both monthly series are measured on the same basis.

### Data quirk to know about

In the upstream file, annual rows store the *year* in `period_number_in_year` rather than a period index. That is why `Period` is null for annual measures here — the export maps month numbers only for `interval_type == "m"`.

---

## 📥 Data Source & Setup

The 23 KB data file **ships with this repository**, so a fresh clone runs the notebook immediately — there is no download or setup step. It is a small, curated extract of a much larger open dataset; the full 1.8 MB source file stays upstream, and the sibling Bike Share project keeps its multi-hundred-MB raw dumps out of git.

Because of that, the committed data can be **verified from first principles** — see [Verify the data](#verify-the-data-sha-256) below.

| Property | Detail |
|---|---|
| Dataset | Toronto's Dashboard Key Indicators |
| Publisher | City of Toronto — City Manager's Office, Performance Management |
| Portal page | https://open.toronto.ca/dataset/toronto-s-dashboard-key-indicators/ |
| Licence | Open Government Licence – Toronto |
| Refresh rate | Daily (dataset last refreshed 2026-11-04) |
| Direct CSV | [`torontos-dashboard-key-metrics.csv`](https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/c6d64e9b-f85a-4084-be14-60cf18509203/resource/d4c2d841-2d74-466c-89a8-d8f7eba17050/download/torontos-dashboard-key-metrics.csv) |

### Verify the data (SHA-256)

The committed CSV is byte-identical to what the City of Toronto feed produces for these four measures — so you don't have to take that on trust. Check it yourself:

```bash
# macOS / Linux
shasum -a 256 Data_source/TorontoMeasureData.csv
# -> a962c429d162586397261281a74c4503b9bebab7d05cd871075c27e232e886e5
```

```powershell
# Windows (PowerShell)
Get-FileHash Data_source\TorontoMeasureData.csv -Algorithm SHA256
```

| Check | Expected |
|---|---|
| **SHA-256** | `a962c429d162586397261281a74c4503b9bebab7d05cd871075c27e232e886e5` |
| Size | 23,132 bytes |
| Rows (excluding header) | 508 |
| Line endings | CRLF (the published export is Windows-formatted) |

If the upstream dashboard is refreshed and a measure's history is revised, this file and its hash change together — silent drift becomes impossible to miss, and the diff in git shows exactly which observations moved.

### Verify or rebuild the data file

The committed file is a **filtered export** of the ~1.8 MB dashboard CSV: four TTC measures only, four columns, month names expanded, annual `Period` left blank, rows ordered by dashboard `measure_id` and written with Windows (CRLF) line endings. Rebuilding it from the City's live feed reproduces the committed file byte-for-byte:

```python
from pathlib import Path

import pandas as pd

URL = (
    "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/"
    "c6d64e9b-f85a-4084-be14-60cf18509203/resource/"
    "d4c2d841-2d74-466c-89a8-d8f7eba17050/download/torontos-dashboard-key-metrics.csv"
)

MEASURES = [
    "TTC Average Weekday Ridership",
    "TTC Monthly Ridership",
    "TTC Annual Passenger Rides Peak (000s)",
    "TTC Annual Passenger Rides Non-Peak (000s)",
]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

src = pd.read_csv(URL)
out = src[src["measure_name"].isin(MEASURES)].copy()

# Monthly rows carry period 1-12; annual rows repeat the year in that column
out["Period"] = [
    MONTHS[int(p) - 1] if it == "m" and pd.notna(p) else None
    for p, it in zip(out["period_number_in_year"], out["interval_type"])
]
out["_month"] = [
    int(p) if it == "m" and pd.notna(p) else 0
    for p, it in zip(out["period_number_in_year"], out["interval_type"])
]

out = out.rename(columns={"measure_name": "Measure Name", "year": "Year"})
out["Value"] = out["measure_value"].astype("int64")

# Order: dashboard measure_id (2.03 -> 2.041 -> 2.042 -> 2.05), then chronologically
out = out.sort_values(["measure_id", "Year", "_month"]).reset_index(drop=True)
out = out[["Measure Name", "Year", "Period", "Value"]]

Path("Data_source").mkdir(exist_ok=True)
# the published export uses Windows (CRLF) line endings
out.to_csv(Path("Data_source") / "TorontoMeasureData.csv", index=False, lineterminator="\r\n")
print(f"wrote {len(out)} rows")   # -> wrote 508 rows
```

Nothing needs to be run to *use* this project — the data is already committed. That snippet is the **provenance check**: run it in a scratch directory and the CSV it writes will match the committed `Data_source/TorontoMeasureData.csv` byte-for-byte, so the export logic and the upstream feed can both be audited.

---

## 🚀 How to Run

```bash
# 1. nothing to install and nothing to download — open the notebook and Run All
jupyter notebook ttc_analysis.ipynb
```

Any Python 3 with pandas and matplotlib will run it (verified on pandas 2.2.2 *and* 3.1.0). To reproduce the exact pinned versions instead:

```bash
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook ttc_analysis.ipynb
```

In VS Code, select `.venv/bin/python` as the kernel for `ttc_analysis.ipynb`. `ipykernel` is in `requirements.txt` so the virtual environment can act as a kernel; if you have no Jupyter installation at all, add `jupyterlab`.

---

## 📈 Analysis Plan

- [x] Load and profile the dataset
- [ ] **Section 1 — Normalise & shape** — split annual vs monthly measures, map `Period` → month number, build a `DatetimeIndex`, derive rides per day
- [ ] **Section 2 — Long-term growth (2003–2019)** — annual totals, peak vs non-peak stacked area
- [ ] **Section 3 — Seasonality** — year × month heatmap, seasonality index, best/worst months per era
- [ ] **Section 4 — COVID shock & recovery** — 2019 = 100 indexed series through 2026 YTD
- [ ] **Section 5 — Peak / non-peak structural shift** — peak-hour share of total rides over time
- [ ] **Section 6 — Weekday vs total relationship** — the stable ~26.5 monthly-to-weekday ratio, and whether it shifted after 2020
- [ ] **Section 7 — Summary dashboard & key insights**

---

## 🔍 Preliminary Findings

Verified while profiling the data; not yet charted.

| Finding | Value |
|---|---|
| 2019 → 2020 collapse | **−57.2%** (525.5M → 225.0M rides) |
| Trough year | **2021** — 197.8M rides |
| 2025 vs 2019 recovery | **−21.4%** — still short of pre-pandemic ridership |
| 2026 YTD (Jan–Sep) vs 2025 | **−1.0%** (303.4M vs 306.5M) — recovery has plateaued |
| Peak-hour share of rides | 47.3% (2003) → 43.0% (2014) → 39.9% (2021) → 42.0% (2025) |

---

## ⚠️ Limitations

- **No route, line or station detail** — this extract is system-wide only, so "which line recovered fastest" is not answerable.
- **No fare revenue** — the upstream dataset also publishes `TTC Ridership Revenues` (237 monthly rows); adding it is the natural next extension.
- **Monthly granularity only** — no daily or hourly ridership.
- **2026 is partial** (Jan–Sep) — always compare year-to-date to year-to-date.
- The upstream notes for TTC's earlier monthly ridership file caution that TTC reports on 4-4-5 week financial periods, so single-month comparisons can be skewed by 4- vs 5-week periods.

---

## 🛠️ Tools Used

- Python 3.12.4
- pandas 3.1.0
- NumPy 2.5.4
- matplotlib 3.11.2
- Jupyter / VS Code notebooks

---

## 📂 Dataset

- **Source:** [City of Toronto Open Data Portal — Toronto's Dashboard Key Indicators](https://open.toronto.ca/dataset/toronto-s-dashboard-key-indicators/)
- **Licence:** [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
- **Records:** 508 observations across 4 TTC indicators, 2003 – 2026
- **Type:** Real open government data, refreshed daily

---

## 👤 Author

**NIO** — data analysis portfolio project. Ridership data © City of Toronto, used under the Open Government Licence – Toronto.
