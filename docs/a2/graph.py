# Voltage vs time for analogWrite(led, 64), 128, and 255 on an Arduino Uno PWM pin
import numpy as np
import matplotlib.pyplot as plt

# PWM frequency of Uno pins 5 and 6 in Hz
FREQ = 980.0
# Supply voltage in volts
VCC = 5.0
# Period of one PWM cycle in milliseconds
PERIOD_MS = 1000.0 / FREQ
# Number of PWM cycles to draw
CYCLES = 3

# Print the math for each analogWrite value
for value in (64, 128, 255):
    # Duty cycle is the analogWrite value divided by 255
    duty = value / 255
    # Time the pin stays HIGH in one period
    high_ms = duty * PERIOD_MS
    # Average voltage is duty cycle times supply voltage
    avg_v = duty * VCC
    print(f"analogWrite({value}): duty = {value}/255 = {duty*100:.1f}%, "
          f"high time = {high_ms:.3f} ms, average = {avg_v:.2f} V")
print(f"Period = 1 / {FREQ:.0f} Hz = {PERIOD_MS:.4f} ms")

# Build a square wave for one analogWrite value
def square_wave(value):
    # Duty cycle as a fraction
    duty = value / 255
    # List of (time, voltage) corner points
    t, v = [0.0], [VCC if duty > 0 else 0.0]
    # Add the corners for each cycle
    for c in range(CYCLES):
        # Start time of this cycle
        start = c * PERIOD_MS
        # Falling edge happens after the HIGH time
        if duty < 1:
            t += [start + duty * PERIOD_MS, start + duty * PERIOD_MS, start + PERIOD_MS, start + PERIOD_MS]
            v += [VCC, 0.0, 0.0, VCC]
        else:
            t += [start + PERIOD_MS]
            v += [VCC]
    return t, v

# Draw all three waves on the same axes so they overlap
fig, ax = plt.subplots(figsize=(9, 4.5))
# Style for each trace: value, color, line width, line style
styles = [(255, "tab:green", 7, "-"), (128, "tab:orange", 4, "-"), (64, "tab:red", 2, "-")]
# Plot the widest line first so thinner lines stay visible on top
for value, color, lw, ls in styles:
    t, v = square_wave(value)
    ax.plot(t, v, color=color, linewidth=lw, linestyle=ls, label=f"analogWrite(led, {value})")

# Axis labels and limits (voltage line is just 0 V to 5 V)
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Pin voltage (V)")
ax.set_ylim(-0.3, 5.3)
ax.set_yticks([0, 5])
ax.set_xlim(0, CYCLES * PERIOD_MS)
ax.set_title("PWM output voltage vs time (980 Hz)")
ax.legend(loc="center right")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("voltage_vs_time.png", dpi=200)
