import dash
from dash import html, dcc, Input, Output
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import dash_core_components as dcc
import dash_html_components as html
from flask import Flask

from dash import dcc, html

import requests

server = Flask(__name__)
# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY])
app.config.suppress_callback_exceptions = True  # Allow callbacks for dynamic content

COLORS = {
    'primary': '#1A73E8',  # Blue
    'secondary': '#FF4081',  # Pink
    'background': '#F5F5F5',  # Light Grey
    'text': '#212121',  # Dark Grey
    'accent': '#FFC107',  # Amber
    'success': '#4CAF50',  # Green
    'warning': '#FF9800',  # Orange
    'danger': '#D32F2F',  # Red
    'info': '#2196F3',  # Light Blue
    'light': '#FFFFFF',  # White
    'dark': '#263238',  # Charcoal Grey
}


# Define the Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("", href="/dashboard", active=True)),
        dbc.NavItem(dbc.NavLink("", href="/portfolio")),
        dbc.NavItem(dbc.NavLink("", href="/market-analysis")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("", href="#"),
                dbc.DropdownMenuItem("", href="#"),
                dbc.DropdownMenuItem("", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="",
        ),
    ],
    brand="Stock Market Dashboard",
    brand_href="/dashboard",
    color="#000000",
    dark=True,
    className="mb-4",
    fluid=True
)

# Layouts for main app
dashboard_layout = html.Div([
    html.H1("Dashboard"),
    html.P("Welcome to the Dashboard."),
])

market_analysis_layout = html.Div([
    html.H1("Market Analysis"),
    html.P("Welcome to the Market Analysis page."),
])

# Main App Layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # Tracks the current URL
    navbar,
    html.Div(id="page-content"),  # Content based on the current URL
])



# Function to convert USD to INR
def usd_to_inr(usd_value):
    if pd.isna(usd_value):
        return 'N/A'
    try:
        # You can replace this with a more reliable forex API
        conversion_rate = 83.0  # Example fixed rate (you should use real-time rates)
        return usd_value * conversion_rate
    except:
        return 'N/A'

# Calculate technical indicators
def calculate_sma(data, window):
    return data.rolling(window=window).mean()

