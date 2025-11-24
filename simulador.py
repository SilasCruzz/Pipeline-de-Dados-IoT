import csv
import random
import time
from datetime import datetime

CSV_FILE = "IOT-temp.csv"

# Garante que o arquivo tem cabeçalho se estiver vazio
def inicializar_csv():
    try:
        with open(CSV_FILE, "r") as f:
            primeira_linha = f.readline()
            if "noted_date" in primeira_linha:
                return
    except FileNotFoundError:
        pass

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["noted_date", "temp", "humidity"])

def gerar_dados():
    temp = round(20 + random.uniform(-1,1), 2)
    humidity = round(55 + random.uniform(-5,5), 2)
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([data, temp, humidity])

    print(f"{data} → Temp={temp}°C | Hum={humidity}%")

if __name__ == "__main__":
    inicializar_csv()
    print("Simulador iniciado. Gerando temperatura a cada 60 segundos...")
    while True:
        gerar_dados()
        time.sleep(60)
