import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt


print("Programm fängt an durchzulaufen")

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
for idx, prob in enumerate(p_ticket_left):
    if prob < 0.5:
        critical_idx = idx
        critical_pos = positions[idx]
        break

#Cutoff-Level bestimmen
cutoff_levels = [0.5, 0.25, 0.15, 0.10, 0.05, 0.01]

#Summary-Positionen
summary_positions = [critical_pos]
for p in cutoff_levels:
    for pos, prob in zip(positions, p_ticket_left):
        if prob < p:
            summary_positions.append(pos)
            break

#Um duplikate zu entfernen 
summary_positions = sorted(list(set(summary_positions)))


#Tabelle
summary_indices=[positions.tolist().index(pos) for pos in summary_positions]
table=pd.DataFrame({"Queue-Position":summary_positions, 
                    "P(Ticket verfügbar)": [p_ticket_left[i]for i in summary_indices], 
                    "P(Kein Ticket)": [1-p_ticket_left[i]for i in summary_indices]})
table["P(Ticket verfügbar)"]=table["P(Ticket verfügbar)"].round(3)
table["P(Kein Ticket)"]=table["P(Kein Ticket)"].round(3)


#Nur die wichtigsten Zeilen anzeigen und nicht die ganze Tabelle (vorher schonmal ausgegeben und da war wichtigster bereich zwischen 30 und 40.000)
important_positions = summary_positions
important_rows = table[table["Queue-Position"].isin(important_positions)]


#Cutoff-Bestimmung 
levels = [0.5, 0.25, 0.15, 0.10, 0.05, 0.01]
cutoffs = {}
for p in cutoff_levels:
    for pos, prob in zip(positions, p_ticket_left):
        if prob < p:
            cutoffs[f"{int(p*100)}% Chance"] = pos
            break

#Ergebnisse Ausgeben
print("\n Simulation abgeschlossen")
print(f"Stadion_Tickets: {TOTAL_TICKETS}")
print(f"Simulationen: {SIMULATIONS}")
print(f"Queue-Größe: {QUEUE_SIZE}")

#Sellout-Statistik
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
ZOOM_MIN = max(0, critical_pos - int(QUEUE_SIZE*0.1))
ZOOM_MAX = min(QUEUE_SIZE, critical_pos + int(QUEUE_SIZE*0.1))
mask = (positions >= ZOOM_MIN) & (positions <= ZOOM_MAX)

plt.figure(figsize=(12, 7))

#Hauptlinie für die Ticketwahrscheinlichkeit
plt.plot(positions[mask], p_ticket_left[mask], color='blue', linewidth=2, label='P(Ticket verfügbar)')

#Horizontale Cutoff-Linien
cutoff_levels = [0.5, 0.25, 0.15, 0.10, 0.05, 0.01]
h_color=['red', 'orange', 'green', 'purple', 'brown', 'cyan']
v_color="darkblue"

for p, c in zip(cutoff_levels, h_color):
     #horizontale Linie (soll die Wahrscheinlichkeit anzeigen)
        plt.axhline(p, linestyle="--", color=c, alpha=0.7, label=f"{int(p*100)}% Chance")
        indices = np.where(p_ticket_left < p)[0]
        if len(indices) > 0:
            cutoff_pos = positions[indices[0]]
            #vertikale Linie soll die Queue-Position anzeigen
            plt.axvline(cutoff_pos, linestyle=":", color=v_color,linewidth=2, alpha=0.8)
            plt.text(0.02, 0.95, "Vertiakle Linien 1&2:\n" "1. Ab hier weniger als 50% W'keit\n" "2. Ab hier weniger als 25% W'keit", transform=plt.gca().transAxes, fontsize=10, va='top', bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

#Kritischen Punkt markieren
critical_prob = p_ticket_left[critical_idx]
plt.scatter(critical_pos, critical_prob, color='black', s=80, zorder=5, label='Kritischer Punkt')
plt.text(critical_pos+500, critical_prob, f"{critical_pos}", fontsize=10, verticalalignment='bottom')

#Achsenbeschriftun, Titel und Raster
plt.xlabel("Queue-Position", fontsize=12)
plt.ylabel("P(Ticket verfügbar)", fontsize=12)
plt.title("Bereich in dem die Ticketverfügbarkeit unwahrscheinlicher wird", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)

#Achsenformatierung
plt.xticks(np.arange(ZOOM_MIN, ZOOM_MAX+1, max(1,(ZOOM_MAX-ZOOM_MIN)//10)), [f"{x:,}" for x in np.arange(ZOOM_MIN, ZOOM_MAX+1, max(1,(ZOOM_MAX-ZOOM_MIN)//10))])
plt.ylim(0,1.05)
plt.legend(title="Linienbedeutung")
plt.tight_layout()

plt.savefig("plot_zoom.png")
plt.show()