# MLB Fantasy 2026

Predicting 2026 fantasy baseball points using machine learning on advanced Statcast metrics.

## Approach

- Collect historical stats (2015-2025) and advanced metrics via **pybaseball**
- Train separate **batter** and **pitcher** gradient boosting models on rate stats (Fpoints/PA, Fpoints/IP)
- Scale predictions to totals using external PA/IP projections
- Explain predictions using **SHAP** values
- Interactive **Streamlit** app for exploring individual player predictions

## Scoring (ESPN Points League)

**Batters:** 1/TB, 1/R, 1/RBI, 1/BB, 1/SB, -1/K

**Pitchers:** 3/IP, 1/K, -1/BB, -1/H, -2/ER, 2/W, -2/L, 2/Hold, 5/Save

## Project Structure

```
mlb-fantasy-2026/
├── config/              # Scoring rules and project settings
├── data/
│   ├── raw/             # Raw data from pybaseball
│   ├── processed/       # Cleaned, merged datasets
│   ├── projections/     # External PA/IP projections
│   └── cache/           # pybaseball cache
├── src/
│   ├── data/            # Collection, processing, fantasy points, features
│   ├── models/          # Training, prediction, evaluation
│   ├── utils/           # Name matching, imputation
│   └── viz/             # Plots and SHAP visualizations
├── notebooks/           # Step-by-step workflow notebooks
├── models/              # Saved model artifacts
├── predictions/         # Output rankings
├── app/                 # Streamlit prediction app
└── mlb-book/            # Jupyter Book write-up
```

## Setup

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

1. Run notebooks in order (`notebooks/01_*` through `05_*`)
2. Or use the source modules directly from `src/`
3. Launch the app: `streamlit run app/app.py`

See [PLAN.md](PLAN.md) for the full project plan and task breakdown.
