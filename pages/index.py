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
_data = mf.ncvs_small(wrangle=True)

zipped = zip([html.P(html.A(f"{mf.dataDictionary[col]['Desc']}", href=f"https://www.icpsr.umich.edu/icpsrweb/NACJD/studies/36834/_datasets/0003/variables/{col}?archive=nacjd", target='_blank')) for col in _data.columns], 
                    [html.Div(dcc.Slider(
                                 id=f"input-{i}", 
                                 step=1, 
                                 value=_data[col].dropna().astype(int).mode()[0], 
                                 min=mf.attempt(min, _data[col].dropna().astype(int)), 
                                 max=mf.attempt(max, _data[col].dropna().astype(int))
                                                            ) for i, col in enumerate(_data.columns.drop(['V2026'])) if len(_data[col].dropna()) > 0
                    )])

result = html.Div(id='predict_content', className='lead')

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
									on my post-wrangled _dataset. 

									### Analysis
									Use this dropdown to see how each feature (after I removed and added features) correlates to income.
									It should be noted that this is only according to less than 1/400th the original number of participants,
									and that correlation is not causation. 

									"All models are wrong, but some are useful"

									\- George Box
								"""
							),
							dcc.Dropdown(
								id='plot_against_income',
								options=[
									{'label': mf.dataDictionary[c]['Desc'], 'value': c} for c in _data.columns
                                ],
								className='mb-5',
								value='YEAR'
							),
							dcc.Markdown(
								"""
									### Predictions
									Use these sliders to generate a prediction for the variables you provide.
								"""
							),
		                    # model prediction input goes here
				 ] + [item for sublist in zipped for item in sublist] + 
                     [
                         html.H5("I guess the income bracket is: ")
                         #result
                     ])
	],
    md=4
)

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
    fig = px.density_heatmap(_data, x=plot_against_income, y="V2026", title='Expected Income', height=450, width=450, range_color=[0, 300]) # size_max=20,
    
    graph = dcc.Graph(
        figure=fig
		# add point on plot for prediction output?
    )
    return graph

@app.callback(
	Output('predict_content', 'children'),
	[
        Input(f"input-{i}", 'value')    for i in range(0, len(  _data.columns.drop(['V2026'])   )   )
    ]
)
def prediction(input_0, input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10, input_11, input_12, input_13, input_14, input_15, input_16, input_17, input_18, input_19, input_20, input_21, input_22, input_23, input_24, input_25, input_26, input_27, input_28, input_29, input_30, input_31, input_32, input_33, input_34, input_35, input_36, input_37, input_38, input_39, input_40, input_41, input_42, input_43, input_44, input_45, input_46, input_47, input_48, input_49, input_50, input_51, input_52, input_53, input_54, input_55, input_56, input_57, input_58, input_59, input_60, input_61, input_62, input_63, input_64, input_65, input_66, input_67):
    forest = model.named_steps['randomforestclassifier']
    num = mf.rprint(forest.predict([[input_0, input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10, input_11, input_12, input_13, input_14, input_15, input_16, input_17, input_18, input_19, input_20, input_21, input_22, input_23, input_24, input_25, input_26, input_27, input_28, input_29, input_30, input_31, input_32, input_33, input_34, input_35, input_36, input_37, input_38, input_39, input_40, input_41, input_42, input_43, input_44, input_45, input_46, input_47, input_48, input_49, input_50, input_51, input_52, input_53, input_54, input_55, input_56, input_57, input_58, input_59, input_60, input_61, input_62, input_63, input_64, input_65, input_66, input_67]]))
    return [0]

#
# [ ] change footer colour
# [ ] change font colour in footer
# [ ] change font colour for brand in header
# [ ] change font to Open Sans
# [ ] change icons for email and github in footer
# [ ] change header links to personal website
# [X] change scatterplot to heatmap
#