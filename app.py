from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load('Models/DecisionTree_Regressor_HousePricePrediction.pkl')

model_columns = joblib.load('Models/model_columns.pkl')

locations = joblib.load("Data/locations_list.pkl")

@app.route('/')
def home():
    return render_template('index.html',location=locations)


@app.route('/predict', methods=['POST'])
def predict():
    rate_persqft = float(request.form['rate'])
    area_insqft = float(request.form['area'])
    title = request.form['title']
    location = request.form['location']
    building_status = request.form['building_status']

    data = pd.DataFrame({
        'rate_persqft': [rate_persqft],
        'area_insqft': [area_insqft],
        'title': [title],
        'location': [location],
        'building_status': [building_status]
    })

    data = pd.get_dummies(
        data,
        columns=['title', 'location', 'building_status'],
        dtype=int
    )

    data = data.reindex(
        columns=model_columns,
        fill_value=0
    )

    prediction = model.predict(data)[0]

    return render_template(
        'index.html',
        prediction_text=f'Predicted House Price: ₹ {prediction:.2f} Lakhs',
        location=locations
    )


if __name__ == '__main__':
    app.run(debug=True)