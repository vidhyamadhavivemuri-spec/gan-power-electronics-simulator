"""Find the minimum modeled transistor loss over candidate frequencies."""

from .frequency_sweep import analyze_frequency_sweep
from .parameters import SwitchingParameters


def optimize_switching_frequency(
    base_parameters: SwitchingParameters,
    frequencies_hz: list[float],
) -> dict[str, object]:
    """Return the candidate frequency with the lowest modeled total loss."""
    if not frequencies_hz:
        raise ValueError("At least one frequency is required.")

    results = analyze_frequency_sweep(base_parameters, frequencies_hz)

    best = min(results, key=lambda result: result["total_loss_w"])

    return {
        "optimal_frequency_hz": best["frequency_hz"],
        "minimum_total_loss_w": best["total_loss_w"],
        "estimated_efficiency_percent": best["estimated_efficiency_percent"],
        "candidate_count": len(results),
        "sweep_results": results,
        "objective": "Minimum modeled transistor loss among supplied candidates",
    }
