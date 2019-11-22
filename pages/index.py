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
import numpy as np
import pandas as pd

# of note: dcc.Markdown("<Markdown>")

# Imports from this application
from app import app

model = mf.ncvs_small_model()
_data = mf.ncvs_small(wrangle=True)



sliders = [html.Div(dcc.Slider(
                                id=f"input-{i}", 
                                step=1, 
                                value=_data[col].dropna().astype(int).mode()[0],
                                min=min(_data[col].dropna().astype(int)), 
                                max=max(_data[col].dropna().astype(int))
                           ), style={'maxWidth': '450px'}, className='col-md-9') 
           for i, col in enumerate(_data.columns.drop(['V2026']))]

zipped = zip([html.P(html.A(f"{mf.dataDictionary[col]['Desc']}", 
                            href=f"https://www.icpsr.umich.edu/icpsrweb/NACJD/studies/36834/_datasets/0003/variables/{col}?archive=nacjd", 
                            target='_blank')) 
             for col in _data.columns], 
             sliders
             )

flatten = [item for sublist in zipped for item in sublist]

#slider_vals = html.Div(id='slider-vals', children=[0]*len(flatten))

#zipped = zip(flatten, slider_vals.children)

#flatten = [item for sublist in zipped for item in sublist]

# 2 column layout. 1st column width = 3/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
		html.Div(style={'maxHeight': '300px', 'overflowY': 'scroll'}, 
				 children=[
							dcc.Markdown(
								"""
									## NCVS
									The National Crime Victimization Survey (NCVS) is a survey containing information on crime victims. 
									The original data contains over 100 variables per recorded incident, but for my purposes I removed 
									some features and added features I engineered from the other features. 

									Following that, I measured feature importance by taking all of the values in a column and swapping them, 
									and sorting by how much the accuracy score changed for each feature.

									I wanted to know if income made people more likely to be a crime victim. So, I've trained a model
									on my post-wrangled dataset. 

									### Analysis
									Use this dropdown to see how each feature (after I removed a lot of features) correlates to income.
									It should be noted both that this is only according to less than 1 / 400th the original number 
									of data samples, and that correlation is not causation. 

									"All models are wrong, but some are useful"

									\- George Box
								"""
							),
							dcc.Dropdown(
								id='plot_against_income',
								options=[
									{'label': mf.dataDictionary[c]['Desc'], 'value': c} for c in _data.columns.drop(['V2026'])
                                ],
								className='mb-5',
								value='YEAR'
							),
							dcc.Markdown(
								"""
									### Predictions
									Since I'm attempting to predict the income bracket feature, and the feature is categorical,
									it's reasonable to just assume that all income brackets are the same as the income bracket
									that occurs most frequently, to establish a baseline. 
									
									In this case, that is bracket 14, which represents making $75,000 and over per year.
									That bracket occurs 26% of the time, making that my baseline accuracy to beat. 
									
									Now, let's go ahead and go back and look at how I trained it and how to improve it.
									First, I needed to fill in missing values. Filling in missing values like this is called imputing. 
									By default, it uses mean to fill in gaps for a feature. However, since these are all categorical 
									features, all of them require mode instead. 
									
									After that, I trained a bunch of decision trees. More that one decision tree is called a 
									forest, and you make predictions by asking each tree what it thinks and averaging the predictions.
									
									After some feature selection, I've narrowed the pool of important features down to 15 features.
									After training the model, I have an accuracy of 43%, for an improvement of 17%.
									
									From here, to make a prediction, all that you have to do is provide values for those features. 
									Use these sliders to generate a prediction for the variables you provide. These values are
									defaulted to the mode of the feature. 
								"""
							),
				 ] + flatten)
	] + [dbc.Row([
            dbc.Col([
                html.H5("I predict the income bracket is: "),
                html.Div(id='predict_content', className='lead')]
            ),
            dbc.Col([
                html.H5("With a confidence of: "),
                html.Div(id='predict_confidence', className='lead')]
            )]
        )],
    md=6
)

column2 = dbc.Col(
    [
		html.Div(id='analysis_content', className='lead', style={'textAlign': 'center'})
    ]
)

layout = dbc.Row([column1, column2])

def heatmap_z(hm):
    counts = {}
    x = pd.Series(hm.data[0].x)
    y = pd.Series(hm.data[0].y)

    for zipped in zip(x,y):
        if zipped not in counts.keys():
            counts[zipped] = 1
        else:
            counts[zipped] += 1
    return counts

def heatmap_z_min_max(hm):
    counts = heatmap_z(hm)

    #print(f"Min: {min(counts.values())}\nMax: {max(counts.values())}")
    return list((min(counts.values()), max(counts.values())))


@app.callback(
	Output('analysis_content', 'children'),
	[Input('plot_against_income', 'value')]
)
def analyze(plot_against_income):
    fig = px.density_heatmap(_data, x=plot_against_income, y="V2026")
    fig = px.density_heatmap(_data, x=plot_against_income, y="V2026", title='<b>Expected Income</b>\r\n(Hover for details)', height=400, width=400, nbinsx=pd.Series(_data[plot_against_income]).nunique(), nbinsy=pd.Series(_data['V2026']).nunique(), range_color=heatmap_z_min_max(fig))
    fig.layout['xaxis']['title']['text'] = mf.dataDictionary[plot_against_income]['Desc'].capitalize()
    fig.layout['yaxis']['title']['text'] = 'Income Bracket'
    fig.layout['coloraxis']['colorbar']['title']['text'] = 'Count'
    graph = dcc.Graph(
        figure=fig
    )
    return graph

empty = html.Div(id='hidden-div', style={'display':'none'})

@app.callback(
	Output('predict_content', 'children'),
	[
        Input(f"input-{i}", 'value') for i in range(0, len(_data.columns.drop(['V2026'])))
    ]
)
def prediction_val(input_0, input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10, input_11, input_12, input_13, input_14):
    forest = model.named_steps['randomforestclassifier']
    num = forest.predict([[input_0, input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10, input_11, input_12, input_13, input_14]])
    return num

@app.callback(
	Output('predict_confidence', 'children'),
	[
        Input(f"input-{i}", 'value') for i in range(0, len(_data.columns.drop(['V2026'])))
    ]
)
def prediction_proba(input_0, input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10, input_11, input_12, input_13, input_14):
    forest = model.named_steps['randomforestclassifier']
    confidence = forest.predict_proba([[input_0, input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10, input_11, input_12, input_13, input_14]])
    return f"{max(confidence[0]) * 100:.2f}%"


@app.callback(
	Output('slider-vals', 'children'),
	[
        Input(f"input-{i}", 'value') for i in range(0, len(_data.columns.drop(['V2026'])))
    ]
)
def prediction_proba(input_0, input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10, input_11, input_12, input_13, input_14):
    return [input_0, input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10, input_11, input_12, input_13, input_14]

#
# MUST FIXES:
# [X] fix colour range in heatmaps
# [X] display prediction value and probability
# [X] write 300 words according to rubric
#
# NICE FIXES:
# [ ] change footer colour
# [X] change font colour in footer
# [X] change font colour for brand in header
# [X] change font to Open Sans
# [ ] change icons for email and github in footer
# [ ] change header links to personal website
# [X] change scatterplot to heatmap
# [ ] add labels to the sliders to show current value
#