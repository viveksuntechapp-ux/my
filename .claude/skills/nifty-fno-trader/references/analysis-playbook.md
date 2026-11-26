# Analysis Playbook — reading the Nifty / Bank Nifty market

Work top-down. No single indicator is a signal; look for confluence.

## 1. Price structure
- Trend on daily + 75-min/15-min: higher highs/lows or lower highs/lows.
- Key levels: previous day high/low/close, weekly high/low, opening range (first 15–30 min),
  round numbers (NIFTY 24,000 / 24,500; BANKNIFTY 52,000 / 53,000), VWAP intraday.
- Gap analysis: gap-up/down vs previous day range; gaps into resistance often fade.
- Bank Nifty is dominated by HDFC Bank, ICICI Bank, SBI, Kotak, Axis — check them.

## 2. Open Interest (option chain)
| Observation | Usual interpretation |
|---|---|
| Highest CE OI strike | Resistance (call writers defending) |
| Highest PE OI strike | Support (put writers defending) |
| CE OI rising at/below spot, price falling | Fresh call writing → bearish pressure |
| PE OI rising at/above spot, price rising | Fresh put writing → bullish support |
| Big OI unwinding at a strike | That level is weakening / about to break |

Futures OI build-up (price vs OI):
- Price ↑ OI ↑ = Long build-up (bullish)
- Price ↓ OI ↑ = Short build-up (bearish)
- Price ↑ OI ↓ = Short covering (bullish, often short-lived)
- Price ↓ OI ↓ = Long unwinding (bearish, often short-lived)

## 3. Put-Call Ratio (OI based)
- PCR = total PE OI / total CE OI (`fno_calc.py pcr`).
- Rough bands: < 0.7 bearish/overbought calls; 0.8–1.2 neutral; > 1.3 bullish but
  can signal over-optimism. Extremes are contrarian. Watch the **change** in PCR
  through the day more than the level.

## 4. Max Pain
- Strike where total option-buyer payout is minimal (`fno_calc.py maxpain`).
- Has some pull on expiry day in range-bound markets; ignore it in trending/news days.

## 5. Volatility
- India VIX: < 12 low (options cheap → favour buying/debit spreads), 12–18 normal,
  > 20 high (favour selling premium with defined risk / credit spreads).
- Compare ATM IV to recent realised volatility. IV ≫ realised → selling edge;
  IV ≪ realised → buying edge.
- IV crush after events (RBI policy, budget, election results) — avoid buying
  straddles just before the event unless you expect a move larger than implied.
- IV skew: puts usually richer than calls on indices.

## 6. Event calendar checklist
RBI MPC, US Fed/CPI, Union Budget, GDP/inflation prints, heavyweight quarterly
results, FII/DII flow data, global cues (GIFT Nifty, US futures, crude, USD/INR),
monthly & weekly expiry days.

## 7. Turning analysis into a view
Write the view in one line: _direction_ (bull / bear / neutral), _magnitude_
(small / large), _volatility expectation_ (IV up / down), _time horizon_.
Then go to `strategies.md` matrix.
