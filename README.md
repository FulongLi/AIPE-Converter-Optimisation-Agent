# Cardiff buck VSI optimisation (Python)

Python reimplementation of the **single-phase buck-type VSI** workflow: multi-objective **volume vs. loss** exploration and a small **neural-network surrogate**, matching the intent of the MATLAB scripts `Step1`–`Step3` in the original project folder.

The original repository shipped CVX/SeDuMi but **did not include** `cvx_initialization.m` / `cvx_optimization.m` or `netdata.mat`. Here, **physics-based loss and volume models** are written explicitly in `physics.py`, and the Pareto sweep uses **weighted-sum scalarisation** solved with **SciPy** (`SLSQP`) on the same decision variables used for the ANN in MATLAB (`A_sw`, `f_sw`, `I_ripple`, `ΔT_j`).

## Setup

```bash
cd cardiff_converter_opt
python -m pip install -e ".[dev]"
```

Requires **Python 3.9+**.

## Pareto sweep and plots (Step 2 analogue)

```bash
python -m cardiff_converter_opt
# or after install:
cardiff-pareto --output-dir outputs
```

Produces `pareto_efficiency_vs_power_density.png`, `pie_volume.png`, and `pie_loss.png`.

SLSQP runs on the decision variables mapped to `[0, 1]` within their bounds, so the sweep moves all four together: from 300 kHz / ~96 cm³ / ~38 W at the volume-weighted end to 50 kHz / ~680 cm³ / ~10.5 W at the loss-weighted end. Without this scaling (raw SI units span about ten orders of magnitude) the finite-difference gradients never moved `f_sw` off its 175 kHz start value. `ΔT_j` settles at its lower bound because the heat sink is excluded from the volume (`include_heat_sink_volume=False`).

## Train ANN surrogate (Step 3 analogue)

Runs a fresh Pareto sweep, saves `models/netdata.npz`, and trains an `sklearn` MLP (`15×12×10` hidden units, L2 `alpha=0.01`) with **Min–Max** scaling (MATLAB `mapminmax` analogue).

```bash
python -m cardiff_converter_opt train-ann
cardiff-train-ann --output-dir models
```

## Tests

```bash
pytest
```

## Package layout

| Module | Role |
|--------|------|
| `parameters.py` | Constants from MATLAB `Step2.m` |
| `physics.py` | Semiconductor, inductor, capacitor loss/volume |
| `optimization.py` | Objective normalisation, variable scaling + Pareto loop |
| `cli.py` | Plotting and ANN training entry points |

## Note on fidelity

Numeric results will **not** match MATLAB bit-for-bit because the convex programs were not available to port. Component splits are **calibrated** (switch / inductor / capacitor volumes) toward the published pie-chart scales; losses follow the same coefficient names but with **SI-consistent scaling** on cross-terms.
