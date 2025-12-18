import numpy as np
#Parameter 
TOTAL_TICKETS=75_000
QUEUE_SIZE=400_000
SIMULATIONS=1_500
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
results=np.array([run_single_simulation()for _ in range (SIMULATIONS)])
#Cutoff-Bestimmung 
cutoff_position= int(np.quantile(results, CUTOFF_PROB))
print("Simulation abgeschlossen")
print(f"Stadion-Tickets:{TOTAL_TICKETS}")
print(f"Simulationen:{SIMULATIONS}")
print(f"Cutoff-Wahrscheinlichkeit:{CUTOFF_PROB*100:.1f}%")
print(f"-> Cutoff-Position:ca. Person{cutoff_position}")
print("\n Weitere Kennzeichen:")
print(f"Median:{int(np.median(results))}")
print(f"95%-Quantil:{int(np.quantile(results, 0.95))}")
print(f"Minimum:{results.min()}")
print(f"Maximum:{results.max()}")
