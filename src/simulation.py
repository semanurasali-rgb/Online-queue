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
#Zufallsgenerator
rng=np.random.default_rng()


#Ticketverteilung 1-4
#nicht gleichverteilt
#Gewicht mit 1/sqrt(k)
#ergibt Erwartungswert=1.65
ticket_value=np.array([1,2,3,4])
weights=1/np.sqrt(ticket_value)
weights/= weights.sum()


#Einzelne Simulation (Simuliert den Ticketverkauf für eine Online-Warteschlange bei Kauf von Konzertkarten):
#- Entscheidet die Ticketanzahl von 0 bis 4
#- Während des Durchlaufs werden die Tickets immer geringer (Zieht also die Tickets ab)
#- Wenn die Tickets alle verkauft sind wird uns die Person zurückgegeben die als letztes ein Ticket bekommen konnte
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


#Wahrscheinlichkeit pro Queue-Position mit Schrittweite von 20
positions=np.arange(0, QUEUE_SIZE +1,20)


#Wahrscheinlichkeit das es noch Tickets gibt
p_ticket_left = np.mean(sellout_positions[:, None]> positions, axis=0)


#Kritischen Punkt bestimmen
#und den Index der ersten Position, bei der die Wahrscheinlichkeit ein Ticket zu bekommen bei < 5% liegt
critical_idx_candidates = np.where(p_ticket_left < 0.05)[0]
if len(critical_idx_candidates) > 0:
    critical_idx = critical_idx_candidates[0]
else: 
    critical_idx = len(p_ticket_left) - 1 
critical_pos = positions[critical_idx]

#Cutoff-Level bestimmen
cutoff_levels = [0.5, 0.25, 0.15, 0.10, 0.05, 0.01]

#Summary-Positionen(die kritischen Punkte pro Cutofflevels)
summary_positions = [critical_pos]
for p in cutoff_levels:
    for pos, prob in zip(positions, p_ticket_left):
        if prob < p:
            summary_positions.append(pos)
            break

#Um duplikate zu entfernen (Falls die selbe Queue-Position z.b als Cutoff-Level und als kritischer Punkt eingefügt wird, wir wollen sicher gehen, dass jede Position nur einmal vorkommt)
#Dadurch soll die Tabelle sowie das Diagramm übersichtlicher bleiben und auch die Logik korrekt
summary_positions = sorted(list(set(summary_positions)))


#Tabelle um die Wahrscheinlichkeiten besser darzustellen
summary_indices=[positions.tolist().index(pos) for pos in summary_positions]
table=pd.DataFrame({"Queue-Position":summary_positions, 
                    "P(Ticket verfügbar)": [p_ticket_left[i]for i in summary_indices], 
                    "P(Kein Ticket)": [1-p_ticket_left[i]for i in summary_indices]})
#Wir wollen die Werte die wir rausbekommen auf 3 Dezimalstellen gerundet haben
table["P(Ticket verfügbar)"]=table["P(Ticket verfügbar)"].round(3)
table["P(Kein Ticket)"]=table["P(Kein Ticket)"].round(3)


#Nur die wichtigsten Zeilen anzeigen  
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


#Diagramm
#Um die Wahrscheinlichkeiten besser und anschaulicher darzustellen
low_p = 0.5
high_p = 0.7

#Wir wollen nicht das ganze Diagramm sondern nur den relevantesten Bereich 
#der uns genau anzeigt ab welchem Punkt es kritisch wird noch Tickets zu bekommen
interesting_idx = np.where((p_ticket_left <= high_p) & (p_ticket_left >= low_p))[0]
if len(interesting_idx)==0:
    ZOOM_MIN = max(0, critical_pos - 500)
    ZOOM_MAX = min (QUEUE_SIZE, critical_pos + 500)
else: 
    ZOOM_MIN = positions[max(0, interesting_idx[0] - 2)]
    ZOOM_MAX = positions[min(len(positions)-1, interesting_idx[-1]+2)]

#Zeigt uns den relevantesten Bereich (relevantesten Queue-Positionen)
mask = (positions >= ZOOM_MIN) & (positions <= ZOOM_MAX)
if critical_pos < ZOOM_MIN:
    ZOOM_MIN = critical_pos
if critical_pos > ZOOM_MAX:
    ZOOM_MAX = critical_pos
mask = (positions >= ZOOM_MIN) & (positions <= ZOOM_MAX)

plt.figure(figsize=(12, 7))

#Hauptlinie für die Ticketwahrscheinlichkeit
plt.plot(positions[mask], p_ticket_left[mask], color='blue', linewidth=2, label='P(Ticket verfügbar)')

#Horizontale Cutoff-Linien
cutoff_levels = [0.5, 0.25, 0.15, 0.10, 0.05, 0.01]
h_color=['red', 'orange', 'green', 'purple', 'brown', 'cyan']
v_color="darkblue"
for p, c in zip(cutoff_levels, h_color):
        plt.axhline(p, linestyle="--", color=c, alpha=0.7, label=f"{int(p*100)}% Chance")
        

#Kritischen Punkt markieren
critical_prob = p_ticket_left[critical_idx]
plt.scatter(critical_pos, critical_prob, color='black', s=200, zorder=5, label='Kritischer Punkt (~5% Chance)')
plt.text(critical_pos+500, critical_prob, f"{critical_pos:,}", fontsize=10, verticalalignment='bottom')

#Achsenbeschriftun, Titel und Raster
plt.xlabel("Queue-Position", fontsize=12)
plt.ylabel("P(Ticket verfügbar)", fontsize=12)
plt.title("Abgeschätzter Bereich in dem die Queue-Position kritsch wird.", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)

#Achsenformatierung
plt.xticks(np.arange(ZOOM_MIN, ZOOM_MAX+1, max(1,(ZOOM_MAX-ZOOM_MIN)//10)), [f"{x:,}" for x in np.arange(ZOOM_MIN, ZOOM_MAX+1, max(1,(ZOOM_MAX-ZOOM_MIN)//10))])
plt.ylim(0,1.05)
plt.legend(title="Linienbedeutung")
plt.tight_layout()

plt.savefig("plot_zoom.png")
plt.savefig("Ergebnisse/plot_zoom.png")
plt.show()