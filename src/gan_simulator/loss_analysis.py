def analyze_loss_breakdown(losses: dict[str, float]) -> dict[str, object]:
    """Identify the dominant modeled transistor loss component."""
    components = {
        "Conduction": losses["conduction_loss_w"],
        "Switching": losses["switching_loss_w"],
        "Gate drive": losses["gate_drive_loss_w"],
    }

    if any(value < 0 for value in components.values()):
        raise ValueError("Loss values cannot be negative.")

    total = sum(components.values())

    if total <= 0:
        return {
            "dominant_component": "None",
            "dominant_loss_w": 0.0,
            "dominant_percentage": 0.0,
            "recommendation": "No modeled transistor losses to analyze.",
        }

    dominant = max(components, key=components.get)
    dominant_loss = components[dominant]
    percentage = 100.0 * dominant_loss / total

    recommendations = {
        "Conduction": (
            "Investigate RMS current and transistor on-resistance. "
            "Check thermal limits before selecting a device."
        ),
        "Switching": (
            "Investigate switching frequency and voltage/current "
            "transition times. Validate switching behavior with "
            "device data or measurements."
        ),
        "Gate drive": (
            "Investigate gate charge, gate-drive voltage, and "
            "driver power requirements."
        ),
    }

    return {
        "dominant_component": dominant,
        "dominant_loss_w": dominant_loss,
        "dominant_percentage": percentage,
        "recommendation": recommendations[dominant],
    }
