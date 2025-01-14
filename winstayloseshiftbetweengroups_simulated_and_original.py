import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Define color schemes
anhedonic_color = 'salmon'  # Anhedonic group remains salmon
non_anhedonic_color = 'turquoise'  # Non-anhedonic group is turquoise

# Define transparency levels
transparency_original = 0.9
transparency_simulated = 0.5

# Function to compute win-stay and lose-shift instances for original data
def compute_strategies(participant_data):
    win_stay_count = 0
    lose_shift_count = 0
    
    for i in range(1, len(participant_data)):
        prev_choice = participant_data.iloc[i-1]["choice"]
        prev_gain = participant_data.iloc[i-1]["gain"]
        prev_loss = participant_data.iloc[i-1]["loss"]
        
        curr_choice = participant_data.iloc[i]["choice"]
        
        # Check for win-stay
        if prev_gain == 1 and prev_loss == 0 and prev_choice == curr_choice:
            win_stay_count += 1
        
        # Check for lose-shift (original data has loss = 1 for lose)
        if prev_gain == 0 and prev_loss == 1 and prev_choice != curr_choice:
            lose_shift_count += 1
    
    return pd.DataFrame({
        "subjID": [participant_data.iloc[0]["Participant.Public.ID"]],
        "win_stay": [win_stay_count],
        "lose_shift": [lose_shift_count]
    })

# Function to compute win-stay and lose-shift for simulated data
def compute_strategies_simulated(participant_data):
    win_stay_count = 0
    lose_shift_count = 0
    
    for i in range(1, len(participant_data)):
        prev_choice = participant_data.iloc[i-1]["choice"]
        prev_gain = participant_data.iloc[i-1]["gain"]
        prev_loss = participant_data.iloc[i-1]["loss"]
        
        curr_choice = participant_data.iloc[i]["choice"]
        
        # Check for win-stay
        if prev_gain == 1 and prev_loss == 0 and prev_choice == curr_choice:
            win_stay_count += 1
        
        # Check for lose-shift (simulated data has loss = -1 for lose)
        if prev_gain == 0 and prev_loss == -1 and prev_choice != curr_choice:
            lose_shift_count += 1
    
    return pd.DataFrame({
        "subjID": [participant_data.iloc[0]["subjID"]],
        "win_stay": [win_stay_count],
        "lose_shift": [lose_shift_count]
    })

# Load original data
data_anhedonic = pd.read_csv('/path/to/anhedonic_cleaned_data.csv')
data_non_anhedonic = pd.read_csv('/path/to/non_anhedonic_cleaned_data.csv')

# Compute strategies for original data
strategies_anhedonic = pd.concat([compute_strategies(participant_data) for _, participant_data in data_anhedonic.groupby('Participant.Public.ID')])
strategies_non_anhedonic = pd.concat([compute_strategies(participant_data) for _, participant_data in data_non_anhedonic.groupby('Participant.Public.ID')])

# Compute percentages for original data
strategies_anhedonic['win_stay_percentage'] = (strategies_anhedonic['win_stay'] / data_anhedonic.groupby('Participant.Public.ID').apply(lambda x: np.sum((x['gain'] == 1) & (x['loss'] == 0))).values) * 100
strategies_anhedonic['lose_shift_percentage'] = (strategies_anhedonic['lose_shift'] / data_anhedonic.groupby('Participant.Public.ID').apply(lambda x: np.sum((x['gain'] == 0) & (x['loss'] == 1))).values) * 100

strategies_non_anhedonic['win_stay_percentage'] = (strategies_non_anhedonic['win_stay'] / data_non_anhedonic.groupby('Participant.Public.ID').apply(lambda x: np.sum((x['gain'] == 1) & (x['loss'] == 0))).values) * 100
strategies_non_anhedonic['lose_shift_percentage'] = (strategies_non_anhedonic['lose_shift'] / data_non_anhedonic.groupby('Participant.Public.ID').apply(lambda x: np.sum((x['gain'] == 0) & (x['loss'] == 1))).values) * 100

# Load simulated data
data_anhedonic_simulated = pd.read_csv('/path/to/anhedonic_simulated_data_combined.csv')
data_non_anhedonic_simulated = pd.read_csv('/path/to/non_anhedonic_simulated_data_combined.csv')

# Compute strategies for simulated data
strategies_anhedonic_simulated = pd.concat([compute_strategies_simulated(participant_data) for _, participant_data in data_anhedonic_simulated.groupby('subjID')])
strategies_non_anhedonic_simulated = pd.concat([compute_strategies_simulated(participant_data) for _, participant_data in data_non_anhedonic_simulated.groupby('subjID')])

