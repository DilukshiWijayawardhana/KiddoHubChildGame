import numpy as np
import pandas as pd

np.random.seed(42)  # Set seed for reproducibility

# Generate synthetic data for 100 samples
num_samples = 1000
game_scores_level1 = np.random.randint(1, 6, size=num_samples)
game_scores_level2 = np.random.randint(1, 6, size=num_samples)
game_scores_level3 = np.random.randint(1, 6, size=num_samples)

# Create a DataFrame
df = pd.DataFrame({
    'Game_Level1_Score': game_scores_level1,
    'Game_Level2_Score': game_scores_level2,
    'Game_Level3_Score': game_scores_level3
})

# Define a function to determine knowledge level based on scores
def determine_knowledge_level(row):
    total_score = row['Game_Level1_Score'] + row['Game_Level2_Score'] + row['Game_Level3_Score']
    if total_score >= 13:
        return 'Best'
    elif total_score >= 10:
        return 'Good'
    elif total_score >= 6:
        return 'Medium'
    else:
        return 'Need More Learn'

# Apply the function to create the 'Knowledge_Level' column
df['Knowledge_Level'] = df.apply(determine_knowledge_level, axis=1)

# Save the DataFrame to a CSV file
df.to_csv('child_knowledge_dataset.csv', index=False)

print("CSV file 'child_knowledge_dataset.csv' has been saved.")
