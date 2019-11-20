# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import MyFuncs as mf

# of note: dcc.Markdown("<Markdown>")

# Imports from this application
from app import app

# 2 column layout. 1st column width = 3/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Your Value Proposition

            Emphasize how the app will benefit users. Don't emphasize the underlying technology.

            ✅ RUN is a running app that adapts to your fitness levels and designs personalized workouts to help you improve your running.

            ❌ RUN is the only intelligent running app that uses sophisticated deep neural net machine learning to make your run smarter because we believe in ML driven workouts.

            """
        ),
        dcc.Link(dbc.Button('Your Call To Action', color='primary'), href='/predictions')
    ],
    md=3,
)

ncvs = mf.ncvs_small()
fig = px.scatter(ncvs, x="YEAR", y="V2026", size="pop", size_max=60)

column2 = dbc.Col(
    [
        dcc.Graph(figure=fig),
    ]
)

layout = dbc.Row([column1, column2])