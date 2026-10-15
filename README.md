# local-llm-benchmark

Ein kleiner Vergleich lokaler Sprachmodelle für typische Büroaufgaben im Mittelstand.
Die Modelle laufen über [Ollama](https://ollama.com) vollständig auf dem eigenen Rechner – kein Text verlässt das Gerät.

## Die Aufgaben

| Aufgabe | Was das Modell tun soll |
|---|---|
| E-Mail zusammenfassen | eine Lieferverzögerungs-Mail in einem Satz zusammenfassen |
| Beleg auslesen | aus einer Rechnung nur Datum, Gesamtbetrag und Händler herausziehen |
| Frage zu internem Dokument | eine Frage ausschließlich anhand eines kurzen Richtlinientextes beantworten |

## Aufbau

```
main.py          liest die installierten Modelle aus "ollama list" und lässt eins auswählen
benchmark.py     schickt die Aufgaben an die Ollama-API und speichert die Ergebnisse
results/         ein JSON-File pro Lauf (Modell, Aufgabe, Dauer, Input-/Output-Token, Antwort)
```

## Ausführen

Voraussetzung: Linux, Python 3, eine laufende Ollama-Installation und mindestens ein geladenes Modell.

Das Skript ist nicht auf bestimmte Modelle festgelegt: `main.py` liest beim Start alle Modelle aus `ollama list` aus und lässt eins davon auswählen. Wer weitere Modelle vergleichen will, lädt sie einfach mit `ollama pull <modellname>` dazu. Eine Übersicht verfügbarer Modelle gibt es unter [ollama.com/library](https://ollama.com/library).

```bash
# Beispiel: ein Modell laden
ollama pull llama3.2

# Python-Abhängigkeit
pip install -r requirements.txt     # oder unter Ubuntu: sudo apt install python3-requests

# Starten und Modell auswählen
python3 main.py
```

Die Ergebnisse landen als `results/benchmark_<model>_<Datum>_<Uhrzeit>.json`.


## Ergebnisse

```bash
# Ergebnisse vergleichen
python3 compare.py
```

compary.py gibt die Ergebnisse der einzelnen Modelle sortiert nach den Aufgaben aus mit
- Anzahl Läufe
- Median
- Min-Dauer
- Max-Dauer
- Ø Token

## Einschränkungen

Die bisherigen Läufe liefen auf meinem Laptop. Auf zusätzliche Prozesse, die währenddessen aktiv waren und somit die Leistung der LLMs beinflusst haben können, wurde keine Rücksicht genommen. Bei der Umsetzung ging es lediglich darum, erste Ergebnisse zu erzielen und Daten zu erlangen. 
Eine genaue Auswertung bzw. ein Vergleich der Modelle untereinander ebenso der einzelnen Läufe wäre an dieser Stelle fehlerbehaftet.
Es ergibt sich jedoch die Fragestellung: Wie performen die LLMs unter schlechteren Arbeitsumgebungen.

