import dash
from dash import html, dcc, register_page, callback
import plotly.graph_objects as go
import yfinance as yf
import numpy as np


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
register_page(__name__, name="Volatile",path='/volatile' )

title = "Stock Market Analytics Dashboard"

# List of predefined stock tickers for the dropdown
stock_options = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
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
    'TVSMOTOR.NS', 'UBL.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'UNITDSPR ( MCD).NS', 'VEDL.NS', 'VOLTAS.NS', 'WIPRO.NS', 'ZEEL.NS', 'ZYDUSLIFE.NS'
]

# Define layout
#Enhanced layout with navigation
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
                    
                    
                    
                ]
            )
        ]
    ),

    # Main Container
    html.Div([
        # Header Section
        html.Div([
            
            html.P("Advanced analytics for informed investment decisions", 
                   style={'textAlign': 'center', 'color': '#666', 'fontSize': '1.2rem', 'marginBottom': '30px'})
        ]),

        # Stock Selection Card
        html.Div([
            html.Div([
                html.H3("Select Stock", style={'color': '#1a237e', 'marginBottom': '20px'}),
                dcc.Dropdown(
                    id='volatility-ticker',
                    options=stock_options,
                    value='AAPL',
                    style={'marginBottom': '20px'}
                ),
                dcc.DatePickerRange(
                    id='volatility-date-picker',
                    start_date='2023-01-01',
                    end_date='2024-01-01',
                    display_format='YYYY-MM-DD',
                    style={'marginBottom': '20px'}
                ),
            ], style=STYLES['card'])
        ]),

        # Analysis Section
        html.Div([
            # Volatility Analysis Card
            html.Div([
                html.H3("Volatility Analysis", style={'color': '#1a237e', 'marginBottom': '20px'}),
                html.Button(
                    'Analyze Volatility',
                    id='volatility-btn',
                    n_clicks=0,
                    style=STYLES['button-primary']
                ),
                html.Div(id='volatility-output', 
                         style={'margin': '20px 0', 'padding': '15px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),
                dcc.Graph(id='volatility-graph')
            ], style=STYLES['card']),

            # VaR Analysis Card
            html.Div([
                html.H3("Value at Risk (VaR)", style={'color': '#1a237e', 'marginBottom': '20px'}),
                html.Button(
                    'Calculate VaR',
                    id='var-btn',
                    n_clicks=0,
                    style=STYLES['button-primary']
                ),
                html.Div(id='var-output',
                         style={'margin': '20px 0', 'padding': '15px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),
                dcc.Graph(id='var-graph')
            ], style=STYLES['card'])
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px', 'marginTop': '20px'}),

    ], style=STYLES['container']),

    # Footer
    html.Footer([
        html.Div([
            html.Div([
                html.H4("Market Risk Analytics", style={'color': 'white', 'marginBottom': '15px'}),
                html.P("Advanced stock market analysis tools for modern investors",
                       style={'color': 'rgba(255,255,255,0.7)'})
            ]),
            html.Div([
                html.H4("Quick Links", style={'color': 'white', 'marginBottom': '15px'}),
                html.A("About", href="#", style={'color': 'rgba(255,255,255,0.7)', 'display': 'block', 'marginBottom': '5px'}),
                html.A("Contact", href="#", style={'color': 'rgba(255,255,255,0.7)', 'display': 'block', 'marginBottom': '5px'}),
                html.A("Terms", href="#", style={'color': 'rgba(255,255,255,0.7)', 'display': 'block', 'marginBottom': '5px'})
            ]),
            html.Div([
                html.P("© 2024 Market Risk Analytics. All rights reserved.",
                       style={'color': 'rgba(255,255,255,0.7)', 'textAlign': 'center'})
            ])
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'maxWidth': '1200px', 'margin': '0 auto', 'padding': '40px 20px'})
    ], style={'backgroundColor': '#1a237e', 'marginTop': '50px'})
])

@callback(
    [dash.dependencies.Output('volatility-output', 'children'),
     dash.dependencies.Output('volatility-graph', 'figure'),
     dash.dependencies.Output('var-output', 'children'),
     dash.dependencies.Output('var-graph', 'figure')],
    [dash.dependencies.Input('volatility-btn', 'n_clicks'),
     dash.dependencies.Input('var-btn', 'n_clicks')],
    [dash.dependencies.State('volatility-ticker', 'value'),
     dash.dependencies.State('volatility-date-picker', 'start_date'),
     dash.dependencies.State('volatility-date-picker', 'end_date')]
)
def update_analysis(volatility_clicks, var_clicks, ticker, start_date, end_date):
    # Initialize default outputs
    volatility_output = ""
    var_output = ""
    volatility_figure = {}
    var_figure = {}

    # Volatility Analysis
    if volatility_clicks > 0:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        stock_data['Returns'] = stock_data['Adj Close'].pct_change()
        volatility = stock_data['Returns'].std() * np.sqrt(252)  # Annualized Volatility
        volatility_output = f"Annualized Volatility for {ticker}: {volatility:.4f}\n\n" \
                            "A higher value indicates more significant price fluctuations, representing higher risk."

        # Volatility Visualization: Bar chart of daily returns
        volatility_figure = {
            'data': [go.Bar(x=stock_data.index, y=stock_data['Returns'], name='Daily Returns')],
            'layout': go.Layout(
                title=f"{ticker} Daily Returns (Volatility)",
                xaxis_title="Date",
                yaxis_title="Daily Returns",
                showlegend=False
            )
        }

    # VaR Analysis
    if var_clicks > 0:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        stock_data['Returns'] = stock_data['Adj Close'].pct_change()
        var = stock_data['Returns'].quantile(0.05)  # 5% quantile for VaR
        var_output = f"Value-at-Risk (VaR) for {ticker}: {abs(var):.4f}\n\n" \
                     "This value represents the maximum expected loss with 95% confidence. A higher absolute VaR suggests higher potential risk."

        # VaR Visualization
        var_figure = {
            'data': [go.Histogram(x=stock_data['Returns'].dropna(), nbinsx=50, name='Returns')],
            'layout': go.Layout(
                title=f"{ticker} Returns Distribution (VaR Highlighted)",
                xaxis_title="Returns",
                yaxis_title="Frequency",
                shapes=[
                    # Vertical line for VaR
                    dict(type="line", x0=var, x1=var, y0=0, y1=1, xref='x', yref='paper', line=dict(color="red", dash="dash"))
                ],
                annotations=[
                    dict(x=var, y=0.95, xref="x", yref="paper", text=f"VaR: {var:.4f}", showarrow=True, arrowhead=2, ax=20, ay=-30)
                ]
            )
        }

    return volatility_output, volatility_figure, var_output, var_figure
