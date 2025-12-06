import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure parent folder is in Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your GitHub loader
from Data_Inlezen import load_biomechanics_data_from_github


# ---------------------------------------------------------
#                 CONFIGURATION
# ---------------------------------------------------------

GITHUB_RAW_URL = (
    "https://raw.githubusercontent.com/Flovdl/Biomechanica/master/Volledige_Data_Set.xlsx"
)

speed_cols_map = {
    "Max(balsnelheid)(m/s)": "Ball speed",
    "Wrist": "Wrist speed",
    "Elbow": "Elbow speed",
    "Shoulder": "Shoulder speed"
}

cols_for_analysis = list(speed_cols_map.values())


# ---------------------------------------------------------
#                 LOAD DATA FROM GITHUB
# ---------------------------------------------------------

dataframe = load_biomechanics_data_from_github(GITHUB_RAW_URL)

if dataframe.empty:
    raise ValueError("Error: No data loaded from GitHub!")

# Rename columns for analysis
dataframe = dataframe.rename(columns=speed_cols_map)


# ---------------------------------------------------------
#       TAKE MAXIMUM SPEEDS PER TEST (sheet = test)
# ---------------------------------------------------------

max_speeds_df = (
    dataframe.groupby("Sheet_Name")[cols_for_analysis]
    .max()
    .reset_index()
)

# Split sheet names into Person and Technique
split_cols = max_speeds_df["Sheet_Name"].str.split("_", expand=True)
max_speeds_df["Person"] = split_cols[0]
max_speeds_df["Technique"] = split_cols[1]


# ---------------------------------------------------------
#           CREATE SUBSETS FOR EACH PARTICIPANT
# ---------------------------------------------------------

df_elien = max_speeds_df[max_speeds_df["Person"] == "Elien"]
df_yenthe = max_speeds_df[max_speeds_df["Person"] == "Yenthe"]

print(f"Elien Data Points: {len(df_elien)}")
print(f"Yenthe Data Points: {len(df_yenthe)}")


# ---------------------------------------------------------
#                  PLOTTING FUNCTIONS
# ---------------------------------------------------------

def plot_scatter_group(df, person):
    """3 scatter plots per person: Wrist / Elbow / Shoulder vs Ball speed."""
    plt.figure(figsize=(15, 4))
    for i, seg in enumerate(["Wrist speed", "Elbow speed", "Shoulder speed"]):
        plt.subplot(1, 3, i + 1)
        sns.regplot(
            x=df[seg],
            y=df["Ball speed"],
            scatter_kws={"s": 100},
            line_kws={"linewidth": 2}
        )
        plt.title(f"{person}: Ball speed vs {seg} (Max per Test)")
        plt.xlabel(seg)
        plt.ylabel("Ball speed")
    plt.tight_layout()
    plt.show()


def plot_heatmap(df, person):
    """Correlation heatmap for max speeds."""
    plt.figure(figsize=(6, 4))
    sns.heatmap(df[cols_for_analysis].corr(), annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.title(f"{person} Correlation Heatmap (Max Speeds)")
    plt.show()


def plot_person_by_technique(max_df, person):
    """
    Creates a 3x3 grid of scatter plots:
    3 techniques × 3 joint speeds (Wrist, Elbow, Shoulder).
    """
    person_df = max_df[max_df["Person"] == person]
    techniques = person_df["Technique"].unique()

    speeds = ["Wrist speed", "Elbow speed", "Shoulder speed"]

    plt.figure(figsize=(16, 12))

    plot_index = 1
    for tech in techniques:
        tech_df = person_df[person_df["Technique"] == tech]

        for seg in speeds:
            plt.subplot(3, 3, plot_index)
            sns.regplot(
                x=tech_df[seg],
                y=tech_df["Ball speed"],
                scatter_kws={"s": 80},
                line_kws={"linewidth": 2}
            )
            plt.title(f"{person} – {tech}\nBall speed vs {seg}")
            plt.xlabel(seg)
            plt.ylabel("Ball speed")
            plot_index += 1

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
#                   EL I E N ANALYSIS
# ---------------------------------------------------------

plot_scatter_group(df_elien, "Elien")
plot_heatmap(df_elien, "Elien")

print("\n--- Elien correlations with Ball Speed ---")
print(df_elien[cols_for_analysis].corr()["Ball speed"][["Wrist speed", "Elbow speed", "Shoulder speed"]])


# ---------------------------------------------------------
#                   Y E N T H E ANALYSIS
# ---------------------------------------------------------

plot_scatter_group(df_yenthe, "Yenthe")
plot_heatmap(df_yenthe, "Yenthe")

print("\n--- Yenthe correlations with Ball Speed ---")
print(df_yenthe[cols_for_analysis].corr()["Ball speed"][["Wrist speed", "Elbow speed", "Shoulder speed"]])


# ---------------------------------------------------------
#          3 × 3 SCATTER PLOTS (9 PER PERSON)
# ---------------------------------------------------------

plot_person_by_technique(max_speeds_df, "Elien")
plot_person_by_technique(max_speeds_df, "Yenthe")