# Compute percentages for simulated data
strategies_anhedonic_simulated['win_stay_percentage'] = (strategies_anhedonic_simulated['win_stay'] / data_anhedonic_simulated.groupby('subjID').apply(lambda x: np.sum((x['gain'] == 1) & (x['loss'] == 0))).values) * 100
strategies_anhedonic_simulated['lose_shift_percentage'] = (strategies_anhedonic_simulated['lose_shift'] / data_anhedonic_simulated.groupby('subjID').apply(lambda x: np.sum((x['gain'] == 0) & (x['loss'] == -1))).values) * 100

strategies_non_anhedonic_simulated['win_stay_percentage'] = (strategies_non_anhedonic_simulated['win_stay'] / data_non_anhedonic_simulated.groupby('subjID').apply(lambda x: np.sum((x['gain'] == 1) & (x['loss'] == 0))).values) * 100
strategies_non_anhedonic_simulated['lose_shift_percentage'] = (strategies_non_anhedonic_simulated['lose_shift'] / data_non_anhedonic_simulated.groupby('subjID').apply(lambda x: np.sum((x['gain'] == 0) & (x['loss'] == -1))).values) * 100

# Compute means and errors for original data
means_anhedonic = strategies_anhedonic[['win_stay_percentage', 'lose_shift_percentage']].mean()
errors_anhedonic = strategies_anhedonic[['win_stay_percentage', 'lose_shift_percentage']].std() / np.sqrt(len(strategies_anhedonic))

means_non_anhedonic = strategies_non_anhedonic[['win_stay_percentage', 'lose_shift_percentage']].mean()
errors_non_anhedonic = strategies_non_anhedonic[['win_stay_percentage', 'lose_shift_percentage']].std() / np.sqrt(len(strategies_non_anhedonic))

# Compute means and errors for simulated data
means_anhedonic_simulated = strategies_anhedonic_simulated[['win_stay_percentage', 'lose_shift_percentage']].mean()
errors_anhedonic_simulated = strategies_anhedonic_simulated[['win_stay_percentage', 'lose_shift_percentage']].std() / np.sqrt(len(strategies_anhedonic_simulated))

means_non_anhedonic_simulated = strategies_non_anhedonic_simulated[['win_stay_percentage', 'lose_shift_percentage']].mean()
errors_non_anhedonic_simulated = strategies_non_anhedonic_simulated[['win_stay_percentage', 'lose_shift_percentage']].std() / np.sqrt(len(strategies_non_anhedonic_simulated))

# Plot original data with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Subplot 1: Win-Stay for original data
bars1 = ax1.bar(['Anhedonic', 'Non-Anhedonic'], 
                [means_anhedonic['win_stay_percentage'], means_non_anhedonic['win_stay_percentage']], 
                yerr=[errors_anhedonic['win_stay_percentage'], errors_non_anhedonic['win_stay_percentage']], 
                capsize=5, color=[anhedonic_color, non_anhedonic_color], alpha=transparency_original)
ax1.set_ylim([0, 100])
ax1.set_ylabel('Win-Stay Percentage')
ax1.set_title('Original Data')
ax1.grid(False)

# Subplot 2: Lose-Shift for original data
bars2 = ax2.bar(['Anhedonic', 'Non-Anhedonic'], 
                [means_anhedonic['lose_shift_percentage'], means_non_anhedonic['lose_shift_percentage']], 
                yerr=[errors_anhedonic['lose_shift_percentage'], errors_non_anhedonic['lose_shift_percentage']], 
                capsize=5, color=[anhedonic_color, non_anhedonic_color], alpha=transparency_original)
ax2.set_ylim([0, 100])
ax2.set_ylabel('Lose-Shift Percentage')
ax2.grid(False)

plt.tight_layout()
plt.show()

# Plot simulated data with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6

# Subplot 1: Win-Stay for simulated data
bars1 = ax1.bar(['Anhedonic', 'Non-Anhedonic'], 
                [means_anhedonic_simulated['win_stay_percentage'], means_non_anhedonic_simulated['win_stay_percentage']], 
                yerr=[errors_anhedonic_simulated['win_stay_percentage'], errors_non_anhedonic_simulated['win_stay_percentage']], 
                capsize=5, color=[anhedonic_color, non_anhedonic_color], alpha=transparency_simulated)
ax1.set_ylim([0, 100])
ax1.set_ylabel('Win-Stay Percentage')
ax1.set_title('Simulated Data')
ax1.grid(False)

# Subplot 2: Lose-Shift for simulated data
bars2 = ax2.bar(['Anhedonic', 'Non-Anhedonic'], 
                [means_anhedonic_simulated['lose_shift_percentage'], means_non_anhedonic_simulated['lose_shift_percentage']], 
                yerr=[errors_anhedonic_simulated['lose_shift_percentage'], errors_non_anhedonic_simulated['lose_shift_percentage']], 
                capsize=5, color=[anhedonic_color, non_anhedonic_color], alpha=transparency_simulated)
ax2.set_ylim([0, 100])
ax2.set_ylabel('Lose-Shift Percentage')
ax2.grid(False)

plt.tight_layout()
plt.show()