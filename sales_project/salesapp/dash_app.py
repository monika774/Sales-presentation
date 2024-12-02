import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from django.conf import settings
import os
from django_plotly_dash import DjangoDash
import dash
import dash_core_components as dcc
import dash_html_components as html


def get_data():
    file_path = os.path.join(settings.BASE_DIR, '\salesapp\salesdata.csv')
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip() 
    return df

df = get_data()
app = DjangoDash('SalesDashboard')
app.layout = html.Div([
    html.H1("Sales Dashboard"),
    dcc.Graph(id="total_sales_graph"),
    dcc.Graph(id="sales_by_region_graph"),
    dcc.Graph(id="sales_trend_graph")
])

@app.callback(
    Output("total_sales_graph", "figure"),
    Output("sales_by_region_graph", "figure"),
    Output("sales_trend_graph", "figure")
)
def update_graphs():
    total_sales = df['sales'].sum()
    total_sales_graph = {
        'data': [{
            'x': ['Total Sales'],
            'y': [total_sales],
            'type': 'bar',
            'name': 'Total Sales'
        }],
        'layout': {
            'title': 'Total Sales'
        }
    }

    # here i write logic for the sale by region 
    sales_by_region = df.groupby('region')['sales'].sum().reset_index()
    sales_by_region_graph = px.bar(sales_by_region, x='region', y='sales', title="Sales by Region")

    # sale by the date
    df['date'] = pd.to_datetime(df['date'])
    sales_trend = df.groupby('date')['sales'].sum().reset_index()
    sales_trend_graph = px.line(sales_trend, x='date', y='sales', title="Sales Trend Over Time")

    return total_sales_graph, sales_by_region_graph, sales_trend_graph

dash_app = DjangoDash('DashboardApp', app) 

if __name__ == '__main__': 
    app.run_server()  