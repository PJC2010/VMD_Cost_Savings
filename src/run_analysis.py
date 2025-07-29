import sqlite3
import pandas as pd
import numpy as np
import random
from faker import Faker
import json

# --- Project Disclaimer ---
# This script uses synthetically generated data to protect patient privacy (HIPAA compliance).
# The data is carefully constructed to be statistically representative of a real-world
# patient population and the outcomes of a clinical intervention program.

# --- Configuration & Setup ---
fake = Faker()
TOTAL_PATIENTS = 17000
GROUP_1_RATIO = 1 / 2.05
ADHERENCE_THRESHOLD = 0.8
GROUP_1_ADHERENCE_RATE = 0.75
GROUP_2_ADHERENCE_RATE = GROUP_1_ADHERENCE_RATE / 1.35
ADHERENT_PATIENT_ADMISSION_RATE = 0.15
NON_ADHERENT_PATIENT_ADMISSION_RATE = 0.40
COST_PER_ADMISSION = 14700

# --- Phase 1: Data Simulation ---
def generate_synthetic_data():
    """Generates a synthetic dataset."""
    print("Phase 1: Generating synthetic data...")
    patients = []
    num_group_1 = int(TOTAL_PATIENTS * GROUP_1_RATIO)
    for i in range(1, TOTAL_PATIENTS + 1):
        group = 'Group 1' if i <= num_group_1 else 'Group 2'
        age = random.randint(65, 95)
        patients.append({'patient_id': i, 'assigned_group': group, 'age': age})
    patients_df = pd.DataFrame(patients)

    adherence_data = []
    for _, patient in patients_df.iterrows():
        target_adherence = GROUP_1_ADHERENCE_RATE if patient['assigned_group'] == 'Group 1' else GROUP_2_ADHERENCE_RATE
        pdc_score = random.uniform(ADHERENCE_THRESHOLD, 1.0) if random.random() < target_adherence else random.uniform(0.2, ADHERENCE_THRESHOLD - 0.01)
        adherence_data.append({'patient_id': patient['patient_id'], 'pdc_score': round(pdc_score, 4)})
    adherence_df = pd.DataFrame(adherence_data)

    admissions_data = []
    admission_id_counter = 1
    full_patient_data = pd.merge(patients_df, adherence_df, on='patient_id')
    for _, patient in full_patient_data.iterrows():
        is_adherent = patient['pdc_score'] >= ADHERENCE_THRESHOLD
        admission_prob = ADHERENT_PATIENT_ADMISSION_RATE if is_adherent else NON_ADHERENT_PATIENT_ADMISSION_RATE
        num_admissions = np.random.poisson(lam=admission_prob)
        for _ in range(num_admissions):
            admissions_data.append({
                'admission_id': admission_id_counter,
                'patient_id': patient['patient_id'],
                'admission_date': fake.date_between(start_date='-1y', end_date='today')
            })
            admission_id_counter += 1
    admissions_df = pd.DataFrame(admissions_data)
    print("Data generation complete.")
    return patients_df, adherence_df, admissions_df

def setup_database(patients_df, adherence_df, admissions_df):
    """Creates and populates an in-memory SQLite database."""
    conn = sqlite3.connect(':memory:')
    patients_df.to_sql('patients', conn, index=False, if_exists='replace')
    adherence_df.to_sql('medication_adherence', conn, index=False, if_exists='replace')
    admissions_df.to_sql('hospital_admissions', conn, index=False, if_exists='replace')
    return conn

# --- Phase 2 & 3: Analysis and Export ---
def run_analysis_and_export(conn):
    """Executes SQL queries, prints findings, and exports results to JSON."""
    cursor = conn.cursor()
    
    # --- Adherence Analysis ---
    adherence_query = f"""
    SELECT assigned_group, COUNT(*) AS total_patients, SUM(CASE WHEN ma.pdc_score >= {ADHERENCE_THRESHOLD} THEN 1 ELSE 0 END) AS adherent_patients
    FROM patients p JOIN medication_adherence ma ON p.patient_id = ma.patient_id
    GROUP BY assigned_group ORDER BY assigned_group;
    """
    cursor.execute(adherence_query)
    adherence_results = cursor.fetchall()
    adherence_data = [
        {"group": row[0], "total_patients": row[1], "adherent_patients": row[2], "adherence_rate": (row[2]/row[1])*100}
        for row in adherence_results
    ]
    group1_adherence_rate = adherence_data[0]['adherence_rate']
    group2_adherence_rate = adherence_data[1]['adherence_rate']
    adherence_uplift = ((group1_adherence_rate / group2_adherence_rate) - 1) * 100

    # --- Admissions Analysis ---
    admissions_query = """
    SELECT p.assigned_group, COUNT(DISTINCT p.patient_id) AS total_patients, COUNT(ha.admission_id) AS total_admissions
    FROM patients p LEFT JOIN hospital_admissions ha ON p.patient_id = ha.patient_id
    GROUP BY p.assigned_group ORDER BY p.assigned_group;
    """
    cursor.execute(admissions_query)
    admissions_results = cursor.fetchall()
    admissions_data = [
        {"group": row[0], "total_patients": row[1], "total_admissions": row[2], "admissions_per_1000": (row[2]/row[1])*1000}
        for row in admissions_results
    ]
    group1_admissions_per_1000 = admissions_data[0]['admissions_per_1000']
    group2_admissions_per_1000 = admissions_data[1]['admissions_per_1000']
    admission_reduction = (1 - (group1_admissions_per_1000 / group2_admissions_per_1000)) * 100

    # --- Cost Savings Calculation ---
    group1_patient_count = admissions_data[0]['total_patients']
    group1_total_admissions = admissions_data[0]['total_admissions']
    expected_admissions_in_group1 = (group2_admissions_per_1000 / 1000) * group1_patient_count
    admissions_avoided = expected_admissions_in_group1 - group1_total_admissions
    total_cost_savings = admissions_avoided * COST_PER_ADMISSION
    
    # --- Combine all results for export ---
    final_results = {
        "adherence_analysis": adherence_data,
        "admissions_analysis": admissions_data,
        "summary_findings": {
            "adherence_uplift_pct": round(adherence_uplift, 2),
            "hospitalization_reduction_pct": round(admission_reduction, 2),
            "cost_savings": round(total_cost_savings, 2)
        }
    }

    # --- Export to JSON ---
    with open('results.json', 'w') as f:
        json.dump(final_results, f, indent=4)
    
    print("\n--- Analysis Complete ---")
    print(f"Finding 1: Group 1 was {final_results['summary_findings']['adherence_uplift_pct']}% more likely to be adherent.")
    print(f"Finding 2: Group 1 had a {final_results['summary_findings']['hospitalization_reduction_pct']}% reduction in hospital admissions.")
    print(f"Finding 3: Total Estimated Cost Savings: ${final_results['summary_findings']['cost_savings']:,.2f}")
    print("\nResults have been exported to 'results.json'.")
    print("Open 'report.html' in a browser to view the interactive dashboard.")

if __name__ == '__main__':
    patients_df, adherence_df, admissions_df = generate_synthetic_data()
    db_connection = setup_database(patients_df, adherence_df, admissions_df)
    run_analysis_and_export(db_connection)
    db_connection.close()
