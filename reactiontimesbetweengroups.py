import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import t

# Load the datasets
data_anhedonic = pd.read_csv('/mnt/data/anhedonic_cleaned_data.csv')
data_non_anhedonic = pd.read_csv('/mnt/data/non_anhedonic_cleaned_data.csv')

# Assign group labels and combine datasets for consistency
data_anhedonic['group'] = 'Anhedonic'
data_non_anhedonic['group'] = 'Non-Anhedonic'
combined_data = pd.concat([data_anhedonic, data_non_anhedonic], ignore_index=True)

# Check sample sizes per group for accurate t-test calculations
n_anhedonic = data_anhedonic['Participant.Public.ID'].nunique()
n_non_anhedonic = data_non_anhedonic['Participant.Public.ID'].nunique()

# Group reaction times by trial number and compute mean and SEM
mean_rt_anhedonic = data_anhedonic.groupby('trial_nr')['rt'].mean()
mean_rt_non_anhedonic = data_non_anhedonic.groupby('trial_nr')['rt'].mean()

anhedonic_sem = data_anhedonic.groupby('trial_nr')['rt'].sem()
non_anhedonic_sem = data_non_anhedonic.groupby('trial_nr')['rt'].sem()

# Convert everything to numpy arrays for plotting
mean_rt_anhedonic_np = mean_rt_anhedonic.to_numpy()
anhedonic_sem_np = anhedonic_sem.to_numpy()

mean_rt_non_anhedonic_np = mean_rt_non_anhedonic.to_numpy()
non_anhedonic_sem_np = non_anhedonic_sem.to_numpy()

# Convert index (trial numbers) to numpy arrays
anhedonic_index_np = mean_rt_anhedonic.index.to_numpy()
non_anhedonic_index_np = mean_rt_non_anhedonic.index.to_numpy()

# Create the plot with shaded SEM regions
plt.figure(figsize=(10, 6))

# Plot reaction times for the Anhedonic group
sns.lineplot(x=anhedonic_index_np, y=mean_rt_anhedonic_np, label='Anhedonic', color='salmon')
plt.fill_between(anhedonic_index_np, 
                 mean_rt_anhedonic_np - anhedonic_sem_np, 
                 mean_rt_anhedonic_np + anhedonic_sem_np, 
                 color='salmon', alpha=0.3)

# Plot reaction times for the Non-Anhedonic group
sns.lineplot(x=non_anhedonic_index_np, y=mean_rt_non_anhedonic_np, label='Non-Anhedonic', color='turquoise')
plt.fill_between(non_anhedonic_index_np, 
                 mean_rt_non_anhedonic_np - non_anhedonic_sem_np, 
                 mean_rt_non_anhedonic_np + non_anhedonic_sem_np, 
                 color='turquoise', alpha=0.3)

# Add labels and title
plt.xlabel('Trial Number')
plt.ylabel('Reaction Time (ms)')
plt.title('Reaction Time Across Trials for Anhedonic and Non-Anhedonic Groups (with Shaded SEM)')
plt.grid(False)  # Remove grid lines for a cleaner look
plt.tight_layout()
plt.show()

# === T-Test Calculation ===

# Calculate the overall mean and standard deviation for each group
mean_anhedonic = data_anhedonic['rt'].mean()
std_anhedonic = data_anhedonic['rt'].std()

mean_non_anhedonic = data_non_anhedonic['rt'].mean()
std_non_anhedonic = data_non_anhedonic['rt'].std()

# Calculate the combined SEM for the t-test
sem_combined = np.sqrt((std_anhedonic**2 / n_anhedonic) + (std_non_anhedonic**2 / n_non_anhedonic))

# Calculate the t-statistic
mean_difference = mean_anhedonic - mean_non_anhedonic
t_statistic = mean_difference / sem_combined

# Calculate degrees of freedom using Welch's approximation
df = ((std_anhedonic**2 / n_anhedonic) + (std_non_anhedonic**2 / n_non_anhedonic))**2 / \
     (((std_anhedonic**2 / n_anhedonic)**2 / (n_anhedonic - 1)) + ((std_non_anhedonic**2 / n_non_anhedonic)**2 / (n_non_anhedonic - 1)))

# Calculate the two-tailed p-value
p_value = 2 * t.cdf(-abs(t_statistic), df)

# Print t-test results
print(f"T-Test Results:")
print(f"Anhedonic Mean: {mean_anhedonic:.2f} ms, SD: {std_anhedonic:.2f} ms, N: {n_anhedonic}")
print(f"Non-Anhedonic Mean: {mean_non_anhedonic:.2f} ms, SD: {std_non_anhedonic:.2f} ms, N: {n_non_anhedonic}")
print(f"T-Statistic: {t_statistic:.2f}, Degrees of Freedom: {df:.2f}, P-Value: {p_value:.4f}")
