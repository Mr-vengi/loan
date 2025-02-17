from dash import Dash, html, dcc, page_registry, page_container
from dash.dependencies import Input, Output
from home import home_layout  # Import home layout from home.py

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

# Define layout for the app
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # For handling page navigation

    # Page content dynamically rendered here (this is where other pages will appear)
    html.Div(id="page-content"),

    # Navigation links (Links are always visible on all pages, placed in a footer)
    html.Footer([
        html.Div([
            html.Div(
                dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"], target="_blank"),
            ) for page in page_registry.values()
        ], className="footer-links")
    ], className="footer")
])

# Callback to display home page only for the "/" route and hide it for other pages
@app.callback(
    Output("page-content", "children"),  # Dynamically change the page content
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/":
        return home_layout  # Return home layout for the home page
    else:
        return page_container  # Return dynamic page content for other routes

if __name__ == '__main__':
    app.run_server(debug=True)
    
