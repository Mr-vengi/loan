import pandas as pd
from prophet import Prophet
from dash import Dash, html, dcc, Input, Output, State, register_page, callback
import plotly.graph_objects as go
import dash_table
import yfinance as yf
import dash_html_components as html

#register page
register_page(__name__, name="calculator",path='/calci' )


# Styles dictionary
STYLES = {
    'nav-container': {
        'backgroundColor': '#1a237e',
        'padding': '15px 0',
        'position': 'fixed',
        'width': '100%',
        'top': '0',
        'zIndex': '1000',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
    },
    'nav-content': {
        'maxWidth': '1200px',
        'margin': '0 auto',
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center',
        'padding': '0 20px',
    },
    'nav-link': {
        'color': 'white',
        'textDecoration': 'none',
        'padding': '8px 15px',
        'borderRadius': '5px',
        'transition': 'all 0.3s ease',
        'fontSize': '1.1rem',
    },
    'search-box': {
        'padding': '8px 15px',
        'borderRadius': '20px',
        'border': '1px solid rgba(255,255,255,0.2)',
        'backgroundColor': 'rgba(255,255,255,0.1)',
        'color': 'white',
        'width': '200px',
        'outline': 'none',
    },
    'container': {
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '0 20px',
    },
    'button-primary': {
        'backgroundColor': '#3498db',
        'color': 'white',
        'padding': '12px 24px',
        'borderRadius': '5px',
        'border': 'none',
        'cursor': 'pointer',
        'fontSize': '1.1rem',
        'transition': 'background-color 0.3s',
    },
    'card': {
        'backgroundColor': 'white',
        'borderRadius': '10px',
        'padding': '30px',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
        'transition': 'transform 0.3s',
        'margin': '15px',
        'flex': '1',
        'minWidth': '250px',
    }
}

# Your existing helper functions remain the same
def fetch_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    data.reset_index(inplace=True)
    return data[['Date', 'Close']]

def prepare_data(data):
    data.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
    data['ds'] = data['ds'].dt.tz_localize(None)
    return data

def predict_stock_trends(data, periods=30):
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast

def calculate_rsi(data, period=14):
    delta = data['y'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    data['Status'] = data['RSI'].apply(
        lambda rsi: 'Overbought' if rsi > 70 else 'Oversold' if rsi < 30 else 'Neutral'
    )
    return data


# Custom CSS for better styling
index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Stock Market Analytics Pro</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                margin: 0;
                background-color: #f3f4f6;
            }
            .header {
                background-color: #ffffff;
                padding: 1rem;
                box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 2rem;
            }
            .card {
                background-color: white;
                border-radius: 0.5rem;
                box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
                padding: 1.5rem;
                margin-bottom: 1.5rem;
            }
            .input-group {
                display: flex;
                gap: 1rem;
                margin-bottom: 1rem;
            }
            .input-label {
                font-weight: 600;
                margin-bottom: 0.5rem;
            }
            .footer {
                background-color: #ffffff;
                padding: 1.5rem;
                text-align: center;
                margin-top: 2rem;
                border-top: 1px solid #e5e7eb;
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

layout = html.Div([
    # Header with Navigation
    html.Div([
        html.Div([
            html.Div([
                html.H1("Investmate", 
                        style={'color': 'white', 'fontSize': '24px', 'fontWeight': '600', 'margin': '0'}),
                html.P("",
                       style={'color': '#d1c4e9', 'margin': '0'})
            ], style={'flex': '1'}),

            # Navigation Links
            html.Div([
                html.A("", href="#", style={**STYLES['nav-link'], 'backgroundColor': '#3949ab'}),
                html.A("", href="#", style=STYLES['nav-link']),
                html.A("", href="#", style=STYLES['nav-link']),
            ], style={'display': 'flex', 'gap': '10px'}),
        ], style=STYLES['nav-content'])
    ], style=STYLES['nav-container']),

    # Main Content
    html.Div([
        # Input Controls Card
        html.Div([
            html.H2("Analysis Parameters", 
                   style={'fontSize': '18px', 'fontWeight': '600', 'marginBottom': '1rem'}),
            html.Div([
                html.Div([
                    html.Label("Stock Ticker", className='input-label'),
                    dcc.Input(
                        id='ticker',
                        type='text',
                        placeholder='e.g., AAPL',
                        style={
                            'width': '100%',
                            'padding': '0.5rem',
                            'border': '1px solid #e5e7eb',
                            'borderRadius': '0.375rem'
                        }
                    )
                ], style={'flex': '1'}),
                html.Div([
                    html.Label("Start Date", className='input-label'),
                    dcc.DatePickerSingle(
                        id='start-date',
                        style={
                            'width': '100%',
                            'border': '1px solid #e5e7eb',
                            'borderRadius': '0.375rem'
                        }
                    )
                ], style={'flex': '1'}),
                html.Div([
                    html.Label("End Date", className='input-label'),
                    dcc.DatePickerSingle(
                        id='end-date',
                        style={
                            'width': '100%',
                            'border': '1px solid #e5e7eb',
                            'borderRadius': '0.375rem'
                        }
                    )
                ], style={'flex': '1'}),
                html.Button(
                    'Analyze',
                    id='submit-button',
                    style={
                        'backgroundColor': '#2563eb',
                        'color': 'white',
                        'padding': '0.5rem 1rem',
                        'borderRadius': '0.375rem',
                        'border': 'none',
                        'cursor': 'pointer',
                        'fontWeight': '600'
                    }
                )
            ], className='input-group')
        ], className='card'),

        # Graphs Container
        html.Div([
            html.Div([
                # Price Prediction Graph
                html.Div([
                    html.H3("Price Prediction", 
                           style={'fontSize': '16px', 'fontWeight': '600', 'marginBottom': '1rem'}),
                    dcc.Graph(id='prediction-graph')
                ], className='card', style={'flex': '1'}),

                # RSI Graph
                html.Div([
                    html.H3("RSI Analysis", 
                           style={'fontSize': '16px', 'fontWeight': '600', 'marginBottom': '1rem'}),
                    dcc.Graph(id='rsi-graph')
                ], className='card', style={'flex': '1'})
            ], style={'display': 'flex', 'gap': '1.5rem', 'marginBottom': '1.5rem'}),

            # Data Table
            html.Div([
                html.H3("Historical Data", 
                       style={'fontSize': '16px', 'fontWeight': '600', 'marginBottom': '1rem'}),
                dash_table.DataTable(
                    id='stock-table',
                    style_header={
                        'backgroundColor': '#f3f4f6',
                        'fontWeight': '600',
                        'border': '1px solid #e5e7eb'
                    },
                    style_cell={
                        'textAlign': 'left',
                        'padding': '0.75rem',
                        'border': '1px solid #e5e7eb'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f9fafb'
                        }
                    ]
                )
            ], className='card')
        ])
    ], className='container', style={'marginTop': '80px'}),

    # Footer with Navigation
    html.Footer([
        html.Div([
            html.Div([
                html.A("", href="#", style={**STYLES['nav-link'], 'color': '#d1c4e9'}),
                html.A("", href="#", style=STYLES['nav-link']),
            ], style={'display': 'flex', 'gap': '10px'}),

            html.P("© 2024 Stock Market Analytics Pro. All rights reserved.",
                   style={'color': '#d1c4e9', 'margin': '10px 0 0'})
        ], style=STYLES['nav-content'])
    ], style={**STYLES['nav-container'], 'bottom': '0', 'top': 'auto', 'position': 'relative'})
]),

