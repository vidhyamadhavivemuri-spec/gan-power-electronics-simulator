import numpy as np


def generate_switching_waveforms(
    voltage_v: float,
    current_a: float,
    frequency_hz: float,
    rise_time_s: float,
    fall_time_s: float,
    samples: int = 1000,
) -> dict[str, np.ndarray]:
    """Generate an illustrative hard-switching voltage/current waveform."""

    values = (
        voltage_v,
        current_a,
        frequency_hz,
        rise_time_s,
        fall_time_s,
    )

    if not all(np.isfinite(value) for value in values):
        raise ValueError("All inputs must be finite.")

    if any(value < 0 for value in values):
        raise ValueError("Inputs cannot be negative.")

    if frequency_hz <= 0:
        raise ValueError("Frequency must be greater than zero.")

    if rise_time_s <= 0 or fall_time_s <= 0:
        raise ValueError("Rise and fall times must be positive.")

    if not isinstance(samples, int) or isinstance(samples, bool):
        raise ValueError("Samples must be an integer.")

    if samples < 10:
        raise ValueError("Use at least 10 samples.")

    period = 1.0 / frequency_hz

    if rise_time_s + fall_time_s >= period:
        raise ValueError("Transition times must sum to less than the period.")

    time = np.linspace(0.0, period, samples, endpoint=False)
    phase = time / period

    voltage = np.full(samples, voltage_v, dtype=float)
    current = np.zeros(samples, dtype=float)

    # Turn-on: current rises while voltage falls.
    turn_on_start = 0.10 * period
    turn_on_end = turn_on_start + rise_time_s

    # Turn-off: current falls while voltage rises.
    turn_off_start = 0.60 * period
    turn_off_end = turn_off_start + fall_time_s

    if turn_on_end >= turn_off_start:
        raise ValueError("Transitions overlap; use shorter transition times.")

    on = (time >= turn_on_start) & (time < turn_on_end)
    on_fraction = (time[on] - turn_on_start) / rise_time_s
    voltage[on] = voltage_v * (1.0 - on_fraction)
    current[on] = current_a * on_fraction

    conducting = (time >= turn_on_end) & (time < turn_off_start)
    voltage[conducting] = 0.0
    current[conducting] = current_a

    off = (time >= turn_off_start) & (time < turn_off_end)
    off_fraction = (time[off] - turn_off_start) / fall_time_s
    voltage[off] = voltage_v * off_fraction
    current[off] = current_a * (1.0 - off_fraction)

    return {
        "time_s": time,
        "voltage_v": voltage,
        "current_a": current,
        "phase": phase,
    }
