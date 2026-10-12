from .loss_model import calculate_losses
from .parameters import SwitchingParameters


def analyze_frequency_sweep(
    base_parameters: SwitchingParameters,
    frequencies_hz: list[float],
) -> list[dict[str, float]]:
    """Calculate simplified losses at multiple switching frequencies."""
    if not frequencies_hz:
        raise ValueError("At least one frequency is required.")

    results = []

    for frequency in frequencies_hz:
        if frequency <= 0:
            raise ValueError("Frequencies must be greater than zero.")

        parameters = SwitchingParameters(
            voltage_v=base_parameters.voltage_v,
            current_a=base_parameters.current_a,
            frequency_hz=frequency,
            rds_on_ohm=base_parameters.rds_on_ohm,
            rise_time_s=base_parameters.rise_time_s,
            fall_time_s=base_parameters.fall_time_s,
            gate_charge_c=base_parameters.gate_charge_c,
            gate_voltage_v=base_parameters.gate_voltage_v,
            output_power_w=base_parameters.output_power_w,
        )

        losses = calculate_losses(parameters)
        results.append({
            "frequency_hz": frequency,
            **losses,
        })

    return results
