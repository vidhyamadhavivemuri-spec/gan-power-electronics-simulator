# GaN Power Electronics Simulator

A Python-based simulation project for exploring **Gallium Nitride (GaN) power devices**, switching losses, converter efficiency, operating-frequency trade-offs, and thermal behavior through numerical models and an interactive dashboard.

## Overview

Gallium Nitride (GaN) is a wide-bandgap semiconductor used in power electronics. Compared with conventional silicon devices, GaN devices can offer faster switching and lower switching-related losses in suitable applications.

This project provides a software-only environment to explore power-device behavior without requiring physical hardware. It combines analytical calculations, numerical simulations, automated tests, and interactive visualizations to help users understand the relationships between electrical losses, switching frequency, and device temperature.

## Project Objectives

- Understand the fundamentals of GaN power electronics.
- Estimate conduction, switching, and gate-drive losses.
- Analyze the effect of switching frequency on power losses.
- Compare illustrative GaN and silicon device parameters.
- Estimate junction temperature using thermal models.
- Explore temperature-dependent resistance and electrothermal feedback.
- Simulate transient temperature response using a first-order thermal RC model.
- Provide an interactive dashboard for experimenting with model inputs.

## Features

| Module | Description |
|---|---|
| Power-loss modeling | Estimates conduction, switching, and gate-drive losses. |
| Waveform generation | Generates illustrative switching waveforms. |
| Frequency sweep | Evaluates losses at multiple switching frequencies. |
| Device comparison | Compares two sets of device parameters representing GaN and silicon. |
| Loss analysis | Identifies the dominant modeled loss component. |
| Frequency optimization | Selects the lowest-loss candidate from the supplied frequency range. |
| Steady-state thermal analysis | Estimates junction temperature from power loss and thermal resistance. |
| Temperature-dependent resistance | Models resistance variation with temperature. |
| Electrothermal analysis | Iteratively estimates coupled resistance, conduction loss, and junction temperature. |
| Transient thermal simulation | Models junction-temperature response over time using a first-order thermal RC model. |
| Interactive dashboard | Provides controls and visualizations through Streamlit. |
| Automated testing | Checks model behavior, input validation, and expected results. |

## Technology Stack

- **Python** — simulation logic and numerical calculations
- **NumPy** — numerical operations
- **Matplotlib** — waveform and analysis plots
- **Streamlit** — interactive dashboard
- **unittest** — automated testing
- **Git and GitHub** — version control and project hosting

## Project Structure

```text
gan-power-electronics-simulator/
├── app/
│   └── dashboard.py
├── docs/
├── examples/
│   ├── plot_waveforms.py
│   └── plot_frequency_sweep.py
├── src/
│   └── gan_simulator/
│       ├── __init__.py
│       ├── parameters.py
│       ├── loss_model.py
│       ├── waveforms.py
│       ├── frequency_sweep.py
│       ├── device_comparison.py
│       ├── loss_analysis.py
│       ├── frequency_optimizer.py
│       ├── thermal_analysis.py
│       ├── temperature_model.py
│       ├── electrothermal.py
│       └── transient_thermal.py
└── tests/
    ├── test_loss_model.py
    ├── test_waveforms.py
    ├── test_frequency_sweep.py
    ├── test_device_comparison.py
    ├── test_loss_analysis.py
    ├── test_frequency_optimizer.py
    ├── test_thermal_analysis.py
    ├── test_temperature_model.py
    ├── test_electrothermal.py
    └── test_transient_thermal.py
```

## Installation and Setup

### Prerequisites

- Python 3.14.7, the version used for development and testing
- Git
- A terminal such as Git Bash
- Visual Studio Code (recommended)

### 1. Clone the repository

```bash
git clone https://github.com/vidhyamadhavivemuri-spec/gan-power-electronics-simulator.git
cd gan-power-electronics-simulator
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

For Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Confirm that `(.venv)` appears in your terminal before installing or running the project.

### 4. Install dependencies

```bash
python -m pip install numpy matplotlib streamlit
```

## Running the Dashboard

From the project root, with the virtual environment activated, run:

```bash
python -m streamlit run app/dashboard.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser to interact with the simulator.

## Running the Tests

Run the complete automated test suite:

