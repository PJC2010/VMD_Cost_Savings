# VillageMD: Adherence Program Impact Analysis

This repository contains the analysis and visualization for a project demonstrating the impact of a clinical outreach program on medication adherence and hospitalization rates for a Medicare Advantage population. This project is part of the **VillageMD Quality Specialist team's efforts for fiscal year 2024**.

## Key Findings

-   **35.1% Increase in Adherence:** The intervention group was significantly more likely to remain adherent to their medications.
-   **24.7% Reduction in Hospitalizations:** The program led to a substantial decrease in the rate of inpatient admissions.
-   **$1.2M in Cost Savings:** The reduction in hospitalizations translated to an estimated $1,218,918 in avoided healthcare costs.

## How to Run This Project

1.  **Prerequisites:** Ensure you have Python 3 and pandas installed.
    ```bash
    pip install pandas numpy faker
    ```
2.  **Run the Analysis:** Execute the Python script to generate the data and analysis results. This will create/update the `results.json` file.
    ```bash
    python src/run_analysis.py
    ```
3.  **View the Report:** Open the `report.html` file in your web browser to see the interactive dashboard with the latest results.

## Project Structure

-   `/src/run_analysis.py`: Python script for data simulation and analysis.
-   `results.json`: Aggregated data output from the Python script.
-   `report.html`: Interactive HTML dashboard for visualizing the results.

3. Create a .gitignore File
It's good practice to have a .gitignore file. For a simple Python project, it might look like this:

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/

# System files
.DS_Store
