from svm_classifier import ModelPredict

data = {
    'question_id':[1,2,3],
    'AverageTimeTaken': [25, 100, 40],
         'NumAttempts': [5, 8, 12],
         'NumCorrectAttempts': [4, 2, 10]}

ModelPredict(data)