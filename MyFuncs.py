import pandas as pd
import numpy as np
import plotly.graph_objs as go
import pickle

def sample_data(df, n_samples=None, output=False):
	if n_samples is None:
		n_samples = len(df.index) / 10

	interval = int(len(df.index) / n_samples)

	sample = pd.DataFrame(columns=df.columns)

	for i, _ in enumerate(df.index):
		if i % interval == 0 and i / interval <= n_samples:
			print(f"{i / interval} / {n_samples}")
			sample = sample.append(df.iloc[i])

	return sample

def reduce_mem_usage(df, output=False, n_samples=None):
	""" iterate through all the columns of a dataframe and modify the data type
        to reduce memory usage.        
	"""
	if n_samples is not None:
		df = sample_data(df, n_samples, output)

	if output is True:
		start_mem = df.memory_usage().sum() / 1024**2
		print(f'Memory usage of dataframe is {start_mem:.2f} MB / {start_mem/1024:.2f} GB')

	for col in df:
		col_type = df[col].dtype

		if col_type != object:
			c_min = df[col].min()
			c_max = df[col].max()
			if str(col_type)[:3] == 'int':
				if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
					df[col] = df[col].astype(np.int8)
				elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
					df[col] = df[col].astype(np.int16)
				elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
					df[col] = df[col].astype(np.int32)
				elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
					df[col] = df[col].astype(np.int64)  
			else:
				if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
					df[col] = df[col].astype(np.float16)
				elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
					df[col] = df[col].astype(np.float32)
				else:
					df[col] = df[col].astype(np.float64)
		else:
			df[col] = df[col].astype('category')

	if output is True:
		end_mem = df.memory_usage().sum() / 1024**2
		print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
		print('Decreased by {:.1f}%\n'.format(100 * (start_mem - end_mem) / start_mem))

	return df

def import_data(file, dtypes=None, delimiter = None, encoding=None, output=False, index_col=None, n_samples=None, **kwargs):
	"""
	Create a dataframe and optimize its memory usage
	"""
	if output is True:
		print("\nLoading DataFrame...\n")
	
	df = pd.read_csv(file, dtype=dtypes, parse_dates=True, keep_date_col=True, delimiter=delimiter, encoding=encoding,index_col=index_col)

	if output is True:
		print("\nDataFrame Loaded\n")

	return reduce_mem_usage(df, output=output, n_samples=n_samples, **kwargs)

def ncvs_small(n_samples=None, output=False):
	return import_data('files/ncvs_small.csv', n_samples=n_samples, output=output)

colors = {	# taken directly from my site
			'text': '#404040',
			'navbar-col': "#3C2934",
			'navbar-text-col': "#908197",
			'navbar-children-col': "#3C2934",
			'page-col': "#F4F7F6",
			'link-col': "#AB4056",
			'hover-col': "#C28768",
			'footer-col': "#3C2934",
			'footer-text-col': "#908197",
			'footer-link-col': "#AB4056"
}

def default_layout():
	return {
			'title': 'Data Visualization',
			'plot_bgcolor': colors['page-col'],
			'paper_bgcolor': colors['page-col'],
			'font': {
				'color': colors['text']
			}
	}

def change_attributes(dicIn, dic_new):
	for key in dic_new.keys():
		dicIn[key] = dic_new[key]
	return dicIn

def ncvs_small_model():
	return pickle.load(open('model.sav', 'rb'))
