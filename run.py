# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

# Imports from this application
from app import app, server
from pages import index, predictions, insights, process
import MyFuncs as mf

# Navbar docs: https://dash-bootstrap-components.opensource.faculty.ai/l/components/navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand(
                [
                    html.Span("National Crime Victimization Survey, 1992-2016", 
                              style={
                                  "color": mf.colors['navbar-text-col'],
                                  "font-family": "Open-Sans"
                                  })
                ]
            )
        ]
    ),
    sticky='top',
    color=mf.colors['navbar-col']
)

# Footer docs:
# dbc.Container, dbc.Row, dbc.Col: https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
# html.P: https://dash.plot.ly/dash-html-components
# fa (font awesome) : https://fontawesome.com/icons/github-square?style=brands
# mr (margin right) : https://getbootstrap.com/docs/4.3/utilities/spacing/
# className='lead' : https://getbootstrap.com/docs/4.3/content/typography/#lead
footer = dbc.Navbar(
    dbc.Row(
        dbc.Col(
            html.P(
                [
                html.Span('Maxie Lawrence', className=' mr-2'),# color=mf.colors['footer-text-col']), 
                    html.A(html.I(className='fas fa-envelope-square mr-1'), href='mailto:max.alexander3721@gmail.com'), 
                    html.A(html.I(className='fab fa-github-square mr-1'), href='https://github.com/MaxTheMooshroom/unit-2-build')
                ], 
                className='lead'
            )
        ),
        style={'backgroundColor':mf.colors['navbar-col'], 'color':mf.colors['footer-text-col'], 'font-family': 'Open-Sans'}
    ),
    sticky='bottom'
)

# Layout docs:
# html.Div: https://dash.plot.ly/getting-started
# dcc.Location: https://dash.plot.ly/dash-core-components/location
# dbc.Container: https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False), 
    navbar, 
    dbc.Container(id='page-content', className='mt-4'), 
    html.Hr(style={'backgroundColor':mf.colors['navbar-col'], 'color':mf.colors['footer-text-col'], 'font-family': 'Open-Sans'}), 
    footer
])


# URL Routing for Multi-Page Apps: https://dash.plot.ly/urls
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
#    if pathname == '/':
#        return index.layout
#    elif pathname == '/predictions':
#        return predictions.layout
#    elif pathname == '/insights':
#        return insights.layout
#    elif pathname == '/process':
#        return process.layout
#    else:
#        return dcc.Markdown('## Page not found')
    return index.layout

# Run app server: https://dash.plot.ly/getting-started
if __name__ == '__main__':
    app.run_server(debug=True)