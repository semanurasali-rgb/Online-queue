import matplotlib.pyplot as plt
import numpy as np

def plot_zoomed_probability(positions, p_ticket_left, zoom_min, zoom_max):
    mask = (positions >= zoom_min) & (positions <= zoom_max)
    plt.figure(figsize=(9, 5))
    plt.plot(positions[mask], p_ticket_left[mask], linewidth=2)
    for p in [0.5, 0.1, 0.05]:
        cutoff = positions[np.argmax(p_ticket_left < p)]
        plt.axhline(p, linestyle="--", alpha=0.6)
        plt.axvline(cutoff, linestyle=":", alpha=0.6)
    plt.xlabel("Queue-Position")
    plt.ylabel("P(Ticket verfügbar)")
    plt.title("Bereich, in dem die Ticketverfügbarkeit unwahrscheinlicher wird")
    plt.grid(True)
    plt.savefig("plot_zoom.png")
    plt.show()