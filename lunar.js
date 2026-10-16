
document.addEventListener("DOMContentLoaded", function () {
    const symbol = document.getElementById("moon-symbol");
    const phaseName = document.getElementById("moon-phase");
    const dateText = document.getElementById("moon-date");
    const description = document.getElementById("moon-description");

    if (!symbol || !phaseName) return;

    // Approximate lunar phase based on the known January 6, 2000 new moon.
    const knownNewMoon = Date.UTC(2000, 0, 6, 18, 14);
    const lunarCycle = 29.530588853 * 24 * 60 * 60 * 1000;
    const now = new Date();
    const age = ((now.getTime() - knownNewMoon) % lunarCycle + lunarCycle) % lunarCycle;
    const fraction = age / lunarCycle;

    let phase;
    if (fraction < 0.035 || fraction >= 0.965) {
        phase = ["New Moon", "🌑",
            "A new lunar cycle begins. The moon is difficult to see in the night sky."];
    } else if (fraction < 0.215) {
        phase = ["Waxing Crescent", "🌒",
            "A slender crescent becomes more visible each evening."];
    } else if (fraction < 0.285) {
        phase = ["First Quarter", "🌓",
            "Approximately half of the visible moon is illuminated."];
    } else if (fraction < 0.465) {
        phase = ["Waxing Gibbous", "🌔",
            "The illuminated portion is growing toward the full moon."];
    } else if (fraction < 0.535) {
        phase = ["Full Moon", "🌕",
            "The moon's visible disk appears fully illuminated."];
    } else if (fraction < 0.715) {
        phase = ["Waning Gibbous", "🌖",
            "The illuminated portion begins to decrease."];
    } else if (fraction < 0.785) {
        phase = ["Last Quarter", "🌗",
            "Approximately half of the visible moon is illuminated again."];
    } else {
        phase = ["Waning Crescent", "🌘",
            "The visible crescent becomes thinner before the next new moon."];
    }

    symbol.textContent = phase[1];
    phaseName.textContent = phase[0];
    description.textContent = phase[2];
    dateText.textContent = now.toLocaleDateString(undefined, {
        year: "numeric", month: "long", day: "numeric"
    }) + " · Approximate phase";
});
