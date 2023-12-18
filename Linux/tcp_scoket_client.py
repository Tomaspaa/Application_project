import socket
import sys

def tallenna_tiedot_tiedostoon(data, tiedostonimi='C:\\python\\Sovellusprojekti_S23\\tcp\\vastaanotetut_datat.txt'):
    try:
        with open(tiedostonimi, 'w') as tiedosto:
            tiedosto.write(data)
        print(f"Tiedot tallennettu tiedostoon:{tiedostonimi}")
    except Exception as e:
        print(f"Virhe tiedon tallentamisessa tiedostoon: {e}")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Yhdistetään palvelimeen
        s.connect(('172.20.241.9', 20000))

        # Lähetetään data palvelimelle
        group_id = '16'
        s.sendall(group_id.encode('utf-8') + b'\n')

        # Vastaanotetaan tiedot
        chunks = []
        while True:
            data = s.recv(1024)
            if len(data) == 0:
                break
            chunks.append(data.decode('utf-8'))

        # Suljetaan yhteys
        s.close()

        # Tulosta vastaanotetut tiedot
        for i in chunks:
            print(i, end='')

        # Tiedon tallennus tiedostoon
        if len(sys.argv) > 1:
            tiedostonimi = sys.argv[1]
            tallenna_tiedot_tiedostoon(''.join(chunks), tiedostonimi)
        else:
            tallenna_tiedot_tiedostoon(''.join(chunks))

    except Exception as e:
        print(f"Virhe yhteyden muodostamisessa tai tiedon vastaanottamisessa: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    main()
