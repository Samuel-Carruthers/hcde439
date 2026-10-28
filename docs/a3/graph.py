# Voltage at A0 over time, from the serial monitor readings in a3output.png
import matplotlib.pyplot as plt

# Supply voltage in volts
VCC = 5.0
# Serial baud rate; loop() has no delay, so printing sets the sample rate
BAUD = 9600
# Bits sent per character (start bit + 8 data bits + stop bit)
BITS_PER_CHAR = 10

# analogRead values copied from the serial monitor, in order
readings = [447, 442, 435, 429, 416, 393, 372, 296, 284, 254, 231, 242, 236, 245]

# Rebuild each line's angle the same way the sketch does, to get its printed length
def angle_for(reading):
    # Same map() as the firmware, using integer math
    angle = (reading - 190) * 180 // (440 - 190)
    # Same constrain() as the firmware
    angle = max(0, min(180, angle))
    # Same dark threshold override as the firmware
    if reading < 250:
        angle = 0
    return angle

# Rebuild each line's LED brightness the same way the sketch does
def brightness_for(reading):
    # Same reversed map() as the firmware, truncating toward zero like C
    brightness = 255 + int((reading - 190) * -255 / (440 - 190))
    # Same constrain() as the firmware
    brightness = max(0, min(255, brightness))
    # Same dark threshold override as the firmware
    if reading < 250:
        brightness = 255
    return brightness

# Time stamps in seconds, one per serial line
times = []
t = 0.0
for r in readings:
    times.append(t)
    # Characters in the printed line, plus \r\n from println
    line = f"Room light: {r} | Blinds: {angle_for(r)} deg | Light: {brightness_for(r)}"
    t += (len(line) + 2) * BITS_PER_CHAR / BAUD

# Convert each reading to a voltage
volts = [r / 1023 * VCC for r in readings]

# Print the conversion for a few key readings
for r in (447, 250, 231):
    print(f"{r} / 1023 x {VCC:.0f} V = {r / 1023 * VCC:.2f} V")

# Draw the voltage trace
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(times, volts, color="tab:blue", linewidth=2, marker="o", markersize=3, label="V-measure (A0)")
# Mark the dark threshold where the blinds snap shut
ax.axhline(250 / 1023 * VCC, color="tab:red", linestyle="--", label="Dark threshold (250 = 1.22 V)")

# Axis labels and limits
ax.set_xlabel("Time (s)")
ax.set_ylabel("Voltage at A0 (V)")
ax.set_ylim(0, VCC)
ax.set_xlim(0, times[-1])
ax.set_title("Voltage at V-measure while covering the photoresistor")
ax.legend(loc="upper right")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("voltage-graph.png", dpi=200)
