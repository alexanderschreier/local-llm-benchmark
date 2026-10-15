import time
import requests
from datetime import datetime
from pathlib import Path
import json

print("Benchmark Start")

OLLAMA_URL = "http://localhost:11434/api/generate"

TASKS = [
    {
        "name": "E-Mail zusammenfassen",
        "prompt": (
            "Fasse diese E-Mail in einem Satz zusammen:"
            "Hallo Frau Berger, leider verzögert sich die Lieferung der 200 Kartons wegen eines Maschinenausfalls bei unserem Zulieferer. Wir rechnen nun mit einer Zustellung am Freitag. Viele Grüße, Thomas Lang"
        ),
        "erwartet": ["Lieferung", "Freitag"],
    },
    {
        "name": "Beleg auslesen",
        "prompt": (
            "Lies aus diesem Beleg Datum, Gesamtbetrag und Händler aus. "
            "Antworte nur mit diesen drei Angaben."
            "Bürobedarf Huber GmbH Rechnung Nr. 4711 Datum: 12.09.2026 2x Druckerpapier A4   19,90 EUR 1x Toner schwarz   27,90 EUR Gesamt: 47,80 EUR"
        ),
        "erwartet": ["12.09.2026", "47,80", "Huber"],
    },
    {
        "name": "Frage zu internem Dokument",
        "prompt": (
            "Beantworte die Frage nur anhand des Textes."
            "Text: Mitarbeitende können bis zu zwei Tage pro Woche im Homeoffice arbeiten. Der Antrag erfolgt formlos bei der direkten Führungskraft."
            "Frage: Wie viele Homeoffice-Tage sind pro Woche erlaubt?"
        ),
        "erwartet": ["zwei"],
    },
]

def question_model(model, prompt):
    response= requests.post(
        OLLAMA_URL,
        json = {"model": model, "prompt": prompt, "stream": False},
        timeout = 300
    )
    response.raise_for_status()
    return response.json()


def benchmark(model):

    print(model)

    results = []



    for task in TASKS:
        print (task['name'])

        start = time.time()

        try:
            data = question_model(model, task['prompt'])
        except requests.exceptions.ConnectionError:
            print("FEHLER")
            return
        
        duration= time.time()- start 

        results.append({
            "Modell": model,
            "Aufgabe": task['name'],
            "Dauer": duration,                      
            "Input-Token": data['prompt_eval_count'],
            "Output-Token": data['eval_count'],
            "Antwort": data['response'],
        })

    results_folder = Path('results')
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file = results_folder / f"benchmark_{timestamp}.json"

    with open(file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    print("Fertig")


