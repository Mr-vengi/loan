import dash
from dash import dcc, html, Input, Output, State, register_page, callback 
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta
import time
import threading
from twilio.rest import Client  # Assuming Twilio is used for SMS


# Styling dictionary
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




#register page
register_page(__name__, name="Portfolio",path='/portfolio' )

title = "Stock Alert System"

# Example stock data for the dropdown (can be extended)
stocks_list = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB',
    'AARTIIND.NS', 'ABB.NS', 'ABBOTINDIA.NS', 'ABCAPITAL.NS', 'ABFRL.NS', 'ACC.NS', 'ADANIENT.NS', 'ADANIPORTS.NS', 'ALKEM.NS', 'AMBUJACEM.NS',
    'APOLLOHOSP.NS', 'APOLLOTYRE.NS', 'ASHOKLEY.NS', 'ASIAN PAINT LTD.NS', 'ASTRAL.NS', 'ATUL LTD.NS', 'AUBANK.NS', 'Aurobindo Pharma Limited.NS',
    'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BALKRISIND.NS', 'BALRAMCHIN.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS',
    'BATAINDIA.NS', 'BEL.NS', 'BERGEPAINT.NS', 'BHARATFORG.NS', 'BHEL.NS', 'BIOCON.NS', 'BOSCHLTD.NS', 'BPCL.NS', 'BRITANNIA.NS', 'BSOFT.NS',
    'CANBK.NS', 'CANFIN HOME.NS', 'CHAMBLFERT.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'COALINDIA.NS', 'COFORGE.NS', 'COLPAL.NS', 'CONCOR.NS', 'COROMANDEL.NS',
    'CROMPTON.NS', 'CUB.NS', 'CUMMINSIND.NS', 'DABUR.NS', 'DALBHARAT.NS', 'DEEPAKNTR.NS', 'DIVISLAB.NS', 'DIXON.NS', 'DLF.NS', 'DRREDDY.NS',
    'EICHERMOT.NS', 'ESCORTS.NS', 'EXIDEIND.NS', 'FEDERALBNK.NS', 'GAIL.NS', 'GLENMARK.NS', 'GMRINFRA.NS', 'GNFC.NS', 'GODREJCP.NS', 'GODREJPROP.NS',
    'GRANULES.NS', 'GRASIM.NS', 'GUJGASLTD.NS', 'HAL.NS', 'HAVELLS.NS', 'HCLTECH.NS', 'HDFCAMC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS',
    'HINDALCO.NS', 'HINDCOPPER.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'ICICIGI.NS', 'ICICIPRULI.NS', 'IDEA.NS', 'IDFCFIRSTB.NS',
    'IEX.NS', 'IGL.NS', 'INDHOTEL.NS', 'INDIACEM.NS', 'INDIAMART.NS', 'INDIGO.NS', 'INDUSINDBK.NS', 'INDUSTOWER.NS', 'INFY.NS', 'IOC.NS', 'IPCALAB.NS',
    'IRCTC.NS', 'ITC.NS', 'JINDALSTEL.NS', 'JKCEM.NS', 'JSWSTEEL.NS', 'JUBLFOOD.NS', 'KOTAKBANK.NS', 'LALPATHLAB.NS', 'LAURUSLABS.NS', 'LICHSGFIN.NS',
    'LT.NS', 'LTF.NS', 'LTIM.NS', 'LTTS.NS', 'LUPIN.NS', 'M&M.NS', 'M&MFIN.NS', 'MANAPPURAM.NS', 'MARICO.NS', 'MARUTI.NS', 'MCX.NS', 'METROPOLIS.NS',
    'MFSL.NS', 'MGL.NS', 'MPHASIS.NS', 'MRF.NS', 'MUTHOOTFIN.NS', 'NATIONALUM.NS', 'NAUKRI ( MEGA).NS', 'NAVINFLUOR.NS', 'NESTLEIND.NS', 'NMDC.NS',
    'NTPC.NS', 'OBEROIRLTY.NS', 'OFSS.NS', 'ONGC.NS', 'PAGEIND.NS', 'PEL.NS', 'PERSISTENT.NS', 'PETRONET.NS', 'PFC.NS', 'PIDILITIND.NS', 'PIIND.NS',
    'PNB.NS', 'POLYCAB.NS', 'POWERGRID.NS', 'PVR.NS', 'RAMCOCEM.NS', 'RBLBANK.NS', 'RECLTD.NS', 'RELIANCE.NS', 'SAIL.NS', 'SAM MOTHERSON.NS', 'SBI CARD.NS',
    'SBI LIFE.NS', 'SBIN.NS', 'SHREECEM.NS', 'SHRIRAM FINANCE LTD.NS', 'SIEMENS.NS', 'SRF.NS', 'SUN TV.NS', 'SUNPHARMA.NS', 'SYNGENE.NS', 'TATACHEM.NS',
    'TATACOMM.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TRENT.NS',
    'TVSMOTOR.NS', 'UBL.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'UNITDSPR ( MCD).NS', 'VEDL.NS', 'VOLTAS.NS', 'WIPRO.NS', 'ZEEL.NS', 'ZYDUSLIFE.NS']

