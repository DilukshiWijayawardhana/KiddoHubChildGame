import csv
import random

# Define knowledge levels
knowledge_levels = ["Best", "Good", "Medium", "Need More Learn"]

# Function to categorize learning level based on input data
def categorize_learning_level(quiz1, quiz2, quiz3, knowledge):
    if knowledge == "Best":
        if quiz1 >= 4 and quiz2 >= 8 and quiz3 >= 12:
            return "Best"
        else:
            return "Good"
    elif knowledge == "Good":
        if quiz1 >= 3 and quiz2 >= 6 and quiz3 >= 10:
            return "Good"
        else:
            return "Medium"
    elif knowledge == "Medium":
        if quiz1 >= 2 and quiz2 >= 4 and quiz3 >= 8:
            return "Medium"
        else:
            return "Need More Learn"
    else:
        return "Need More Learn"

# Generate dataset
data = []
for _ in range(100):
    quiz1 = random.randint(1, 5)
    quiz2 = random.randint(1, 10)
    quiz3 = random.randint(1, 15)
    knowledge = random.choice(knowledge_levels)
    learn_level = categorize_learning_level(quiz1, quiz2, quiz3, knowledge)
    data.append([quiz1, quiz2, quiz3, knowledge, learn_level])

# Write data to CSV file
with open('learning_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Quiz 1", "Quiz 2", "Quiz 3", "Knowledge", "Learn Level"])
    writer.writerows(data)

print("CSV file generated successfully!")
