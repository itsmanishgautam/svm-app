import numpy as np
import pandas as pd

def generate_mcq_data(num_samples):
    """
    Generate multiple-choice question (MCQ) data for two classes: "Easy" and "Hard".

    Parameters:
    num_samples (int): Number of samples to generate for each class.

    Returns:
    pd.DataFrame: A DataFrame containing the generated MCQ data.

    Example:
    >>> generate_mcq_data(200)
           AverageTimeTaken  NumAttempts  NumCorrectAttempts Label
    0             29.671568            2                   3  Easy
    1             33.812526            3                   4  Easy
    2             47.654152            1                   2  Easy
    3            157.931957            9                   1  Hard
    4            322.654789            7                   0  Hard
    """
    # Set seed for reproducibility
    np.random.seed(42)

    # Generating data for the "Easy" class
    easy_data = {
        'AverageTimeTaken': np.random.uniform(10, 60, num_samples),  # 10 to 60 seconds
        'NumAttempts': np.random.randint(1, 5, num_samples),  # 1 to 4 attempts
        'NumCorrectAttempts': np.random.randint(2, 5, num_samples)  # 2 to 4 correct attempts
    }

    easy_df = pd.DataFrame(easy_data)
    easy_df['Label'] = 'Easy'

    # Generating data for the "Hard" class
    hard_data = {
        'AverageTimeTaken': np.random.uniform(120, 600, num_samples),  # 2 to 10 minutes
        'NumAttempts': np.random.randint(5, 11, num_samples),  # 5 to 10 attempts
        'NumCorrectAttempts': np.random.randint(0, 2, num_samples)  # 0 to 1 correct attempts
    }

    hard_df = pd.DataFrame(hard_data)
    hard_df['Label'] = 'Hard'

    # Combine both datasets
    dataset = pd.concat([easy_df, hard_df], ignore_index=True)

    # Shuffle the dataset
    dataset = dataset.sample(frac=1).reset_index(drop=True)

    return dataset

# Generate MCQ data with 200 samples for each class
mcq_data = generate_mcq_data(200)

# Display the first few rows of the dataset
print(mcq_data.head())

# Save the dataset to a CSV file if needed
mcq_data.to_csv('question_classification_dataset.csv', index=False)
