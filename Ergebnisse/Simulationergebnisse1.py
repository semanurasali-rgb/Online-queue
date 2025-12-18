import numpy as np
import pandas as pd 
#Parameter 
TOTAL_TICKETS=75_000
QUEUE_SIZE=400_000
SIMULATIONS=2_000
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
        if rng.random ()<P_ZERO:
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
#Wahrscheinlichkeit pro Queue-Position
positions=np.arange(0, QUEUE_SIZE +1)
#Wahrscheinlichkeit das es noch Tickets gibt
p_ticket_left=np.array([np.mean(sellout_positions>pos)for pos in positions])
#Tabelle um zu sehen welche Postionen in der Warteschlange welche Wahrscheinlichkeit haben noch Tickets zu bekommen
summary_positions=[20_000,30_000,40_000,50_000,60_000]
table=pd.DataFrame({"Queue-Position":summary_positions, "P(Ticket verfügbar)": [p_ticket_left[pos]for pos in summary_positions], "P(Kein Ticket)":[1-p_ticket_left[pos] for pos in summary_positions]})
table["P(Ticket verfügbar)"]=table ["P(Ticket verfügbar)"].round(3)
table["P(Kein Ticket)"]=table["P(Kein Ticket)"].round(3)
print ("\n=Ticket-Chancen nach Queue-Position =\n")
print(table.to_string(index=False))
#Cutoff-Bestimmung 
cutoffs={"50% Chance": np.argmax(p_ticket_left<0.5), "25% Chance": np.argmax(p_ticket_left<0.25), "15& Chance": np.argmax(p_ticket_left<0.15), "10% Chance": np.argmax(p_ticket_left<0.10), "5% Chance": np.argmax(p_ticket_left<0.05), "1% Chance": np.argmax(p_ticket_left<0.01)}
print("\n=Grenze in der es eher Kritisch ist Tickts zu bekommen=\n")
for k, v in cutoffs.items(): 
    print (f"{k:>10}: ca. Position{v:,}")
print("Simulation abgeschlossen")
print(f"Stadion-Tickets:{TOTAL_TICKETS}")
print(f"Simulationen:{SIMULATIONS}")
print(f"Queue-Größe:{QUEUE_SIZE}")
print("\n=Sellout-Postition (Zusammenfassung)=")
print(f"Minimum: {sellout_positions.min():,}")
print(f"5%-Quantil:{int(np.quantile(sellout_positions, 0.05)):,}")
print(f"Median: {int(np.median(sellout_positions)):,}")
print(f"95%-Quantil: {int(np.quantile(sellout_positions, 0.95)):,}")
print(f"Maximum: {sellout_positions.max():,}")