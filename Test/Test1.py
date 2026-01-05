import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

print("Programm fängt an durchzulaufen")

#Parameter 
TOTAL_TICKETS=75#000
QUEUE_SIZE=400#_000
SIMULATIONS=3#000
TICKET_VALUES=[1,2,3,4]
#Wahrscheinlichkeit für 0 Tickets 
P_ZERO=0.05
#5%-Cutoff
CUTOFF_PROB=0.05
rng=np.random.default_rng()


#Ticketverteilung 1-4
#nicht gleichverteilt
#Gewicht mit 1/sqrt(k)
#ergibt Erwartungswert=1.65
ticket_value=np.array([1,2,3,4])
weights=1/np.sqrt(ticket_value)
weights/= weights.sum()


#Einzelne Simulation - Vektorisiert
def run_single_simulation_vectorized(): 
    # Zufällige Nachfrage für alles Personen generieren
    demands = rng.choice(ticket_value, size=QUEUE_SIZE, p=weights)

    #5% Chance, dass jemand nicht kauft
    zeros = rng.random(size=QUEUE_SIZE) < P_ZERO
    demands [zeros] = 0

    # Kumlierte Summe berechnen 
    cumsum = np.cumsum(demands)

    #Position finden, an der Tickets alle weg sind 
    sellout_idx = np.searchsorted(cumsum, TOTAL_TICKETS, side='right')
    return sellout_idx


#Monte-Carlo-Simulation (vektorisiert pro Simulation)
sellout_positions=np.array([run_single_simulation_vectorized()for _ in range(SIMULATIONS)])


#Wahrscheinlichkeit pro Queue-Position mit Schrittweite von 100
positions=np.arange(0, QUEUE_SIZE +1,100)


#Wahrscheinlichkeit das es noch Tickets gibt
p_ticket_left = np.mean(sellout_positions[:, None]> positions, axis=0)


#Tabelle um zu sehen welche Postionen in der Warteschlange welche Wahrscheinlichkeit haben noch Tickets zu bekommen
summary_positions=[5_000,10_000,15_000,20_000,25_000,30_000,35_000,40_000,45_000,50_000,55_000,60_000,65_000,75_000]


#Index eimal berechnen 
summary_indices=[np.abs(positions-pos).argmin() for pos in summary_positions]
table=pd.DataFrame({"Queue-Position":summary_positions, 
                    "P(Ticket verfügbar)": [p_ticket_left[i]for i in summary_indices], 
                    "P(Kein Ticket)": [1-p_ticket_left[i]for i in summary_indices]})
table["P(Ticket verfügbar)"]=table["P(Ticket verfügbar)"].round(3)
table["P(Kein Ticket)"]=table["P(Kein Ticket)"].round(3)


#Nur die wichtigsten Zeilen anzeigen und nicht die ganze Tabelle (vorher schonmal ausgegeben und da war wichtigster bereich zwischen 30 und 40.000)
important_positions = [5_000, 25_000, 30_000, 31_000, 32_000, 33_000, 34_000, 35_000, 36_000, 37_000, 38_000, 39_000, 40_000, 41_000]
important_rows = table[table["Queue-Position"].isin(important_positions)]


#Cutoff-Bestimmung 
levels = [0.5, 0.25, 0.15, 0.10, 0.05, 0.01]
cutoffs = {f"{int(p*100)}% Chance": positions[np.argmax(p_ticket_left < p)]for p in levels}


#Ausgabe
print("\nSimulation abgeschlossen")
print(f"Stadion_Tickets: {TOTAL_TICKETS}")
print(f"Simulationen: {SIMULATIONS}")
print(f"Queue-Größe: {QUEUE_SIZE}")

print("\nSellout-Postion:")
print(f"Minimum: {sellout_positions.min():,}")
print(f"5%-Quantil: {int(np.quantile(sellout_positions, 0.05)):,}")
print(f"Median: {int(np.median(sellout_positions)):,}")
print(f"95%-Quantil: {int(np.quantile(sellout_positions, 0.95)):,}")
print(f"Maximum: {sellout_positions.max():,}")

print("\nKritische Queue-Positionen:")
for k, v in cutoffs.items():
    print(f"{k:>10} ca. {v:,}")


#Tabelle 
print(table)
#davon nur die wichtigen Zahlen
print("\nWichtige Queue-Positionen:")
print(important_rows)


#Wahrscheinlichkeiten besser darstellen in Diagramm
plt.figure(figuresize=(10,6))
plt.plot(positions/1000, p_ticket_left, label="P(Tickt verfügbar)")
for label, v in cutoffs.items():
    if 30_000 <= v <= 40_000:
        plt.axvline(v/ 1000, color='red', linestyle='--', alpha=0.7)
        plt.text(v / 1000 +0.2, 0.05, label, rotation=90, color='red', fontsize=8)
plt.xlabel("Queue-Position (in Tausend)")
plt.ylabel("P(Ticket verfügbar)")
plt.title("Wahrscheinlichkeit, dass noch Tickets verfügbar sind")
plt.grid (True)
plt.savefig("plot.png")
plt.show()

print("Simulation komplett abgeschlossen")