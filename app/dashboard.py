"""Interactive dashboard for the GaN Power Electronics Simulator."""

from pathlib import Path
import sys

# Add the project root before importing local modules.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from src.gan_simulator.device_comparison import compare_devices
from src.gan_simulator.electrothermal import solve_electrothermal
from src.gan_simulator.frequency_optimizer import optimize_switching_frequency
from src.gan_simulator.frequency_thermal_analysis import (
    analyze_frequency_thermal_behavior,
)
from src.gan_simulator.electrothermal_optimizer import (
    optimize_electrothermal_frequency,
)
from src.gan_simulator.loss_analysis import analyze_loss_breakdown
from src.gan_simulator.loss_model import calculate_losses
from src.gan_simulator.parameters import SwitchingParameters
from src.gan_simulator.temperature_model import (
    estimate_temperature_dependent_resistance,
)
from src.gan_simulator.thermal_analysis import estimate_junction_temperature
from src.gan_simulator.transient_thermal import simulate_transient_temperature
from src.gan_simulator.temperature_dependent_losses import (
    calculate_temperature_dependent_losses,
)

st.set_page_config(
    page_title="GaN Power Electronics Simulator",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ GaN Power Electronics Simulator")
st.write(
    "Explore how operating conditions affect estimated transistor losses, "
    "efficiency, switching-frequency trade-offs, and thermal response."
)

# ---------------------------------------------------------------------------
# Operating parameters
# ---------------------------------------------------------------------------
st.sidebar.header("Operating Parameters")

voltage_v = st.sidebar.slider(
    "Drain-source voltage (V)", 50, 650, 400, step=10
)
current_a = st.sidebar.slider("RMS current (A)", 1, 40, 10)
frequency_khz = st.sidebar.slider(
    "Switching frequency (kHz)", 10, 500, 100, step=10
)
rds_on_mohm = st.sidebar.slider("On-resistance (mΩ)", 5, 200, 50, step=5)
rise_time_ns = st.sidebar.slider("Rise time (ns)", 5, 200, 20, step=5)
fall_time_ns = st.sidebar.slider("Fall time (ns)", 5, 200, 20, step=5)
gate_charge_nc = st.sidebar.slider("Gate charge (nC)", 1, 100, 10)
gate_voltage_v = st.sidebar.slider(
    "Gate-drive voltage (V)", 3.0, 10.0, 5.0, step=0.5
)
output_power_w = st.sidebar.number_input(
    "Output power (W)",
    min_value=1.0,
    max_value=100_000.0,
    value=500.0,
    step=50.0,
    key="operating_output_power_w",
)

parameters = SwitchingParameters(
    voltage_v=float(voltage_v),
    current_a=float(current_a),
    frequency_hz=float(frequency_khz * 1000),
    rds_on_ohm=float(rds_on_mohm / 1000),
    rise_time_s=float(rise_time_ns * 1e-9),
    fall_time_s=float(fall_time_ns * 1e-9),
    gate_charge_c=float(gate_charge_nc * 1e-9),
    gate_voltage_v=float(gate_voltage_v),
    output_power_w=float(output_power_w),
)

results = calculate_losses(parameters)
breakdown = analyze_loss_breakdown(results)

# ---------------------------------------------------------------------------
# Loss analysis
# ---------------------------------------------------------------------------
st.header("Loss Breakdown Analysis")

col1, col2, col3 = st.columns(3)
col1.metric("Dominant loss component", breakdown["dominant_component"])
col2.metric("Dominant loss", f'{breakdown["dominant_loss_w"]:.4f} W')
col3.metric("Share of total loss", f'{breakdown["dominant_percentage"]:.2f}%')

st.write("**Recommendation**")
st.info(breakdown["recommendation"])

st.subheader("Simulation Results")
col1, col2, col3 = st.columns(3)
col1.metric("Total transistor loss", f'{results["total_loss_w"]:.3f} W')
col2.metric("Switching loss", f'{results["switching_loss_w"]:.3f} W')
col3.metric(
    "Estimated efficiency",
    f'{results["estimated_efficiency_percent"]:.2f}%',
)

st.subheader("Power Loss Breakdown")
loss_labels = ["Conduction", "Switching", "Gate drive"]
loss_values = [
    results["conduction_loss_w"],
    results["switching_loss_w"],
    results["gate_drive_loss_w"],
]
fig, ax = plt.subplots(figsize=(9, 4))
bars = ax.bar(loss_labels, loss_values)
ax.set_ylabel("Power loss (W)")
ax.set_title("Estimated Transistor Loss Components")
ax.grid(axis="y", alpha=0.3)
ax.bar_label(bars, fmt="%.3f W", padding=3)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.subheader("Detailed Results")
st.dataframe(
    {
        "Parameter": [
            "Conduction loss",
            "Switching loss",
            "Gate-drive loss",
            "Total loss",
            "Estimated efficiency",
        ],
        "Value": [
            f'{results["conduction_loss_w"]:.6f} W',
            f'{results["switching_loss_w"]:.6f} W',
            f'{results["gate_drive_loss_w"]:.6f} W',
            f'{results["total_loss_w"]:.6f} W',
            f'{results["estimated_efficiency_percent"]:.4f}%',
        ],
    },
    hide_index=True,
    use_container_width=True,
)

st.info(
    "Educational model only: estimates use simplified hard-switching "
    "assumptions and do not include output-capacitance losses, reverse "
    "conduction, dead time, or parasitic effects. Estimated efficiency "
    "uses output power plus modeled transistor losses."
)

# ---------------------------------------------------------------------------
# GaN versus Silicon comparison
# ---------------------------------------------------------------------------
st.divider()
st.header("⚡ GaN vs. Silicon Comparison")
st.write(
    "Compare two illustrative device parameter sets under the same operating "
    "conditions. These are assumptions, not measured specifications for "
    "particular transistors."
)

gan_parameters = parameters
silicon_parameters = SwitchingParameters(
    voltage_v=parameters.voltage_v,
    current_a=parameters.current_a,
    frequency_hz=parameters.frequency_hz,
    rds_on_ohm=0.08,
    rise_time_s=50e-9,
    fall_time_s=50e-9,
    gate_charge_c=30e-9,
    gate_voltage_v=10.0,
    output_power_w=parameters.output_power_w,
)
comparison = compare_devices(gan_parameters, silicon_parameters)
gan = comparison["GaN"]
silicon = comparison["Silicon"]

col1, col2 = st.columns(2)
with col1:
    st.subheader("GaN — Current Parameters")
    st.metric("Total modeled loss", f'{gan["total_loss_w"]:.3f} W')
    st.metric("Estimated efficiency", f'{gan["estimated_efficiency_percent"]:.2f}%')
with col2:
    st.subheader("Silicon — Illustrative Parameters")
    st.metric("Total modeled loss", f'{silicon["total_loss_w"]:.3f} W')
    st.metric(
        "Estimated efficiency",
        f'{silicon["estimated_efficiency_percent"]:.2f}%',
    )

comparison_fig, comparison_ax = plt.subplots(figsize=(9, 4))
labels = ["Conduction", "Switching", "Gate drive"]
gan_losses = [
    gan["conduction_loss_w"],
    gan["switching_loss_w"],
    gan["gate_drive_loss_w"],
]
silicon_losses = [
    silicon["conduction_loss_w"],
    silicon["switching_loss_w"],
    silicon["gate_drive_loss_w"],
]
x = range(len(labels))
width = 0.35
comparison_ax.bar(
    [i - width / 2 for i in x], gan_losses, width, label="GaN"
)
comparison_ax.bar(
    [i + width / 2 for i in x], silicon_losses, width, label="Silicon"
)
comparison_ax.set_xticks(list(x))
comparison_ax.set_xticklabels(labels)
comparison_ax.set_ylabel("Modeled power loss (W)")
comparison_ax.set_title("Illustrative Loss Comparison")
comparison_ax.legend()
comparison_ax.grid(axis="y", alpha=0.3)
comparison_fig.tight_layout()
st.pyplot(comparison_fig)
plt.close(comparison_fig)

# ---------------------------------------------------------------------------
# Switching-frequency optimization
# ---------------------------------------------------------------------------
st.divider()
st.header("🎯 Switching-Frequency Optimization")
st.write(
    "Find the candidate switching frequency with the lowest modeled "
    "transistor loss within a selected range."
)

opt_col1, opt_col2 = st.columns(2)
with opt_col1:
    min_frequency_khz = st.number_input(
        "Minimum frequency (kHz)",
        min_value=10,
        max_value=500,
        value=50,
        step=10,
        key="optimizer_min_frequency_khz",
    )
with opt_col2:
    max_frequency_khz = st.number_input(
        "Maximum frequency (kHz)",
        min_value=10,
        max_value=500,
        value=300,
        step=10,
        key="optimizer_max_frequency_khz",
    )

if min_frequency_khz >= max_frequency_khz:
    st.warning("Maximum frequency must be greater than minimum frequency.")
else:
    candidate_frequencies_hz = [
        float(f * 1000)
        for f in range(
            int(min_frequency_khz), int(max_frequency_khz) + 1, 10
        )
    ]
    if candidate_frequencies_hz[-1] != float(max_frequency_khz * 1000):
        candidate_frequencies_hz.append(float(max_frequency_khz * 1000))

    optimization = optimize_switching_frequency(
        parameters, candidate_frequencies_hz
    )
    best_frequency_khz = optimization["optimal_frequency_hz"] / 1000

    opt_col1, opt_col2, opt_col3 = st.columns(3)
    opt_col1.metric("Lowest-loss candidate", f"{best_frequency_khz:.0f} kHz")
    opt_col2.metric(
        "Minimum modeled loss",
        f'{optimization["minimum_total_loss_w"]:.4f} W',
    )
    opt_col3.metric(
        "Estimated efficiency",
        f'{optimization["estimated_efficiency_percent"]:.2f}%',
    )

    sweep_results = optimization["sweep_results"]
    frequencies_khz = [r["frequency_hz"] / 1000 for r in sweep_results]
    total_losses = [r["total_loss_w"] for r in sweep_results]
    switching_losses = [r["switching_loss_w"] for r in sweep_results]
    conduction_losses = [r["conduction_loss_w"] for r in sweep_results]
    gate_drive_losses = [r["gate_drive_loss_w"] for r in sweep_results]

    optimization_fig, optimization_ax = plt.subplots(figsize=(10, 5))
    optimization_ax.plot(
        frequencies_khz, total_losses, marker="o", label="Total loss"
    )
    optimization_ax.plot(
        frequencies_khz, switching_losses, linestyle="--", label="Switching loss"
    )
    optimization_ax.plot(
        frequencies_khz, conduction_losses, linestyle=":", label="Conduction loss"
    )
    optimization_ax.plot(
        frequencies_khz, gate_drive_losses, linestyle="-.", label="Gate-drive loss"
    )
    optimization_ax.axvline(
        best_frequency_khz, linestyle=":", label="Lowest-loss candidate"
    )
    optimization_ax.set_xlabel("Switching frequency (kHz)")
    optimization_ax.set_ylabel("Modeled power loss (W)")
    optimization_ax.set_title("Modeled Loss vs. Switching Frequency")
    optimization_ax.grid(alpha=0.3)
    optimization_ax.legend()
    optimization_fig.tight_layout()
    st.pyplot(optimization_fig)
    plt.close(optimization_fig)

    st.caption(
        "The optimizer selects the lowest-loss candidate among tested "
        "frequencies. This is not a universal real-device optimum; practical "
        "designs must also consider thermal limits, converter topology, "
        "passive components, EMI, and operating requirements."
    )

# ---------------------------------------------------------------------------
# Steady-state thermal analysis
# ---------------------------------------------------------------------------
st.divider()
st.header("🌡️ Thermal Analysis")
st.write(
    "Estimate steady-state transistor junction temperature from the modeled "
    "total power loss."
)

thermal_col1, thermal_col2 = st.columns(2)
with thermal_col1:
    ambient_temperature_c = st.number_input(
        "Ambient temperature (°C)",
        min_value=-50.0,
        max_value=150.0,
        value=25.0,
        step=5.0,
        key="steady_ambient_temperature_c",
    )
with thermal_col2:
    thermal_resistance = st.number_input(
        "Effective thermal resistance (°C/W)",
        min_value=0.0,
        max_value=100.0,
        value=2.0,
        step=0.5,
        key="steady_thermal_resistance",
    )

thermal_result = estimate_junction_temperature(
    power_loss_w=results["total_loss_w"],
    ambient_temperature_c=ambient_temperature_c,
    thermal_resistance_c_per_w=thermal_resistance,
)

thermal_metric_col1, thermal_metric_col2 = st.columns(2)
thermal_metric_col1.metric(
    "Estimated junction temperature",
    f'{thermal_result["junction_temperature_c"]:.2f} °C',
)
thermal_metric_col2.metric(
    "Temperature rise",
    f'{thermal_result["temperature_rise_c"]:.2f} °C',
)
st.caption(
    "Simplified steady-state estimate. The thermal resistance must represent "
    "the intended complete thermal path. This model excludes transient "
    "heating, temperature-dependent device losses, and detailed package or "
    "heatsink behavior. Use device datasheets and validated models for "
    "real hardware design."
)

# ---------------------------------------------------------------------------
# Temperature-dependent on-resistance
# ---------------------------------------------------------------------------
st.subheader("Temperature-Dependent On-Resistance")
st.write(
    "Estimate how junction temperature changes on-resistance and conduction "
    "loss using a configurable linear model."
)

temp_col1, temp_col2 = st.columns(2)
with temp_col1:
    reference_temperature_c = st.number_input(
        "Reference temperature (°C)",
        min_value=-50.0,
        max_value=200.0,
        value=25.0,
        step=5.0,
        key="reference_temperature_c",
    )
with temp_col2:
    temperature_coefficient = st.number_input(
        "Assumed temperature coefficient (1/°C)",
        min_value=0.0,
        max_value=0.02,
        value=0.004,
        step=0.001,
        format="%.4f",
        key="temperature_coefficient_per_c",
    )

temperature_result = estimate_temperature_dependent_resistance(
    reference_resistance_ohm=parameters.rds_on_ohm,
    reference_temperature_c=reference_temperature_c,
    junction_temperature_c=thermal_result["junction_temperature_c"],
    temperature_coefficient_per_c=temperature_coefficient,
)
adjusted_resistance = temperature_result["estimated_resistance_ohm"]
adjusted_conduction_loss = parameters.current_a**2 * adjusted_resistance
reference_conduction_loss = (
    parameters.current_a**2 * parameters.rds_on_ohm
)

resistance_col1, resistance_col2 = st.columns(2)
resistance_col1.metric(
    "Estimated on-resistance",
    f"{adjusted_resistance * 1000:.2f} mΩ",
    delta=(
        f"{(adjusted_resistance / parameters.rds_on_ohm - 1) * 100:.1f}% "
        "vs. reference"
    ),
)
resistance_col2.metric(
    "Adjusted conduction loss",
    f"{adjusted_conduction_loss:.4f} W",
    delta=(
        f"{adjusted_conduction_loss - reference_conduction_loss:.4f} W "
        "vs. reference"
    ),
)
st.caption(
    "Illustrative linear model only. The temperature coefficient is user-"
    "assumed, and actual GaN on-resistance depends on the specific device, "
    "datasheet conditions, gate voltage, and other operating factors. This "
    "section adjusts conduction loss only; it does not recalculate total "
    "losses or iterate thermal equilibrium."
)

# ---------------------------------------------------------------------------
# Electrothermal fixed-point analysis
# ---------------------------------------------------------------------------
st.divider()
st.header("♨️ Electrothermal Analysis")
st.write(
    "Iteratively estimate junction temperature, temperature-dependent "
    "on-resistance, and conduction loss using a simplified coupled model."
)

et_col1, et_col2 = st.columns(2)
with et_col1:
    et_ambient_c = st.number_input(
        "Electrothermal ambient temperature (°C)",
        min_value=-50.0,
        max_value=150.0,
        value=25.0,
        step=5.0,
        key="electrothermal_ambient_temperature_c",
    )
    et_rth = st.number_input(
        "Electrothermal thermal resistance (°C/W)",
        min_value=0.1,
        max_value=100.0,
        value=2.0,
        step=0.1,
        key="electrothermal_thermal_resistance",
    )
with et_col2:
    et_reference_temp = st.number_input(
        "Electrothermal reference temperature (°C)",
        min_value=-50.0,
        max_value=200.0,
        value=25.0,
        step=5.0,
        key="electrothermal_reference_temperature_c",
    )
    et_alpha = st.number_input(
        "Electrothermal temperature coefficient (1/°C)",
        min_value=0.0,
        max_value=0.02,
        value=0.004,
        step=0.001,
        format="%.4f",
        key="electrothermal_temperature_coefficient_per_c",
    )

electrothermal_result = solve_electrothermal(
    current_a=parameters.current_a,
    reference_resistance_ohm=parameters.rds_on_ohm,
    reference_temperature_c=et_reference_temp,
    ambient_temperature_c=et_ambient_c,
    thermal_resistance_c_per_w=et_rth,
    temperature_coefficient_per_c=et_alpha,
)

et_metric1, et_metric2, et_metric3 = st.columns(3)
et_metric1.metric(
    "Junction temperature",
    f'{electrothermal_result["junction_temperature_c"]:.2f} °C',
)
et_metric2.metric(
    "Estimated on-resistance",
    f'{electrothermal_result["estimated_resistance_ohm"] * 1000:.2f} mΩ',
)
et_metric3.metric(
    "Conduction loss",
    f'{electrothermal_result["conduction_loss_w"]:.3f} W',
)
st.caption(
    f'Converged: {electrothermal_result["converged"]} · '
    f'Iterations: {electrothermal_result["iterations"]} · '
    f'Temperature rise: {electrothermal_result["temperature_rise_c"]:.2f} °C'
)
st.caption(
    "Simplified coupled estimate: current, thermal resistance, and a linear "
    "temperature coefficient are assumed constant. Switching and gate-drive "
    "losses are not included in this electrothermal iteration."
)

# ---------------------------------------------------------------------------
# Transient thermal simulation
# ---------------------------------------------------------------------------
st.divider()
st.header("⏱️ Transient Thermal Simulation")
st.write(
    "Simulate junction temperature versus time after a power change using "
    "a first-order thermal RC model. A negative power change represents a "
    "reduction from the initial operating power."
)

transient_col1, transient_col2 = st.columns(2)
with transient_col1:
    transient_power_w = st.number_input(
        "Power change (W; negative = cooling step)",
        min_value=-100000.0,
        max_value=100000.0,
        value=10.0,
        step=1.0,
        key="transient_power_change",
    )
    transient_ambient_c = st.number_input(
        "Transient ambient temperature (°C)",
        min_value=-50.0,
        max_value=150.0,
        value=25.0,
        step=1.0,
        key="transient_ambient_temperature",
    )
    transient_initial_c = st.number_input(
        "Initial junction temperature (°C)",
        min_value=-50.0,
        max_value=300.0,
        value=25.0,
        step=1.0,
        key="transient_initial_temperature",
    )
with transient_col2:
    transient_rth = st.number_input(
        "Transient thermal resistance (°C/W)",
        min_value=0.1,
        max_value=100.0,
        value=2.0,
        step=0.1,
        key="transient_thermal_resistance",
    )
    transient_cth = st.number_input(
        "Transient thermal capacitance (J/°C)",
        min_value=0.001,
        max_value=10000.0,
        value=5.0,
        step=0.5,
        key="transient_thermal_capacitance",
    )
    duration_s = st.number_input(
        "Simulation duration (seconds)",
        min_value=0.1,
        max_value=100000.0,
        value=50.0,
        step=5.0,
        key="transient_simulation_duration",
    )

time_values = [i * duration_s / 200 for i in range(201)]
transient_result = simulate_transient_temperature(
    time_s=time_values,
    ambient_temperature_c=transient_ambient_c,
    power_step_w=transient_power_w,
    thermal_resistance_c_per_w=transient_rth,
    thermal_capacitance_j_per_c=transient_cth,
    initial_temperature_c=transient_initial_c,
)

transient_fig, transient_ax = plt.subplots(figsize=(10, 5))
transient_ax.plot(
    transient_result["time_s"],
    transient_result["junction_temperature_c"],
    linewidth=2,
    label="Junction temperature",
)
transient_ax.axhline(
    transient_result["steady_state_temperature_c"],
    linestyle="--",
    label="Predicted steady-state temperature",
)
transient_ax.set_xlabel("Time (seconds)")
transient_ax.set_ylabel("Junction temperature (°C)")
transient_ax.set_title("Transient Thermal Response")
transient_ax.grid(True, alpha=0.3)
transient_ax.legend()
transient_fig.tight_layout()
st.pyplot(transient_fig)
plt.close(transient_fig)

transient_metric1, transient_metric2, transient_metric3 = st.columns(3)
transient_metric1.metric(
    "Thermal time constant",
    f'{transient_result["time_constant_s"]:.3f} s',
)
transient_metric2.metric(
    "Final simulated temperature",
    f'{transient_result["junction_temperature_c"][-1]:.2f} °C',
)
transient_metric3.metric(
    "Predicted steady-state temperature",
    f'{transient_result["steady_state_temperature_c"]:.2f} °C',
)
st.caption(
    "Engineering approximation using a first-order thermal RC model. It "
    "assumes constant thermal resistance, thermal capacitance, and power "
    "change. Validate against device datasheets and suitable thermal models "
    "before applying results to real hardware."
)
st.divider()
st.header("🌡️ Frequency vs. Junction Temperature")
st.write(
"Explore how switching frequency affects modeled power loss and "
"estimated steady-state junction temperature."
)

freq_thermal_col1, freq_thermal_col2, freq_thermal_col3 = st.columns(3)

with freq_thermal_col1:
    ft_min_khz = st.slider(
        "Minimum sweep frequency (kHz)",
        min_value=10,
        max_value=490,
        value=50,
        step=10,
        key="ft_min_frequency_khz",
    )

with freq_thermal_col2:
    ft_max_khz = st.slider(
        "Maximum sweep frequency (kHz)",
        min_value=20,
        max_value=500,
        value=500,
        step=10,
        key="ft_max_frequency_khz",
    )

with freq_thermal_col3:
    ft_points = st.slider(
        "Number of sweep points",
        min_value=5,
        max_value=100,
        value=30,
        step=5,
        key="ft_sweep_points",
    )

ft_ambient_c = st.number_input(
"Frequency sweep ambient temperature (°C)",
min_value=-50.0,
max_value=150.0,
value=25.0,
step=5.0,
key="ft_ambient_temperature_c",
)

ft_rth = st.number_input(
"Frequency sweep thermal resistance (°C/W)",
min_value=0.1,
max_value=100.0,
value=2.0,
step=0.1,
key="ft_thermal_resistance",
)

if ft_min_khz >= ft_max_khz:
    st.warning("Maximum frequency must be greater than minimum frequency.")
else:
    ft_frequencies_hz = [
        float(ft_min_khz * 1000)
        + i * (
            (ft_max_khz - ft_min_khz) * 1000 / (ft_points - 1)
        )
        for i in range(ft_points)
    ]

    ft_results = analyze_frequency_thermal_behavior(
        base_parameters=parameters,
        frequencies_hz=ft_frequencies_hz,
        ambient_temperature_c=float(ft_ambient_c),
        thermal_resistance_c_per_w=float(ft_rth),
    )

    ft_frequency_khz = [
        item["frequency_hz"] / 1000 for item in ft_results
    ]
    ft_losses_w = [item["total_loss_w"] for item in ft_results]
    ft_temperatures_c = [
        item["junction_temperature_c"] for item in ft_results
    ]

    ft_fig, ft_ax1 = plt.subplots(figsize=(10, 5))

    loss_line = ft_ax1.plot(
        ft_frequency_khz,
        ft_losses_w,
        label="Total power loss",
        linewidth=2,
    )
    ft_ax1.set_xlabel("Switching frequency (kHz)")
    ft_ax1.set_ylabel("Total modeled power loss (W)")
    ft_ax1.grid(True, alpha=0.3)

    ft_ax2 = ft_ax1.twinx()
    temperature_line = ft_ax2.plot(
        ft_frequency_khz,
        ft_temperatures_c,
        label="Junction temperature",
        linewidth=2,
        linestyle="--",
    )
    ft_ax2.set_ylabel("Estimated junction temperature (°C)")

    ft_lines = loss_line + temperature_line
    ft_labels = [line.get_label() for line in ft_lines]
    ft_ax1.legend(ft_lines, ft_labels, loc="best")

    ft_fig.tight_layout()
    st.pyplot(ft_fig)
    plt.close(ft_fig)

    st.dataframe(
        [
            {
                "Frequency (kHz)": round(item["frequency_hz"] / 1000, 2),
                "Total power loss (W)": round(item["total_loss_w"], 4),
                "Efficiency (%)": round(
                    item["estimated_efficiency_percent"], 2
                ),
                "Temperature rise (°C)": round(
                    item["temperature_rise_c"], 2
                ),
                "Junction temperature (°C)": round(
                    item["junction_temperature_c"], 2
                ),
            }
            for item in ft_results
        ],
        use_container_width=True,
    )

st.caption(
    "Educational steady-state estimate. Total modeled transistor loss "
    "is multiplied by a fixed thermal resistance to estimate junction "
    "temperature. This sweep does not model temperature-dependent losses, "
    "thermal transients, device-specific limits, or cooling-system changes."
)

st.divider()
st.header("🌡️ Temperature-Dependent Power Losses")

st.write(
    "Compare the baseline loss calculation with losses adjusted for "
    "junction-temperature-dependent on-resistance."
)

td_col1, td_col2 = st.columns(2)

with td_col1:
    td_reference_temp = st.number_input(
        "Reference temperature (°C)",
        min_value=-50.0,
        max_value=200.0,
        value=25.0,
        step=5.0,
        key="td_reference_temp",
    )

    td_junction_temp = st.number_input(
        "Junction temperature (°C)",
        min_value=-50.0,
        max_value=250.0,
        value=100.0,
        step=5.0,
        key="td_junction_temp",
    )

with td_col2:
    td_coefficient = st.number_input(
        "On-resistance temperature coefficient (1/°C)",
        min_value=0.0,
        max_value=0.02,
        value=0.004,
        step=0.001,
        format="%.4f",
        key="td_temperature_coefficient",
    )

td_baseline = calculate_losses(parameters)

try:
    td_adjusted = calculate_temperature_dependent_losses(
        parameters=parameters,
        reference_temperature_c=float(td_reference_temp),
        junction_temperature_c=float(td_junction_temp),
        temperature_coefficient_per_c=float(td_coefficient),
    )
except ValueError as error:
    st.error(f"Unable to calculate temperature-dependent losses: {error}")
else:
    td_metric1, td_metric2, td_metric3 = st.columns(3)

    td_metric1.metric(
        "Baseline total loss",
        f"{td_baseline['total_loss_w']:.4f} W",
    )

    td_metric2.metric(
        "Temperature-adjusted loss",
        f"{td_adjusted['total_loss_w']:.4f} W",
        delta=(
            f"{td_adjusted['total_loss_w'] - td_baseline['total_loss_w']:+.4f} W"
        ),
    )

    td_metric3.metric(
        "Adjusted efficiency",
        f"{td_adjusted['estimated_efficiency_percent']:.2f}%",
        delta=(
            f"{td_adjusted['estimated_efficiency_percent'] - td_baseline['estimated_efficiency_percent']:+.2f} percentage points"
        ),
    )

    td_categories = [
        "Conduction",
        "Switching",
        "Gate drive",
    ]

    td_baseline_values = [
        td_baseline["conduction_loss_w"],
        td_baseline["switching_loss_w"],
        td_baseline["gate_drive_loss_w"],
    ]

    td_adjusted_values = [
        td_adjusted["conduction_loss_w"],
        td_adjusted["switching_loss_w"],
        td_adjusted["gate_drive_loss_w"],
    ]

    td_fig, td_ax = plt.subplots(figsize=(9, 5))
    td_x = list(range(len(td_categories)))
    td_width = 0.35

    td_ax.bar(
        [x - td_width / 2 for x in td_x],
        td_baseline_values,
        width=td_width,
        label="Baseline",
    )
    td_ax.bar(
        [x + td_width / 2 for x in td_x],
        td_adjusted_values,
        width=td_width,
        label="Temperature-adjusted",
    )

    td_ax.set_xticks(td_x)
    td_ax.set_xticklabels(td_categories)
    td_ax.set_ylabel("Power loss (W)")
    td_ax.set_title("Baseline vs. Temperature-Adjusted Losses")
    td_ax.legend()
    td_ax.grid(axis="y", alpha=0.3)

    td_fig.tight_layout()
    st.pyplot(td_fig)
    plt.close(td_fig)

    st.caption(
        "Simplified educational model: only conduction loss changes with "
        "temperature through the assumed linear on-resistance coefficient. "
        "Switching and gate-drive losses remain at their baseline values. "
        "The coefficient is configurable and is not a universal GaN property."
    )

st.divider()
st.header("Electrothermal Frequency Optimization")

st.write(
    "Find the lowest-loss switching frequency while accounting for "
    "temperature-dependent on-resistance and a junction-temperature limit."
)

col1, col2, col3 = st.columns(3)

with col1:
    et_ambient_temp = st.number_input(
        "Ambient temperature (°C)",
        min_value=-40.0,
        max_value=150.0,
        value=25.0,
        step=5.0,
        key="et_ambient_temp",
    )

with col2:
    et_thermal_resistance = st.number_input(
        "Thermal resistance (°C/W)",
        min_value=0.01,
        max_value=100.0,
        value=2.0,
        step=0.1,
        key="et_thermal_resistance",
    )

with col3:
    et_temp_coefficient = st.number_input(
        "RDS(on) temperature coefficient (1/°C)",
        min_value=0.0,
        max_value=0.02,
        value=0.004,
        step=0.001,
        format="%.4f",
        key="et_temp_coefficient",
    )

col4, col5 = st.columns(2)

with col4:
    et_reference_temp = st.number_input(
        "Reference temperature (°C)",
        min_value=-40.0,
        max_value=150.0,
        value=25.0,
        step=5.0,
        key="et_reference_temp",
    )

with col5:
    et_max_temp = st.number_input(
        "Maximum junction temperature (°C)",
        min_value=25.0,
        max_value=250.0,
        value=125.0,
        step=5.0,
        key="et_max_temp",
    )

col6, col7 = st.columns(2)

with col6:
    et_min_frequency = st.number_input(
        "Minimum switching frequency (Hz)",
        min_value=1000.0,
        max_value=1000000.0,
        value=50000.0,
        step=10000.0,
        key="et_min_frequency",
    )

with col7:
    et_max_frequency = st.number_input(
        "Maximum switching frequency (Hz)",
        min_value=1000.0,
        max_value=1000000.0,
        value=300000.0,
        step=10000.0,
        key="et_max_frequency",
    )

et_candidate_count = st.slider(
    "Number of candidate frequencies",
    min_value=3,
    max_value=30,
    value=10,
    key="et_candidate_count",
)

if et_min_frequency >= et_max_frequency:
    st.error("Maximum frequency must be greater than minimum frequency.")
else:
    et_frequencies = [
        float(value)
        for value in __import__("numpy").linspace(
            et_min_frequency,
            et_max_frequency,
            et_candidate_count,
        )
    ]

    try:
        et_result = optimize_electrothermal_frequency(
            base_parameters=parameters,
            frequencies_hz=et_frequencies,
            ambient_temperature_c=float(et_ambient_temp),
            thermal_resistance_c_per_w=float(et_thermal_resistance),
            temperature_coefficient_per_c=float(et_temp_coefficient),
            reference_temperature_c=float(et_reference_temp),
            max_junction_temperature_c=float(et_max_temp),
        )

        st.subheader("Optimization Results")

        metric1, metric2 = st.columns(2)
        metric1.metric(
            "Optimal frequency",
            f"{et_result['optimal_frequency_hz'] / 1000:.2f} kHz",
        )
        metric2.metric(
            "Minimum total loss",
            f"{et_result['minimum_total_loss_w']:.4f} W",
        )

        metric3, metric4 = st.columns(2)
        metric3.metric(
            "Estimated efficiency",
            f"{et_result['estimated_efficiency_percent']:.3f}%",
        )
        metric4.metric(
            "Estimated junction temperature",
            f"{et_result['estimated_junction_temperature_c']:.2f} °C",
        )

        et_results_df = pd.DataFrame(et_result["sweep_results"])

        st.subheader("Frequency vs. Total Loss")
        st.line_chart(
            et_results_df.set_index("frequency_hz")["total_loss_w"]
        )

        st.subheader("Frequency vs. Junction Temperature")
        st.line_chart(
            et_results_df.set_index("frequency_hz")[
                "junction_temperature_c"
            ]
        )

        st.subheader("Candidate Frequency Results")
        st.dataframe(et_results_df, use_container_width=True)

        st.success(
            f"Selected {et_result['optimal_frequency_hz'] / 1000:.2f} kHz "
            "from the temperature-feasible candidates."
        )

    except ValueError as error:
        st.warning(f"Optimization could not be completed: {error}")

st.caption(
    "Educational model: the optimizer iteratively estimates junction "
    "temperature using a fixed thermal resistance and a linear "
    "temperature coefficient for on-resistance. Results depend on the "
    "simplifying assumptions and are not hardware safety guarantees."
)
