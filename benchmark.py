import time
import requests
from datetime import datetime
from pathlib import Path
import json

TASKS = [
    {
        "name": "E-Mail zusammenfassen",
        "prompt": "Fasse diese E-Mail in einem Satz zusammen: Hallo Frau Berger, leider verzögert sich die Lieferung der 200 Kartons wegen eines Maschinenausfalls bei unserem Zulieferer. Wir rechnen nun mit einer Zustellung am Freitag. Viele Grüße, Thomas Lang",
    },
    {
        "name": "Beleg auslesen",
        "prompt": "Lies aus diesem Beleg Datum, Gesamtbetrag und Händler aus. Antworte nur mit diesen drei Angaben.Bürobedarf Huber GmbH Rechnung Nr. 4711 Datum: 12.09.2026 2x Druckerpapier A4   19,90 EUR 1x Toner schwarz   27,90 EUR Gesamt: 47,80 EUR",
    },
    {
        "name": "Frage zu internem Dokument",
        "prompt": "Beantworte die Frage nur anhand des Textes.Text: Mitarbeitende können bis zu zwei Tage pro Woche im Homeoffice arbeiten. Der Antrag erfolgt formlos bei der direkten Führungskraft. Frage: Wie viele Homeoffice-Tage sind pro Woche erlaubt?"
    },
]

def question_model(model, prompt):
    response= requests.post(
        "http://localhost:11434/api/generate",
        json = {"model": model, "prompt": prompt, "stream": False},
        timeout = 300
    )
    response.raise_for_status()
    return response.json()


def benchmark(model):

    print(model)

    results = []


    for task in TASKS:

        start = time.time()

        try:
            data = question_model(model, task['prompt'])
        except requests.exceptions.ConnectionError:
            print("FEHLER")
            return
        except requests.exceptions.Timeout:
            print("FEHLER: Keine Antwort innerhalb von 300 Sekunden")
            continue
        except requests.exceptions.HTTPError as fehler:
            print(f"FEHLER von Ollama: {fehler.response.text}")
            continue
        
        duration= time.time()- start 

        results.append({
            "Modell": model,
            "Aufgabe": task['name'],
            "Dauer": duration,                      
            "Input-Token": data['prompt_eval_count'],
            "Output-Token": data['eval_count'],
            "Token/s": data['eval_count'] / (data['eval_duration'] / 1e9),
            "Ladezeit": data['load_duration'] / 1e9,
            "Antwort": data['response'],
        })

    results_folder = Path('results')
    results_folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file = results_folder / f"benchmark_{model}_{timestamp}.json"

    with open(file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    print("Fertig")


