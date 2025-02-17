import dash
from dash import html, dcc, Input, Output, State, register_page, callback
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import yfinance as yf
from dash.exceptions import PreventUpdate
import numpy as np
from datetime import datetime

# Register page
register_page(__name__, name="Data", path='/data')

# List of stocks
STOCKS = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS', 'AAPL', 
          'MSFT', 'GOOGL', 'AMZN', 'FB', 'AARTIIND.NS', 'ABB.NS', 'ABBOTINDIA.NS']

layout = html.Div([
    # Header
    html.Header([
        html.Div([
            html.H1("", className="header-title"),
        ], className="header-left"),
        
      dcc.Dropdown(
        id='stock-selector',
        options=[{'label': stock, 'value': stock} for stock in STOCKS],
        value='RELIANCE.NS',
        placeholder="Select Stock",
        style={
            'width': '100%',  # Make the dropdown responsive
            'max-width': '600px',  # Limit the maximum width for better presentation
            'margin': '0 auto',  # Center the dropdown horizontally
            'padding': '10px',  # Add padding for better click area
            'border-radius': '5px',  # Rounded corners for a modern look
            'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',  # Subtle shadow effect
            'background-color': '#f7f7f7',  # Light background for better contrast
            'font-family': 'Arial, sans-serif',  # Clean font
            'font-size': '14px',  # Font size for readability
            'border': '1px solid #ccc',  # Light border for clarity
            'cursor': 'pointer',  # Pointer cursor for better UX
        }
    )

            
    ], className="header"),

      

      # Main Content
    html.Main([
        # Quick Stats Section
        html.Div([
            html.Div([
                html.Span("Current Price :", className="card-label"),
                html.Span(id='current-price', className="card-value"),
                html.Span(id='price-change', className="card-change", style={'marginLeft': '10px'})
            ], className="metric-card"),
            
            html.Div([
                html.Span("Market Cap :", className="card-label"),
                html.Span(id='market-cap', className="card-value")
            ], className="metric-card"),
            
            html.Div([
                html.Span("P/E Ratio :", className="card-label"),
                html.Span(id='pe-ratio', className="card-value")
            ], className="metric-card"),
            
            html.Div([
                html.Span("24h Volume :", className="card-label"),
                html.Span(id='volume', className="card-value")
            ], className="metric-card"),
        ], className="metrics-grid"),
        # Charts Section
        html.Div([
            html.Div([
                html.H2("Price Analysis", className="chart-title"),
                dcc.Graph(id='price-chart', className="chart-content")
            ], className="chart-card full-width"),
            
            html.Div([
                html.Div([
                    html.H2("Volume Analysis", className="chart-title"),
                    dcc.Graph(id='volume-chart', className="chart-content")
                ], className="chart-card"),
                
                html.Div([
                    html.H2("Technical Indicators", className="chart-title"),
                    dcc.Graph(id='technical-indicators', className="chart-content")
                ], className="chart-card")
            ], className="chart-container split"),
        ], className="charts-section"),
        
        # Tabs Section
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Financial Metrics', children=[
                    html.Div(id='financial-metrics', className="tab-content")
                ]),
                
                dcc.Tab(label='Trading Statistics', children=[
                    html.Div(id='trading-stats', className="tab-content")
                ])
            ])
        ], className="tabs-section"),
    ], className="main-content"),
    
   
    
    # Interval component for updates
    dcc.Interval(
        id='interval-component',
        interval=60 * 1000,  # Interval in milliseconds (60 seconds)
        n_intervals=0
    )
], className="app-container")


