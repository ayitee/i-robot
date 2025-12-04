from machine import Pin
import time

# --- Configuration des GPIO capteur ---
TRIG_PIN = 17   # GP17
ECHO_PIN = 16   # GP16

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

# --- Configuration du bouton ---
BUTTON_PIN = 15  # GP15
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)  # bouton entre GPIO15 et GND
prev_button_state = 1  # 1 = relâché, 0 = appuyé

# --- Paramètres de fréquence ---
SAMPLE_INTERVAL_MS = 67   # ~15 mesures par seconde
AVERAGE_INTERVAL_MS = 333 # ~3 moyennes par seconde

# --- Paramètres de la moyenne mobile ---
BUFFER_SIZE = 7
distances_buffer = []

# --- Enregistrement des données ---
recording = False
record_start_ticks = None
log_data = []       # liste de tuples (time_ms, last_distance, avg_distance)
file_index = 1      # pour générer des noms de fichiers uniques


def mesurer_distance_cm():
    """Mesure une distance en cm avec le capteur ultrason.
       Retourne None en cas de problème (timeout).
    """
    # S'assurer que TRIG est bas
    trig.value(0)
    time.sleep_us(5)

    # Impulsion de 10 µs sur TRIG
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    timeout_us = 30000  # 30 ms max pour attendre les transitions sur ECHO

    # Attente que ECHO passe à 1
    debut_attente = time.ticks_us()
    while echo.value() == 0:
        if time.ticks_diff(time.ticks_us(), debut_attente) > timeout_us:
            return None

    # ECHO vient de passer à 1 -> début du pulse
    t_haut_debut = time.ticks_us()

    # Attente que ECHO repasse à 0
    while echo.value() == 1:
        if time.ticks_diff(time.ticks_us(), t_haut_debut) > timeout_us:
            return None

    # ECHO vient de repasser à 0 -> fin du pulse
    t_haut_fin = time.ticks_us()

    # Durée du signal haut (en µs)
    duree = time.ticks_diff(t_haut_fin, t_haut_debut)

    # Conversion en cm
    distance_cm = duree / 58.0
    return distance_cm


def save_csv(data):
    """Enregistre la liste de mesures dans un fichier CSV sur le Pico."""
    global file_index

    if not data:
        print(">>> Aucun point à enregistrer, fichier non créé.")
        return

    filename = "ultra_log_{:03d}.csv".format(file_index) 
    file_index += 1

    try:
        with open(filename, "w") as f:
            # En-tête
            f.write("time_ms,last_distance_cm,avg_distance_cm\n")
            # Lignes de données
            for t_ms, last_d, avg_d in data:
                if last_d is None:
                    last_d_str = ""
                else:
                    last_d_str = "{:.2f}".format(last_d)
                avg_d_str = "{:.2f}".format(avg_d)
                f.write("{},{},{}\n".format(t_ms, last_d_str, avg_d_str))

        print(">>> Données sauvegardées dans le fichier :", filename)
    except Exception as e:
        print(">>> ERREUR lors de l'écriture du fichier :", e)


print("Initialisation capteur ultrason")
print("TRIG sur GP{}, ECHO sur GP{}".format(TRIG_PIN, ECHO_PIN))
print("Bouton sur GP{} (entre GPIO et GND)".format(BUTTON_PIN))

last_average_time = time.ticks_ms()

while True:
    loop_start = time.ticks_ms()

    # --- Gestion du bouton (détection appui) ---
    button_state = button.value()
    # front descendant : 1 -> 0 -> appui détecté
    if prev_button_state == 1 and button_state == 0:
        if not recording:
            # Démarrer l'enregistrement
            recording = True
            record_start_ticks = time.ticks_ms()
            log_data = []
            print(">>> Enregistrement DEMARRE")
        else:
            # Arrêter l'enregistrement et sauver
            recording = False
            print(">>> Enregistrement ARRETE, sauvegarde du fichier...")
            save_csv(log_data)
            record_start_ticks = None
            log_data = []

    prev_button_state = button_state

    # --- 1) Mesure à ~15 Hz ---
    distance = mesurer_distance_cm()

    if distance is not None:
        distances_buffer.append(distance)
        if len(distances_buffer) > BUFFER_SIZE:
            distances_buffer.pop(0)

    # --- 2) Calcul de la moyenne mobile à ~3 Hz ---
    now = time.ticks_ms()
    if time.ticks_diff(now, last_average_time) >= AVERAGE_INTERVAL_MS:
        if distances_buffer:
            moyenne = sum(distances_buffer) / len(distances_buffer)

            # Affichage en temps réel
            if distance is not None:
                print("Dernière mesure: {:.1f} cm | Moyenne mobile ({} dernières): {:.1f} cm"
                      .format(distance, len(distances_buffer), moyenne))
            else:
                print("Dernière mesure: invalide | Moyenne mobile ({} dernières): {:.1f} cm"
                      .format(len(distances_buffer), moyenne))

            # Enregistrement si mode "record" actif
            if recording and record_start_ticks is not None:
                elapsed_ms = time.ticks_diff(now, record_start_ticks)
                log_data.append((elapsed_ms, distance, moyenne))
        else:
            print("Aucune mesure valide pour calculer la moyenne.")

        last_average_time = now

    # --- 3) Respecter ~15 mesures/s ---
    elapsed = time.ticks_diff(time.ticks_ms(), loop_start)
    reste = SAMPLE_INTERVAL_MS - elapsed
    if reste > 0:
        time.sleep_ms(reste)
