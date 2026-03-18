# MLB Fantasy 2026

[![Deploy Jupyter Book](https://github.com/mcgillies/mlb-fantasy-2026/actions/workflows/deploy-book.yml/badge.svg)](https://github.com/mcgillies/mlb-fantasy-2026/actions/workflows/deploy-book.yml)

**[Read the Write-Up](https://mcgillies.github.io/mlb-fantasy-2026/)** | **[Interactive Rankings App](https://mgfantasyranks2026.streamlit.app/)**

---

Machine learning-based fantasy baseball projections using advanced Statcast metrics.

## Customizing Scoring

All scoring rules are configurable in the `config/` folder. Modify these files to match your league settings, then re-run the workflow.

### `config/scoring.py` - Fantasy Point Values

**Batter Stats:**
- `TB` - Total Bases
- `R` - Runs
- `RBI` - Runs Batted In
- `BB` - Walks
- `SB` - Stolen Bases
- `K` - Strikeouts

**Pitcher Stats (Skill-Based):**
- `IP` - Innings Pitched
- `K` - Strikeouts
- `BB` - Walks
- `H` - Hits
- `ER` - Earned Runs

**Pitcher Stats (Team-Dependent):**
- `W` - Wins
- `L` - Losses
- `SV` - Saves
- `HLD` - Holds

### `config/roster.py` - League Settings

- `LEAGUE_SIZE` - Number of teams
- `ROSTER_SLOTS` - Position slots per team (C, 1B, 2B, 3B, SS, OF, DH, P)
- `RP_PER_TEAM` - Assumed RP slots for PAR calculation

### `config/settings.py` - Data Settings

- `TRAIN_START_YEAR` / `TRAIN_END_YEAR` - Historical data range
- `MIN_PA_BATTER` / `MIN_IP_PITCHER` - Minimum thresholds for training data
- `MIN_PA_PREDICT` / `MIN_IP_PREDICT` - Minimum thresholds for prediction candidates

## Environment Setup

```bash
# Clone the repository
git clone https://github.com/mcgillies/mlb-fantasy-2026.git
cd mlb-fantasy-2026

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Workflow

After modifying scoring settings, re-run the notebooks in order:

```bash
# Run notebooks sequentially
jupyter execute notebooks/01_data_collection.ipynb
jupyter execute notebooks/02_data_processing.ipynb
jupyter execute notebooks/03_batter_model.ipynb
jupyter execute notebooks/04_pitcher_model.ipynb
jupyter execute notebooks/05_2026_predictions.ipynb
```

Or open each notebook in Jupyter and run manually:

```bash
jupyter notebook
```

Then navigate to `notebooks/` and run `01_*` through `05_*` in order.

## Launch the App

```bash
streamlit run app/app.py
```
