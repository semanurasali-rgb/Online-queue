import numpy as np

def run_single_simulation(total_tickets, queue_size, p_zero, ticket_values, weights, rng):
    
    tickets_left = total_tickets

    for person in range (queue_size):
        if rng.random() < p_zero:
            demand = 0
        else:
            demand = rng.choice(ticket_values, p=weights)
        tickets_left -= demand
        if tickets_left < 0:
                return person
            
        return queue_size
    
def run_monte_carlo(simulations, total_tickets, queue_size, p_zero, ticket_value, weights, rng):
    return np.array([run_single_simulation(total_tickets, queue_size, p_zero, ticket_value, weights, rng)for _ in range (simulations)])