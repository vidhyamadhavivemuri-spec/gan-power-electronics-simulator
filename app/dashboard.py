from pathlib import Path
import sys

import matplotlib.pyplot as plt
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.gan_simulator.device_comparison import compare_devices
from src.gan_simulator.loss_model import calculate_losses
from src.gan_simulator.parameters import SwitchingParameters


st.set_page_config(
    page_title="GaN Power Electronics Simulator",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ GaN Power Electronics Simulator")
st.write(
    "Explore how operating conditions affect estimated transistor "
    "losses and efficiency using a simplified engineering model."
)

st.sidebar.header("Operating Parameters")

voltage_v = st.sidebar.slider(
    "Drain-source voltage (V)", 50, 650, 400, step=10
)
current_a = st.sidebar.slider(
    "RMS current (A)", 1, 40, 10
)
frequency_khz = st.sidebar.slider(
    "Switching frequency (kHz)", 10, 500, 100, step=10
)
rds_on_mohm = st.sidebar.slider(
    "On-resistance (mΩ)", 5, 200, 50, step=5
)
rise_time_ns = st.sidebar.slider(
    "Rise time (ns)", 5, 200, 20, step=5
)
fall_time_ns = st.sidebar.slider(
    "Fall time (ns)", 5, 200, 20, step=5
)
gate_charge_nc = st.sidebar.slider(
    "Gate charge (nC)", 1, 100, 10
)
gate_voltage_v = st.sidebar.slider(
    "Gate-drive voltage (V)", 3.0, 10.0, 5.0, step=0.5
)
output_power_w = st.sidebar.number_input(
    "Output power (W)",
    min_value=1.0,
    max_value=100_000.0,
    value=500.0,
    step=50.0,
)

parameters = SwitchingParameters(
    voltage_v=float(voltage_v),
    current_a=float(current_a),
    frequency_hz=float(frequency_khz * 1000),
    rds_on_ohm=rds_on_mohm / 1000,
    rise_time_s=rise_time_ns * 1e-9,
    fall_time_s=fall_time_ns * 1e-9,
    gate_charge_c=gate_charge_nc * 1e-9,
    gate_voltage_v=gate_voltage_v,
    output_power_w=float(output_power_w),
)

results = calculate_losses(parameters)

st.subheader("Simulation Results")

col1, col2, col3 = st.columns(3)
col1.metric("Total transistor loss", f"{results['total_loss_w']:.3f} W")
col2.metric("Switching loss", f"{results['switching_loss_w']:.3f} W")
col3.metric(
    "Estimated efficiency",
    f"{results['estimated_efficiency_percent']:.2f}%",
)

st.subheader("Power Loss Breakdown")

loss_labels = [
    "Conduction",
    "Switching",
    "Gate drive",
]
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
            f"{results['conduction_loss_w']:.6f} W",
            f"{results['switching_loss_w']:.6f} W",
            f"{results['gate_drive_loss_w']:.6f} W",
            f"{results['total_loss_w']:.6f} W",
            f"{results['estimated_efficiency_percent']:.4f}%",
        ],
    },
    hide_index=True,
    use_container_width=True,
)

st.info(
    "Educational model only: estimates assume simplified hard switching "
    "and do not include temperature effects, output-capacitance losses, "
    "reverse conduction, dead time, or parasitic effects. "
    "Estimated efficiency uses output power plus modeled transistor losses."
)
st.divider()

st.header("⚡ GaN vs. Silicon Comparison")

st.write(
    "Compare two illustrative device parameter sets under the same "
    "operating conditions. These are assumptions, not measured "
    "specifications for particular transistors."
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
    st.metric("Total modeled loss", f"{gan['total_loss_w']:.3f} W")
    st.metric(
        "Estimated efficiency",
        f"{gan['estimated_efficiency_percent']:.2f}%",
    )

with col2:
    st.subheader("Silicon — Illustrative Parameters")
    st.metric("Total modeled loss", f"{silicon['total_loss_w']:.3f} W")
    st.metric(
        "Estimated efficiency",
        f"{silicon['estimated_efficiency_percent']:.2f}%",
    )

st.subheader("Loss Comparison")

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
    [i - width / 2 for i in x],
    gan_losses,
    width,
    label="GaN",
)
comparison_ax.bar(
    [i + width / 2 for i in x],
    silicon_losses,
    width,
    label="Silicon",
)

comparison_ax.set_xticks(list(x))
comparison_ax.set_xticklabels(labels)
comparison_ax.set_ylabel("Modeled power loss (W)")
comparison_ax.legend()
comparison_ax.grid(axis="y", alpha=0.3)

comparison_fig.tight_layout()
st.pyplot(comparison_fig)
plt.close(comparison_fig)