# Callback to update all components
@callback(
    [Output('current-price', 'children'),
     Output('market-cap', 'children'),
     Output('pe-ratio', 'children'),
     Output('volume', 'children'),
     Output('price-chart', 'figure'),
     Output('volume-chart', 'figure'),
     Output('technical-indicators', 'figure'),
     Output('financial-metrics', 'children'),
     Output('trading-stats', 'children')],
    [Input('stock-selector', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_metrics(selected_stock, n):
    # Fetch stock data
    stock = yf.Ticker(selected_stock)
    hist = stock.history(period="1y")
    
    # Calculate metrics
    current_price = hist['Close'].iloc[-1]
    market_cap = stock.info.get('marketCap', 'N/A')
    pe_ratio = stock.info.get('trailingPE', 'N/A')
    volume = hist['Volume'].iloc[-1]
    
    # Create price chart
    price_fig = go.Figure()
    price_fig.add_trace(go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close'],
        name='OHLC'
    ))
    price_fig.update_layout(title='Price History', xaxis_title='Date', yaxis_title='Price')
    
    # Create volume chart
    volume_fig = px.bar(hist, x=hist.index, y='Volume')
    volume_fig.update_layout(title='Volume Analysis', xaxis_title='Date', yaxis_title='Volume')
    
    # Calculate technical indicators
    hist['SMA20'] = hist['Close'].rolling(window=20).mean()
    hist['SMA50'] = hist['Close'].rolling(window=50).mean()
    
    technical_fig = go.Figure()
    technical_fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name='Price'))
    technical_fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA20'], name='SMA20'))
    technical_fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA50'], name='SMA50'))
    technical_fig.update_layout(title='Technical Indicators')
    
    # Financial metrics
    financial_metrics = html.Div([
        html.Table([
            html.Tr([html.Td("Price to Book :"), html.Td(f"{stock.info.get('priceToBook', 'N/A')}")]),
            html.Tr([html.Td("Forward P/E :"), html.Td(f"{stock.info.get('forwardPE', 'N/A')}")]),
            html.Tr([html.Td("Profit Margins :"), html.Td(f"{stock.info.get('profitMargins', 'N/A')}")]),
            html.Tr([html.Td("Operating Margins :"), html.Td(f"{stock.info.get('operatingMargins', 'N/A')}")])
        ])
    ])
    
    # Trading statistics
    trading_stats = html.Div([
        html.Table([
            html.Tr([html.Td("Day High :"), html.Td(f"₹{hist['High'].iloc[-1]:.2f}")]),
            html.Tr([html.Td("Day Low :"), html.Td(f"₹{hist['Low'].iloc[-1]:.2f}")]),
            html.Tr([html.Td("52 Week High :"), html.Td(f"₹{hist['High'].max():.2f}")]),
            html.Tr([html.Td("52 Week Low :"), html.Td(f"₹{hist['Low'].min():.2f}")]),
            html.Tr([html.Td("Avg Volume :"), html.Td(f"{hist['Volume'].mean():.0f}")])
        ])
    ])
    
    return (
        f"₹{current_price:.2f}",
        f"₹{market_cap:,}",
        f"{pe_ratio:.2f}" if isinstance(pe_ratio, float) else "N/A",
        f"{volume:,}",
        price_fig,
        volume_fig,
        technical_fig,
        financial_metrics,
        trading_stats
    )

index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>StockVision Pro - Advanced Market Analysis</title>
        <style>
            /* Reset and Base Styles */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
            
            body {
                background-color: #f5f6fa;
                color: #2c3e50;
            }
            
            /* Header Styles */
            .header-container {
                background-color: #1a237e;
                color: white;
                padding: 1rem 2rem;
                position: fixed;
                width: 100%;
                top: 0;
                z-index: 1000;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .header-title {
                font-size: 1.5rem;
                font-weight: 600;
            }
            
            .header-right {
                display: flex;
                align-items: center;
                gap: 1rem;
            }
            
            .refresh-button {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 4px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            
            .refresh-button:hover {
                background-color: #2980b9;
            }
            
            /* Main Content Styles */
            .main-content {
                max-width: 1400px;
                margin: 80px auto 0;
                padding: 2rem;
            }
            
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }
            
            .metric-card {
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.3s;
            }
            
            .metric-card:hover {
                transform: translateY(-5px);
            }
            
            .card-label {
                color: #7f8c8d;
                font-size: 0.9rem;
                margin-bottom: 0.5rem;
            }
            
            .card-value {
                font-size: 1.8rem;
                font-weight: 600;
            }
            
            .charts-section {
                margin-bottom: 2rem;
            }
            
            .chart-card {
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin-bottom: 1.5rem;
            }
            
            .chart-title {
                margin-bottom: 1rem;
                color: #2c3e50;
            }
            
            .chart-container.split {
                display: flex;
                gap: 1.5rem;
                flex-wrap: wrap;
            }
            
            /* Footer Styles */
            .footer {
                background-color: #2c3e50;
                color: white;
                padding: 3rem 2rem 1.5rem;
            }
            
            .footer-content {
                max-width: 1400px;
                margin: 0 auto;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
            }
            
            .footer-section h4 {
                margin-bottom: 1rem;
                font-size: 1.2rem;
            }
            
            .footer-link {
                display: block;
                color: #bdc3c7;
                text-decoration: none;
                margin-bottom: 0.5rem;
                transition: color 0.3s;
            }
            
            .footer-link:hover {
                color: white;
            }
            
            .footer-bottom {
                max-width: 1400px;
                margin: 2rem auto 0;
                padding: 1.5rem 2rem 0;
                border-top: 1px solid rgba(255,255,255,0.1);
                text-align: center;
                color: #bdc3c7;
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .header-container {
                    flex-direction: column;
                    gap: 1rem;
                }
                
                .metrics-grid {
                    grid-template-columns: 1fr;
                }
                
                .chart-container.split {
                    flex-direction: column;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''