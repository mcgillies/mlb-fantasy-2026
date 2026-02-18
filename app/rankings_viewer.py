"""
Streamlit app to visualize MLB Fantasy 2026 Master Rankings.

Run with: streamlit run app/rankings_viewer.py
"""

import streamlit as st
import pandas as pd
import os

# Page config
st.set_page_config(
    page_title="MLB Fantasy 2026 Rankings",
    page_icon="⚾",
    layout="wide"
)

st.title("⚾ MLB Fantasy 2026 Rankings")

# Column rename mapping for display
COLUMN_RENAMES = {
    "ML_Raw_Rank": "Non-Adjusted ML Rank",
    "ML_PAR_Rank": "Adjusted ML Rank",
    "Proj_Raw_Rank": "FanGraphs Raw Rank",
    "Proj_PAR_Rank": "Adjusted FanGraphs Rank",
    "ESPN_Rank": "ESPN Rank",
    "Projected_Fpoints": "ML Projected Fpoints",
    "Avg_Proj_Fpts": "FanGraphs Projected Fpoints",
    "ML_PAR": "ML PAR",
    "Proj_PAR": "FanGraphs PAR",
}

# Reverse mapping for internal use
COLUMN_RENAMES_REV = {v: k for k, v in COLUMN_RENAMES.items()}

# Load master rankings
@st.cache_data
def load_rankings():
    file_path = "predictions/master_rankings_2026.csv"
    if not os.path.exists(file_path):
        # Try relative to app directory
        file_path = "../predictions/master_rankings_2026.csv"
    if not os.path.exists(file_path):
        st.error("Master rankings file not found. Run notebook 05 first.")
        return None
    df = pd.read_csv(file_path)
    return df

df = load_rankings()

if df is not None:
    # Sidebar filters
    st.sidebar.header("Filters")

    # Player search
    search = st.sidebar.text_input("Search Player Name", "")

    # Position filter
    all_positions = ["All"]
    if "Position" in df.columns:
        # Extract unique positions (handle multi-position like "2B/SS")
        positions = set()
        for pos in df["Position"].dropna().unique():
            for p in str(pos).split("/"):
                positions.add(p.strip())
        all_positions += sorted(positions)

    selected_position = st.sidebar.selectbox("Filter by Position", all_positions)

    # Type filter (Batter/SP/RP)
    if "Type" in df.columns:
        types = ["All"] + sorted(df["Type"].dropna().unique().tolist())
        selected_type = st.sidebar.selectbox("Filter by Type", types)
    else:
        selected_type = "All"

    # Apply filters
    filtered_df = df.copy()

    # Search filter
    if search:
        filtered_df = filtered_df[
            filtered_df["Name"].str.contains(search, case=False, na=False)
        ]

    # Position filter
    if selected_position != "All":
        filtered_df = filtered_df[
            filtered_df["Position"].str.contains(selected_position, case=False, na=False)
        ]

    # Type filter
    if selected_type != "All":
        filtered_df = filtered_df[filtered_df["Type"] == selected_type]

    # Display stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Players", len(filtered_df))
    col2.metric("Batters", len(filtered_df[filtered_df["Type"] == "Batter"]))
    col3.metric("Starting Pitchers", len(filtered_df[filtered_df["Type"] == "SP"]))
    col4.metric("Relief Pitchers", len(filtered_df[filtered_df["Type"] == "RP"]))

    # Column selection
    st.sidebar.header("Columns")
    available_cols = df.columns.tolist()
    # Remove Type from available columns
    available_cols = [c for c in available_cols if c != "Type"]

    default_cols = ["ML_Raw_Rank", "ML_PAR_Rank", "Proj_Raw_Rank", "Proj_PAR_Rank", "ESPN_Rank",
                    "Name", "Team", "Position", "Projected_Fpoints", "Avg_Proj_Fpts"]
    default_cols = [c for c in default_cols if c in available_cols]

    # Create display names for multiselect
    available_display = [COLUMN_RENAMES.get(c, c) for c in available_cols]
    default_display = [COLUMN_RENAMES.get(c, c) for c in default_cols]

    selected_display = st.sidebar.multiselect(
        "Select Columns to Display",
        available_display,
        default=default_display
    )

    # Convert back to internal column names
    selected_cols = [COLUMN_RENAMES_REV.get(c, c) for c in selected_display]

    if not selected_cols:
        selected_cols = default_cols

    # Sort options
    st.sidebar.header("Sort")
    sort_display = [COLUMN_RENAMES.get(c, c) for c in selected_cols]
    sort_col_display = st.sidebar.selectbox("Sort by", sort_display, index=0)
    sort_col = COLUMN_RENAMES_REV.get(sort_col_display, sort_col_display)
    sort_order = st.sidebar.radio("Order", ["Ascending", "Descending"])

    # Apply sort
    filtered_df = filtered_df.sort_values(
        sort_col,
        ascending=(sort_order == "Ascending"),
        na_position="last"
    )

    # Display table
    st.subheader(f"Rankings ({len(filtered_df)} players)")

    # Format numeric columns
    display_df = filtered_df[selected_cols].copy()

    # Round float columns for display
    for col in display_df.select_dtypes(include=['float64']).columns:
        if 'Rank' in col:
            display_df[col] = display_df[col].fillna(-1).astype(int).replace(-1, None)
        else:
            display_df[col] = display_df[col].round(1)

    # Rename columns for display
    display_df = display_df.rename(columns=COLUMN_RENAMES)

    st.dataframe(
        display_df,
        use_container_width=True,
        height=600,
        hide_index=True
    )

    # Download button
    download_df = filtered_df[selected_cols].copy()
    download_df = download_df.rename(columns=COLUMN_RENAMES)
    csv = download_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_rankings.csv",
        mime="text/csv"
    )

    # Comparison section
    st.subheader("Quick Comparison")
    st.write("Compare ranking systems for top players:")

    comparison_cols = ["Name", "Position", "ML_Raw_Rank", "ML_PAR_Rank", "Proj_Raw_Rank", "Proj_PAR_Rank", "ESPN_Rank"]
    comparison_cols = [c for c in comparison_cols if c in df.columns]

    top_n = st.slider("Show top N players", 10, 100, 30)

    comparison_df = filtered_df.head(top_n)[comparison_cols].copy()

    # Add rank difference columns
    if "ML_PAR_Rank" in comparison_df.columns and "ESPN_Rank" in comparison_df.columns:
        comparison_df["Adjusted ML vs ESPN"] = comparison_df["ESPN_Rank"] - comparison_df["ML_PAR_Rank"]
    if "Proj_PAR_Rank" in comparison_df.columns and "ESPN_Rank" in comparison_df.columns:
        comparison_df["Adjusted FG vs ESPN"] = comparison_df["ESPN_Rank"] - comparison_df["Proj_PAR_Rank"]

    # Rename columns for display
    comparison_df = comparison_df.rename(columns=COLUMN_RENAMES)

    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
