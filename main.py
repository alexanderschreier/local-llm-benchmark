from benchmark import benchmark
import subprocess

def main ():

    result = subprocess.run(
        ["ollama", "list"],
        capture_output = True,
        text = True
    ).stdout

    models = []

    for line in result.splitlines()[1:]:
        model = line.split()[0]
        models.append(model)

    for nummer, model in enumerate(models):
        print(f"{nummer}. {model}")

    while True:

        try:
            inn = int(input("Wähle das Modell für den Benchmark\n"))

            if 0 <= inn < len(models):
                break
            else:
                print("Diese Modellnummer existiert nicht ")

        except ValueError:
            print("Bitte gib eine gültige Zahl ein")

    benchmark(models[inn])


if __name__ == "__main__":
    main()