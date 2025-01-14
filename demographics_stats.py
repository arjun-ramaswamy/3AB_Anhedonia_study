# Running the provided Python code to verify results and display updated summaries

# Re-import necessary libraries
import pandas as pd
import numpy as np
import ace_tools as tools  # Custom tool for displaying DataFrames to user

# Load the first file
file_path_1 = '/mnt/data/participant_details_questionnaire.csv'
data_1 = pd.read_csv(file_path_1)

# Load the second file
file_path_2 = '/mnt/data/organized_data.csv'
data_2 = pd.read_csv(file_path_2)

# Filter participants with realistic ages (18+) in the first file
age_data_1 = data_1[data_1['Question Key'] == 'demographic_age']['Response'].dropna().astype(float)
filtered_age_data_1 = age_data_1[age_data_1 >= 18]

# Calculate rounded Age statistics for 1,000 participants
age_range_1 = (int(filtered_age_data_1.min()), int(filtered_age_data_1.max()))
age_mean_1 = round(filtered_age_data_1.mean(), 1)
age_sd_1 = round(filtered_age_data_1.std(), 1)

# Sex, Ethnicity, and Education breakdowns for 1,000 participants
sex_data_1 = data_1[data_1['Question Key'] == 'demographic_sex']['Response'].dropna()
ethnicity_data_1 = data_1[data_1['Question Key'] == 'demographic_ethnicity']['Response'].dropna()
education_data_1 = data_1[data_1['Question Key'] == 'demographic_education']['Response'].dropna()

# Raw counts and percentages for first file
sex_counts_1 = sex_data_1.value_counts()
ethnicity_counts_1 = ethnicity_data_1.value_counts()
education_counts_1 = education_data_1.value_counts()

sex_percentage_1 = (sex_counts_1 / sex_counts_1.sum() * 100).round(0).astype(int)
ethnicity_percentage_1 = (ethnicity_counts_1 / ethnicity_counts_1.sum() * 100).round(0).astype(int)
education_percentage_1 = (education_counts_1 / education_counts_1.sum() * 100).round(0).astype(int)

# Display demographic summary for 1,000 participants
demographic_summary_1 = pd.DataFrame({
    'Metric': ['Age Range', 'Mean Age (SD)', 'Male', 'Female', 'Other', *ethnicity_counts_1.index, *education_counts_1.index],
    'Count': [
        '---', '---', *sex_counts_1.values, *ethnicity_counts_1.values, *education_counts_1.values
    ],
    'Percentage': [
        f"{age_range_1[0]} - {age_range_1[1]}", 
        f"{age_mean_1} ({age_sd_1})",
        *sex_percentage_1.values, *ethnicity_percentage_1.values, *education_percentage_1.values
    ]
})

tools.display_dataframe_to_user(name="Demographic Summary for All Participants (1000)", dataframe=demographic_summary_1)

# Filter for 206 selected participants in the first file
selected_participants_data = data_1[data_1['Participant Public ID'].isin(data_2['Participant.Public.ID'])]

# Age statistics for selected participants
selected_age_data = selected_participants_data[selected_participants_data['Question Key'] == 'demographic_age']['Response'].dropna().astype(float)
selected_age_range = (int(selected_age_data.min()), int(selected_age_data.max()))
selected_age_mean = round(selected_age_data.mean(), 1)
selected_age_sd = round(selected_age_data.std(), 1)

# Sex, Ethnicity, and Education breakdowns for selected participants
selected_sex_data = selected_participants_data[selected_participants_data['Question Key'] == 'demographic_sex']['Response'].dropna()
selected_ethnicity_data = selected_participants_data[selected_participants_data['Question Key'] == 'demographic_ethnicity']['Response'].dropna()
selected_education_data = selected_participants_data[selected_participants_data['Question Key'] == 'demographic_education']['Response'].dropna()

# Raw counts and percentages for selected participants
selected_sex_counts = selected_sex_data.value_counts()
selected_ethnicity_counts = selected_ethnicity_data.value_counts()
selected_education_counts = selected_education_data.value_counts()

selected_sex_percentage = (selected_sex_counts / selected_sex_counts.sum() * 100).round(0).astype(int)
selected_ethnicity_percentage = (selected_ethnicity_counts / selected_ethnicity_counts.sum() * 100).round(0).astype(int)
selected_education_percentage = (selected_education_counts / selected_education_counts.sum() * 100).round(0).astype(int)

# Display demographic summary for selected participants
demographic_summary_selected = pd.DataFrame({
    'Metric': ['Age Range', 'Mean Age (SD)', 'Male', 'Female', 'Other', *selected_ethnicity_counts.index, *selected_education_counts.index],
    'Count': [
        '---', '---', *selected_sex_counts.values, *selected_ethnicity_counts.values, *selected_education_counts.values
    ],
    'Percentage': [
        f"{selected_age_range[0]} - {selected_age_range[1]}", 
        f"{selected_age_mean} ({selected_age_sd})",
        *selected_sex_percentage.values, *selected_ethnicity_percentage.values, *selected_education_percentage.values
    ]
})

tools.display_dataframe_to_user(name="Demographic Summary for Selected Participants (206)", dataframe=demographic_summary_selected)

