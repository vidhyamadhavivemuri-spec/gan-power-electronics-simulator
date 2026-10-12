from .loss_model import calculate_losses
from .parameters import SwitchingParameters


def compare_devices(
    gan_parameters: SwitchingParameters,
    silicon_parameters: SwitchingParameters,
) -> dict[str, dict[str, float]]:
    """Compare modeled losses for two sets of transistor parameters."""
    gan_results = calculate_losses(gan_parameters)
    silicon_results = calculate_losses(silicon_parameters)

    return {
        "GaN": gan_results,
        "Silicon": silicon_results,
    }
