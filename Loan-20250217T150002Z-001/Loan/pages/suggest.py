import dash
from dash import html, dcc, Input, Output, State, register_page, callback
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

#register page
register_page(__name__, name="Suggest",path='/suggest' )



styles = {
    'header': {
        'background-color': '#00aaff',  # Change the background color here
        'color': 'white',
        'padding': '20px',
    },
    'header-container': {
        'max-width': '1200px',
        'margin': '0 auto',
    },
    'container': {
        'max-width': '1200px',
        'margin': '20px auto',
    },
    'input-card': {
        'background-color': '#ffffff',
        'box-shadow': '0px 2px 10px rgba(0, 0, 0, 0.1)',
        'border-radius': '10px',
        'padding': '20px',
    },
    'chart-card': {
        'background-color': '#ffffff',
        'box-shadow': '0px 2px 10px rgba(0, 0, 0, 0.1)',
        'border-radius': '10px',
        'padding': '20px',
    },
    'results-card': {
        'background-color': '#ffffff',
        'box-shadow': '0px 2px 10px rgba(0, 0, 0, 0.1)',
        'border-radius': '10px',
        'padding': '20px',
    },
    'footer': {
        'background-color': '#343a40',
        'color': 'white',
        'padding': '20px',
    },
    'footer-container': {
        'max-width': '1200px',
        'margin': '0 auto',
    },
}