def calculate_rsi(data, periods=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Format large numbers in Indian format
def format_indian_number(number):
    if isinstance(number, str) or pd.isna(number):
        return 'N/A'
    try:
        s = str(int(number))
        if len(s) > 7:
            return f'₹{float(s[:-7]):.2f}Cr'
        elif len(s) > 5:
            return f'₹{float(s[:-5]):.2f}L'
        else:
            return f'₹{float(s):,.2f}'
    except:
        return 'N/A'

# Enhanced stock details function
def get_enhanced_stock_details(stock):
    info = stock.info
    
    # Get quarterly financials
    quarterly_cashflow = stock.quarterly_cashflow
    quarterly_financials = stock.quarterly_financials
    
    cashflow_metrics = {
        'Operating Cash Flow': quarterly_cashflow.loc['Total Cash From Operating Activities'].iloc[-1] if not quarterly_cashflow.empty else None,
        'Investing Cash Flow': quarterly_cashflow.loc['Total Cashflows From Investing Activities'].iloc[-1] if not quarterly_cashflow.empty else None,
        'Financing Cash Flow': quarterly_cashflow.loc['Total Cash From Financing Activities'].iloc[-1] if not quarterly_cashflow.empty else None,
    }
    
    financial_metrics = {
        'Revenue': quarterly_financials.loc['Total Revenue'].iloc[-1] if not quarterly_financials.empty else None,
        'Net Income': quarterly_financials.loc['Net Income'].iloc[-1] if not quarterly_financials.empty else None,
        'Operating Income': quarterly_financials.loc['Operating Income'].iloc[-1] if not quarterly_financials.empty else None,
    }
    
    return {
        'cashflow': cashflow_metrics,
        'financials': financial_metrics,
        'basic_info': info
    }

# Main layout
app.layout = html.Div([
    navbar,
    html.Div(id='ticker-tape', className='ticker-tape'),
    dbc.Container([
        # Header Section
        dbc.Row([
            dbc.Col([
                html.H1("Stock Market Dashboard", className="text-primary mb-4"),
            ], width=12)
        ]),

        # Stock Analysis Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Stock Analysis", className="card-title"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Stock Symbol:", className="font-weight-bold"),
                                dcc.Input(
                                    id='stock-input',
                                    value='RELIANCE.NS',  # Default to Reliance Industries
                                    type='text',
                                    className='form-control mb-3',
                                    placeholder='Enter NSE Symbol (e.g., RELIANCE.NS)'
                                ),
                            ], width=6),
                            dbc.Col([
                                html.Label("Timeframe:", className="font-weight-bold"),
                                dcc.Dropdown(
                                    id='timeframe-dropdown',
                                    options=[
                                        {'label': '1 Day', 'value': '1d'},
                                        {'label': '1 Week', 'value': '1wk'},
                                        {'label': '1 Month', 'value': '1mo'},
                                        {'label': '3 Months', 'value': '3mo'},
                                        {'label': '1 Year', 'value': '1y'},
                                    ],
                                    value='1mo',
                                    className='mb-3'
                                ),
                            ], width=6),
                        ]),
                        dcc.Graph(id='stock-price-chart'),
                        html.Div(id='technical-indicators', className="mt-3"),
                    ])
                ], className="mb-4")
            ], width=12)
        ]),
        
        # Financial Metrics Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("Financial Metrics", className="mb-0")
                    ]),
                    dbc.CardBody(id='key-metrics')
                ], className="mb-4")
            ], width=12)
        ]),
        
        # Trading Information and Volume Analysis
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Trading Statistics"),
                    dbc.CardBody(id='trading-stats')
                ])
            ], width=12, lg=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Volume Analysis"),
                    dbc.CardBody([
                        dcc.Graph(id='volume-chart')
                    ])
                ])
            ], width=12, lg=6)
        ], className="mb-4"),
        
        # Cash Flow Analysis Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("Cash Flow Analysis", className="mb-0")
                    ]),
                    dbc.CardBody(id='cash-flow-metrics')
                ], className="mb-4")
            ], width=12)
        ]),
        
        # Additional Analysis Tabs
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Detailed Analysis"),
                    dbc.CardBody([
                        dbc.Tabs([
                            dbc.Tab([
                                html.Div(id='balance-sheet-content', className="mt-3")
                            ], label="Balance Sheet"),
                            dbc.Tab([
                                html.Div(id='income-statement-content', className="mt-3")
                            ], label="Income Statement"),
                            dbc.Tab([
                                html.Div(id='ratio-analysis-content', className="mt-3")
                            ], label="Ratio Analysis")
                        ])
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # News Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("Latest Market News", className="mb-0")
                    ]),
                    dbc.CardBody(id='news-feed')
                ])
            ], width=12)
        ])
    ], fluid=True)
])

# First, add this function for stock news
def get_stock_news(symbol):
    try:
        stock = yf.Ticker(symbol)
        news = stock.news
        return news[:5]  # Return latest 5 news items
    except:
        return []

