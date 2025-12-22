import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt


#Parameter 
TOTAL_TICKETS=75_000
QUEUE_SIZE=400_000
SIMULATIONS=3_000
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


#Einzelne Simulation
def run_single_simulation():
    tickets_left=TOTAL_TICKETS
    for person in range(QUEUE_SIZE):
        #entscheidet ob Person Tickets kauft
        if rng.random()<P_ZERO:
            demand=0
        else:
            demand=rng.choice(ticket_value, p=weights)
        tickets_left -=demand
        #Tickets sind aufgebraucht
        if tickets_left<0:
            #letzte Person die noch ein Ticket bekommt
            return person
    return QUEUE_SIZE


#Monte-Carlo-Simulation
sellout_positions=np.array([run_single_simulation()for _ in range(SIMULATIONS)])


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


print("\n Simulation abgeschlossen")
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


#Wahrscheinlichkeiten besser darstellen in Diagramm
plt.plot(positions, p_ticket_left)
plt.xlabel("Queue-Position")
plt.ylabel("P(Ticket verfügbar)")
plt.title("Wahrscheinlichkeit, dass noch Tickets verfügbar sind")
plt.grid (True)
plt.savefig("plot.png")
