# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import MyFuncs as mf
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

# of note: dcc.Markdown("<Markdown>")

# Imports from this application
from app import app

model = mf.ncvs_small_model()
data = mf.ncvs_small(wrangle=True)

# 2 column layout. 1st column width = 3/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
		html.Div(style={'maxHeight': '400px', 'overflowY': 'scroll'}, 
				 children=[
							dcc.Markdown(
								"""
									## NCVS
									The National Crime Victimization Survey (NCVS) is a survey containing information on crime victims. 
									The original data contains over 100 variables per person, but for my purposes I removed 
									some features and added features I engineered from the other features.

									I wanted to know if income made people more likely to be a crime victim. So, I've trained a model
									on my post-wrangled dataset. 

									### Analysis
									Use this dropdown to see how each feature (after I removed and added features) correlates to income.
									It should be noted that this is only according to less than 1/400th the original number of participants,
									and that correlation is not causation. 

									"All models are wrong, but some are useful" - George Box
								"""
							),
							dcc.Dropdown(
								id='plot_against_income',
								options=[
									{'label': mf.dataDictionary[c]['Desc'], 'value': c} for c in data.columns],
								className='mb-5',
								value='EDUCATIONAL ATTAINMENT'
							),
							dcc.Markdown(
								"""
									### Predictions
									Use these sliders to generate a prediction for the variables you provide.

								"""
							)
				 ]),
		# model prediction input goes here
	],
    md=4
)

fig = px.scatter(data, x="YEAR", y="V2026", size_max=40)#, range_y=(0,15))


column2 = dbc.Col(
    [
		html.Div(id='analysis_content', className='lead')
    ]
)

layout = dbc.Row([column1, column2])

@app.callback(
	Output('analysis_content', 'children'),
	[Input('plot_against_income', 'value')]
)
def analyze(plot_against_income):
	column2 = dbc.Col(
    [
        #html.H2('Expected Income'),# className='mb-5'), 
		html.Div(id='analysis_content', className='lead')
	])

	graph = dcc.Graph(
		figure=px.density_heatmap(data, x=plot_against_income, y="V2026", title='Expected Income', height=450, width=450) #  size_max=20,
		# add point on plot for prediction output?
	)
	return graph

#
# [ ] change footer colour
# [ ] change font colour in footer
# [ ] change font colour for brand in header
# [ ] change font to Open Sans
# [ ] change icons for email and github in footer
# [ ] change header links to personal website
# [X] change scatterplot to heatmap
#