# Update the callback function
@app.callback(
    [Output('stock-price-chart', 'figure'),
     Output('volume-chart', 'figure'),
     Output('key-metrics', 'children'),
     Output('technical-indicators', 'children'),
     Output('trading-stats', 'children'),
     Output('cash-flow-metrics', 'children'),
     Output('balance-sheet-content', 'children'),
     Output('income-statement-content', 'children'),
     Output('ratio-analysis-content', 'children'),
     Output('news-feed', 'children')],
    [Input('stock-input', 'value'),
     Input('timeframe-dropdown', 'value')]
)
def update_dashboard(symbol, timeframe):
    try:
        stock = yf.Ticker(symbol)
        end_date = datetime.now()
        
        # Calculate date range
        if timeframe == '1d':
            start_date = end_date - timedelta(days=1)
            interval = '5m'
        elif timeframe == '1wk':
            start_date = end_date - timedelta(days=7)
            interval = '15m'
        elif timeframe == '1mo':
            start_date = end_date - timedelta(days=30)
            interval = '1d'
        elif timeframe == '3mo':
            start_date = end_date - timedelta(days=90)
            interval = '1d'
        else:  # 1y
            start_date = end_date - timedelta(days=365)
            interval = '1d'
            
        # Get historical data
        df = stock.history(start=start_date, end=end_date, interval=interval)
        if df.empty:
            raise Exception("No data available for this symbol")
            
        # Calculate technical indicators
        df['SMA_20'] = calculate_sma(df['Close'], 20)
        df['SMA_50'] = calculate_sma(df['Close'], 50)
        df['RSI'] = calculate_rsi(df['Close'])
        
        # Create price chart
        price_fig = go.Figure()
        price_fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC'
        ))
        
        price_fig.add_trace(go.Scatter(
            x=df.index, y=df['SMA_20'],
            name='SMA 20',
            line=dict(color='orange')
        ))
        
        price_fig.add_trace(go.Scatter(
            x=df.index, y=df['SMA_50'],
            name='SMA 50',
            line=dict(color='blue')
        ))
        
        price_fig.update_layout(
            title=f'{symbol} Stock Price',
            yaxis_title='Price (₹)',
            xaxis_title='Date',
            template='plotly_dark',
            height=600,
            paper_bgcolor=COLORS['background'],
            plot_bgcolor='rgba(0,0,0,0.1)'
        )
        
        # Volume chart
        volume_fig = go.Figure()
        volume_fig.add_trace(go.Bar(
            x=df.index,
            y=df['Volume'],
            name='Volume',
            marker_color=df['Close'].diff().apply(lambda x: COLORS['success'] if x > 0 else COLORS['accent'])
        ))
        
        volume_fig.update_layout(
            title=f'{symbol} Trading Volume',
            yaxis_title='Volume',
            xaxis_title='Date',
            template='plotly_dark',
            height=300,
            paper_bgcolor=COLORS['background'],
            plot_bgcolor='rgba(0,0,0,0.1)'
        )
        
        # Get stock info
        info = stock.info if hasattr(stock, 'info') else {}
        
        # Safe get function for stock info
        def safe_get(key, default='N/A'):
            value = info.get(key, default)
            if isinstance(value, (int, float)) and key not in ['priceToBook', 'priceToEarnings', 'profitMargins']:
                return f"₹{value:,.2f}" if value != 'N/A' else 'N/A'
            return value

        # Key Metrics
        key_metrics = html.Div([
            dbc.Row([
                dbc.Col([
                    html.H3(safe_get('currentPrice'), className="text-primary"),
                    html.P("Current Price", className="text-muted")
                ], width=4),
                dbc.Col([
                    html.H3(safe_get('marketCap'), className="text-info"),
                    html.P("Market Cap", className="text-muted")
                ], width=4),
                dbc.Col([
                    html.H3(str(safe_get('priceToBook')), className="text-warning"),
                    html.P("Price to Book", className="text-muted")
                ], width=4)
            ])
        ])
        
        # Technical Indicators
        technical_indicators = dbc.Card([
            dbc.CardBody([
                html.H5("Technical Indicators", className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        html.P(f"RSI (14): {df['RSI'].iloc[-1]:.2f}" if not df.empty else "N/A")
                    ], width=4),
                    dbc.Col([
                        html.P(f"20-day SMA: ₹{df['SMA_20'].iloc[-1]:.2f}" if not df.empty else "N/A")
                    ], width=4),
                    dbc.Col([
                        html.P(f"50-day SMA: ₹{df['SMA_50'].iloc[-1]:.2f}" if not df.empty else "N/A")
                    ], width=4)
                ])
            ])
        ])
        
        # Trading Statistics
        trading_stats = html.Div([
            dbc.Row([
                dbc.Col([
                    html.H5(safe_get('dayHigh')),
                    html.P("Day High", className="text-muted")
                ], width=6),
                dbc.Col([
                    html.H5(safe_get('dayLow')),
                    html.P("Day Low", className="text-muted")
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5(str(safe_get('volume'))),
                    html.P("Volume", className="text-muted")
                ], width=6),
                dbc.Col([
                    html.H5(str(safe_get('averageVolume'))),
                    html.P("Avg Volume", className="text-muted")
                ], width=6)
            ])
        ])
        
        # Get financial data
        quarterly_financials = stock.quarterly_financials if hasattr(stock, 'quarterly_financials') else pd.DataFrame()
        quarterly_balance_sheet = stock.quarterly_balance_sheet if hasattr(stock, 'quarterly_balance_sheet') else pd.DataFrame()
        quarterly_cashflow = stock.quarterly_cashflow if hasattr(stock, 'quarterly_cashflow') else pd.DataFrame()
        
        # Safe get function for financial data
        def safe_get_financial(df, key, default='N/A'):
            try:
                value = df.loc[key].iloc[0] if not df.empty and key in df.index else default
                return f"₹{value:,.2f}Cr" if isinstance(value, (int, float)) else 'N/A'
            except:
                return 'N/A'
        
        # Cash Flow Metrics
        cash_flow_metrics = html.Div([
            dbc.Row([
                dbc.Col([
                    html.H5(safe_get_financial(quarterly_cashflow, 'Total Cash From Operating Activities')),
                    html.P("Operating Cash Flow", className="text-muted")
                ], width=4),
                dbc.Col([
                    html.H5(safe_get_financial(quarterly_cashflow, 'Total Cashflows From Investing Activities')),
                    html.P("Investing Cash Flow", className="text-muted")
                ], width=4),
                dbc.Col([
                    html.H5(safe_get_financial(quarterly_cashflow, 'Total Cash From Financing Activities')),
                    html.P("Financing Cash Flow", className="text-muted")
                ], width=4)
            ])
        ])
        
        # Balance Sheet
        balance_sheet = html.Div([
            dbc.Row([
                dbc.Col([
                    html.H5(safe_get_financial(quarterly_balance_sheet, 'Total Assets')),
                    html.P("Total Assets", className="text-muted")
                ], width=4),
                dbc.Col([
                    html.H5(safe_get_financial(quarterly_balance_sheet, 'Total Liabilities')),
                    html.P("Total Liabilities", className="text-muted")
                ], width=4),
                dbc.Col([
                    html.H5(safe_get_financial(quarterly_balance_sheet, 'Total Stockholder Equity')),
                    html.P("Stockholder Equity", className="text-muted")
                ], width=4)
            ])
        ])
        
        # Income Statement
        income_statement = html.Div([
            dbc.Row([
                dbc.Col([
                    html.H5(safe_get_financial(quarterly_financials, 'Total Revenue')),
                    html.P("Total Revenue", className="text-muted")
                ], width=4),
                dbc.Col([
                    html.H5(safe_get_financial(quarterly_financials, 'Gross Profit')),
                    html.P("Gross Profit", className="text-muted")
                ], width=4),
                dbc.Col([
                    html.H5(safe_get_financial(quarterly_financials, 'Net Income')),
                    html.P("Net Income", className="text-muted")
                ], width=4)
            ])
        ])
        
        # Ratio Analysis
        ratio_analysis = html.Div([
            dbc.Row([
                dbc.Col([
                    html.H5(str(safe_get('priceToEarnings'))),
                    html.P("P/E Ratio", className="text-muted")
                ], width=4),
                dbc.Col([
                    html.H5(f"{safe_get('profitMargins', 0):.2%}" if safe_get('profitMargins', 0) != 'N/A' else 'N/A'),
                    html.P("Profit Margin", className="text-muted")
                ], width=4),
                dbc.Col([
                    html.H5(str(safe_get('debtToEquity'))),
                    html.P("Debt to Equity", className="text-muted")
                ], width=4)
            ])
        ])
        
        # News Feed
        news = get_stock_news(symbol)
        news_items = [
            dbc.ListGroupItem([
                html.H6(item.get('title', 'No title')),
                html.Small(datetime.fromtimestamp(item.get('providerPublishTime', 0)).strftime('%Y-%m-%d %H:%M:%S'))
            ]) for item in news if item.get('title') and item.get('providerPublishTime')
        ]
        news_feed = dbc.ListGroup(news_items) if news_items else html.P("No recent news available")
        
        return price_fig, volume_fig, key_metrics, technical_indicators, trading_stats, \
               cash_flow_metrics, balance_sheet, income_statement, ratio_analysis, news_feed
               
    except Exception as e:
        print(f"Error: {str(e)}")
        empty_chart = go.Figure()
        empty_chart.update_layout(
            title="No Data Available",
            height=400
        )
        error_message = html.P(f"Error: {str(e)}" if str(e) != "" else "Error fetching data")
        return empty_chart, empty_chart, error_message, error_message, error_message, \
               error_message, error_message, error_message, error_message, error_message

# Update ticker callback with error handling
@app.callback(
    Output('ticker-tape', 'children'),
    Input('ticker-tape', 'id')
)



def update_ticker(_):
    tickers = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
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

    ticker_data = []  # Initialize ticker_data as an empty list to avoid errors
    
    for symbol in tickers:
        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period='1d')
            if not df.empty:
                current_price = df['Close'].iloc[-1]
                df_prev = stock.history(period='2d')
                if len(df_prev) >= 2:
                    change = ((df_prev['Close'].iloc[-1] - df_prev['Close'].iloc[-2]) / 
                             df_prev['Close'].iloc[-2] * 100)
                    color = 'green' if change > 0 else 'red'
                    ticker_data.append(
                        html.Span([
                            f"{symbol}: ₹{current_price:.2f} ",
                            html.Span(f"({change:+.2f}%)", style={'color': color}),
                            " | "
                        ])
                    )
        except:
            continue
    
    return ticker_data if ticker_data else html.P("")

if __name__ == '__main__':
    app.run_server(debug=True)
    