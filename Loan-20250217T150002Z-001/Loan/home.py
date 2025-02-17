from dash import html, dcc, Dash, Input, Output, State

# Initialize Dash app
app = Dash(__name__)

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

# Generate HTML layout for home page
home_layout = html.Div([
    # Navigation
    html.Header([
        html.Div([
            # Left side - Brand and Search
            html.Div([
                html.Div([
                    html.H1("InvestMate", style={
                        'fontSize': '2.5rem',
                        'margin': '0',
                        'color': 'white',
                        'fontWeight': 'bold'
                    })
                ]),
                
              
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '30px'}),

            # Right side - Navigation Links
            html.Nav([
                dcc.Link("Home", href="/", style=STYLES['nav-link']),
                dcc.Link("Alerts", href="/portfolio", style=STYLES['nav-link']),
                dcc.Link("AI Recommendations", href="/suggest", style=STYLES['nav-link']),
                dcc.Link("Price Prediction", href="/calci", style=STYLES['nav-link']),
                dcc.Link("Volatility Analysis", href="/volatile", style=STYLES['nav-link']),
                dcc.Link("Data", href="/data", style=STYLES['nav-link']),
               
               

            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '20px'})
        ], style=STYLES['nav-content'])
    ], style=STYLES['nav-container']),

    # Hero Section
    html.Div([
        html.Div([
            html.H1("Smart Investment Decisions Start Here", style={
                'fontSize': '3.5rem',
                'color': 'white',
                'marginBottom': '30px',
                'fontWeight': 'bold',
            }),
            html.P("Make data-driven investment choices with our powerful analytics platform", style={
                'fontSize': '1.5rem',
                'color': 'rgba(255,255,255,0.9)',
                'marginBottom': '40px',
            }),
            html.Div([
                html.Button("Learn More", style={
                    **STYLES['button-primary'],
                    'marginRight': '20px',
                }),
                
            ], style={'display': 'flex', 'justifyContent': 'center', 'gap': '20px'}),
        ], style={
            'textAlign': 'center',
            'padding': '160px 20px 120px',
            'maxWidth': '800px',
            'margin': '0 auto',
        })
    ], style={
        'background': 'linear-gradient(135deg, #1a237e 0%, #0d47a1 100%)',
        'marginTop': '70px',
    }),
    

 # About Us Section with Image and Text Side by Side
    html.Div([
        html.Div([
            # Left side - Image
            html.Img(src="/assets/stock_analysis.jpg", alt="About Us Image", style={
                'width': '100%',
                'maxWidth': '500px',
                'borderRadius': '8px',
            }),
        ], style={
            'flex': '1',
            'paddingRight': '20px',
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
        }),

        html.Div([
            # Right side - Text
            html.H2("About Us", style={
                'fontSize': '2.5rem',
                'color': '#333',
                'marginBottom': '20px',
                'fontWeight': 'bold',
            }),
            html.P("InvestMate is a data-driven investment analytics platform designed to help investors make informed and smart decisions. Our powerful tools and insights enable you to manage your portfolio, analyze market trends, and predict the future of stocks with confidence.", style={
                'fontSize': '1.25rem',
                'color': '#555',
                'marginBottom': '30px',
            }),
            html.P("Our team of experts continuously works on integrating advanced analytics, machine learning algorithms, and real-time data to bring you the most reliable and actionable investment insights.", style={
                'fontSize': '1.25rem',
                'color': '#555',
            })
        ], style={
            'flex': '1',
            'paddingLeft': '20px',
            'display': 'flex',
            'flexDirection': 'column',
            'justifyContent': 'center',
        })
    ], style={
        'display': 'flex',
        'background': '#f4f4f4',
        'padding': '80px 20px',
        'borderTop': '1px solid #ddd',
    }),

 # Our Mission Section with Image and Text Side by Side
html.Div([
    html.Div([
        # Left side - Text
        html.Div([
            html.H2("Our Mission", style={
                'fontSize': '2.5rem',
                'color': '#333',
                'marginBottom': '10px',
                'fontWeight': 'bold',
            }),
            html.P("Our mission is to empower investors with the tools and insights they need to make informed and confident decisions in the stock market. We aim to democratize access to advanced financial analytics, making smart investment decisions accessible to everyone.", style={
                'fontSize': '1.25rem',
                'color': '#555',
                'marginBottom': '30px',
            }),
            html.P("By leveraging cutting-edge technology and deep market knowledge, we provide our users with personalized investment strategies and actionable insights that can help them achieve their financial goals.", style={
                'fontSize': '1.25rem',
                'color': '#555',
            })
        ], style={
            'flex': '1',
            'paddingLeft': '20px',
            'display': 'flex',
            'flexDirection': 'column',
            'justifyContent': 'center',
        }),

    ], style={
        'flex': '1',
        'paddingRight': '20px',
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
    }),

    html.Div([
        # Right side - Image
        html.Img(src="/assets/team.jpg", alt="Our Mission Image", style={
            'width': '100%',
            'maxWidth': '500px',
            'borderRadius': '8px',
        }),
    ], style={
        'flex': '1',
        'paddingLeft': '20px',
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
    }),

], style={
    'display': 'flex',
    'background': '#f4f4f4',
    'padding': '80px 20px',
    'borderTop': '1px solid #ddd',
}),

    # Features Section
    html.Section([
        html.H2("Why Choose InvestMate", style={
            'fontSize': '2.5rem',
            'textAlign': 'center',
            'marginBottom': '50px',
            'color': '#1a237e',
        }),
        html.Div([
            html.Div([
                html.H3("Real-Time Analytics", style={
                    'fontSize': '1.8rem',
                    'marginBottom': '20px',
                    'color': '#1a237e',
                }),
                html.P("Get instant insights into market trends and make informed decisions", style={
                    'color': '#666',
                    'lineHeight': '1.6',
                    'fontSize': '1.1rem',
                }),
            ], style=STYLES['card']),
            
            html.Div([
                html.H3("Portfolio Management", style={
                    'fontSize': '1.8rem',
                    'marginBottom': '20px',
                    'color': '#1a237e',
                }),
                html.P("Track and optimize your investments with professional-grade tools", style={
                    'color': '#666',
                    'lineHeight': '1.6',
                    'fontSize': '1.1rem',
                }),
            ], style=STYLES['card']),
            
            html.Div([
                html.H3("Smart Suggestions", style={
                    'fontSize': '1.8rem',
                    'marginBottom': '20px',
                    'color': '#1a237e',
                }),
                html.P("Receive personalized investment recommendations based on your goals", style={
                    'color': '#666',
                    'lineHeight': '1.6',
                    'fontSize': '1.1rem',
                }),
            ], style=STYLES['card']),
        ], style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'justifyContent': 'center',
            'gap': '30px',
            'margin': '40px 0',
        }),
    ], style=STYLES['container']),


    

    # Statistics Section
    html.Div([
        html.Div([
            html.Div([
                html.H3("1000+", style={
                    'fontSize': '3rem',
                    'color': '#1a237e',
                    'marginBottom': '10px',
                }),
                html.P("Stocks Analyzed", style={
                    'color': '#666',
                    'fontSize': '1.2rem',
                }),
            ], style={'textAlign': 'center', 'flex': '1'}),
            
            html.Div([
                html.H3("More", style={
                    'fontSize': '3rem',
                    'color': '#1a237e',
                    'marginBottom': '10px',
                }),
                html.P("Assets Analyzed", style={
                    'color': '#666',
                    'fontSize': '1.2rem',
                }),
            ], style={'textAlign': 'center', 'flex': '1'}),
            
            html.Div([
                html.H3("90%", style={
                    'fontSize': '3rem',
                    'color': '#1a237e',
                    'marginBottom': '10px',
                }),
                html.P("Success Rate", style={
                    'color': '#666',
                    'fontSize': '1.2rem',
                }),
            ], style={'textAlign': 'center', 'flex': '1'}),
        ], style={
            'display': 'flex',
            'justifyContent': 'space-around',
            'padding': '80px 20px',
            'maxWidth': '1200px',
            'margin': '0 auto',
        })
    ], style={'backgroundColor': '#f8f9fa'}),


   html.Div([
    html.H2("Gallery", style={
        'fontSize': '2.5rem',
        'color': '#333',
        'marginBottom': '20px',
        'fontWeight': 'bold',
        'textAlign': 'center',
    }),
    html.Div([
        # First Row with 3 images
        html.Div([
            html.Div([
                html.Img(src="/assets/predict.jpg", alt="Image 1", style={
                    'width': '100%',
                    'maxWidth': '250px',
                    'height': '250px',
                    'borderRadius': '8px',
                }),
                html.P("Price Prediction", style={
                    'textAlign': 'center',
                    'color': '#555',
                    'fontSize': '1.1rem',
                    'marginTop': '10px',
                }),
            ], style={'padding': '10px'}),
            html.Div([
                html.Img(src="/assets/live.jpg", alt="Image 2", style={
                    'width': '100%',
                    'maxWidth': '250px',
                    'height': '250px',
                    'borderRadius': '8px',
                }),
                html.P("Live Data", style={
                    'textAlign': 'center',
                    'color': '#555',
                    'fontSize': '1.1rem',
                    'marginTop': '10px',
                }),
            ], style={'padding': '10px'}),
            html.Div([
                html.Img(src="/assets/hu.jpg", alt="Image 3", style={
                    'width': '100%',
                    'maxWidth': '250px',
                    'height': '250px',
                    'borderRadius': '8px',
                }),
                html.P("World in Your Hand", style={
                    'textAlign': 'center',
                    'color': '#555',
                    'fontSize': '1.1rem',
                    'marginTop': '10px',
                }),
            ], style={'padding': '10px'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'flexWrap': 'wrap'}),

        # Second Row with 3 images
        html.Div([
            html.Div([
                html.Img(src="/assets/ai.jpg", alt="Image 4", style={
                    'width': '100%',
                    'maxWidth': '250px',
                    'height': '250px',
                    'borderRadius': '8px',
                }),
                html.P("Ai Recommendation", style={
                    'textAlign': 'center',
                    'color': '#555',
                    'fontSize': '1.1rem',
                    'marginTop': '10px',
                }),
            ], style={'padding': '10px'}),
            html.Div([
                html.Img(src="/assets/alert.jpg", alt="Image 5", style={
                    'width': '100%',
                    'maxWidth': '250px',
                    'height': '250px',
                    'borderRadius': '8px',
                }),
                html.P("Sending Alerts", style={
                    'textAlign': 'center',
                    'color': '#555',
                    'fontSize': '1.1rem',
                    'marginTop': '10px',
                }),
            ], style={'padding': '10px'}),
            html.Div([
                html.Img(src="/assets/mobile.jpg", alt="Image 6", style={
                    'width': '100%',
                    'maxWidth': '250px',
                    'height': '250px',
                    'borderRadius': '8px',
                }),
                html.P("Mobile Alerts", style={
                    'textAlign': 'center',
                    'color': '#555',
                    'fontSize': '1.1rem',
                    'marginTop': '10px',
                }),
            ], style={'padding': '10px'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'flexWrap': 'wrap'}),

    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'padding': '20px'}),
]),

html.Div([
    # Section Title
    html.H2("Our Services", style={
        'fontSize': '2.5rem',
        'color': '#333',
        'marginBottom': '20px',
        'fontWeight': 'bold',
        'textAlign': 'center',  # Center-align the title
    }),

    # Large Image Section
    html.Div([
        html.Img(src="/assets/ser.jpg", alt="Large Service Image", style={
            'width': '100%',
            'maxWidth': '600px',
            'borderRadius': '8px',
            'marginBottom': '40px',  # Space between the image and the paragraph
        }),
    ], style={'textAlign': 'center'}),  # Center-align the image

    # Paragraph Section
    html.Div([
        html.P("We provide a wide range of services designed to help you make smarter investment decisions. Our team of experts uses advanced analytics and machine learning to offer you actionable insights that can enhance your portfolio's performance. Whether you're looking for data-driven investment strategies, personalized recommendations, or the latest market trends, we have the tools and expertise to support your success.", style={
            'fontSize': '1.25rem',
            'color': '#555',
            'padding': '20px',
            'textAlign': 'center',  # Center-align the paragraph
            'maxWidth': '900px',
            'margin': '0 auto',  # Center the paragraph horizontally
        }),
    ]),
]),
    # Footer
    html.Footer([
        html.Div([
            html.Div([
                html.H4("InvestMate", style={
                    'color': 'white',
                    'marginBottom': '20px',
                    'fontSize': '1.5rem',
                }),
                html.P("Making investing accessible for everyone", style={
                    'color': 'rgba(255,255,255,0.8)',
                }),
            ], style={'flex': '1', 'minWidth': '250px'}),
            
            html.Div([
                html.H4("Quick Links", style={
                    'color': 'white',
                    'marginBottom': '20px',
                    'fontSize': '1.5rem',
                }),
                html.A("About Us", href="#", style={
                    'color': 'rgba(255,255,255,0.8)',
                    'display': 'block',
                    'marginBottom': '10px',
                    'textDecoration': 'none',
                }),
                html.A("Features", href="#", style={
                    'color': 'rgba(255,255,255,0.8)',
                    'display': 'block',
                    'marginBottom': '10px',
                    'textDecoration': 'none',
                }),
                html.A("Contact", href="#", style={
                    'color': 'rgba(255,255,255,0.8)',
                    'display': 'block',
                    'textDecoration': 'none',
                }),
            ], style={'flex': '1', 'minWidth': '250px'}),
        ], style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'gap': '40px',
            'maxWidth': '1200px',
            'margin': '0 auto',
            'padding': '60px 20px',
        }),
        html.Div("© 2024 InvestMate. All rights reserved.", style={
            'textAlign': 'center',
            'color': 'rgba(255,255,255,0.8)',
            'borderTop': '1px solid rgba(255,255,255,0.1)',
            'padding': '20px 0',
        }),
    ], style={
        'backgroundColor': '#1a237e',
        'marginTop': '80px',
    }),
])

# Set the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback for page routing
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/calci':
        return html.Div("Calculator Page Content", style={'marginTop': '80px'})
    elif pathname == '/portfolio':
        return html.Div("Portfolio Page Content", style={'marginTop': '80px'})
    elif pathname == '/suggest':
        return html.Div("Suggestions Page Content", style={'marginTop': '80px'})
    return home_layout

if __name__ == '__main__':
    app.run_server(debug=True)