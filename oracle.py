import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(jsnum(n)) + " " + (word if n == 1 else (form or word + "s"))
def money(c): return "$" + str(c // 100) + "." + str(c % 100).zfill(2)
def fmt(x): return str(jsnum(x))
def rnd(x): return math.floor(x + 0.5)

def heat_plan(liters, kW, startC, targetC):
    if not (liters > 0) or not (kW > 0) or not (targetC > startC):
        return {"error": "volume, heater power and temperatures must be positive, target above start"}
    wh = liters * (targetC - startC) * 1.163
    return {"kwh": jsnum(rnd(wh / 1000 * 100) / 100), "hours": jsnum(rnd(wh / (kW * 1000) * 10) / 10)}

def session_plan(kwhPerHeat, sessionsPerWeek, pricePerKwh):
    if not (kwhPerHeat > 0) or not (sessionsPerWeek > 0) or not (pricePerKwh > 0):
        return {"error": "kilowatt-hours, sessions and price must be positive"}
    return {"weekCents": rnd(kwhPerHeat * sessionsPerWeek * pricePerKwh * 100),
            "yearCents": rnd(kwhPerHeat * sessionsPerWeek * 52 * pricePerKwh * 100),
            "priceCents": rnd(pricePerKwh * 100)}

def cover_plan(lossWUncovered, lossWCovered, hoursPerDay, daysPerYear, pricePerKwh):
    if not (lossWUncovered > 0) or not (lossWCovered > 0) or not (lossWUncovered > lossWCovered) or not (hoursPerDay > 0) or not (daysPerYear > 0) or not (pricePerKwh > 0):
        return {"error": "losses, hours, days and price must be positive, covered below uncovered"}
    savedKwh = jsnum((lossWUncovered - lossWCovered) * hoursPerDay * daysPerYear / 1000)
    return {"savedKwh": savedKwh, "savedCents": rnd(savedKwh * pricePerKwh * 100), "priceCents": rnd(pricePerKwh * 100)}

def render_heat(r, liters, kW, startC, targetC):
    return ("Heating " + fmt(liters) + " liters from " + fmt(startC) + " C to " + fmt(targetC) + " C with a " + fmt(kW)
            + " kW heater: " + fmt(r["kwh"]) + " kWh - about " + plural(r["hours"], "hour") + ".")

def render_session(r, kwhPerHeat, sessionsPerWeek, pricePerKwh):
    return (plural(sessionsPerWeek, "soak") + " a week at " + fmt(kwhPerHeat) + " kWh a heat-up and " + money(r["priceCents"])
            + " a kWh: " + money(r["weekCents"]) + " a week, " + money(r["yearCents"]) + " a year of heat-ups.")

def render_cover(r, lossWUncovered, lossWCovered, hoursPerDay, daysPerYear, pricePerKwh):
    return ("A labeled " + fmt(lossWUncovered) + " W standby loss uncovered against " + fmt(lossWCovered) + " W covered, "
            + plural(hoursPerDay, "hour") + " a day for " + plural(daysPerYear, "day") + ": the cover saves " + fmt(r["savedKwh"])
            + " kWh - about " + money(r["savedCents"]) + " a year at " + money(r["priceCents"]) + " a kWh.")

cases = []
for a in [(1500, 3, 15, 38), (1000, 2, 20, 40), (800, 1.5, 18, 36), (0, 3, 15, 38)]:
    r = heat_plan(*a)
    cases.append({"fn": "heatPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_heat(r, *a)})
for a in [(40, 3, 0.15), (25, 2, 0.3), (35, 4, 0.22), (40, 0, 0.15)]:
    r = session_plan(*a)
    cases.append({"fn": "sessionPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_session(r, *a)})
for a in [(300, 150, 24, 365, 0.15), (500, 250, 24, 365, 0.22), (200, 100, 20, 300, 0.18), (150, 300, 24, 365, 0.15)]:
    r = cover_plan(*a)
    cases.append({"fn": "coverPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_cover(r, *a)})

with open("expected.json", "w") as f:
    f.write(json.dumps(cases, separators=(",", ":")) + "\n")
print("wrote", len(cases), "cases")
