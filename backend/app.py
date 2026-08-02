# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_sales_predictor_api = Flask("Superkart Sales Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@superkart_sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Superkart Sales Prediction API!"

# Define an endpoint for single property prediction (POST request)
@superkart_sales_predictor_api.post('/v1/superkart')
def predict_superkart_sales():
    """
    This function handles POST requests to the '/v1/superkart' endpoint.
    It expects a JSON payload containing product and store details and returns
    the predicted sales as a JSON response.
    """
    # Get the JSON data from the request body
    request_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': request_data['Product_Weight'],
        'Product_Allocated_Area': request_data['Product_Allocated_Area'],
        'Product_MRP': request_data['Product_MRP'],
        'Store_Age_Years': request_data['Store_Age_Years'],
        'Product_Id_char': request_data['Product_Id_char'],
        'Product_Sugar_Content': request_data['Product_Sugar_Content'],
        'Product_Type_Category': request_data['Product_Type_Category'],
        'Store_Size': request_data['Store_Size'],
        'Store_Location_City_Type': request_data['Store_Location_City_Type'],
        'Store_Type': request_data['Store_Type']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction
    predicted_sales = model.predict(input_data)[0]

    # Convert predicted_sales to Python float
    predicted_sales = round(float(predicted_sales), 2)

    # Return the actual sales
    return jsonify({'Predicted Sales': predicted_sales})


# Define an endpoint for batch prediction (POST request)
@superkart_sales_predictor_api.post('/v1/superkartbatch')
def predict_superkart_sales_batch():
    """
    This function handles POST requests to the '/v1/superkartbatch' endpoint.
    It expects a CSV file containing product details for multiple items
    and returns the predicted sales as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all items in the DataFrame
    predicted_sales = model.predict(input_data).tolist()

    # Format actual prices
    predicted_sales_rounded = [round(float(sales), 2) for sales in predicted_sales]

    # Create a dictionary of predictions with row index as keys
    output_dict = {i: sale for i, sale in enumerate(predicted_sales_rounded)}

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkart_sales_predictor_api.run(debug=True)