```bash
python -m unittest discover -s tests -v
```

**Latest verified result:** 59 tests passed.

The tests cover the implemented loss models, waveform generation, frequency analysis, device comparison, thermal calculations, electrothermal iteration, transient temperature simulation, and input validation.

## Mathematical Models

### 1. Conduction loss

The simplified conduction-loss model is:

\[
P_{\mathrm{cond}} = I^2 R_{\mathrm{DS(on)}}
\]

where:

- \(I\) is the modeled RMS current.
- \(R_{\mathrm{DS(on)}}\) is the on-state resistance.

### 2. Switching loss

The simulator estimates switching loss as:

\[
P_{\mathrm{sw}} =
\frac{1}{2} V I (t_r+t_f) f_s
\]

where:

- \(V\) is the modeled switching voltage.
- \(I\) is the modeled switching current.
- \(t_r\) and \(t_f\) are rise and fall times.
- \(f_s\) is the switching frequency.

### 3. Gate-drive loss

The simplified gate-drive loss is:

\[
P_{\mathrm{gate}} = Q_g V_g f_s
\]

where \(Q_g\) is gate charge and \(V_g\) is gate-drive voltage.

### 4. Total modeled loss

\[
P_{\mathrm{total}} =
P_{\mathrm{cond}}+P_{\mathrm{sw}}+P_{\mathrm{gate}}
\]

The estimated efficiency is calculated as:

\[
\eta =
\frac{P_{\mathrm{out}}}
{P_{\mathrm{out}}+P_{\mathrm{total}}}
\times 100\%
\]

### 5. Steady-state junction temperature

The steady-state thermal estimate is:

\[
T_j = T_a + P_{\mathrm{loss}}R_{\theta}
\]

where \(T_j\) is junction temperature, \(T_a\) is ambient temperature, and \(R_{\theta}\) is the modeled thermal resistance.

### 6. Transient thermal response

The transient thermal module uses a first-order thermal RC model:

\[
T_j(t) = T_{\mathrm{initial}}+
\Delta P R_{\theta}
\left(1-e^{-t/\tau}\right)
\]

where:

\[
\tau=R_{\theta}C_{\theta}
\]

Here, \(\Delta P\) is the modeled change in power dissipation, \(C_{\theta}\) is thermal capacitance, and \(\tau\) is the thermal time constant.

These equations are simplified analytical models intended for learning and exploration, not complete semiconductor-device models.

## Model Assumptions and Limitations

- The simulator is software-only and does not require physical GaN hardware.
- GaN and silicon comparisons depend on the input parameters; they are not universal claims about every device.
- Switching-loss calculations use a simplified voltage-current overlap approximation.
- The loss model does not comprehensively account for reverse conduction, output-capacitance losses, dead time, parasitic inductance, or gate-drive circuit dynamics.
- The steady-state thermal model assumes a fixed thermal resistance.
- The temperature-dependent resistance model uses a simplified linear relationship.
- The electrothermal model uses iterative calculations and simplified electrical and thermal assumptions.
- The transient thermal model uses a first-order RC approximation with constant thermal properties.
- Results have not been established as hardware-validated predictions.

Use the results to understand trends and compare modeled scenarios. Real design decisions require appropriate device datasheets, more complete models, and experimental validation.

## Learning Outcomes

This project provides practical experience with:

- Wide-bandgap semiconductor applications
- Power-electronics loss estimation
- Python modular programming
- Numerical modeling and parameter sweeps
- Thermal analysis and electrothermal feedback
- Data visualization and interactive dashboards
- Unit testing and Git-based development

## Future Improvements

Potential extensions include:

- Datasheet-based parameter extraction for specific GaN and silicon devices
- Output-capacitance and reverse-conduction loss models
- Dead-time and parasitic-effect analysis
- More detailed thermal networks
- Model calibration against manufacturer data or experimental measurements
- Exportable simulation reports and additional comparison plots

## Author

**Vemuri Vidhya Madhavi**

GitHub: [@vidhyamadhavivemuri-spec](https://github.com/vidhyamadhavivemuri-spec)

---

*An educational power-electronics simulation project focused on understanding GaN device losses, switching-frequency trade-offs, and thermal behavior.*
