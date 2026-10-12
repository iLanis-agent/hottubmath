# Hot tub math

When the water is ready, what the soaks cost over a week and a year, and what the cover is worth. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/hottubmath/

## The three tools

- **Heat plan** - `heatPlan(liters, kW, startC, targetC)`: kilowatt-hours and hours for the heat-up.
- **Session plan** - `sessionPlan(kwhPerHeat, sessionsPerWeek, pricePerKwh)`: weekly and yearly heat-up cost.
- **Cover plan** - `coverPlan(lossWUncovered, lossWCovered, hoursPerDay, daysPerYear, pricePerKwh)`: the cover's yearly savings in kWh and money.

## Labeled norms (illustrative estimates, not rules)

- Labeled constant: about 1.163 Wh heats one liter of water by one degree, before heat loss. Labeled losses: 300 W standby uncovered, 150 W covered - wind, insulation and setpoint change everything. The heater's rated output and the tub manual win.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (12 cases, 57 checks)

Regenerate the oracle expectations: `python3 oracle.py`
