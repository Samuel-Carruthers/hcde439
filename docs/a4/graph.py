# Voltage at pin 9 vs time for the Question 1 sweep loop (servo.write(pos) every 100 ms)
import matplotlib.pyplot as plt

# Logic HIGH voltage on the Uno
VCC = 5.0
# The Servo library sends one pulse every 20 ms (50 Hz)
FRAME_MS = 20.0
# Servo library default pulse widths at 0 and 180 degrees, in ms
MIN_PULSE_MS = 0.544
MAX_PULSE_MS = 2.400
# delay(100) between angle steps, and 181 steps (pos = 0 to 180)
STEP_MS = 100.0
SWEEP_MS = 181 * STEP_MS

# Window: the last 100 ms of the sweep (pos = 180) and the first 100 ms after loop() restarts (pos = 0)
START_MS = SWEEP_MS - 100
END_MS = SWEEP_MS + 100


# Pulse width for an angle, same as the library's map(angle, 0, 180, 544, 2400)
def pulse_ms(angle):
    return MIN_PULSE_MS + angle * (MAX_PULSE_MS - MIN_PULSE_MS) / 180


# Angle written at time t (loop() restarts at 0 every 18.1 s)
def angle_at(t_ms):
    return int((t_ms % SWEEP_MS) // STEP_MS)


# Build the square wave: high for the pulse width at the start of each 20 ms frame, low otherwise
ts, vs = [], []
frame = START_MS
while frame < END_MS:
    width = pulse_ms(angle_at(frame))
    ts += [frame, frame, frame + width, frame + width]
    vs += [0, VCC, VCC, 0]
    frame += FRAME_MS
ts.append(END_MS)
vs.append(0)

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot([t / 1000 for t in ts], vs, color="tab:blue", linewidth=1.5)
# Mark where loop() restarts and pos goes from 180 back to 0
ax.axvline(SWEEP_MS / 1000, color="tab:red", linestyle="--", linewidth=1)
ax.text(SWEEP_MS / 1000 - 0.003, 5.25, "loop() restarts", color="tab:red", fontsize=9, ha="right")
ax.text((START_MS + 50) / 1000, 5.25, "pos = 180: 2.4 ms pulses", fontsize=9, ha="center")
ax.text((SWEEP_MS + 50) / 1000, 5.25, "pos = 0: 0.544 ms pulses", fontsize=9, ha="center")

ax.set_xlabel("Time (s)")
ax.set_ylabel("Voltage at pin 9 (V)")
ax.set_ylim(-0.3, 5.8)
ax.set_yticks([0, 5])
ax.set_xlim(START_MS / 1000, END_MS / 1000)
ax.set_title("Voltage at pin 9 with respect to ground")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("servo-voltage-graph.png", dpi=200)
print("saved")
