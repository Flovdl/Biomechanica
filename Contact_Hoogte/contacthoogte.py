import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Data_Inlezen import load_biomechanics_data_from_github

GITHUB_RAW_URL = "https://raw.githubusercontent.com/Flovdl/Biomechanica/master/Volledige_Data_Set.xlsx"

# rest of your code unchanged

# Load the data once, so it's ready for any further use in this module
dataframe = load_biomechanics_data_from_github(GITHUB_RAW_URL)

# Select columns
contact_height_table = dataframe[["Contact height (cm)", "Sheet_Name"]]
contact_height_table_clean = contact_height_table.dropna(subset=["Contact height (cm)"])

# Convert to HTML with some basic styling
html_table = contact_height_table_clean.to_html(
    index=False,
    border=1,
    justify="center",
    classes="table"
)

# Add simple CSS to make it look nicer
html_content = f"""
<html>
<head>
    <title>Contact Heights Table</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        table {{ border-collapse: collapse; width: 50%; margin: auto; }}
        th, td {{ border: 1px solid #000; padding: 8px; text-align: center; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h2 style="text-align:center;">Contact Heights with Sheet Names</h2>
    {html_table}
</body>
</html>
"""

# Save to HTML
output_file = "contact_heights_table.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Styled HTML table saved as {output_file}. Open it in a browser.")

import matplotlib.pyplot as plt
import seaborn as sns
from statannotations.Annotator import Annotator
from scipy.stats import ttest_ind  # or use mannwhitneyu if data isn't normal

# Split 'Sheet_Name' into 'Person' and 'Technique'
split_cols = dataframe['Sheet_Name'].str.split('_', expand=True)
dataframe['Person'] = split_cols[0]
dataframe['Technique'] = split_cols[1]

# Create subsets per person
df_elien = dataframe[dataframe['Person'] == 'Elien']
df_yenthe = dataframe[dataframe['Person'] == 'Yenthe']

plt.figure(figsize=(12, 5))

# ---------------------- ELIEN ----------------------
plt.subplot(1, 2, 1)
ax1 = sns.boxplot(x='Technique', y='Contact height (cm)', data=df_elien)
plt.title('Contact Heights - Elien')
plt.xlabel('Technique')
plt.ylabel('Contact height (cm)')

pairs = [(tech1, tech2) for i, tech1 in enumerate(df_elien['Technique'].unique())
         for tech2 in df_elien['Technique'].unique()[i+1:]]

annotator = Annotator(ax1, pairs, data=df_elien,
                      x='Technique', y='Contact height (cm)')
annotator.configure(
    test='t-test_ind',
    text_format='star',
    loc='inside',
    verbose=0
)
annotator.apply_and_annotate()

# ---------------------- YENTHE ----------------------
plt.subplot(1, 2, 2)
ax2 = sns.boxplot(x='Technique', y='Contact height (cm)', data=df_yenthe)
plt.title('Contact Heights - Yenthe')
plt.xlabel('Technique')
plt.ylabel('')

pairs = [(tech1, tech2) for i, tech1 in enumerate(df_yenthe['Technique'].unique())
         for tech2 in df_yenthe['Technique'].unique()[i+1:]]

annotator = Annotator(ax2, pairs, data=df_yenthe,
                      x='Technique', y='Contact height (cm)')
annotator.configure(
    test='t-test_ind',
    text_format='star',
    loc='inside',
    verbose=0
)
annotator.apply_and_annotate()

plt.tight_layout()
plt.show()
