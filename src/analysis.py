import numpy as np
import pandas as pd 

def ticket_prababilities(sellout_positions, positions):
    return np.mean(sellout_positions[:, None] > positions, axis=0)

def create_summary_table(positions, p_ticket_left, summary_positions):
    summary_indices = [np.abs(positions - pos).argmin() for pos in summary_positions]
    table = pd.DataFrame({"Queue-Position": summary_positions, "P(Ticket verfügbar)": [p_ticket_left[i] for i in summary_indices], "P(Kein Ticket)": [1 - p_ticket_left[i] for i in summary_indices]})
    return table.round(3)

def calculate_cutoffs(positions, p_ticket_left, levels):
    return{f"{int(p*100)}% Chance": positions[np.argmax(p_ticket_left < p)] for p in levels}