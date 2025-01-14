import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the source files
# Replace the file paths with the correct paths to your files
dars_source_file = '/path/to/data_exp_122448-v5_questionnaire-at3h.csv'  # Source DARS data
anhedonic_file = '/path/to/anhedonic_cleaned_data.csv'
non_anhedonic_file = '/path/to/non_anhedonic_cleaned_data.csv'
model_parameters_file = '/path/to/organized_data.csv'  # R-calculated DARS scores with parameters

# Load datasets
dars_data = pd.read_csv(dars_source_file)
anhedonic_data = pd.read_csv(anhedonic_file)
non_anhedonic_data = pd.read_csv(non_anhedonic_file)
model_parameters_data = pd.read_csv(model_parameters_file)

# Step 2: Identify unique participant IDs
# Find participants common to all datasets
unique_ids_anhedonic = set(anhedonic_data['Participant.Public.ID'].unique())
unique_ids_non_anhedonic = set(non_anhedonic_data['Participant.Public.ID'].unique())
unique_ids_dars = set(dars_data['Participant Public ID'].unique())

common_ids = unique_ids_anhedonic.union(unique_ids_non_anhedonic).intersection(unique_ids_dars)

# Step 3: Filter DARS data for these unique participants
dars_data = dars_data[dars_data['Participant Public ID'].isin(common_ids)]

# Step 4: Recode responses in DARS data
response_recode = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4}
dars_data['Recoded_Response'] = dars_data['Response'].map(response_recode)

# Step 5: Define domain mappings and calculate subscores
domain_mappings = {
    'Hobbies': ['DARS-1-quantised', 'DARS-2-quantised', 'DARS-3-quantised', 'DARS-4-quantised'],
    'Food_Drink': ['DARS-5-quantised', 'DARS-6-quantised', 'DARS-7-quantised', 'DARS-8-quantised'],
    'Social_Interaction': ['DARS-9-quantised', 'DARS-10-quantised', 'DARS-11-quantised', 'DARS-12-quantised'],
    'Sensory_Experiences': [
        'DARS-13-quantised', 'DARS-14-quantised', 'DARS-15-quantised', 'DARS-16-quantised', 'DARS-17-quantised'
    ]
}

# Calculate subscores for each domain
subscores = pd.DataFrame({'Participant.Public.ID': list(common_ids)})

for domain, items in domain_mappings.items():
    domain_scores = (
        dars_data[dars_data['Question Key'].isin(items)]
        .groupby('Participant Public ID')['Recoded_Response']
        .sum()
    )
    subscores[domain] = subscores['Participant.Public.ID'].map(domain_scores)

# Step 6: Merge subscores with model parameters and calculate total subscores
merged_data = subscores.merge(model_parameters_data, on='Participant.Public.ID', how='inner')
merged_data['Total_Subscore'] = merged_data[['Hobbies', 'Food_Drink', 'Social_Interaction', 'Sensory_Experiences']].sum(axis=1)

# Save the comparison file
comparison_file_path = '/path/to/dars_comparison_updated.csv'
merged_data.to_csv(comparison_file_path, index=False)
print(f"Comparison file saved to: {comparison_file_path}")

# Step 7: Define subscales and model parameters
subscores_columns = ['Hobbies', 'Food_Drink', 'Social_Interaction', 'Sensory_Experiences']
model_parameters_columns = ['Arew', 'Apun', 'R', 'P']

# Step 8: Calculate correlations for each subscale vs each model parameter
correlation_results = []
for subscore in subscores_columns:
    for parameter in model_parameters_columns:
        # Remove rows with missing data for this pair
        valid_data = merged_data[[subscore, parameter]].dropna()
        # Calculate Pearson correlation and p-value
        r, p = pearsonr(valid_data[subscore], valid_data[parameter])
        correlation_results.append({
            'Subscore': subscore,
            'Parameter': parameter,
            'Correlation': r,
            'p-value': p
        })

# Convert correlation results into a DataFrame
correlation_results_df = pd.DataFrame(correlation_results)

# Step 9: Apply Bonferroni correction for multiple comparisons
# Multiply p-values by the number of tests
correction_factor = len(correlation_results_df)
correlation_results_df['Corrected p-value'] = correlation_results_df['p-value'] * correction_factor
correlation_results_df['Corrected p-value'] = correlation_results_df['Corrected p-value'].clip(upper=1.0)

# Save the correlation results
correlation_results_path = '/path/to/dars_correlation_results.csv'
correlation_results_df.to_csv(correlation_results_path, index=False)
print(f"Correlation results saved to: {correlation_results_path}")

# Step 10: Generate scatter plots with trend lines
for subscore in subscores_columns:
    for parameter in model_parameters_columns:
        plt.figure(figsize=(6, 4))
        sns.scatterplot(data=merged_data, x=subscore, y=parameter, alpha=0.7)
        sns.regplot(data=merged_data, x=subscore, y=parameter, scatter=False, color='red')
        plt.title(f'{subscore} vs {parameter}')
        plt.xlabel(subscore)
        plt.ylabel(parameter)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
