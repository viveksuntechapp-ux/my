# Pre-Trade Checklist (go through this before every buy/sell)

Walk the user through these in order. Mark each item ✅ supports the trade,
❌ against it, or ➖ neutral/unknown. Ask the user for data you don't have —
never invent values.

## A. Pre-market (8:45–9:15 AM)

1. **GIFT Nifty** — expected gap. Gap > ~0.5% after a multi-week rally often fades
   (e.g. 23 Nov 2026: gap-up open reversed into a −1.75% day).
2. **Global cues** — US close (Dow, Nasdaq), Asian markets, crude oil, USD/INR.
   Weak rupee or crude spike = negative for Nifty.
3. **FII/DII flows** (previous day) — FIIs selling several days in a row = headwind.
4. **Events** — RBI policy, Fed, CPI/GDP, Budget, heavyweight results.
   Expiry day or day before a holiday → smaller size or skip.
5. **India VIX** — < 12 options cheap (buying OK); > 18 options costly (prefer spreads).
   VIX rising while Nifty falls = strong fall.

## B. Chart levels (mark before 9:15)

6. Previous day high / low / close; weekly high / low.
7. Trend on daily and 15-min chart — don't buy calls into lower highs/lower lows.
8. Round numbers (25,500 / 26,000; Bank Nifty 62,000 / 63,000).

## C. First 15–30 minutes after open

9. **Opening range** high/low — buy CE only on break & hold above ORH;
   buy PE only on break & hold below ORL.
10. **VWAP** — above = buyers in control; below = sellers in control.
11. **Heavyweights** — HDFC Bank, ICICI Bank, Reliance, Infosys, Bharti Airtel, TCS.
    If 4–5 are red, a call buy is risky.
12. **Bank Nifty vs Nifty** — Bank Nifty weaker than Nifty = weak market.

## D. Option chain & OI

13. **Change in OI** (not just total): fresh PE writing below price = support;
    fresh CE writing near price = resistance.
    Check current **and** next expiry for Nifty, and Bank Nifty monthly.
14. **PCR trend** through the day (`fno_calc.py pcr`) — rising = bullish tilt.
15. **Futures OI build-up**: price↑ OI↑ long build-up; price↓ OI↑ short build-up;
    price↑ OI↓ short covering; price↓ OI↓ long unwinding.
16. **Strike quality** — tight bid-ask, good volume, ATM or 1 strike ITM
    (avoid far OTM). Use `fno_calc.py greeks` to see delta & theta.

## E. Trade plan (must be written before clicking buy)

17. One-line entry reason.
18. Stop-loss — premium (−25 to −30%) or a Nifty level (e.g. opening-range low).
19. Target ≥ 1.5–2× the stop; book half at first target.
20. Size — risk ≤ 1–2% of capital (`fno_calc.py size`).
21. Time stop — exit if no move in 60–90 min (theta decay).
22. Daily loss limit — stop after 2 losing trades or −3% in a day.

## Verdict rule

- **Take the trade** only if most of A–D agree with the direction and E is complete.
- **2–3 important items against** → skip, or use a defined-risk spread
  (bull call / bear put) with smaller size.
- Output the checklist as a compact table (item, reading, ✅/❌/➖) followed by
  GO / NO-GO / SPREAD-ONLY and the trade card from SKILL.md.
