# 🚇 TTC Ridership Analysis

An exploratory data analysis of **Toronto Transit Commission ridership from 2003 to 2026**, built on open data published by the City of Toronto. The project traces two decades of growth to a **2016 peak**, the COVID-19 collapse, and the recovery that has stalled at **78% of 2019**, measured across four indicators: monthly ridership, average weekday ridership, and annual peak / non-peak passenger rides.

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
├── visualizations/                     # charts exported by the notebook (150 dpi)
│   ├── 02_annual_ridership.png         #   annual totals + trailing 12-month series
│   ├── 02_peak_vs_nonpeak.png          #   peak vs non-peak stacked area
│   ├── 02_yoy_growth.png               #   year-over-year change by era
│   ├── 03_seasonality_heatmap.png      #   rides per day, year × month
│   ├── 03_seasonality_era.png          #   seasonality index by era
│   ├── 03_445_artifact.png             #   raw totals vs rides per reporting day
│   ├── 04_recovery_index.png           #   monthly index vs the same month of 2019
│   ├── 04_recovery_by_month.png        #   recovery completeness by calendar month
│   ├── 04_recovery_ladder.png          #   Jan–Sep recovery ladder, per reporting day
│   ├── 05_peak_share.png               #   peak-hour share, measured vs constructed years
│   ├── 05_peak_vs_nonpeak_index.png    #   peak vs non-peak indexed to 2019
│   ├── 06_weekday_vs_weekend.png       #   weekday and implied weekend ridership
│   ├── 06_weekend_recovery.png         #   weekday vs weekend recovery index
│   └── 07_dashboard.png                #   2×2 summary dashboard
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
- **Series reconcile internally** — summed monthly ridership reproduces the annual peak + non-peak total to within **0.011%** for every year from 2008 to 2025. Once the annual figures are rescaled from thousands to whole rides, the two independently published series agree to rounding.
- **The monthly series is reported on 4-4-5 financial periods, not calendar months** — eight 4-week blocks plus four 5-week blocks, so every year covers exactly `8 × 28 + 4 × 35 = 364` days. This is why monthly ÷ weekday ridership sits at ~26.5 in every year: it is the weighted mix of two regimes, ~24.3 (4-week) and ~30.1 (5-week). See [Reporting periods](#-reporting-periods-are-4-4-5) below.
- **The peak / non-peak split is not always measured.** In 7 of 23 years the published peak figure is a *round percentage* of the annual total — 2022, 2023 and 2024 are **41.0001%**, **41.0001%** and **41.0000%**, and 2025 is **42.0000%**, all accurate to within a few hundred rides out of ~170M. That cannot arise from measurement. Section 5.1 flags those years, so the split is treated as evidence only up to 2021.
- **The 4-4-5 model checks itself.** Using period length and the weekday series to back out weekend ridership gives 817,438 rides/day from 4-week periods and 819,200 from 5-week periods — **0.22% apart**. Two independent period lengths agreeing that closely is confirmation that the recovered period table is right.

### Data quirk to know about

In the upstream file, annual rows store the *year* in `period_number_in_year` rather than a period index. That is why `Period` is null for annual measures here — the export maps month numbers only for `interval_type == "m"`.

### 📐 Reporting periods are 4-4-5

The periodisation is not published in this extract, so the notebook recovers it from two independent columns — `monthly rides ÷ average weekday rides` gives **weekday-equivalent days** per reporting month:

| | 4-week period | 5-week period |
|---|---|---|
| Weekday-equivalent days (median) | 24.34 | 30.26 |
| Observations (2008–2025, excl. 2020–22) | 126 | 63 |
| Range | 20.4 – 27.4 | 27.6 – 38.4 |

The two regimes separate by 5.9 days with no overlap, and every complete year sums to 364 days. **Mar and Jun are 5-week in every year on record**; the other two 5-week slots rotate between Jan, Sep, Nov and Dec — 2018 is the only year where the fourth 5-week period falls in **November**, which is why that year shows a −22.6% December against a +21.2% November.

Practical consequences, all handled in the notebook:

| If you… | Why it breaks | What the notebook does instead |
|---|---|---|
| compare consecutive months | a 5-week month reads as a **+25%** jump | reports `rides_per_day`, not monthly totals |
| divide by calendar days | 5-week months look 25% more productive | divides by `period_days` (28 / 35) |
| quote a monthly figure as a month | it is a 4- or 5-week period total | labels it a reporting period throughout |

Section 3.3 measures the size of that effect: indexed across months, the raw totals vary **2.36×** more than the same ridership measured per reporting day.

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
- [x] **Section 1 — Normalise & shape** — split annual vs monthly measures, map `Period` → month number, build a `DatetimeIndex`, recover the 4-4-5 reporting periods, derive rides per day, and build the `monthly` / `annual` / `ytd()` analysis frames
- [x] **Section 2 — Long-term growth** — annual totals with a trailing 12-month overlay, peak vs non-peak stacked area, and year-over-year change split into growth / plateau / collapse / recovery eras
- [x] **Section 3 — Seasonality** — year × month heatmap of rides per reporting day, seasonality index by era, and the 4-4-5 distortion isolated against the corrected series
- [x] **Section 4 — COVID shock & recovery** — monthly 2019-indexed series on a per-reporting-day basis, recovery completeness by calendar month, and the Jan–Sep recovery ladder through 2026
- [x] **Section 5 — Peak / non-peak structural shift** — peak-hour share with a roundness test that separates measured years from constructed splits, and the two halves indexed to 2019
- [x] **Section 6 — Weekday vs weekend** — weekend ridership backed out of the weekday series using the recovered period table, cross-validated across period lengths, then indexed to 2019
- [x] **Section 7 — Summary dashboard & key insights** — 2×2 dashboard plus a written findings table and limitations recap

---

## 🔍 Preliminary Findings

Verified while profiling, charting and asserting the series in Sections 1–7.

| Finding | Value |
|---|---|
| **Calendar-year peak** | **2016** — 538.1M rides. Not 2019: ridership fell in three of the four years to 2018 and 2019 was still **−2.3%** below 2016 |
| **Strongest 12 months on record** | **541.3M**, the window ending **February 2018** — higher than any calendar year, because it blends a strong 2017 second half with a strong 2018 first half |
| Growth rate, 2003 → 2016 | **+2.20%/yr** compound, **+32.7%** in total |
| Pre-COVID plateau | 2015–2019: ridership fell in 3 of 5 years, netting out 2.3% below the 2016 peak before the pandemic |
| 2019 → 2020 collapse | **−57.2%** (525.5M → 225.0M rides) |
| Trough year | **2021** — 197.8M rides, **−63.2%** from the 2016 peak |
| 2025 vs 2019 recovery | **−21.4%** — still short of pre-pandemic ridership |
| Peak-hour vs non-peak recovery | peak-hour rides **−27.0%** vs 2019, non-peak **−16.8%** — a 10.2-point gap. The direction matches every measured year, but see the split warning below: the 2025 numbers come from a constructed split |
| **Peak-hour share (measured years)** | **47.25% (2003) → 43.00% (2014) → 45.22% (2019) → 39.92% (2021)**: down 4.3 points over eleven years, back up 2.2 by 2019 (off-peak slipped faster than peak in the plateau), then down 5.3 in the collapse |
| **Peak/non-peak split quality** | the split is a round percentage of the total in **7 of 23 years** (2014, 2016, 2020, **2022, 2023, 2024, 2025**) — so it is evidence only through 2021 (§5.1) |
| **Weekends came back, weekdays did not** | 2025 vs 2019: weekday ridership **76.5%**, implied weekend ridership **91.4%** — a **14.9-point** gap, and the weekend/weekday ratio rose from 0.48 to 0.57 |
| 4-4-5 cross-validation | backing out weekend ridership from 4-week periods gives 817,438 rides/day, from 5-week periods 819,200 — **0.22% apart**, which independently confirms the period table |
| 2026 YTD (Jan–Sep) vs 2025 | **−1.0%** (303.4M vs 306.5M) — recovery has plateaued |
| Trailing 12 months to Sep 2026 | **410.0M**, −22.0% vs 2019 |
| **Strongest month** | **November** (index 1.07 vs the year's average month) — not September, which is second at 1.05 |
| **Weakest month** | **January** now, at index **0.87** — it was 0.99 before 2020. Pre-pandemic the trough was August (0.93) |
| Seasonal spread | widened from **13%** (2015–19) to **20%** (2023–25): the swing has deepened, not flattened |
| 4-4-5 distortion | raw monthly totals vary **2.36×** more across months than the true seasonal shape; March reads as +15.5% when its real index is 0.996 |
| **Fastest collapse** | April 2020 fell to **12.8%** of April 2019 in one reporting period; March 2020 was 51.5%, and January 2020 was still 122% |
| **Recovery plateau** | Jan–Sep recovery peaked at **79.9%** of 2019 in **2024**, then slipped to **78.7%** (2025) and **77.9%** (2026) — it is drifting down, not levelling |
| **Where recovery is stuck** | 2025 by month: everything sits at 77–81% of 2019 **except January at 72%**, and January is falling (77.7% → 72.4% → 65.9%) |
| Trap avoided | indexing *raw* monthly totals to 2019 makes December 2025 look like a **98.5%** recovery; per reporting day it is **78.8%**, because Dec 2019 was a 4-week period and Dec 2025 a 5-week one |

---

## ⚠️ Limitations

- **No route, line or station detail** — this extract is system-wide only, so "which line recovered fastest" is not answerable.
- **No fare revenue** — the upstream dataset also publishes `TTC Ridership Revenues` (237 monthly rows); adding it is the natural next extension.
- **Monthly granularity only** — no daily or hourly ridership.
- **2026 is partial** (Jan–Sep) — always compare year-to-date to year-to-date; the notebook's `ytd()` helper exists for exactly this.
- **TTC reports on 4-4-5 week financial periods**, so a "month" in this data is a 4- or 5-week block, not a calendar month. The period table is recovered and asserted in Section 1.3; raw month-over-month comparisons are not used anywhere, and month-level rates are always divided by reporting days (28 / 35), never calendar days.
- **The peak / non-peak split is a modelled number in 7 of 23 years**, including every year since 2022, so claims about the commuter market's recovery cannot lean on it — they lean on the weekday series in Section 6 instead.
- **Single-month values can be revised upstream** — e.g. December 2024 average weekday ridership (1,061k) is 13.0% below both December 2023 and December 2025 in a year that otherwise grew, while the same month's total stayed at 40.7M. It is flagged rather than "corrected", since the true figure is unknown; it also inflates the implied weekend estimate for that month.

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
