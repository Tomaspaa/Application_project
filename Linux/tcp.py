import requests
import csv
import pandas as pd
from io import StringIO

# HTTP-palvelimen osoite ja portti
palvelimen_osoite = "172.20.241.9"
portti = 80

# HTTP-endpoint, josta dataa haetaan
endpoint = "/luedataa_kannasta_groupid_csv.php?groupid=16"

# Tee HTTP-pyyntö ja hae data
url = f"http://{palvelimen_osoite}:{portti}{endpoint}"
vastaus = requests.get(url)

# Tarkista, että pyyntö onnistui (status code 200)
if vastaus.status_code == 200:
    try:
        # Käsittely tekstimuotoisena vastauksena
        vastausteksti = vastaus.text.strip()
        if vastausteksti:
            # Luodaan DataFrame
            df = pd.read_csv(StringIO(vastausteksti), sep=';')

            # Määritellään kenttien nimet
            df.columns = ["id", "timestamp", "groupid", "from_mac", "to_mac", "sensorvalue_a", "sensorvalue_b", "sensorvalue_c", "sensorvalue_d", "sensorvalue_e", "sensorvalue_f"]

            # Tallennetaan DataFrame CSV-tiedostoon
            df.to_csv("C:/Sovellusprojekti_S2023/data.csv", index=False)

            print("Data tallennettu CSV-tiedostoon.")
        else:
            print("Vastaus on tyhjä. Ei dataa tallennettavaksi.")
    except Exception as e:
        print(f"Virhe käsittelyssä: {e}")
else:
    print(f"HTTP-pyyntö epäonnistui. Status code: {vastaus.status_code}")