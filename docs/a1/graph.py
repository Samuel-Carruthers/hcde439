# Draw the voltage-vs-time graph for the three LEDs on one set of axes
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Time axis from 0 to 3600 ms (one full repeat of the pattern)
t = np.arange(0, 3600, 1)
# Name, on-state voltage (Vf), toggle interval in ms, plot color, and line width for each LED
leds = [
    ("Red", 2.0, 900, "#c0392b", 5),
    ("Green", 2.0, 600, "#2e8b3d", 3),
    ("Blue", 3.3, 300, "#2a5db0", 1.5),
]

# Create a single figure and axes so the lines overlap
fig, ax = plt.subplots(figsize=(9, 4.5))
# Plot one square wave per LED
for name, vf, interval, color, width in leds:
    # LEDs start off and turn on after the first interval, so odd intervals are "on"
    v = np.where((t // interval) % 2 == 1, vf, 0)
    # Draw the wave as a step plot
    ax.step(t, v, where="post", color=color, linewidth=width, label=name)

# Label the axes, set the limits, and show the legend
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Voltage across LED (V)")
ax.set_title("Voltage across each LED over time")
ax.set_ylim(-0.3, 3.8)
ax.legend(loc="upper right")
# Save the figure as a PNG
fig.tight_layout()
fig.savefig("voltage-graph.png", dpi=150)