STOCK_OPTIONS = [
    {'label': 'Reliance Industries', 'value': 'RELIANCE.NS'},
    {'label': 'Tata Consultancy Services', 'value': 'TCS.NS'},
    {'label': 'HDFC Bank', 'value': 'HDFCBANK.NS'},
    {'label': 'Infosys', 'value': 'INFY.NS'},
    {'label': 'ICICI Bank', 'value': 'ICICIBANK.NS'},
    {'label': 'Apple Inc.', 'value': 'AAPL'},
    {'label': 'Microsoft Corporation', 'value': 'MSFT'},
    {'label': 'Alphabet Inc.', 'value': 'GOOGL'},
    {'label': 'Amazon.com Inc.', 'value': 'AMZN'},
    {'label': 'Meta Platforms', 'value': 'FB'},
    {'label': 'Aarti Industries', 'value': 'AARTIIND.NS'},
    {'label': 'ABB India', 'value': 'ABB.NS'},
    {'label': 'Abbott India', 'value': 'ABBOTINDIA.NS'},
    {'label': 'Aditya Birla Capital', 'value': 'ABCAPITAL.NS'},
    {'label': 'Aditya Birla Fashion', 'value': 'ABFRL.NS'},
    {'label': 'ACC Limited', 'value': 'ACC.NS'},
    {'label': 'Adani Enterprises', 'value': 'ADANIENT.NS'},
    {'label': 'Adani Ports', 'value': 'ADANIPORTS.NS'},
    {'label': 'Alkem Laboratories', 'value': 'ALKEM.NS'},
    {'label': 'Ambuja Cements', 'value': 'AMBUJACEM.NS'},
    {'label': 'Apollo Hospitals', 'value': 'APOLLOHOSP.NS'},
    {'label': 'Apollo Tyres', 'value': 'APOLLOTYRE.NS'},
    {'label': 'Ashok Leyland', 'value': 'ASHOKLEY.NS'},
    {'label': 'Asian Paints', 'value': 'ASIAN PAINT LTD.NS'},
    {'label': 'Astral', 'value': 'ASTRAL.NS'},
    {'label': 'Atul Ltd', 'value': 'ATUL LTD.NS'},
    {'label': 'AU Small Finance Bank', 'value': 'AUBANK.NS'},
    {'label': 'Aurobindo Pharma', 'value': 'Aurobindo Pharma Limited.NS'},
    {'label': 'Axis Bank', 'value': 'AXISBANK.NS'},
    {'label': 'Bajaj Auto', 'value': 'BAJAJ-AUTO.NS'},
    {'label': 'Bajaj Finserv', 'value': 'BAJAJFINSV.NS'},
    {'label': 'Bajaj Finance', 'value': 'BAJFINANCE.NS'},
    {'label': 'Balkrishna Industries', 'value': 'BALKRISIND.NS'},
    {'label': 'Balrampur Chini Mills', 'value': 'BALRAMCHIN.NS'},
    {'label': 'Bandhan Bank', 'value': 'BANDHANBNK.NS'},
    {'label': 'Bank of Baroda', 'value': 'BANKBARODA.NS'},
    {'label': 'Bata India', 'value': 'BATAINDIA.NS'},
    {'label': 'Bharat Electronics', 'value': 'BEL.NS'},
    {'label': 'Berger Paints', 'value': 'BERGEPAINT.NS'},
    {'label': 'Bharat Forge', 'value': 'BHARATFORG.NS'},
    {'label': 'BHEL', 'value': 'BHEL.NS'},
    {'label': 'Biocon', 'value': 'BIOCON.NS'},
    {'label': 'Bosch Ltd', 'value': 'BOSCHLTD.NS'},
    {'label': 'BPCL', 'value': 'BPCL.NS'},
    {'label': 'Britannia', 'value': 'BRITANNIA.NS'},
    {'label': 'BSoft', 'value': 'BSOFT.NS'},
    {'label': 'Canara Bank', 'value': 'CANBK.NS'},
    {'label': 'Can Fin Homes', 'value': 'CANFIN HOME.NS'},
    {'label': 'Chambal Fertilizers', 'value': 'CHAMBLFERT.NS'},
    {'label': 'Cholamandalam', 'value': 'CHOLAFIN.NS'},
    {'label': 'Cipla', 'value': 'CIPLA.NS'},
    {'label': 'Coal India', 'value': 'COALINDIA.NS'},
    {'label': 'Coforge', 'value': 'COFORGE.NS'},
    {'label': 'Colgate-Palmolive', 'value': 'COLPAL.NS'},
    {'label': 'Container Corp', 'value': 'CONCOR.NS'},
    {'label': 'Coromandel Intl', 'value': 'COROMANDEL.NS'},
    {'label': 'Crompton', 'value': 'CROMPTON.NS'},
    {'label': 'City Union Bank', 'value': 'CUB.NS'},
    {'label': 'Cummins India', 'value': 'CUMMINSIND.NS'},
    {'label': 'Dabur', 'value': 'DABUR.NS'},
    {'label': 'Dalmia Bharat', 'value': 'DALBHARAT.NS'},
    {'label': 'Deepak Nitrite', 'value': 'DEEPAKNTR.NS'},
    {'label': 'Divis Laboratories', 'value': 'DIVISLAB.NS'},
    {'label': 'Dixon Tech', 'value': 'DIXON.NS'},
    {'label': 'DLF', 'value': 'DLF.NS'},
    {'label': 'Dr. Reddy’s', 'value': 'DRREDDY.NS'},
    {'label': 'Eicher Motors', 'value': 'EICHERMOT.NS'},
    {'label': 'Escorts', 'value': 'ESCORTS.NS'},
    {'label': 'Exide Industries', 'value': 'EXIDEIND.NS'},
    {'label': 'Federal Bank', 'value': 'FEDERALBNK.NS'},
    {'label': 'GAIL', 'value': 'GAIL.NS'},
    {'label': 'Glenmark', 'value': 'GLENMARK.NS'},
    {'label': 'GMR Infra', 'value': 'GMRINFRA.NS'},
    {'label': 'GNFC', 'value': 'GNFC.NS'},
    {'label': 'Godrej Consumer', 'value': 'GODREJCP.NS'},
    {'label': 'Godrej Properties', 'value': 'GODREJPROP.NS'},
    {'label': 'Granules', 'value': 'GRANULES.NS'},
    {'label': 'Grasim', 'value': 'GRASIM.NS'},
    {'label': 'Gujarat Gas', 'value': 'GUJGASLTD.NS'},
    {'label': 'HAL', 'value': 'HAL.NS'},
    {'label': 'Havells', 'value': 'HAVELLS.NS'},
    {'label': 'HCL Technologies', 'value': 'HCLTECH.NS'},
    {'label': 'HDFC AMC', 'value': 'HDFCAMC.NS'},
    {'label': 'HDFC Life', 'value': 'HDFCLIFE.NS'},
    {'label': 'Hero Motocorp', 'value': 'HEROMOTOCO.NS'},
    {'label': 'Hindalco', 'value': 'HINDALCO.NS'},
    {'label': 'Hindustan Copper', 'value': 'HINDCOPPER.NS'},
    {'label': 'Hindustan Petroleum', 'value': 'HINDPETRO.NS'},
    {'label': 'Hindustan Unilever', 'value': 'HINDUNILVR.NS'},
    {'label': 'IDFC First Bank', 'value': 'IDFCFIRSTB.NS'},
    {'label': 'IRCTC', 'value': 'IRCTC.NS'},
    {'label': 'ITC', 'value': 'ITC.NS'},
    {'label': 'Jindal Steel', 'value': 'JINDALSTEL.NS'},
    {'label': 'JK Cement', 'value': 'JKCEM.NS'},
    {'label': 'JSW Steel', 'value': 'JSWSTEEL.NS'},
    {'label': 'Jubilant Foodworks', 'value': 'JUBLFOOD.NS'},
    {'label': 'Kotak Mahindra Bank', 'value': 'KOTAKBANK.NS'},
    {'label': 'M&M', 'value': 'M&M.NS'},
    {'label': 'Mphasis', 'value': 'MPHASIS.NS'}
]


