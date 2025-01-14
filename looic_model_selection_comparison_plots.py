import matplotlib.pyplot as plt

# Model descriptions and corresponding LOOIC values
models = ['Learning Rate, Reward Sensitivity, Lapse',
          'Learning from Reward/Punishment, Sensitivity',
          'Delta Rule with Lapse',
          'Kalman Filter for Learning',
          'Lapse with Exponential Decay']
looic_values = [801.332, 738.885, 791.991, 774.502, 740.501]

# Subtracting the lowest LOOIC value from all values
min_looic = min(looic_values)
relative_looic = [val - min_looic for val in looic_values]

# Creating horizontal bar plot
plt.figure(figsize=(10, 6))

# Transparent salmon color for all bars
bars = plt.barh(models, relative_looic, color='salmon', alpha=0.7)

# Label the best model (which is the one with relative LOOIC of 0)
best_model_index = relative_looic.index(0)
plt.text(relative_looic[best_model_index] + 5, best_model_index, 'Best Model', 
         va='center', ha='left', fontsize=10, color='black', weight='bold')

# Aesthetic improvements: remove grid lines and axis lines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)

# No grid lines
plt.grid(False)

# Labels and title
plt.xlabel('Relative LOOIC Values')
plt.ylabel('Model Key Parameters')
plt.title('Relative LOOIC Values for Model Selection')

# Highlight the best model's bar with a distinct color (gold)
bars[best_model_index].set_color('#FFD700')

# Invert y-axis to have the best model at the top
plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()
