# NSE Index F&O Contract Specs (NIFTY & BANK NIFTY)

_Last reviewed: November 2026. Lot sizes and expiry rules change — always confirm on
nseindia.com → Products → Derivatives (or your broker's contract info) before trading._

| Item | NIFTY 50 | BANK NIFTY |
|---|---|---|
| Underlying | NIFTY 50 index | NIFTY Bank index |
| Lot size (verify) | 65 (revised from 75 in the Dec-2025/Jan-2026 cycle) | 30 (revised from 35 in the same cycle) |
| Weekly options | Yes — expire **Tuesday** | **No** weekly (discontinued Nov 2024) |
| Monthly options & futures | Last **Tuesday** of the month | Last **Tuesday** of the month |
| Holiday rule | Expiry moves to previous trading day | Same |
| Strike interval (near ATM) | 50 points (100 for far strikes) | 100 points |
| Settlement | Cash, at final settlement price (index close-based) | Cash |
| Trading hours | 9:15 AM – 3:30 PM IST (pre-open 9:00–9:08) | Same |
| Option style | European | European |

## SEBI F&O framework points (from Oct 2024 / 2025 circulars)

- Minimum contract value for index derivatives ≈ ₹15 lakh at introduction (lot sizes
  are calibrated to this — that's why they get revised as the index moves).
- Each exchange may have only **one** benchmark index with weekly expiry
  (NSE: NIFTY; BSE: SENSEX).
- Option premium is collected **upfront** from buyers.
- Extra ELM (2%) on short options on expiry day.
- Calendar-spread margin benefit removed on expiry day.
- Intraday monitoring of position limits.

## Quick reference: ₹ value of a 1-point move

- NIFTY: 1 pt × lot size (65) = ₹65 per lot
- BANK NIFTY: 1 pt × lot size (30) = ₹30 per lot

## Typical daily range heuristics (use VIX to estimate)

Expected 1-day 1σ move ≈ Spot × (VIX / 100) / √252
e.g. NIFTY 24,000 with VIX 14 → 24,000 × 0.14 / 15.87 ≈ ±212 pts.
Use `fno_calc.py futures --spot 24000 --vix 14` to compute.
