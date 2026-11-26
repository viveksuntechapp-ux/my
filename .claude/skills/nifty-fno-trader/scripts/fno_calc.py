#!/usr/bin/env python3
"""NIFTY / BANK NIFTY F&O calculator (pure Python, no dependencies).

Sub-commands:
  greeks   Black-Scholes price & Greeks for a single option
  payoff   Multi-leg option/futures payoff at expiry: max P/L, breakevens, table
  size     Lots to trade from capital, risk %, and stop distance
  maxpain  Max-pain strike from an option-chain CSV (strike,ce_oi,pe_oi)
  pcr      Put-call ratio (OI) from the same CSV
  futures  Futures P&L and VIX-implied expected move

Lot sizes below are defaults - override with --lot-size when NSE revises them.
Educational tool only; not investment advice.
"""
import argparse
import csv
import math
import sys

LOT_SIZES = {"NIFTY": 65, "BANKNIFTY": 30}  # verify on nseindia.com
STRIKE_STEP = {"NIFTY": 50, "BANKNIFTY": 100}


def _n_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _n_pdf(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bs(spot, strike, days, iv_pct, r_pct, opt, q_pct=0.0):
    t = max(days, 1e-6) / 365.0
    s, k, v, r, q = spot, strike, iv_pct / 100.0, r_pct / 100.0, q_pct / 100.0
    d1 = (math.log(s / k) + (r - q + 0.5 * v * v) * t) / (v * math.sqrt(t))
    d2 = d1 - v * math.sqrt(t)
    if opt == "CE":
        price = s * math.exp(-q * t) * _n_cdf(d1) - k * math.exp(-r * t) * _n_cdf(d2)
        delta = math.exp(-q * t) * _n_cdf(d1)
        theta = (-s * math.exp(-q * t) * _n_pdf(d1) * v / (2 * math.sqrt(t))
                 - r * k * math.exp(-r * t) * _n_cdf(d2)
                 + q * s * math.exp(-q * t) * _n_cdf(d1))
        rho = k * t * math.exp(-r * t) * _n_cdf(d2)
    else:
        price = k * math.exp(-r * t) * _n_cdf(-d2) - s * math.exp(-q * t) * _n_cdf(-d1)
        delta = -math.exp(-q * t) * _n_cdf(-d1)
        theta = (-s * math.exp(-q * t) * _n_pdf(d1) * v / (2 * math.sqrt(t))
                 + r * k * math.exp(-r * t) * _n_cdf(-d2)
                 - q * s * math.exp(-q * t) * _n_cdf(-d1))
        rho = -k * t * math.exp(-r * t) * _n_cdf(-d2)
    gamma = math.exp(-q * t) * _n_pdf(d1) / (s * v * math.sqrt(t))
    vega = s * math.exp(-q * t) * _n_pdf(d1) * math.sqrt(t)
    return {
        "price": price,
        "delta": delta,
        "gamma": gamma,
        "theta_per_day": theta / 365.0,
        "vega_per_1pct": vega / 100.0,
        "rho_per_1pct": rho / 100.0,
    }


def implied_vol(target, spot, strike, days, r_pct, opt):
    lo, hi = 0.1, 300.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if bs(spot, strike, days, mid, r_pct, opt)["price"] > target:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def lot_size(args):
    return args.lot_size or LOT_SIZES[args.index]


# ---------------------------------------------------------------- commands

def cmd_greeks(a):
    iv = a.iv
    if iv is None:
        if a.premium is None:
            sys.exit("Give --iv or --premium (to solve implied volatility).")
        iv = implied_vol(a.premium, a.spot, a.strike, a.days, a.rate, a.type)
        print(f"Implied volatility : {iv:.2f}%")
    g = bs(a.spot, a.strike, a.days, iv, a.rate, a.type)
    print(f"{a.type} {a.strike:g}  spot {a.spot:g}  {a.days:g}d  IV {iv:.2f}%  r {a.rate}%")
    print(f"Theoretical price  : {g['price']:.2f}")
    print(f"Delta              : {g['delta']:.4f}")
    print(f"Gamma              : {g['gamma']:.6f}")
    print(f"Theta (per day)    : {g['theta_per_day']:.2f}")
    print(f"Vega  (per 1% IV)  : {g['vega_per_1pct']:.2f}")
    print(f"Rho   (per 1%)     : {g['rho_per_1pct']:.2f}")


def parse_leg(text):
    # "BUY CE 24300 182" | "SELL PE 24000 95" | "BUY FUT 24380"
    parts = text.upper().split()
    side = parts[0]
    if side not in ("BUY", "SELL"):
        sys.exit(f"Bad leg '{text}': must start with BUY or SELL")
    sign = 1 if side == "BUY" else -1
    kind = parts[1]
    qty_mult = 1
    if kind == "FUT":
        price = float(parts[2])
        if len(parts) > 3:
            qty_mult = int(parts[3])
        return {"sign": sign, "kind": "FUT", "strike": price, "prem": price, "mult": qty_mult}
    if kind not in ("CE", "PE"):
        sys.exit(f"Bad leg '{text}': type must be CE, PE or FUT")
    strike, prem = float(parts[2]), float(parts[3])
    if len(parts) > 4:
        qty_mult = int(parts[4])
    return {"sign": sign, "kind": kind, "strike": strike, "prem": prem, "mult": qty_mult}


def leg_pnl(leg, s):
    if leg["kind"] == "FUT":
        return leg["sign"] * (s - leg["prem"]) * leg["mult"]
    intrinsic = max(s - leg["strike"], 0) if leg["kind"] == "CE" else max(leg["strike"] - s, 0)
    return leg["sign"] * (intrinsic - leg["prem"]) * leg["mult"]


def cmd_payoff(a):
    legs = [parse_leg(x) for x in a.leg]
    qty = lot_size(a) * a.lots
    strikes = sorted({l["strike"] for l in legs})
    ref = a.spot or strikes[len(strikes) // 2]
    step = STRIKE_STEP[a.index]
    lo = min(strikes + [ref]) * 0.85
    hi = max(strikes + [ref]) * 1.15
    n = int((hi - lo) / 1) + 1
    grid = [lo + i for i in range(n)]
    pnl = [sum(leg_pnl(l, s) for l in legs) * qty for s in grid]

    net_prem = sum(-l["sign"] * l["prem"] * l["mult"] for l in legs if l["kind"] != "FUT")
    # unlimited checks: slope at the edges
    slope_hi = pnl[-1] - pnl[-2]
    slope_lo = pnl[1] - pnl[0]
    max_p = "Unlimited" if slope_hi > 1e-9 or slope_lo < -1e-9 else f"₹{max(pnl):,.0f}"
    max_l = "Unlimited" if slope_hi < -1e-9 or slope_lo > 1e-9 else f"₹{min(pnl):,.0f}"

    bes = []
    for i in range(1, n):
        if (pnl[i - 1] < 0 <= pnl[i]) or (pnl[i - 1] > 0 >= pnl[i]):
            bes.append(grid[i])

    print(f"{a.index}  lots {a.lots} × {lot_size(a)} = qty {qty}")
    for x in a.leg:
        print(f"  {x}")
    kind = "credit" if net_prem > 0 else "debit"
    print(f"Net premium        : {abs(net_prem):.2f} pts {kind}  (₹{abs(net_prem) * qty:,.0f})")
    print(f"Max profit         : {max_p}")
    print(f"Max loss           : {max_l}")
    print("Breakeven(s)       : " + (", ".join(f"{b:,.0f}" for b in bes) or "none"))
    if a.spot:
        now = sum(leg_pnl(l, a.spot) for l in legs) * qty
        print(f"P&L at expiry if spot stays {a.spot:,.0f}: ₹{now:,.0f}")

    print("\nExpiry payoff table")
    centre = round(ref / step) * step
    rows = a.rows
    for i in range(-rows, rows + 1):
        s = centre + i * step * (2 if a.index == "NIFTY" else 3)
        v = sum(leg_pnl(l, s) for l in legs) * qty
        print(f"  {s:>9,.0f} : ₹{v:>12,.0f}")


def cmd_size(a):
    ls = lot_size(a)
    risk_rs = a.capital * a.risk_pct / 100.0
    per_lot = a.stop_points * ls
    lots = int(risk_rs // per_lot) if per_lot > 0 else 0
    print(f"Capital            : ₹{a.capital:,.0f}")
    print(f"Risk budget        : {a.risk_pct}% = ₹{risk_rs:,.0f}")
    print(f"Loss per lot @stop : {a.stop_points} pts × {ls} = ₹{per_lot:,.0f}")
    print(f"Max lots           : {lots}")
    if lots == 0:
        print("Stop too wide for this risk budget - tighten stop, use a spread, or skip the trade.")


def read_chain(path):
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            rows.append((float(r["strike"]), float(r["ce_oi"]), float(r["pe_oi"])))
    if not rows:
        sys.exit("Empty chain CSV")
    return sorted(rows)


def cmd_maxpain(a):
    chain = read_chain(a.csv)
    best = None
    for k, _, _ in chain:
        pain = sum(max(k - s, 0) * ce + max(s - k, 0) * pe for s, ce, pe in chain)
        if best is None or pain < best[1]:
            best = (k, pain)
    print(f"Max pain strike    : {best[0]:,.0f}")
    top_ce = max(chain, key=lambda r: r[1])
    top_pe = max(chain, key=lambda r: r[2])
    print(f"Highest CE OI      : {top_ce[0]:,.0f} ({top_ce[1]:,.0f})  -> resistance")
    print(f"Highest PE OI      : {top_pe[0]:,.0f} ({top_pe[2]:,.0f})  -> support")


def cmd_pcr(a):
    chain = read_chain(a.csv)
    ce = sum(r[1] for r in chain)
    pe = sum(r[2] for r in chain)
    pcr = pe / ce if ce else float("inf")
    if pcr < 0.7:
        tone = "bearish / call-heavy (watch for contrarian bounce)"
    elif pcr <= 1.2:
        tone = "neutral"
    elif pcr <= 1.5:
        tone = "bullish (put writers supporting)"
    else:
        tone = "very high - possible over-optimism (contrarian caution)"
    print(f"Total CE OI {ce:,.0f}  PE OI {pe:,.0f}  PCR {pcr:.2f}  -> {tone}")


def cmd_futures(a):
    ls = lot_size(a)
    if a.vix:
        mv = a.spot * a.vix / 100 / math.sqrt(252)
        wk = a.spot * a.vix / 100 / math.sqrt(52)
        print(f"VIX {a.vix}: expected 1-day 1σ move ±{mv:,.0f} pts "
              f"({a.spot - mv:,.0f} – {a.spot + mv:,.0f}); 1-week ±{wk:,.0f}")
    if a.entry and a.exit:
        sign = 1 if a.side == "BUY" else -1
        pts = (a.exit - a.entry) * sign
        print(f"{a.side} {a.lots} lot(s) {a.index} FUT {a.entry:g} -> {a.exit:g}: "
              f"{pts:+.2f} pts = ₹{pts * ls * a.lots:,.0f} (before costs)")
    print(f"Notional per lot at {a.spot:,.0f}: ₹{a.spot * ls:,.0f}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--index", choices=list(LOT_SIZES), default="NIFTY")
        sp.add_argument("--lot-size", type=int, help="override default lot size")

    g = sub.add_parser("greeks")
    g.add_argument("--spot", type=float, required=True)
    g.add_argument("--strike", type=float, required=True)
    g.add_argument("--days", type=float, required=True, help="calendar days to expiry")
    g.add_argument("--iv", type=float, help="implied vol in %")
    g.add_argument("--premium", type=float, help="market premium (solves IV)")
    g.add_argument("--rate", type=float, default=6.5, help="risk-free rate %%")
    g.add_argument("--type", choices=["CE", "PE"], required=True)
    g.set_defaults(fn=cmd_greeks)

    po = sub.add_parser("payoff", help='legs like "BUY CE 24300 182" or "SELL FUT 24380"')
    common(po)
    po.add_argument("--lots", type=int, default=1)
    po.add_argument("--leg", action="append", required=True)
    po.add_argument("--spot", type=float)
    po.add_argument("--rows", type=int, default=6)
    po.set_defaults(fn=cmd_payoff)

    s = sub.add_parser("size")
    common(s)
    s.add_argument("--capital", type=float, required=True)
    s.add_argument("--risk-pct", type=float, default=1.0)
    s.add_argument("--stop-points", type=float, required=True)
    s.set_defaults(fn=cmd_size)

    m = sub.add_parser("maxpain")
    m.add_argument("--csv", required=True)
    m.set_defaults(fn=cmd_maxpain)

    pc = sub.add_parser("pcr")
    pc.add_argument("--csv", required=True)
    pc.set_defaults(fn=cmd_pcr)

    f = sub.add_parser("futures")
    common(f)
    f.add_argument("--spot", type=float, required=True)
    f.add_argument("--vix", type=float)
    f.add_argument("--side", choices=["BUY", "SELL"], default="BUY")
    f.add_argument("--entry", type=float)
    f.add_argument("--exit", type=float)
    f.add_argument("--lots", type=int, default=1)
    f.set_defaults(fn=cmd_futures)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
