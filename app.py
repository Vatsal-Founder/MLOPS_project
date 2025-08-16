from flask import Flask, render_template, request, redirect, url_for
import os
import numpy as np
from src.MLOPS.pipeline.prediction_pipeline import PredictionPipeline

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    message = request.args.get('message')
    # Support showing a prediction on main page if passed in query (optional)
    prediction = request.args.get('prediction')
    return render_template('index.html', message=message, prediction=prediction)

@app.route('/train', methods=['GET'])
def train():
    os.system('python main.py')
    # Redirect back to home with success message
    return redirect(url_for('home', message='Training Successful...'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        fixed_acidity = float(request.form['fixed_acidity'])
        volatile_acidity = float(request.form['volatile_acidity'])
        citric_acid = float(request.form['citric_acid'])
        residual_sugar = float(request.form['residual_sugar'])
        chlorides = float(request.form['chlorides'])
        free_sulfur_dioxide = float(request.form['free_sulfur_dioxide'])
        total_sulfur_dioxide = float(request.form['total_sulfur_dioxide'])
        density = float(request.form['density'])
        pH = float(request.form['pH'])
        sulphates = float(request.form['sulphates'])
        alcohol = float(request.form['alcohol'])

        data = [fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
                chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density,
                pH, sulphates, alcohol]
        data = np.array(data).reshape(1, 11)

        obj = PredictionPipeline()
        pred = obj.predict(data)

        # Render main page with prediction displayed below the buttons
        return render_template('index.html', prediction=str(pred))

    except Exception as e:
        print('The Exception message is:', e)
        # Show a friendly error on the main page
        return render_template('index.html', error_message='Something went wrong while predicting. Please check inputs and try again.')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)