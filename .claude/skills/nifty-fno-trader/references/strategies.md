# Strategy Selection

## Decision matrix (view × IV)

| View | Low IV (VIX < 13) | High IV (VIX > 18) |
|---|---|---|
| Strong bullish | Buy ATM/ITM CE, long futures + protective PE | Bull put spread (credit) |
| Mild bullish | Bull call spread (debit) | Bull put spread, short OTM PE (hedged) |
| Neutral / range | Calendar spread, long butterfly | Iron condor, short strangle (hedged), iron fly |
| Mild bearish | Bear put spread (debit) | Bear call spread (credit) |
| Strong bearish | Buy ATM/ITM PE, short futures + protective CE | Bear call spread |
| Big move, unsure direction | Long straddle / strangle | Avoid buying — premiums rich |

## Strategy notes

**Bull call / bear put spread (debit)** — defined risk, cheaper than naked buy,
less theta bleed. Width usually 100–200 pts NIFTY, 300–500 pts BANKNIFTY.

**Bull put / bear call spread (credit)** — sell near OTM, buy further OTM hedge.
Hedge also reduces margin substantially. Exit if short strike is breached on a
closing basis or loss = 1.5–2× credit.

**Iron condor** — sell OTM CE + PE near 1σ (or around highest OI strikes), buy
wings 100–300 pts further. Best in high IV, range-bound weeks. Adjust by rolling the
untested side closer, never by widening losses indefinitely.

**Short straddle / strangle** — high probability, unlimited risk. Only with hedges
(buy far OTM wings) or strict stops. Expiry-day versions need ~1.5× premium stop
per leg.

**Long straddle / strangle** — needs move > combined premium before expiry.
Breakevens = strike ± total premium (straddle).

**Futures** — linear P&L, full exposure (~₹15L+ notional per lot). Always pair with
a stop, or hedge with an OTM option ("synthetic" protective position).

## Adjustment rules (keep them mechanical)
1. Decide the adjustment trigger before entry (e.g. spot touches short strike, or
   delta of a short leg > 0.40).
2. Prefer closing the threatened side and re-opening further out over adding size.
3. Max 1–2 adjustments per trade; after that, exit.

## Worked calculator examples

Greeks for a NIFTY 24300 CE, spot 24,350, 7 days to expiry, IV 13%, r 6.5%:
```bash
python3 .claude/skills/nifty-fno-trader/scripts/fno_calc.py greeks \
  --spot 24350 --strike 24300 --days 7 --iv 13 --type CE
```

Bull call spread payoff (2 lots NIFTY):
```bash
python3 .claude/skills/nifty-fno-trader/scripts/fno_calc.py payoff --index NIFTY --lots 2 \
  --leg "BUY CE 24300 182" --leg "SELL CE 24500 88" --spot 24350
```

Iron condor on BANKNIFTY:
```bash
python3 .claude/skills/nifty-fno-trader/scripts/fno_calc.py payoff --index BANKNIFTY --lots 1 \
  --leg "SELL PE 51500 210" --leg "BUY PE 51000 95" \
  --leg "SELL CE 53000 230" --leg "BUY CE 53500 105" --spot 52250
```

Position sizing — ₹5L capital, 1.5% risk, stop 40 pts premium on NIFTY:
```bash
python3 .claude/skills/nifty-fno-trader/scripts/fno_calc.py size \
  --index NIFTY --capital 500000 --risk-pct 1.5 --stop-points 40
```

Max pain & PCR from a CSV (columns: strike,ce_oi,pe_oi):
```bash
python3 .claude/skills/nifty-fno-trader/scripts/fno_calc.py maxpain --csv chain.csv
python3 .claude/skills/nifty-fno-trader/scripts/fno_calc.py pcr --csv chain.csv
```
