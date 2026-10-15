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

compare.py gibt die Ergebnisse der einzelnen Modelle sortiert nach den Aufgaben aus mit
- Anzahl Läufe
- Median
- Min-Dauer
- Max-Dauer
- Ø Token
- Ø Token/s
- Ø Ladezeit

```bash
Aufgabe                      Modell          Läufe   Median     Min     Max  Ø Token  Ø Token/s  Ø Laden
------------------------------------------------------------------------------------------------------
Beleg auslesen               llama3.2:latest     2     5.7s    3.4s    8.0s       33        9.4     0.0s
Beleg auslesen               qwen2.5:3b          2     7.9s    4.0s   11.8s       40        8.7     0.0s
E-Mail zusammenfassen        llama3.2:latest     2    15.2s    8.9s   21.4s       48        9.3     6.5s
E-Mail zusammenfassen        qwen2.5:3b          2    13.0s    8.7s   17.2s       56        9.7     4.2s
Frage zu internem Dokument   llama3.2:latest     2     4.8s    2.8s    6.7s       26        9.3     0.0s
Frage zu internem Dokument   qwen2.5:3b          2     5.7s    2.9s    8.5s       26        8.5     0.0s
```



## Beobachtungen

- Beide Modelle erzeugen auf cem Test-Laptop gleich schnell Text (ca. 9 Token/s).
- Die E-Mail-Aufgabe dauert pro Modell spürbar länger, weil das Modell erst in den Arbeitsspeicher geladen wird (4–7 s Ladezeit, Rest 0 s).
- Die Laufzeiten schwanken stark: In jeder Kombination aus Modell und Aufgabe dauerte der langsamste Lauf zwei- bis dreimal so lange wie der schnellste. Mit nur zwei Läufen pro Kombination sind die Medianwerte daher nur eine grobe Orientierung.

## Einschränkungen

Die bisherigen Läufe liefen auf meinem Laptop. Auf zusätzliche Prozesse, die währenddessen aktiv waren und somit die Leistung der LLMs beinflusst haben können, wurde keine Rücksicht genommen. Bei der Umsetzung ging es lediglich darum, erste Ergebnisse zu erzielen und Daten zu erlangen. 
Eine genaue Auswertung bzw. ein Vergleich der Modelle untereinander ebenso der einzelnen Läufe wäre an dieser Stelle fehlerbehaftet.
Es ergibt sich jedoch die Fragestellung: Wie performen die LLMs unter schlechteren Arbeitsumgebungen.

