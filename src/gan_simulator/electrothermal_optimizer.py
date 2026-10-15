
"""Optimize switching frequency using an iterative electrothermal model."""

import math

from .loss_model import calculate_losses
from .parameters import SwitchingParameters
from .temperature_dependent_losses import (
    calculate_temperature_dependent_losses,
)
from .thermal_analysis import estimate_junction_temperature


def optimize_electrothermal_frequency(
    base_parameters: SwitchingParameters,
    frequencies_hz: list[float],
    ambient_temperature_c: float,
    thermal_resistance_c_per_w: float,
    temperature_coefficient_per_c: float,
    reference_temperature_c: float = 25.0,
    max_junction_temperature_c: float | None = None,
    tolerance_c: float = 1e-6,
    max_iterations: int = 1000,
) -> dict[str, object]:
    """Select the lowest-loss frequency satisfying the thermal limit.

    Junction temperature and conduction loss are iterated until the
    temperature change is within tolerance. Switching and gate-drive
    losses remain based on the existing simplified loss model.
    """
    if not frequencies_hz:
        raise ValueError("At least one frequency is required.")

    numeric_values = {
        "ambient_temperature_c": ambient_temperature_c,
        "thermal_resistance_c_per_w": thermal_resistance_c_per_w,
        "temperature_coefficient_per_c": temperature_coefficient_per_c,
        "reference_temperature_c": reference_temperature_c,
        "tolerance_c": tolerance_c,
    }
    if max_junction_temperature_c is not None:
        numeric_values["max_junction_temperature_c"] = (
            max_junction_temperature_c
        )

    for name, value in numeric_values.items():
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
        ):
            raise ValueError(f"{name} must be a finite number.")

    if thermal_resistance_c_per_w <= 0:
        raise ValueError("Thermal resistance must be positive.")
    if temperature_coefficient_per_c < 0:
        raise ValueError("Temperature coefficient cannot be negative.")
    if tolerance_c <= 0:
        raise ValueError("Temperature tolerance must be positive.")
    if (
        isinstance(max_iterations, bool)
        or not isinstance(max_iterations, int)
        or max_iterations < 1
    ):
        raise ValueError("max_iterations must be a positive integer.")

    candidates = []

    for frequency_hz in frequencies_hz:
        if (
            isinstance(frequency_hz, bool)
            or not isinstance(frequency_hz, (int, float))
            or not math.isfinite(frequency_hz)
            or frequency_hz <= 0
        ):
            raise ValueError(
                "Candidate frequencies must be finite and positive."
            )

        parameters = SwitchingParameters(
            voltage_v=base_parameters.voltage_v,
            current_a=base_parameters.current_a,
            frequency_hz=float(frequency_hz),
            rds_on_ohm=base_parameters.rds_on_ohm,
            rise_time_s=base_parameters.rise_time_s,
            fall_time_s=base_parameters.fall_time_s,
            gate_charge_c=base_parameters.gate_charge_c,
            gate_voltage_v=base_parameters.gate_voltage_v,
            output_power_w=base_parameters.output_power_w,
        )

        baseline = calculate_losses(parameters)
        junction_temperature_c = float(ambient_temperature_c)
        converged = False
        adjusted = None
        iterations = 0

        for iterations in range(1, max_iterations + 1):
            adjusted = calculate_temperature_dependent_losses(
                parameters=parameters,
                reference_temperature_c=float(reference_temperature_c),
                junction_temperature_c=junction_temperature_c,
                temperature_coefficient_per_c=float(
                    temperature_coefficient_per_c
                ),
            )

            thermal = estimate_junction_temperature(
                power_loss_w=adjusted["total_loss_w"],
                ambient_temperature_c=float(ambient_temperature_c),
                thermal_resistance_c_per_w=float(
                    thermal_resistance_c_per_w
                ),
            )
            updated_temperature_c = thermal["junction_temperature_c"]

            if abs(updated_temperature_c - junction_temperature_c) <= tolerance_c:
                junction_temperature_c = updated_temperature_c
                converged = True
                break

            junction_temperature_c = updated_temperature_c

        if not converged:
            raise ValueError(
                f"Electrothermal calculation did not converge at "
                f"{frequency_hz:g} Hz within {max_iterations} iterations."
            )

        # Recalculate losses at the converged temperature.
        adjusted = calculate_temperature_dependent_losses(
            parameters=parameters,
            reference_temperature_c=float(reference_temperature_c),
            junction_temperature_c=junction_temperature_c,
            temperature_coefficient_per_c=float(
                temperature_coefficient_per_c
            ),
        )

        candidate = {
            "frequency_hz": float(frequency_hz),
            "baseline_total_loss_w": baseline["total_loss_w"],
            "total_loss_w": adjusted["total_loss_w"],
            "conduction_loss_w": adjusted["conduction_loss_w"],
            "switching_loss_w": adjusted["switching_loss_w"],
            "gate_drive_loss_w": adjusted["gate_drive_loss_w"],
            "estimated_efficiency_percent": (
                adjusted["estimated_efficiency_percent"]
            ),
            "junction_temperature_c": junction_temperature_c,
            "iterations": iterations,
            "converged": converged,
        }
        candidate["temperature_feasible"] = (
            max_junction_temperature_c is None
            or junction_temperature_c <= max_junction_temperature_c
        )
        candidates.append(candidate)

    feasible = [
        candidate
        for candidate in candidates
        if candidate["temperature_feasible"]
    ]

    if not feasible:
        raise ValueError(
            "No candidate frequency satisfies the maximum junction "
            "temperature constraint."
        )

    best = min(feasible, key=lambda item: item["total_loss_w"])

    return {
        "optimal_frequency_hz": best["frequency_hz"],
        "minimum_total_loss_w": best["total_loss_w"],
        "estimated_efficiency_percent": (
            best["estimated_efficiency_percent"]
        ),
        "estimated_junction_temperature_c": (
            best["junction_temperature_c"]
        ),
        "candidate_count": len(candidates),
        "feasible_candidate_count": len(feasible),
        "sweep_results": candidates,
        "objective": (
            "Minimum converged temperature-adjusted modeled loss among "
            "candidates satisfying the junction-temperature constraint"
        ),
    }
