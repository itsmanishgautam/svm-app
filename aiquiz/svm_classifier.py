import pickle
import pandas as pd
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



model_filename = BASE_DIR/'Data works/SVMmodel.pkl'

with open (model_filename,'rb') as model_file:
    classfier = pickle.load(model_file)



def ModelPredict(data):
    """
    Predicts the class labels for the given data using the classifier.

    Args:
        data (list): The input data for prediction.

    Returns:
        None
    """
    original = data
    if data.get('question_id'):
        print(data.get('question_id'))

    question_id = data.pop('question_id')
    df_test = pd.DataFrame(data)
    predictions = classfier.predict(df_test)
    print("Predictions:", predictions)
    print(question_id)
    # predictions['question_id'] = question_id
    print(type(predictions))
    return predictions,question_id




data = {'AverageTimeTaken': [25, 30, 40],
         'NumAttempts': [5, 8, 12],
         'NumCorrectAttempts': [4, 7, 10]}

# ModelPredict(data)