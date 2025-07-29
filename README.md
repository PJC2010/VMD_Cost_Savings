# Portfolio Project: Analyzing the ROI of a Clinical Healthcare Intervention

### A Data-Driven Demonstration of Value for VillageMD's Quality Program (FY 2024)

**Author:** Pete Castillo | www.linkedin.com/in/petecastillo92/ | www.castillopete.com

---

### Interactive Dashboard: Final Report

Below is a preview of the interactive HTML dashboard created to present the final analysis to stakeholders.



![Dashboard Screenshot](https://i.imgur.com/uZLscep.png)

---

### 1. Project Summary & Business Problem

In value-based healthcare, it is critical to demonstrate that clinical initiatives not only improve patient outcomes but also provide a tangible return on investment (ROI). This project simulates and analyzes the effectiveness of a proactive outreach program by the **VillageMD Quality Specialist team**.

The core business question is: **"Does the cost of a dedicated clinical outreach team justify itself through improved patient adherence, reduced hospitalizations, and subsequent cost savings?"**

This analysis serves as a proof-of-concept to answer that question with data. The statistical models for this project are based on de-identified, aggregated data sourced from enterprise systems, including **AthenaHealth EHR** (from Snowflake) and **Salesforce**, to ensure a realistic simulation.

**Technologies Used:**
* **Language:** Python
* **Libraries:** Pandas (Data Manipulation), NumPy (Numerical Operations), Faker (Data Simulation)
* **Database:** SQLite (for SQL-based analysis)
* **Visualization:** HTML, Tailwind CSS, Chart.js

---

### 2. Objectives & Hypotheses

The analysis was designed to validate three key hypotheses for a cohort of ~17,000 Medicare Advantage members over one year:

1.  **Improved Adherence:** The *Intervention Group* (receiving outreach) will show a significantly higher medication adherence rate compared to the *Control Group*.
2.  **Reduced Hospitalizations:** Improved adherence will lead to a measurable reduction in costly inpatient hospital admissions.
3.  **Positive ROI:** The reduction in hospitalizations will result in substantial cost savings, justifying the program's operational expense.

---

### 3. Methodology

The project was executed in four distinct phases:

#### Phase 1: Synthetic Data Generation
To protect patient privacy and comply with HIPAA regulations, a statistically representative dataset was generated using Python. The synthetic data accurately models the real-world population by incorporating patterns and baselines derived from real-world systems.

The model's parameters are based on aggregated, de-identified data sourced from:
* **AthenaHealth EHR**, queried from the `ATHENA_DATAVIEW` table in the company's **Snowflake** data warehouse.
* **Salesforce data**, which tracks patient outreach and engagement activities.

This approach ensures the findings are realistic and reflect the dynamics of the actual patient population without exposing any protected health information (PHI).

#### Phase 2: Database Storage & SQL Analysis
The generated data was loaded into an in-memory **SQLite database**. SQL queries were then used to perform the core analysis, calculating and comparing key metrics between the two groups:
* Medication Adherence Rate (Proportion of Days Covered >= 80%)
* Hospital Admissions per 1,000 Patients (to normalize for population size differences)

#### Phase 3: Cost-Benefit Analysis
The financial impact was calculated by:
1.  Determining the number of **avoided hospital admissions**.
2.  Multiplying this number by the average cost of a Medicare Advantage inpatient stay: **$14,700**. This figure is based on the AHRQ HCUP Statistical Brief #262.

#### Phase 4: Interactive Visualization
The final, aggregated results were exported to a `results.json` file. An **interactive HTML dashboard** consumes this JSON file to present the findings through KPI cards and charts, making the results accessible and understandable for a non-technical audience.

---

### 4. Key Findings & Results

The analysis confirmed all three hypotheses, demonstrating the significant positive impact of the outreach program.

* ✅ **Adherence Uplift: +35.1%**
    * The Intervention Group's adherence rate was **75.0%**, compared to just **55.5%** for the Control Group. This shows the outreach program was highly effective at improving patient behavior.

* ✅ **Hospitalization Reduction: -24.7%**
    * The Intervention Group had **251 admissions per 1,000 patients**, while the Control Group had **333**. This is a statistically significant reduction directly attributable to the program.

* ✅ **Estimated Cost Savings: $1,218,918**
    * The program successfully prevented an estimated **83 hospital admissions**, leading to over **$1.2 million** in avoided healthcare costs for the fiscal year.

---

### 5. How to Run This Project Locally

Follow these steps to replicate the analysis and view the report on your own machine.

1.  **Prerequisites:**
    * Ensure you have Python 3 installed.
    * Clone this repository:
        ```bash
        git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
        cd YOUR_REPOSITORY_NAME
        ```

2.  **Install Dependencies:**
    * Install the required Python libraries from the `src` directory.
        ```bash
        pip install pandas numpy faker
        ```

3.  **Run the Analysis Script:**
    * Execute the Python script. This will simulate the data, run the analysis, and generate the `results.json` file in the project's root directory.
        ```bash
        python src/run_analysis.py
        ```

4.  **View the Interactive Report:**
    * Open the `report.html` file in any web browser to see the final, visualized results.

### Repository Structure
```
├── README.md           # You are here!
├── report.html         # The final, interactive dashboard
├── results.json        # Data output from the Python script, consumed by the report
└── src/
    └── run_analysis.py # The core Python script for simulation and analysis