# Your existing callback remains the same
@callback(
    [Output('prediction-graph', 'figure'),
     Output('rsi-graph', 'figure'),
     Output('stock-table', 'data')],
    [Input('submit-button', 'n_clicks')],
    [State('ticker', 'value'),
     State('start-date', 'date'),
     State('end-date', 'date')]
)
def update_graph(n_clicks, ticker, start_date, end_date):
    if n_clicks == 0 or not ticker or not start_date or not end_date:
        return {}, {}, []

    # Fetch and prepare data
    stock_data = fetch_stock_data(ticker, start_date, end_date)
    prepared_data = prepare_data(stock_data)

    # Prediction
    forecast = predict_stock_trends(prepared_data)

    # RSI Calculation
    stock_with_rsi = calculate_rsi(prepared_data)

    # Prediction Graph
    prediction_fig = go.Figure()
    prediction_fig.add_trace(go.Scatter(x=prepared_data['ds'], y=prepared_data['y'], 
                                      mode='lines', name='Historical',
                                      line=dict(color='#2563eb')))
    prediction_fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], 
                                      mode='lines', name='Predicted',
                                      line=dict(color='#16a34a')))
    prediction_fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], 
                                      mode='lines', name='Upper CI',
                                      line=dict(dash='dash', color='#9ca3af')))
    prediction_fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], 
                                      mode='lines', name='Lower CI',
                                      line=dict(dash='dash', color='#9ca3af')))
    prediction_fig.update_layout(
        title=f'Stock Price Prediction for {ticker}',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    # RSI Graph
    rsi_fig = go.Figure()
    rsi_fig.add_trace(go.Scatter(x=stock_with_rsi['ds'], y=stock_with_rsi['RSI'], 
                                mode='lines', name='RSI',
                                line=dict(color='#2563eb')))
    rsi_fig.add_trace(go.Scatter(x=stock_with_rsi['ds'], y=[70] * len(stock_with_rsi), 
                                mode='lines', name='Overbought (70)',
                                line=dict(dash='dash', color='#dc2626')))
    rsi_fig.add_trace(go.Scatter(x=stock_with_rsi['ds'], y=[30] * len(stock_with_rsi), 
                                mode='lines', name='Oversold (30)',
                                line=dict(dash='dash', color='#16a34a')))
    rsi_fig.update_layout(
        title=f'RSI Analysis for {ticker}',
        xaxis_title='Date',
        yaxis_title='RSI Value',
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    # Prepare table data
    table_data = stock_with_rsi[['ds', 'y', 'RSI', 'Status']].to_dict('records')

    return prediction_fig, rsi_fig, table_data