# Set up Twilio SMS API
account_sid = 'AC0204e758e6fc7e5ea1e5ef17ed2ed99e'
auth_token = 'bc2a1afe4fcefbda7d64976125e300bb'
twilio_phone_number = '+12184928003'
recipient_phone_number = '+919962780982,+919884080982,+918778523085'

client = Client(account_sid, auth_token)

# Enhanced layout with navigation
layout = html.Div([
    # Navigation Bar
    html.Nav(
        style=STYLES['nav-container'],
        children=[
            html.Div(
                style=STYLES['nav-content'],
                children=[
                    # Logo/Brand
                    html.Div([
                        html.H1("Investmate", style={'color': 'white', 'margin': '0', 'fontSize': '24px'})
                    ]),
                    
                    # Navigation Links
                   
                    
                    
                ]
            )
        ]
    ),
    
    # Main Content Container (with padding-top to account for fixed navbar)
    html.Div(
        style={**STYLES['container'], 'paddingTop': '80px'},
        children=[
            # Stock Selection Card
            html.Div(
                style=STYLES['card'],
                children=[
                    html.H2("Select Stock", style={'marginBottom': '20px'}),
                    dcc.Dropdown(
                        id="stock-dropdown",
                        options=[{"label": stock, "value": stock} for stock in stocks_list],
                        placeholder="Choose a stock to track...",
                        style={'marginBottom': '20px'}
                    )
                ]
            ),

            # Stock Graph Card
            html.Div(
                style={**STYLES['card'], 'marginTop': '20px'},
                children=[
                    dcc.Graph(
                        id="stock-graph",
                        style={'height': '500px'}
                    )
                ]
            ),

            # Alert Settings Grid
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(auto-fit, minmax(300px, 1fr))',
                    'gap': '20px',
                    'marginTop': '20px'
                },
                children=[
                    # Price Threshold Card
                    html.Div(
                        style=STYLES['card'],
                        children=[
                            html.H3("Price Alert", style={'marginBottom': '15px'}),
                            dcc.Input(
                                id="price-threshold",
                                type="number",
                                placeholder="Set price threshold...",
                                style={
                                    'width': '100%',
                                    'padding': '10px',
                                    'borderRadius': '5px',
                                    'border': '1px solid #ddd'
                                }
                            )
                        ]
                    ),

                    # Percentage Change Card
                    html.Div(
                        style=STYLES['card'],
                        children=[
                            html.H3("Percentage Alert", style={'marginBottom': '15px'}),
                            dcc.Input(
                                id="percentage-threshold",
                                type="number",
                                placeholder="Set % threshold...",
                                style={
                                    'width': '100%',
                                    'padding': '10px',
                                    'borderRadius': '5px',
                                    'border': '1px solid #ddd'
                                }
                            )
                        ]
                    ),

                    # Profit/Loss Card
                    html.Div(
                        style=STYLES['card'],
                        children=[
                            html.H3("Profit/Loss Alert", style={'marginBottom': '15px'}),
                            dcc.Input(
                                id="profit-threshold",
                                type="number",
                                placeholder="Set profit threshold...",
                                style={
                                    'width': '100%',
                                    'padding': '10px',
                                    'borderRadius': '5px',
                                    'border': '1px solid #ddd'
                                }
                            )
                        ]
                    )
                ]
            ),

            # Alert Frequency Card
            html.Div(
                style={**STYLES['card'], 'marginTop': '20px'},
                children=[
                    html.H3("Alert Frequency", style={'marginBottom': '15px'}),
                    dcc.Dropdown(
                        id="alert-frequency-dropdown",
                        options=[
                            {"label": "Real-Time", "value": "real-time"},
                            {"label": "Daily", "value": "daily"},
                            {"label": "Weekly", "value": "weekly"},
                        ],
                        placeholder="Select frequency...",
                        style={'marginBottom': '20px'}
                    ),
                    html.Button(
                        "Set Alert",
                        id="submit-alert-button",
                        n_clicks=0,
                        style=STYLES['button-primary']
                    ),
                    html.Div(id="alert-output", style={'marginTop': '15px'})
                ]
            ),

            # Recommendations Card
            html.Div(
                style={**STYLES['card'], 'marginTop': '20px'},
                children=[
                    html.H3("Market Recommendations", style={'marginBottom': '15px'}),
                    html.Div(id="recommendation-content")
                ]
            )
        ]
    )
]),
# Callback to generate stock graph
@callback(
    Output("stock-graph", "figure"),
    Input("stock-dropdown", "value")
)
def update_stock_graph(stock):
    if not stock:
        return go.Figure()
    try:
        # Fetch live stock data
        stock_data = yf.Ticker(stock).history(period="1mo")
        if stock_data.empty:
            return go.Figure()

        # Create stock price graph
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=stock_data.index,
            open=stock_data['Open'],
            high=stock_data['High'],
            low=stock_data['Low'],
            close=stock_data['Close'],
            name="Price History"
        ))
        fig.update_layout(title=f"Price History of {stock}", xaxis_title="Date", yaxis_title="Price (₹)")
        return fig
    except Exception as e:
        return go.Figure()

