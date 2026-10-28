
# GaN Power Electronics Simulator — Architecture

```mermaid
flowchart TD
    A["User Inputs<br/>Voltage, Current, Frequency"] 
    B["Device Profiles<br/>Illustrative & Datasheet-Based"]
    C["Parameter Validation"]
    D["Power-Loss Model"]
    E["Frequency Sweep & Optimization"]
    F["Thermal Analysis"]
    G["Electrothermal Feedback"]
    H["Streamlit Dashboard"]
    I["Results & Visualizations"]
    J["Automated Test Suite"]

    A --> C
    B --> C
    C --> D
    D --> E
    D --> F
    F --> G
    G --> E
    E --> H
    F --> H
    G --> H
    H --> I
    J -. "Validates calculations" .-> D
    J -. "Validates behavior" .-> F
    J -. "Validates behavior" .-> G
```

## Architecture Overview

- **Inputs:** User-selected operating conditions and device parameters.
- **Device profiles:** Illustrative semiconductor parameters and the GS66508B datasheet-based profile.
- **Simulation engine:** Calculates losses and evaluates frequency and thermal behavior.
- **Electrothermal feedback:** Models interactions between electrical losses and device temperature.
- **Dashboard:** Presents model outputs and comparisons interactively.
- **Automated tests:** Check calculations, validation, and expected model behavior.
