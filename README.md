# ⚡ Momentum Rank Screener

A quantitative equity screening and position-sizing web app built with **Python**, **Streamlit**, and **yfinance**. It dynamically pulls constituent lists across 14 NSE broad-market indices, ranks stocks by historical price momentum, calculates equal-weight share quantities in INR, and exports actionable watchlists to CSV.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![yfinance](https://img.shields.io/badge/yfinance-Market%20Data-6001D2)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-brightgreen)](https://momentum-screener.streamlit.app/)

---

## 📌 Overview

Implementing a systematic momentum investing strategy on Indian equities typically requires manually downloading index constituents, pulling historical prices, calculating returns, and sizing positions in a spreadsheet. **Momentum Rank Screener** automates this entire pipeline:

1. **Universe Selection:** Choose from 14 official NSE broad-market indices (spanning Large-cap, Mid-cap, Small-cap, and Micro-cap segments).
2. **Momentum Ranking:** Downloads daily closing prices over any custom lookback window (default: 1 year) and ranks constituents by percentage return.
3. **Position Sizing & Export:** Automatically calculates the number of shares (`Qty`) to buy per stock based on your INR allocation and exports the top `N` stocks as a ready-to-use CSV.

---

## ✨ Key Features

- **14 Live NSE Stock Universes:** Fetches official constituent lists directly from NSE India archives—covering Nifty 50, Nifty Next 50, Nifty 100, Nifty 200, Nifty Midcap 50/100/150, Nifty Smallcap 50/100/250, Nifty LargeMidcap 250, Nifty MidSmallcap 400, Nifty 500, and Nifty Microcap 250.
- **Custom Lookback Period:** Flexible start and end date pickers (defaults to a trailing 365-day window).
- **Automated Position Sizing:** Takes a user-defined per-stock allocation in `₹` and computes rounded share quantities against each stock's Latest Traded Price (LTP).
- **One-Click CSV Export:** Download the ranked portfolio list (`data.csv`) for immediate execution or further backtesting.
- **Built-in Index Reference Guide:** Displays an in-app market-cap positioning table explaining the rank coverage of each NSE index (e.g., `1–50` for Nifty 50 up to `501–750` for Nifty Microcap 250).

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python |
| **Frontend / UI** | Streamlit |
| **Market Data** | `yfinance` (Yahoo Finance) & NSE India Index Archives |
| **Data Processing** | Pandas, NumPy |

---

## ⚙️ How It Works

1. **Constituent Ingestion:** Reads the selected NSE index CSV directly from `archives.nseindia.com` and appends `.NS` to each ticker symbol for Yahoo Finance compatibility.
2. **Historical Data Retrieval:** Uses `yf.download()` to fetch daily `Close` prices across the entire selected universe for the chosen date range.
3. **Return & Sizing Calculation:**
   - **Momentum Return:**
     $$\text{Return (\%)} = \left(\frac{\text{End Close} - \text{Start Close}}{\text{Start Close}}\right) \times 100$$
   - **Share Quantity:**
     $$\text{Qty} = \text{round}\left(\frac{\text{Allocation (₹)}}{\text{LTP}}\right)$$
4. **Output:** Sorts all constituents in descending order of return, filters to the top `N` stocks, and renders an interactive table with a CSV download button.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- `pip` package manager

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone [https://github.com/shubhamharwani/](https://github.com/shubhamharwani/)<repo-name>.git
   cd <repo-name>
