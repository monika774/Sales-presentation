from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SalesDataSerializer
from .utils import CSVHandler
import os
from django.shortcuts import render

CSV_FILE_PATH = "salesapp/salesdata.csv"

def dash_view(request):
    return render(request, "dash_app.html")

class SaleDataAPIView(APIView):
    def get(self, request):
        """Read sales data."""
        csv_handler = CSVHandler(CSV_FILE_PATH)
        data = csv_handler.read_csv()
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        """Add a new sale data"""
        serializer = SalesDataSerializer(data=request.data)
        if serializer.is_valid():
            csv_handler = CSVHandler(CSV_FILE_PATH)
            data = csv_handler.read_csv()
            data.append(serializer.validated_data)
            csv_handler.write_csv(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SaleDataDetailAPIView(APIView):
    def get(self, request, pk):
        """Read single data by sale"""
        csv_handler = CSVHandler(CSV_FILE_PATH)
        data = csv_handler.read_csv()
        if pk < 0 or pk >= len(data):
            return Response({"detail": "Record not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(data[pk], status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Update a sale data"""
        serializer = SalesDataSerializer(data=request.data)
        if serializer.is_valid():
            csv_handler = CSVHandler(CSV_FILE_PATH)
            data = csv_handler.read_csv()
            if pk < 0 or pk >= len(data):
                return Response({"detail": "Record not found."}, status=status.HTTP_404_NOT_FOUND)
            data[pk] = serializer.validated_data
            csv_handler.write_csv(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a sale data"""
        csv_handler = CSVHandler(CSV_FILE_PATH)
        data = csv_handler.read_csv()
        if pk < 0 or pk >= len(data):
            return Response({"detail": "Record not found."}, status=status.HTTP_404_NOT_FOUND)
        del data[pk]
        csv_handler.write_csv(data)
        return Response({"detail": "Record deleted."}, status=status.HTTP_204_NO_CONTENT)

def get_data():
    try:
        df = pd.read_csv('salesapp/salesdata.csv')
        df.columns = df.columns.str.strip()  # Removing  spaces in column names
        return df
    except FileNotFoundError:
        raise Exception("The sales data file is not found.")
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")


# Descriptive Analysis View
class DescriptiveAnalysis(APIView):
    """   API to perform descriptive analysis on the sales data      """
    def get(self, request):
        try:
            df = get_data()                 
            total_sales = df['sales'].sum()
            average_sales = df['sales'].mean()
            sales_by_region = df.groupby('region')['sales'].sum().to_dict() 
            response_data = {
                "total_sales": total_sales,
                "average_sales": average_sales,
                "sales_by_region": sales_by_region,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Predictive Analysis View
class PredictiveAnalysis(APIView):
    """"API to perform predictive analysis on the sales data. """
    def get(self, request):
        try:
            df = get_data()
            df['date'] = pd.to_datetime(df['date']) 
            df['timestamp'] = df['date'].astype(np.int64) // 10**9  
            X = df[['timestamp']].values
            y = df['sales'].values

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Here i used  Train for  the linear regression model
            model = LinearRegression()
            model.fit(X_train, y_train)

            # Predicted  of the  sales for the next 7 days
            next_day = pd.Timestamp('now') + pd.Timedelta(days=7)
            next_day_timestamp = int(next_day.timestamp())
            prediction = model.predict([[next_day_timestamp]])

            # Prepare response
            return Response({"next_30_days_prediction": prediction[0]}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
