import matplotlib.pyplot as plt
import numpy as np
import os

# Create output directory if it doesn't exist
output_dir = "evaluation"
os.makedirs(output_dir, exist_ok=True)

# Data
epochs = list(range(1, 11))

# 60% Math Patch Model (4k Math / 3k Chat)
train_60 = [2.696, 2.142, 1.983, 1.915, 1.882, 1.86, 1.845, 1.838, 1.832, 1.83]
val_60 = [2.134, 1.424, 1.187, 1.097, 1.051, 1.023, 1.008, 1.0, 0.995, 0.993]

# 40% Math Patch Model (2k Math / 3k Chat)
train_40 = [2.6047, 2.3171, 2.2027, 2.1378, 2.1017, 2.0761, 2.0595, 2.0465, 2.0422, 2.0350]
val_40 = [2.7913, 2.1166, 1.8008, 1.6232, 1.5174, 1.4559, 1.4190, 1.3976, 1.3854, 1.3815]

# 100% Math Patch Model (0 Chat)
train_100 = [5.432, 3.592, 2.148, 1.523, 1.216, 1.048, 0.963, 0.905, 0.876, 0.861]
val_100 = [4.43, 2.423, 1.531, 1.118, 0.922, 0.823, 0.771, 0.739, 0.724, 0.72]

# 1. Plotting Training Loss
plt.figure(figsize=(10, 6))
plt.plot(epochs, train_60, label='60% Math', marker='o', linewidth=2)
plt.plot(epochs, train_40, label='40% Math', marker='s', linewidth=2)
plt.plot(epochs, train_100, label='100% Math', marker='^', linewidth=2, linestyle='--')

plt.title('Training Loss: Math Patch Variations', fontsize=14)
plt.xlabel('Epoch', fontsize=12)
plt.ylabel('Cross-Entropy Loss', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig(os.path.join(output_dir, 'training_loss_comparison.png'), dpi=300)
print(f"Saved training plot to {output_dir}/training_loss_comparison.png")

# 2. Plotting Validation Loss
plt.figure(figsize=(10, 6))
plt.plot(epochs, val_60, label='60% Math', marker='o', linewidth=2)
plt.plot(epochs, val_40, label='40% Math', marker='s', linewidth=2)
plt.plot(epochs, val_100, label='100% Math', marker='^', linewidth=2, linestyle='--')

plt.title('Validation Loss: Math Patch Variations', fontsize=14)
plt.xlabel('Epoch', fontsize=12)
plt.ylabel('Cross-Entropy Loss', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig(os.path.join(output_dir, 'validation_loss_comparison.png'), dpi=300)
print(f"Saved validation plot to {output_dir}/validation_loss_comparison.png")



# Data categories
categories = ['Location', 'Obj. Tracking', 'Pronoun', 'Math', 'Common Sense']
models = ['Baseline', '40% Math', '60% Math', '100% Math']

# Averaged data from 3 runs
data_means = {
    'Baseline': [15.0, 21.7, 6.7, 0.0, 16.7],
    '40% Math': [0.0, 30.0, 11.7, 25.0, 5.0],
    '60% Math': [0.0, 23.3, 6.7, 16.7, 10.0],
    '100% Math': [0.0, 0.0, 0.0, 21.7, 0.0]
}

# Standard Deviations 
data_stds = {
    'Baseline': [0.0, 2.8, 2.8, 0.0, 2.8],
    '40% Math': [0.0, 5.0, 2.8, 5.0, 0.0],
    '60% Math': [0.0, 5.7, 2.8, 11.5, 0.0],
    '100% Math': [0.0, 0.0, 0.0, 10.4, 0.0]
}

x = np.arange(len(categories))
width = 0.2 
fig, ax = plt.subplots(figsize=(12, 7))

# Colors for the "Spectrum"
colors = ['#bdc3c7', '#27ae60', '#f39c12', '#c0392b'] 

for i, model in enumerate(models):
    ax.bar(x + (i - 1.5) * width, data_means[model], width, 
           label=model, color=colors[i], yerr=data_stds[model], 
           capsize=4, alpha=0.9, edgecolor='black', linewidth=0.8)

# Formatting for a scientific presentation
ax.set_ylabel('Mean Accuracy (%)', fontsize=12, fontweight='bold')
ax.set_title('Impact of Training Data Ratios on Logic Accuracy (N=60)', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=11)
ax.legend(title="Model Type", loc='upper right', fontsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.set_ylim(0, 45)

plt.tight_layout()
plt.savefig('evaluation/accuracy_comparison_chart.png', dpi=300)
print("Bar chart saved to evaluation/accuracy_comparison_chart.png")