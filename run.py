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
navbar = dbc.NavbarSimple(
    brand='National Crime Victimization Survey, 1992-2016',
    brand_href='/', 
    children=[
		#html.Img(src='https://picsum.photos/200', alt='Random Image', height='30px'),
        #dbc.NavItem(dcc.Link('Predictions', href='/predictions', className='nav-link', style={'color': mf.colors['navbar-text-col']})), 
        #dbc.NavItem(dcc.Link('Insights', href='/insights', className='nav-link', style={'color': mf.colors['navbar-text-col']})), 
        #dbc.NavItem(dcc.Link('Process', href='/process', className='nav-link', style={'color': mf.colors['navbar-text-col']}))
    ],
    sticky='top',
    color=mf.colors['text'],
    light=False, 
    dark=True
)

# Footer docs:
# dbc.Container, dbc.Row, dbc.Col: https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
# html.P: https://dash.plot.ly/dash-html-components
# fa (font awesome) : https://fontawesome.com/icons/github-square?style=brands
# mr (margin right) : https://getbootstrap.com/docs/4.3/utilities/spacing/
# className='lead' : https://getbootstrap.com/docs/4.3/content/typography/#lead
footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P(
                [
                    html.Span('Maxie Lawrence', className='mr-2'),# color=mf.colors['footer-text-col']), 
                    html.A(html.I(className='fas fa-envelope-square mr-1'), href='mailto:max.alexander3721@gmail.com'), 
                    html.A(html.I(className='fab fa-github-square mr-1'), href='https://github.com/MaxTheMooshroom/Build-2')
                ], 
                className='lead'
            )
        )
		#color=mf.colors['footer-col']
    )
)

# Layout docs:
# html.Div: https://dash.plot.ly/getting-started
# dcc.Location: https://dash.plot.ly/dash-core-components/location
# dbc.Container: https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False), 
    navbar, 
    dbc.Container(id='page-content', className='mt-4'), 
    html.Hr(), 
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