# Callback to generate recommendations based on selected stock
@callback(
    Output("recommendation-content", "children"),
    Input("stock-dropdown", "value")
)
def generate_recommendations(stock):
    if not stock:
        return "Select a stock to see recommendations."
    try:
        # Fetch live stock data
        stock_data = yf.Ticker(stock).history(period="1d")
        if stock_data.empty:
            return "Unable to fetch data. Please check the stock symbol."

        # Extract the latest price
        latest_price = stock_data["Close"].iloc[-1]
        recommendations = [
            f"Current Price: ₹{latest_price:.2f}",
            f"Recommendation: Buy if below ₹{latest_price * 0.95:.2f}, Sell if above ₹{latest_price * 1.05:.2f}.",
            f"Set alerts for ±5% price changes."
        ]
        return html.Ul([html.Li(rec) for rec in recommendations])

    except Exception as e:
        return f"Error fetching data for {stock}: {e}"

# Function to send SMS alert
def send_sms_alert(message):
    phone_numbers = recipient_phone_number.split(',')  # Split the comma-separated phone numbers
    try:
        for number in phone_numbers:
            message = client.messages.create(
                body=message,
                from_=twilio_phone_number,
                to=number.strip()  # Remove any extra spaces
            )
            print(f"Alert sent to {number}: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")


# Callback to handle form submission
@callback(
    Output("alert-output", "children"),
    Input("submit-alert-button", "n_clicks"),
    State("stock-dropdown", "value"),
    State("price-threshold", "value"),
    State("percentage-threshold", "value"),
    State("profit-threshold", "value"),
    State("alert-frequency-dropdown", "value"),
)
def handle_alert_submission(n_clicks, stock, price, percentage, profit, frequency):
    if n_clicks > 0:
        # Validate inputs
        if not stock:
            return "Please select a stock or your entire portfolio."
        if not (price or percentage or profit):
            return "Please set at least one threshold (Price, Percentage Change, or Profit)."
        if not frequency:
            return "Please select an alert frequency."
        
        # Simulate saving the alert (you can replace this with a database save)
        alert_message = f"Alert set successfully for {stock} with the following details: " \
                        f"Price Threshold: {price}, Percentage Change: {percentage}%, " \
                        f"Profit: {profit}, Frequency: {frequency.capitalize()}."
        
        # Start alert checking in a separate thread
        threading.Thread(target=check_alerts, args=(stock, price, percentage, profit, frequency)).start()

        return alert_message
    
    return ""


# Function to check stock price against thresholds
def check_alerts(stock, price, percentage, profit, frequency):
    while True:
        try:
            stock_data = yf.Ticker(stock).history(period="1d")
            if stock_data.empty:
                print(f"Error fetching data for {stock}. Retrying.")
                time.sleep(60)
                continue

            latest_price = stock_data["Close"].iloc[-1]

            # Check conditions for price, percentage change, and profit/loss
            if price and (float(price) <= latest_price):
                send_sms_alert(f"Price Alert: {stock} has reached or exceeded ₹{latest_price}.")
            # Implement logic for percentage and profit alerts if needed

            time.sleep(60)  # Delay before checking again (based on frequency)
        except Exception as e:
            print(f"Error checking alerts: {e}")
            time.sleep(60)



