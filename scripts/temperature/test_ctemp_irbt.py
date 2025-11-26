import time
import board
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20

# Pin où est connecté DATA du DS18B20
# Adapte ici si tu utilises un autre GPIO (par ex. GP26 etc.)
ow_bus = OneWireBus(board.GP15)

# On scanne le bus 1-Wire pour trouver les capteurs
devices = ow_bus.scan()
print("Capteurs trouvés :", devices)

if not devices:
    print("Aucun capteur DS18B20 détecté. Vérifie le câblage.")
else:
    # On prend le premier capteur trouvé
    ds = DS18X20(ow_bus, devices[0])

    while True:
        temperature_c = ds.temperature
        print(f"Température : {temperature_c:0.2f} °C")
        time.sleep(1)
