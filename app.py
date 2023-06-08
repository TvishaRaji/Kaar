import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)
api = Api(app)

CORS(app)
ALLOWED_EXTENSIONS = {'csv'}

@api.route('/predict_sales', methods=["POST"])
class PredictSales(Resource):
    def post(self):
        file = request.files['file']
        
        # Read the CSV file
        df = pd.read_csv(file, parse_dates=['Date'], index_col='Date')
        
        # Preprocess the data
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df.values.reshape(-1, 1))
        
        # Define the input parameters for the LSTM model
        n_input = 12
        n_features = 1
        
        generator = TimeseriesGenerator(scaled_data, scaled_data, length=n_input, batch_size=1)
        
        model = Sequential()
        model.add(LSTM(100, activation='relu', input_shape=(n_input, n_features)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        model.fit(generator, epochs=50)
        
        time_period = int(request.form['timePeriod'])
        forecast_generator = TimeseriesGenerator(scaled_data, scaled_data, length=n_input, batch_size=1)
        forecast = model.predict(forecast_generator)
        forecast = forecast.flatten()[-time_period:]
        forecast = scaler.inverse_transform(forecast.reshape(-1, 1)).flatten()
        
        # Plot the forecast
        fig, ax = plt.subplots(figsize=(12, 6)) 
        
        forecast_dates = pd.date_range(start=df.index[-1], periods=time_period, freq='M')
        
        
        start_date = pd.to_datetime('1974-01-01')
        end_date = forecast_dates[-1]
        x_ticks = pd.date_range(start=start_date, end=end_date, freq='M')
        x_tick_labels = [date.strftime('%b %Y') for date in x_ticks]

        actual_data = df.loc[df.index >= start_date]
        ax.plot(actual_data.index, actual_data.values, label='Actual')

        forecast_data = pd.Series(forecast, index=forecast_dates)
        forecast_data = forecast_data.loc[forecast_data.index >= start_date]

        last_actual_date = actual_data.index[-1]
        last_actual_value = actual_data.values[-1]
        forecast_data = pd.concat([pd.Series(last_actual_value, index=[last_actual_date]), forecast_data])

        ax.plot(forecast_data.index, forecast_data.values, label='Forecast')

        ax.set_xlabel('Date')
        ax.set_ylabel('Sales')
        ax.set_title('Sales Forecast')
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_tick_labels, rotation='vertical')
        ax.legend()
        plt.tight_layout() 
        plt.show()
        
        return 'success'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(debug=False, port=5000)