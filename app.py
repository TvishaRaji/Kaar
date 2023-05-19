import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split as tts
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
api = Api(app)

CORS(app)
ALLOWED_EXTENSIONS = {'csv'}

@api.route('/predict_sales', methods=["POST"])
class PredictSales(Resource):
    def post(self):
        file = request.files['file']
        time_period = request.form['timePeriod']
        
        df = pd.read_csv(file)
        
        # Split dataset into x and y
        x = df.loc[:, ('region', 'value')].values
        y = df.iloc[:, -1].values
        
        # Use LabelEncoder
        lab = LabelEncoder()
        x[:, 0] = lab.fit_transform(x[:, 0])
        x[:, 1] = lab.fit_transform(x[:, 1])
        
        # Split data into train and test dataset
        x_train, x_test, y_train, y_test = tts(x, y, test_size=0.1)
        
        # Create model
        model = LinearRegression()
        model.fit(x_train, y_train)
        
        # Check the accuracy of the model
        y_pred = model.predict(x_test)
        plt.figure(figsize=(8, 6))
        plt.scatter(range(len(y_test)), y_test, color='blue', label='Actual')
        plt.plot(range(len(y_test)), y_pred, color='red', linewidth=2, label='Predicted')
        plt.xlabel('Data Points')
        plt.ylabel('Sales')
        plt.title('Forecasted Sales vs. Actual Sales')
        plt.legend()
        plt.show()
        
        return 'success'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(debug=False, port=5000)