layout = html.Div([
    # Header
    html.Header(
        html.Div([
            html.Div([
                html.I(className="fas fa-chart-line me-3"),
                html.H1(id="header-title", children="Investmate", className="mb-0 fw-bold"),
            ], className="d-flex align-items-center"),
            html.P("Professional Technical Analysis & Trading Recommendations", className="text-light mb-0 mt-2"),
        ], style={**styles['header-container'], 'backgroundColor': '#1a237e'}),  # Updated header background color
        style={**styles['header'], 'backgroundColor': '#1a237e', 'color': 'white'}  # Ensuring text is white
    ),

    # Main Content Container
    html.Div([
        # Input Card
        html.Div([
            html.Div([ 
                # Stock Dropdown
                html.Div([
                    html.Label("Select Stock", className="form-label fw-bold text-dark fs-5"),
                    dcc.Dropdown(
                        id="stock-input",
                        options=STOCK_OPTIONS,
                        value="RELIANCE.NS",
                        className="form-select shadow-sm border-0 rounded-3 bg-light text-dark px-3 py-2",
                        style={'font-size': '16px', 'border-radius': '8px'}
                    ),
                ], className="col-md-4 mb-4"),

                # Time Period Dropdown
                html.Div([
                    html.Label("Time Period", className="form-label fw-bold text-dark fs-5"),
                    dcc.Dropdown(
                        id="timeframe-dropdown",
                        options=[
                            {"label": "1 Month", "value": "1mo"},
                            {"label": "3 Months", "value": "3mo"},
                            {"label": "6 Months", "value": "6mo"},
                            {"label": "1 Year", "value": "1y"},
                        ],
                        value="3mo",
                        className="form-select shadow-sm border-0 rounded-3 bg-light text-dark px-3 py-2",
                        style={'font-size': '16px', 'border-radius': '8px'}
                    ),
                ], className="col-md-4 mb-4"),

                # Analyze Button
                html.Div([
                    html.Button(
                        [html.I(className="fas fa-search me-2"), "Analyze"],
                        id="analyze-button",
                        className="btn btn-primary w-100 mt-4 shadow-lg rounded-3 py-2 px-4 text-white fs-5",
                        style={'font-size': '16px'}
                    ),
                ], className="col-md-2 mb-4"),
            ], className="row align-items-center"),
        ], style={**styles['input-card'], 'border-radius': '10px', 'padding': '20px', 'background-color': '#f8f9fa', 'box-shadow': '0 4px 10px rgba(0, 0, 0, 0.1)'}),

        # Results Section
        html.Div([
            # Chart Card
            html.Div([
                dcc.Graph(id="stock-price-chart", config={'displayModeBar': False}),
            ], style={**styles['chart-card'], 'border-radius': '10px'}),

            # Analysis Results Card
            html.Div([
                html.Div([
                    html.H3([
                        html.I(className="fas fa-chart-bar me-2"),
                        "Analysis Results"
                    ], className="mb-4 text-primary"),

                    # Grid for results
                    html.Div([
                        # Left column - Recommendation
                        html.Div([
                            html.Div(id="recommendation-output", className="fw-bold fs-5 mb-3"),
                            html.Div(id="recommendation-explanation", className="text-muted"),
                        ], className="col-md-7"),

                        # Right column - Technical Indicators
                        html.Div([
                            html.Div(id="technical-indicators", className="border-start ps-4"),
                        ], className="col-md-5"),
                    ], className="row"),
                ], className="card-body"),
            ], style={**styles['results-card'], 'border-radius': '10px'}),
        ]),

    ], style={**styles['container'], 'padding-top': '20px'}),

    # Footer
    html.Footer(
        html.Div([
            html.Div([
                # Footer content
                html.Div([
                    html.Div([
                        html.H5("About", className="text-light mb-3"),
                        html.P("Professional stock market analysis tool powered by advanced technical indicators"),
                    ], className="col-md-4"),

                    html.Div([
                        html.H5("Data Source", className="text-light mb-3"),
                        html.P([
                            "Powered by ",
                            html.A("Yahoo Finance", href="https://finance.yahoo.com/", className="text-light")
                        ])
                    ], className="col-md-4"),

                    html.Div([
                        html.H5("Last Updated", className="text-light mb-3"),
                        html.P(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    ], className="col-md-4"),
                ], className="row"),

                # Copyright
                html.Hr(className="my-4"),
                html.P("© 2024 Stock Market Analysis Dashboard. All rights reserved.", className="text-center text-light mb-0"),
            ])
        ], style={**styles['footer-container'], 'border-top': '1px solid #444'}),
        style={**styles['footer'], 'background-color': '#1a237e', 'color': 'white'}  # Updated footer color and text color
    )
])



def calculate_technical_indicators(df):
    """Calculate technical indicators for analysis"""
    # Calculate 20-day and 50-day moving averages
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    
    # Calculate RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Calculate MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Calculate price momentum (5-day)
    df['Momentum'] = df['Close'].pct_change(periods=5) * 100
    
    return df

def generate_recommendation(df):
    """Generate detailed buy/hold/sell recommendation based on technical indicators"""
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    # Initialize scoring and reasoning
    score = 0
    reasons = []
    
    # Moving Average analysis
    if latest['Close'] > latest['MA20']:
        score += 1
        reasons.append("Price is above 20-day moving average, showing short-term upward momentum")
    else:
        score -= 1
        reasons.append("Price is below 20-day moving average, showing short-term weakness")
        
    if latest['MA20'] > latest['MA50']:
        score += 1
        reasons.append("20-day MA is above 50-day MA, indicating a positive trend")
    else:
        score -= 1
        reasons.append("20-day MA is below 50-day MA, suggesting a negative trend")
    
    # RSI analysis
    if latest['RSI'] < 30:
        score += 2
        reasons.append("RSI below 30 indicates oversold conditions - potential buying opportunity")
    elif latest['RSI'] > 70:
        score -= 2
        reasons.append("RSI above 70 indicates overbought conditions - consider taking profits")
    else:
        reasons.append(f"RSI at {latest['RSI']:.2f} shows neutral momentum")
    
    # MACD analysis
    if latest['MACD'] > latest['Signal'] and prev['MACD'] <= prev['Signal']:
        score += 2
        reasons.append("MACD just crossed above signal line - bullish signal")
    elif latest['MACD'] < latest['Signal'] and prev['MACD'] >= prev['Signal']:
        score -= 2
        reasons.append("MACD just crossed below signal line - bearish signal")
    
    # Momentum analysis
    if latest['Momentum'] > 2:
        score += 1
        reasons.append(f"Strong positive momentum of {latest['Momentum']:.1f}% over 5 days")
    elif latest['Momentum'] < -2:
        score -= 1
        reasons.append(f"Strong negative momentum of {latest['Momentum']:.1f}% over 5 days")
    
    # Generate final recommendation based on score
    if score >= 2:
        recommendation = "BUY"
        color = "green"
    elif score <= -2:
        recommendation = "SELL"
        color = "red"
    else:
        recommendation = "HOLD"
        color = "orange"
    
    return recommendation, color, reasons

@callback(
    [Output("stock-price-chart", "figure"),
     Output("recommendation-output", "children"),
     Output("recommendation-explanation", "children"),
     Output("technical-indicators", "children")],
    [Input("analyze-button", "n_clicks")],
    [State("stock-input", "value"),
     State("timeframe-dropdown", "value")]
)
def update_analysis(n_clicks, symbol, timeframe):
    if n_clicks is None:
        raise PreventUpdate
    
    try:
        # Fetch stock data
        stock = yf.Ticker(symbol)
        df = stock.history(period=timeframe)
        
        if df.empty:
            return {}, "No data available for this symbol", "", ""
        
        # Calculate technical indicators
        df = calculate_technical_indicators(df)
        
        # Generate recommendation
        recommendation, color, reasons = generate_recommendation(df)
        
        # Create price chart
        fig = go.Figure()
        
        # Add candlestick chart
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name="Price"
        ))
        
        # Add moving averages
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MA20'],
            name="20-day MA",
            line=dict(color="blue")
        ))
        
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MA50'],
            name="50-day MA",
            line=dict(color="orange")
        ))
        
        fig.update_layout(
            title=f"{symbol} Stock Price",
            yaxis_title="Price",
            xaxis_title="Date",
            template="plotly_white"
        )
        
        # Generate technical indicators summary
        latest = df.iloc[-1]
        indicators_html = html.Div([
            html.H4("Current Technical Indicators:", className="mt-4"),
            html.P(f"Current Price: ${latest['Close']:.2f}"),
            html.P(f"RSI (14): {latest['RSI']:.2f}"),
            html.P(f"MACD: {latest['MACD']:.2f}"),
            html.P(f"Signal Line: {latest['Signal']:.2f}"),
            html.P(f"20-day MA: ${latest['MA20']:.2f}"),
            html.P(f"50-day MA: ${latest['MA50']:.2f}"),
            html.P(f"5-day Momentum: {latest['Momentum']:.1f}%"),
        ])
        
        # Create recommendation output
        recommendation_html = html.H4([
            "Recommendation: ",
            html.Span(recommendation, style={"color": color, "font-weight": "bold"})
        ])
        
        # Create detailed explanation
        explanation_html = html.Div([
            html.H4("Analysis Explanation:", className="mt-4"),
            html.Ul([html.Li(reason) for reason in reasons])
        ])
        
        return fig, recommendation_html, explanation_html, indicators_html
        
    except Exception as e:
        return {}, f"Error: {str(e)}", "", ""
