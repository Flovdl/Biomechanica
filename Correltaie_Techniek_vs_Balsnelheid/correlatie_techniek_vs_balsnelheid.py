# ---------------------------------------------------------
# correlatie_techniek_vs_balsnelheid_boxplot_significance.py
# ---------------------------------------------------------

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from scipy.stats import ttest_ind

# Ensure parent folder is in Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Data_Inlezen import load_biomechanics_data_from_github

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Flovdl/Biomechanica/master/Volledige_Data_Set.xlsx"

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
df = load_biomechanics_data_from_github(GITHUB_RAW_URL)
if df.empty:
    raise ValueError("Dataset failed to load. Stopping execution.")

# Rename columns for consistency
df = df.rename(columns={
    "Max(balsnelheid)(m/s)": "Ball speed",
    "Contact height (cm)": "Contact height",
    "Wrist": "Wrist speed",
    "Elbow": "Elbow speed",
    "Shoulder": "Shoulder speed"
})

# ---------------------------------------------------------
# CALCULATE MAX BALL SPEED & CONTACT HEIGHT PER SHEET
# ---------------------------------------------------------
max_speeds_df = df.groupby("Sheet_Name").agg({
    "Ball speed": "max",
    "Contact height": "max"
}).reset_index()

# Split Sheet_Name to Person and Technique
split_cols = max_speeds_df["Sheet_Name"].str.split("_", expand=True)
max_speeds_df["Person"] = split_cols[0]
max_speeds_df["Technique"] = split_cols[1]

# ---------------------------------------------------------
# PLOTTING FUNCTION: BOX + SCATTER + SIGNIFICANCE
# ---------------------------------------------------------
def plot_technique_vs_variable_box_significance(df, person, variable, ylabel, alpha=0.05):
    """
    Plots variable per Technique for a single person using a box plot with scatter points
    and annotates statistical significance (t-test) between techniques.
    """
    person_df = df[df["Person"] == person][["Technique", variable]]
    
    plt.figure(figsize=(8, 5))
    
    # Boxplot
    sns.boxplot(x="Technique", y=variable, data=person_df, palette="viridis", showfliers=False)
    # Scatter points
    sns.stripplot(x="Technique", y=variable, data=person_df, color="black", size=8, jitter=True)
    
    # Statistical significance (pairwise t-tests)
    techniques = person_df["Technique"].unique()
    combs = list(combinations(techniques, 2))
    y_max = person_df[variable].max()
    y_min = person_df[variable].min()
    height = y_max - y_min
    
    for i, (tech1, tech2) in enumerate(combs):
        data1 = person_df[person_df["Technique"] == tech1][variable]
        data2 = person_df[person_df["Technique"] == tech2][variable]
        t_stat, p_val = ttest_ind(data1, data2)
        
        # Draw significance if p < alpha
        if p_val < alpha:
            x1, x2 = techniques.tolist().index(tech1), techniques.tolist().index(tech2)
            y = y_max + height*0.05*(i+1)
            plt.plot([x1, x1, x2, x2], [y, y+height*0.02, y+height*0.02, y], lw=1.5, c='black')
            plt.text((x1+x2)/2, y+height*0.02, "*", ha='center', va='bottom', color='black', fontsize=14)
    
    plt.title(f"{person}: {ylabel} per Technique")
    plt.ylabel(ylabel)
    plt.xlabel("Technique")
    plt.show()


# ---------------------------------------------------------
# PLOT 4 GRAPHS WITH SIGNIFICANCE
# ---------------------------------------------------------
# EL I E N
plot_technique_vs_variable_box_significance(max_speeds_df, "Elien", "Ball speed", "Max Ball Speed (m/s)")
plot_technique_vs_variable_box_significance(max_speeds_df, "Elien", "Contact height", "Contact Height (cm)")

# Y E N T H E
plot_technique_vs_variable_box_significance(max_speeds_df, "Yenthe", "Ball speed", "Max Ball Speed (m/s)")
plot_technique_vs_variable_box_significance(max_speeds_df, "Yenthe", "Contact height", "Contact Height (cm)")
