import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from scipy import stats
import ace_tools as tools

# Load data
data_anhedonic = pd.read_csv('/mnt/data/anhedonic_cleaned_data.csv')
data_non_anhedonic = pd.read_csv('/mnt/data/non_anhedonic_cleaned_data.csv')

# Function to compute win-stay and lose-shift instances
def compute_strategies(participant_data):
    win_stay_count = 0
    lose_shift_count = 0
    total_win_cases = np.sum((participant_data['gain'] == 1) & (participant_data['loss'] == 0))
    total_loss_cases = np.sum((participant_data['gain'] == 0) & (participant_data['loss'] == 1))
    
    for i in range(1, len(participant_data)):
        prev_choice = participant_data.iloc[i-1]["choice"]
        prev_gain = participant_data.iloc[i-1]["gain"]
        prev_loss = participant_data.iloc[i-1]["loss"]
        curr_choice = participant_data.iloc[i]["choice"]
        
        # Check for win-stay
        if prev_gain == 1 and prev_loss == 0 and prev_choice == curr_choice:
            win_stay_count += 1
        
        # Check for lose-shift
        if prev_gain == 0 and prev_loss == 1 and prev_choice != curr_choice:
            lose_shift_count += 1

    return pd.DataFrame({
        "Participant.Public.ID": [participant_data.iloc[0]["Participant.Public.ID"]],
        "win_stay": [win_stay_count],
        "lose_shift": [lose_shift_count],
        "total_win_cases": [total_win_cases],
        "total_loss_cases": [total_loss_cases]
    })

# Compute strategies for each participant in both groups
strategies_anhedonic = pd.concat([compute_strategies(participant_data) for _, participant_data in data_anhedonic.groupby('Participant.Public.ID')])
strategies_non_anhedonic = pd.concat([compute_strategies(participant_data) for _, participant_data in data_non_anhedonic.groupby('Participant.Public.ID')])

# Calculate win-stay and lose-shift percentages
strategies_anhedonic['win_stay_percentage'] = (strategies_anhedonic['win_stay'] / strategies_anhedonic['total_win_cases']) * 100
strategies_anhedonic['lose_shift_percentage'] = (strategies_anhedonic['lose_shift'] / strategies_anhedonic['total_loss_cases']) * 100

strategies_non_anhedonic['win_stay_percentage'] = (strategies_non_anhedonic['win_stay'] / strategies_non_anhedonic['total_win_cases']) * 100
strategies_non_anhedonic['lose_shift_percentage'] = (strategies_non_anhedonic['lose_shift'] / strategies_non_anhedonic['total_loss_cases']) * 100

# Compute means and standard errors
means_anhedonic = strategies_anhedonic[['win_stay_percentage', 'lose_shift_percentage']].mean()
errors_anhedonic = strategies_anhedonic[['win_stay_percentage', 'lose_shift_percentage']].std() / np.sqrt(len(strategies_anhedonic))

means_non_anhedonic = strategies_non_anhedonic[['win_stay_percentage', 'lose_shift_percentage']].mean()
errors_non_anhedonic = strategies_non_anhedonic[['win_stay_percentage', 'lose_shift_percentage']].std() / np.sqrt(len(strategies_non_anhedonic))

# Perform Welch's t-tests between the win-stay and lose-shift strategies for both groups
win_stay_ttest = ttest_ind(strategies_anhedonic['win_stay_percentage'], strategies_non_anhedonic['win_stay_percentage'], equal_var=False)
lose_shift_ttest = ttest_ind(strategies_anhedonic['lose_shift_percentage'], strategies_non_anhedonic['lose_shift_percentage'], equal_var=False)

# Summary results with updated Welch's t-test
summary_table = pd.DataFrame({
    "Strategy": ["Win-Stay", "Lose-Shift"],
    "Anhedonic Mean (SD)": [f"{means_anhedonic['win_stay_percentage']:.2f} ({errors_anhedonic['win_stay_percentage']:.2f})",
                             f"{means_anhedonic['lose_shift_percentage']:.2f} ({errors_anhedonic['lose_shift_percentage']:.2f})"],
    "Non-Anhedonic Mean (SD)": [f"{means_non_anhedonic['win_stay_percentage']:.2f} ({errors_non_anhedonic['win_stay_percentage']:.2f})",
                                 f"{means_non_anhedonic['lose_shift_percentage']:.2f} ({errors_non_anhedonic['lose_shift_percentage']:.2f})"],
    "t Statistic": [win_stay_ttest.statistic, lose_shift_ttest.statistic],
    "p-value": [win_stay_ttest.pvalue, lose_shift_ttest.pvalue]
})

# Display summary table to user
tools.display_dataframe_to_user(name="Win-Stay and Lose-Shift Strategy Comparisons (Welch's Test)", dataframe=summary_table)

# Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Colors for each group
anhedonic_color = 'salmon'
non_anhedonic_color = 'turquoise'

# Plot win-stay percentages for both groups
bars1 = ax1.bar(['Anhedonic', 'Non-Anhedonic'], 
                [means_anhedonic['win_stay_percentage'], means_non_anhedonic['win_stay_percentage']], 
                yerr=[errors_anhedonic['win_stay_percentage'], errors_non_anhedonic['win_stay_percentage']], 
                capsize=5, color=[anhedonic_color, non_anhedonic_color], alpha=0.7)
ax1.set_ylim([0, 100])
ax1.set_ylabel('Win-Stay Percentage')
ax1.set_title('Win-Stay Comparison Group Means')
ax1.legend(bars1, ['Anhedonic', 'Non-Anhedonic'], loc='upper right')
ax1.grid(False)

# Plot lose-shift percentages for both groups
bars2 = ax2.bar(['Anhedonic', 'Non-Anhedonic'], 
                [means_anhedonic['lose_shift_percentage'], means_non_anhedonic['lose_shift_percentage']], 
                yerr=[errors_anhedonic['lose_shift_percentage'], errors_non_anhedonic['lose_shift_percentage']], 
                capsize=5, color=[anhedonic_color, non_anhedonic_color], alpha=0.7)
ax2.set_ylim([0, 100])
ax2.set_ylabel('Lose-Shift Percentage')
ax2.set_title('Lose-Shift Comparison Group Means')
ax2.legend(bars2, ['Anhedonic', 'Non-Anhedonic'], loc='upper right')
ax2.grid(False)

# Adjust layout and display plot
plt.tight_layout()
plt.show()

