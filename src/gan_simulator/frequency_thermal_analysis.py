from src.gan_simulator.frequency_sweep import analyze_frequency_sweep
from src.gan_simulator.thermal_analysis import estimate_junction_temperature


def analyze_frequency_thermal_behavior(
    base_parameters,
    frequencies_hz,
    ambient_temperature_c,
    thermal_resistance_c_per_w,
):
    """Analyze power loss and steady-state junction temperature across frequencies."""

    sweep_results = analyze_frequency_sweep(
        base_parameters,
        frequencies_hz,
    )

    results = []

    for result in sweep_results:
        thermal_result = estimate_junction_temperature(
            power_loss_w=result["total_loss_w"],
            ambient_temperature_c=ambient_temperature_c,
            thermal_resistance_c_per_w=thermal_resistance_c_per_w,
        )

        results.append(
            {
                "frequency_hz": result["frequency_hz"],
                "total_loss_w": result["total_loss_w"],
                "estimated_efficiency_percent": result[
                    "estimated_efficiency_percent"
                ],
                "temperature_rise_c": thermal_result["temperature_rise_c"],
                "junction_temperature_c": thermal_result[
                    "junction_temperature_c"
                ],
            }
        )

    return results
