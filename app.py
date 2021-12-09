import os

from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

PAPER_FOLDER = os.path.join('static', 'paper')
app.config['UPLOAD_FOLDER'] = PAPER_FOLDER


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


standard_to = StandardScaler()


@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/model', methods=['GET'])
def car():
    return render_template('model.html')


@app.route('/vehicle_price_prediction.pdf', methods=['GET'])
def paper():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'vehicle_price_prediction.pdf')
    print(full_filename)
    return render_template("paper.html", pdf=full_filename)


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Present_Price = Present_Price * 59.00 / 100000
        Kms_Driven = int(request.form['Kms_Driven'])
        Kms_Driven2 = np.log(Kms_Driven)
        Owner = request.form['Owner']
        if Owner == "Zero":
            Owner = 0
        elif Owner == "One":
            Owner = 1
        else:
            Owner = 2
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if Fuel_Type_Petrol == 'Petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        Year = 2021 - Year
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if Seller_Type_Individual == 'Individual':
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_Mannual = request.form['Transmission_Mannual']
        if Transmission_Mannual == 'Manual':
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0
        prediction = model.predict([[Present_Price, Kms_Driven2, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol,
                                     Seller_Type_Individual, Transmission_Mannual]])
        output = round(prediction[0], 2)
        output = output * 100000 * 0.017
        output = round(output, 2)
        if output < 0:
            return render_template('predict.html', prediction_texts="Sorry, you cannot sell or buy this car.")
        else:
            return render_template('predict.html',
                                   prediction_text="You can sell or buy this vehicle at {} CAD.".format(output))
    else:
        return render_template('predict.html')


if __name__ == "__main__":
    app.run(debug=True)
