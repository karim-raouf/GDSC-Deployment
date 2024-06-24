from django.shortcuts import render
from django.http import JsonResponse
from tensorflow.keras.models import load_model
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Load the model once
x = pd.read_csv("https://drive.google.com/uc?id=1QxCoxIv-N8YNJxhg6RG-o0Ay7ZtHbv7T").drop(columns=['GPA' , 'StudentID','GradeClass'])
MODEL_PATH = "./nn_model/grade_class_prediction_model.h5"
model = load_model(MODEL_PATH)
scaler = StandardScaler().fit(x)

def predict(params):
    reshaped_params = params.reshape(1, -1)
    reshaped_params = reshaped_params.astype(np.float32)
    scaled_params = scaler.transform(reshaped_params)
    print(scaled_params)
    predictions = model.predict(scaled_params)  
    prediction = np.argmax(predictions)
    return prediction

def homepage(request):
    context = {}
    return render(request, 'deployment/home_page.html', context)

def grade_class_prediction(request):
    if request.method == "POST":
        try:
            # Extract parameters from POST request and convert to float
            params = [
                float(request.POST.get(f'feature{i+1}', 0)) for i in range(12)
            ]
            
            params_array = np.array(params)
            print(params_array)
            prediction_num = predict(params_array)
            print('got there')
            # Map the prediction number to the grade
            prediction = ['A', 'B', 'C', 'D', 'F'][prediction_num]
            
            response_data = {
                'success': True,
                'prediction': prediction
            }
        except Exception as e:
            response_data = {
                'success': False,
                'error': str(e)
            }
    else:
        response_data = {
            'success': False,
            'error': 'Invalid request method'
        }
    
    return JsonResponse(response_data)
