from Data_Inlezen import load_biomechanics_data_from_github

# URL to the raw Excel file in your GitHub repo
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Flovdl/Biomechanica/master/Volledige_Data_Set.xlsx"

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

