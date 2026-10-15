import json
import statistics
from pathlib import Path

# Alle Läufe einlesen und nach (Modell, Aufgabe) gruppieren
groups = {}
for file in sorted(Path("results").glob("*.json")):
    for entry in json.loads(file.read_text(encoding="utf-8")):
        key = (entry["Modell"], entry["Aufgabe"])
        groups.setdefault(key, []).append(entry)

# Tabelle ausgeben
print(f"{'Aufgabe':<28} {'Modell':<15} {'Läufe':>5} {'Median':>8} {'Min':>7} {'Max':>7} {'Ø Token':>8} {'Ø Token/s':>10} {'Ø Laden':>8}")
print("-" * 102)

for (model, task), runs in sorted(groups.items(), key=lambda item: (item[0][1], item[0][0])):

    durations = [r["Dauer"] for r in runs]
    tokens = [r["Output-Token"] for r in runs]
    speeds = [r["Token/s"] for r in runs]
    loads = [r["Ladezeit"] for r in runs]
    print(
        f"{task:<28} {model:<15} {len(runs):>5} "
        f"{statistics.median(durations):>7.1f}s {min(durations):>6.1f}s {max(durations):>6.1f}s "
        f"{statistics.mean(tokens):>8.0f} {statistics.mean(speeds):>10.1f} {statistics.mean(loads):>7.1f}s"
    )

