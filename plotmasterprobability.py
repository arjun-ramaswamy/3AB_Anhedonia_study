import scipy.io
import matplotlib.pyplot as plt

# Load the .mat file
file_path = '/mnt/data/master_prob_new.mat'
mat_data = scipy.io.loadmat(file_path)

# Extract the 'master_money_prob' and 'master_pain_prob' data
master_money_prob = mat_data['master_money_prob']
master_pain_prob = mat_data['master_pain_prob']

# Define standard green and red base colors for win and loss
standard_green = (0/255, 128/255, 0/255)  # Standard green base
standard_red = (255/255, 0/255, 0/255)  # Standard red base

# Function to darken colors while staying within valid RGB range
def darken_color(color, factor=0.1):
    return tuple(max(0, c - factor) for c in color)

# Create shades of standard green and red by adjusting brightness
win_shades_standard = [darken_color(standard_green, factor=i * 0.2) for i in range(3)]
loss_shades_standard = [darken_color(standard_red, factor=i * 0.2) for i in range(3)]

# Function to remove y-axis tick lines but keep ticks
def customize_ticks(ax):
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_visible(False)  # Hide the y-axis line
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_linewidth(1)  # Keep x-axis line visible
    ax.tick_params(axis='y', length=0)  # Keep the y-axis ticks, but remove the lines

# Plotting and saving the Master Money Probability plot with standard green shades
plt.figure(figsize=(10, 6))
ax = plt.gca()
for i in range(3):
    plt.plot(master_money_prob[i, :200], label=f'Arm {i+1}', color=win_shades_standard[i])

# Customize the plot for win
plt.xlabel('Trials')
plt.ylabel('Win Probability')
customize_ticks(ax)  # Apply the tick customization
plt.grid(False)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout(rect=[0, 0, 0.85, 1])

# Save the plot as a PNG file
money_prob_path_standard = '/mnt/data/master_money_probability_standard.png'
plt.savefig(money_prob_path_standard)

# Plotting and saving the Master Pain Probability plot with standard red shades
plt.figure(figsize=(10, 6))
ax = plt.gca()
for i in range(3):
    plt.plot(master_pain_prob[i, :200], label=f'Arm {i+1}', color=loss_shades_standard[i])

# Customize the plot for loss
plt.xlabel('Trials')
plt.ylabel('Loss Probability')
customize_ticks(ax)  # Apply the tick customization
plt.grid(False)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout(rect=[0, 0, 0.85, 1])

# Save the plot as a PNG file
pain_prob_path_standard = '/mnt/data/master_pain_probability_standard.png'
plt.savefig(pain_prob_path_standard)

# Output the file paths
print(f'Money Probability Plot saved to: {money_prob_path_standard}')
print(f'Pain Probability Plot saved to: {pain_prob_path_standard}')
