# GaN Power Electronics Simulator

A Python-based simulation platform for exploring **Gallium Nitride (GaN) power devices**, switching losses, converter efficiency, frequency optimization, and thermal behavior through numerical models and an interactive dashboard.

[![Python](https://img.shields.io/badge/Python-3.14-blue)](https://www.python.org/)
[![Testing](https://img.shields.io/badge/Tests-94%20passing-brightgreen)](#running-the-tests)
[![Platform](https://img.shields.io/badge/Platform-Software--Only-informational)](#model-assumptions-and-limitations)

## Overview

Gallium Nitride (GaN) is a wide-bandgap semiconductor used in high-frequency power electronics. Its switching characteristics can offer advantages over silicon devices in suitable applications.

This project provides a software-only environment for studying power-device losses and thermal behavior without requiring physical hardware. It combines analytical calculations, numerical simulations, automated tests, and an interactive Streamlit dashboard.

The simulator also includes a datasheet-based profile for the **GS66508B GaN transistor**, alongside illustrative device profiles for comparing modeled operating scenarios.

## Project Objectives

- Understand the fundamentals of GaN power electronics.
- Estimate conduction, switching, and gate-drive losses.
- Investigate the effect of switching frequency on power dissipation.
- Compare modeled GaN and silicon device parameters.
- Estimate steady-state and transient junction temperatures.
- Model temperature-dependent on-state resistance.
- Analyze electrothermal feedback between electrical losses and temperature.
- Explore frequency optimization under thermal and loss constraints.
- Provide interactive visualizations for engineering experimentation.

## Features

| Module | Description |
|---|---|
| Power-loss modeling | Estimates conduction, switching, and gate-drive losses. |
| Waveform generation | Generates illustrative switching waveforms. |
| Frequency sweep | Evaluates modeled losses over a range of switching frequencies. |
| Device comparison | Compares device parameter sets under common operating conditions. |
| Device profiles | Supports illustrative devices and a datasheet-based GS66508B profile. |
| Loss analysis | Breaks down losses into modeled components. |
| Frequency optimization | Searches candidate frequencies for a minimum-loss operating point. |
| Steady-state thermal analysis | Estimates junction temperature using thermal resistance. |
| Temperature-dependent resistance | Models resistance variation with temperature. |
| Electrothermal analysis | Iteratively couples resistance, conduction loss, and junction temperature. |
| Transient thermal simulation | Estimates temperature response using a first-order thermal RC model. |
| Frequency-versus-temperature analysis | Explores how switching frequency affects modeled junction temperature. |
| Temperature-dependent losses | Evaluates power losses as device temperature changes. |
| Electrothermal frequency optimization | Evaluates frequency candidates with electrothermal effects. |
| Full electrothermal feedback | Analyzes coupled electrical and thermal behavior. |
| Interactive dashboard | Provides controls, comparisons, metrics, and visualizations through Streamlit. |
| Automated testing | Checks calculations, model behavior, and input validation. |

## Technology Stack

- **Python** — simulation logic and numerical calculations
- **NumPy** — numerical operations
- **Matplotlib** — plots and visualizations
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
│       ├── transient_thermal.py
│       ├── frequency_thermal_analysis.py
│       ├── temperature_dependent_losses.py
│       ├── electrothermal_optimizer.py
│       ├── full_electrothermal.py
│       ├── device_profiles.py
│       └── device_profile_adapter.py
└── tests/
    └── [automated test modules]
```
See [Architecture Diagram](docs/architecture.md) for an overview of the simulator's modules and data flow.
The tree highlights the principal modules; additional files may be present in the repository.

## Installation and Setup

### Prerequisites

- Python 3.14.7, the version used during development
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

If that activation path does not work in your environment, use the activation script appropriate to your shell.

### 4. Install dependencies

```bash
python -m pip install numpy matplotlib streamlit
```

## Running the Dashboard

From the project root, with the virtual environment activated:

```bash
python -m streamlit run app/dashboard.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser to explore the simulator.

The dashboard includes device comparisons, loss breakdowns, frequency analysis, and thermal/electrothermal investigations.

## Running the Tests

Run the complete automated test suite:

```bash
python -m unittest discover -s tests -v
```

**Latest reported result: 94 tests passed.**

This result reflects the project's reported test run; rerun the command to verify the current checkout.

The test suite covers power-loss calculations, waveform generation, frequency analysis, device comparisons, thermal modeling, electrothermal behavior, device profiles, and input validation.

## Mathematical Models

### 1. Conduction loss

The simplified conduction-loss model is:

\[
P_{\mathrm{cond}} = I^2 R_{\mathrm{DS(on)}}
\]

where:

- \(I\) is the modeled current.
- \(R_{\mathrm{DS(on)}}\) is the on-state resistance.

### 2. Switching loss

The switching-loss estimate is:

\[
P_{\mathrm{sw}} =
\frac{1}{2}VI(t_r+t_f)f_s
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

### 5. Estimated efficiency

\[
\eta =
\frac{P_{\mathrm{out}}}
{P_{\mathrm{out}}+P_{\mathrm{total}}}
\times 100\%
\]

This is a simplified estimate based on the losses represented in the model.

### 6. Steady-state junction temperature

\[
T_j = T_a + P_{\mathrm{loss}}R_\theta
\]

where:

- \(T_j\) is junction temperature.
- \(T_a\) is ambient temperature.
- \(P_{\mathrm{loss}}\) is modeled dissipated power.
- \(R_\theta\) is the selected thermal resistance.

### 7. Transient thermal response

The first-order thermal RC model uses:

\[
T_j(t) = T_{\mathrm{initial}}+
\Delta P R_\theta
\left(1-e^{-t/\tau}\right)
\]

with:

\[
\tau=R_\theta C_\theta
\]

where \(\Delta P\) is the modeled change in power dissipation, \(C_\theta\) is thermal capacitance, and \(\tau\) is the thermal time constant.

These equations are simplified analytical approximations. Actual semiconductor behavior can depend on operating conditions, device construction, parasitic effects, and the surrounding circuit.

## Datasheet-Based Device Profile

The simulator includes a profile for the **GS66508B GaN transistor** based on its manufacturer datasheet.

- **Manufacturer reference:** [GS66508B datasheet — Infineon](https://www.infineon.com/dgdl/Infineon-GS66508B-DataSheet-v01_00-EN.pdf?fileId=8ac78c8c8d2fe47b018e5161c92653de)
- **Typical on-state resistance:** 50 mΩ under the specified datasheet conditions.
- **Gate charge:** 6.1 nC under the specified gate-charge test conditions.
- **Rise time:** 3.7 ns under the stated switching test conditions.
- **Fall time:** 5.2 ns under the stated switching test conditions.
- **Gate-drive voltage used in the profile:** 6 V.

The dashboard exposes device-source metadata and test conditions for profiles that include them.

**Important:** These values are associated with particular datasheet test conditions. They should not be treated as universal values for all operating points. The simulator's simplified loss equations do not reproduce every characteristic of the physical device.

Illustrative profiles are clearly distinguished from the datasheet-based profile. Comparisons are meaningful only in the context of their chosen parameters and assumptions.

## Model Assumptions and Limitations

- The simulator is software-only and does not require physical GaN hardware.
- Device comparisons depend on the chosen parameters and are not universal claims about all GaN or silicon devices.
- Switching loss is estimated using a simplified voltage-current overlap approximation.
- The loss model does not comprehensively represent reverse conduction, output-capacitance losses, dead time, parasitic inductance, or gate-driver dynamics.
- Datasheet parameters may vary with voltage, current, temperature, and test setup.
- The steady-state thermal model uses a simplified thermal resistance.
- Temperature-dependent resistance is approximated using a simplified relationship.
- Electrothermal results depend on the assumptions and convergence behavior of the implemented iterative model.
- The transient thermal model uses a first-order RC approximation with simplified thermal properties.
- The project has not been established as a hardware-validated predictor of real-world device performance.

Use the results to understand trends and compare modeled scenarios. Real design decisions require suitable device datasheets, more complete circuit and thermal models, and experimental validation.

## Learning Outcomes

This project provides practical experience with:

- Wide-bandgap semiconductor applications
- Power-electronics loss estimation
- Python modular software design
- Numerical modeling and parameter sweeps
- Thermal analysis and electrothermal feedback
- Interactive visualization with Streamlit
- Automated testing and input validation
- Version control and collaborative engineering practices

## Future Improvements

Potential extensions include:

- More detailed output-capacitance and reverse-conduction loss models
- Dead-time and parasitic-effect analysis
- Advanced multi-node thermal networks
- Model calibration against experimental measurements
- Additional datasheet-backed GaN and silicon profiles
- Exportable simulation reports and comparison plots
- Continuous integration for automated testing

## Author

**Vemuri Vidhya Madhavi**

GitHub: [@vidhyamadhavivemuri-spec](https://github.com/vidhyamadhavivemuri-spec)

---

*An educational power-electronics simulation project focused on understanding GaN device losses, switching-frequency trade-offs, and thermal behavior.*
