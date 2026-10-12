(function (root) {
  "use strict";
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }
  function money(c) { return "$" + Math.floor(c / 100) + "." + ("0" + (c % 100)).slice(-2); }

  function heatPlan(liters, kW, startC, targetC) {
    if (!(liters > 0) || !(kW > 0) || !(targetC > startC)) return { error: "volume, heater power and temperatures must be positive, target above start" };
    var wh = liters * (targetC - startC) * 1.163;
    var kwh = Math.round(wh / 1000 * 100) / 100;
    var hours = Math.round(wh / (kW * 1000) * 10) / 10;
    return { kwh: kwh, hours: hours };
  }

  function sessionPlan(kwhPerHeat, sessionsPerWeek, pricePerKwh) {
    if (!(kwhPerHeat > 0) || !(sessionsPerWeek > 0) || !(pricePerKwh > 0)) return { error: "kilowatt-hours, sessions and price must be positive" };
    var weekCents = Math.round(kwhPerHeat * sessionsPerWeek * pricePerKwh * 100);
    var yearCents = Math.round(kwhPerHeat * sessionsPerWeek * 52 * pricePerKwh * 100);
    var priceCents = Math.round(pricePerKwh * 100);
    return { weekCents: weekCents, yearCents: yearCents, priceCents: priceCents };
  }

  function coverPlan(lossWUncovered, lossWCovered, hoursPerDay, daysPerYear, pricePerKwh) {
    if (!(lossWUncovered > 0) || !(lossWCovered > 0) || !(lossWUncovered > lossWCovered) || !(hoursPerDay > 0) || !(daysPerYear > 0) || !(pricePerKwh > 0)) return { error: "losses, hours, days and price must be positive, covered below uncovered" };
    var savedKwh = (lossWUncovered - lossWCovered) * hoursPerDay * daysPerYear / 1000;
    var savedCents = Math.round(savedKwh * pricePerKwh * 100);
    var priceCents = Math.round(pricePerKwh * 100);
    return { savedKwh: savedKwh, savedCents: savedCents, priceCents: priceCents };
  }

  function renderHeat(r, liters, kW, startC, targetC) {
    return "Heating " + liters + " liters from " + startC + " C to " + targetC + " C with a " + kW + " kW heater: " + r.kwh + " kWh - about " + plural(r.hours, "hour") + ".";
  }

  function renderSession(r, kwhPerHeat, sessionsPerWeek, pricePerKwh) {
    return plural(sessionsPerWeek, "soak") + " a week at " + kwhPerHeat + " kWh a heat-up and " + money(r.priceCents) + " a kWh: " + money(r.weekCents) + " a week, " + money(r.yearCents) + " a year of heat-ups.";
  }

  function renderCover(r, lossWUncovered, lossWCovered, hoursPerDay, daysPerYear, pricePerKwh) {
    return "A labeled " + lossWUncovered + " W standby loss uncovered against " + lossWCovered + " W covered, " + plural(hoursPerDay, "hour") + " a day for " + plural(daysPerYear, "day") + ": the cover saves " + r.savedKwh + " kWh - about " + money(r.savedCents) + " a year at " + money(r.priceCents) + " a kWh.";
  }

  var api = { heatPlan: heatPlan, sessionPlan: sessionPlan, coverPlan: coverPlan, renderHeat: renderHeat, renderSession: renderSession, renderCover: renderCover };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.HottubMath = api;
})(this);
