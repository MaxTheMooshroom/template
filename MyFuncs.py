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

def import_data(file, dtypes=None, delimiter = None, encoding=None, output=False, index_col=None, n_samples=None, columns_to_keep=None, **kwargs):
	"""
	Create a dataframe and optimize its memory usage
	"""
	if output is True:
		print("\nLoading DataFrame...\n")
	
	df = pd.read_csv(file, dtype=dtypes, parse_dates=True, keep_date_col=True, delimiter=delimiter, encoding=encoding,index_col=index_col)

	if columns_to_keep is not None:
		df = df[columns_to_keep]

	if output is True:
		print("\nDataFrame Loaded\n")

	return reduce_mem_usage(df, output=output, n_samples=n_samples, **kwargs)

cols_to_keep = ['YEAR', 'V2015', 'V2021', 'V2022', 'V2024', 'V2078', 
        'V2119', 'V2120', 'V2122', 'V2126B', 'V2127B', 'V2129', 
        'V2130', 'V3006', 'V3013', 'V3015', 'V3017', 'V3019', 'V3020', 
        'V3021', 'V3024', 'V3028', 'V3029', 'V3030', 'V3031', 'V3033', 'V3034', 
        'V3035', 'V3036', 'V3037', 'V3038', 'V3039', 'V3040', 'V3041', 'V3042', 
        'V3043', 'V3044', 'V3045', 'V3046', 'V3047', 'V3048', 'V3049', 'V3050', 
        'V3052', 'V3053', 'V3054', 'V3055', 'V3056', 'V3058', 
        'V3059', 'V3_V4526H3A', 'V3_V4526H3B', 'V3_V4526H5', 'V3_V4526H4', 
        'V3_V4526H6', 'V3_V4526H7', 'V3071', 'V3072', 'V3073', 'V3074', 'V3075', 
        'V3076', 'V3077', 'V3078', 'V3079', 'V3081', 
        'VFLAG', 'VTYPE', 'RECENTLY_MARRIED', 'RECENTLY_SINGLE', 'V2026']

def ncvs_small(n_samples=None, output=False, wrangle=False):

    df = import_data('assets/files/ncvs_small.csv', n_samples=n_samples, output=output)

    if wrangle is True:
        for col in df.columns:
            for k in dataDictionary[col]['Null']:
                df[col] = df[col].where(df[col] != k, None)

        df['RECENTLY_MARRIED'] = ((df['V3015'] == 1) & (df['V3016'] != 1) & (df['V3016'] != None))
        df['RECENTLY_SINGLE'] = ((df['V3015'] != 1) & (df['V3015'] != None) & (df['V3016'] == 1))

    df = df[cols_to_keep]
    
    return df

dataDictionary = {"YEAR": 
                          {"Desc": "YEAR",
                           "Null": []}, 
                  "YEARQ": 
                          {"Desc": "YEAR AND QUARTER OF INTERVIEW (YYYY.Q)",
                           "Null": []}, 
                  "IDHH": 
                          {"Desc": "NCVS ID FOR HOUSEHOLDS",
                           "Null": []}, 
                  "V2015": 
                          {"Desc": "TENURE (ALLOCATED)",
                           1: "Owned or being bought",
                           2: "Rented for cash",
                           3: "No cash rent",
                           8: "Residue",
                           9: "Out of universe",
                           "Null": [8,9]},
                  "V2021": 
                          {"Desc": "TYPE OF LIVING QUARTERS (ALLOCATED)",
                           1: "House, apartment, flat",
                           2: "Housing unit in nontransient hotel, motel, etc.",
                           3: "Housing unit permanent in transient hotel, motel, etc",
                           4: "Housing unit in rooming house",
                           5: "Mobile home or trailer with no permanent room added",
                           6: "Mobile home or trailer with one or more permanent rooms added",
                           7: "Housing unit not specified above",
                           8: "Quarters not housing unit in rooming or boarding house",
                           9: "Unit not permanent in transient hotel, motel, etc.",
                           10: "Unoccupied site for mobile home, trailer, or tent",
                           11: "Student quarters in college dormitory",
                           12: "Other unit not specified above",
                           98: "Residue",
                           99: "Out of Universe",
                           "Null": [98,99]},
                  "V2022": 
                          {"Desc": "LOCATION OF PHONE",
                           1: "Phone in unit",
                           2: "Phone in common area (hallway, etc.)",
                           3: "Phone in another unit (neighbor, friend, etc.)",
                           4: "Work/office phone",
                           5: "No phone",
                           8: "Residue",
                           9: "Out of universe",
                           "Null": [8,9]},
                  "V2024":
                          {"Desc": "NUMBER OF HOUSING UNITS IN STRUCTURE",
                           1: 1,
                           2: 2,
                           3: 3,
                           4: 4,
                           5: "5-9",
                           6: "10+",
                           7: "Mobile home or trailer",
                           8: "Only OTHER units",
                           98: "Residue",
                           99: "Out of universe",
                           "Null": [98,99]},
                  "V2026":
                          {"Desc": "HOUSEHOLD INCOME (ALLOCATED) (START 2015, Q1) ",
                           1: "Less than $5,000",
                           2: "$5,000 to $7,499",
                           3: "$7,500 to $9,999",
                           4: "$10,000 to $12,499",
                           5: "$12,500 to $14,999",
                           6: "$15,000 to $17,499",
                           7: "$17,500 to $19,999",
                           8: "$20,000 to $24,999",
                           9: "$25,000 to $29,999",
                           10: "$30,000 to $34,999",
                           11: "$35,000 to $39,999",
                           12: "$40,000 to $49,999",
                           13: "$50,000 to $74,999",
                           14: "$75,000 and over",
                           98: "Residue",
                           99: "Out of universe",
                           "Null": [98,99]},
                  "SC214A":
                          {"Desc": "HOUSEHOLD INCOME (ALLOCATED) (START 2015, Q1) ",
                           "Null": [99,-1]},
                  "V2078":
                          {"Desc": "NUMBER MOTOR VEHICLES OWNED ",
                           "Null": [8,9]},
                  "V2116":
                          {"Desc": "HOUSEHOLD WEIGHT",
                           "Null": []},
                  "V2117":
                          {"Desc": "PSEUDOSTRATUM",
                           "Null": [999]},
                  "V2118":
                          {"Desc": "SECUCODE",
                           "Null": [9]},
                  "V2119": 
                          {"Desc": "COLLEGE/UNIVERSITY ",
                           "Null": [8,9]},
                  "V2120":
                          {"Desc": "PUBLIC HOUSING ",
                           "Null": [7,8,9]},
                  "V2122":
                          {"Desc": "FAMILY STRUCTURE CODE",
                           "Null": [98,99]},
                  "V2126B":
                          {"Desc": "PLACE SIZE CODE",
                           "Null": [-1,0]},
                  "V2127B":
                          {"Desc": "REGION",
                           "Null": [-1]},
                  "V2129":
                          {"Desc": "CBSA MSA STATUS",
                           "Null": [8,9]},
                  "V2130":
                          {"Desc": "MONTH ALLOCATED FROM PANEL/ROT NO.",
                           "Null": []},
                  "V3001":
                          {"Desc": "PERSON RECORD TYPE",
                           "Null": []},
                  "IDPER":
                          {"Desc": "NCVS ID FOR PERSONS",
                           "Null": []},
                  "V3002":
                          {"Desc": "ICPSR HOUSEHOLD IDENTIFICATION NUMBER",
                           "Null": []},
                  "V3003":
                          {"Desc": "YEAR AND QUARTER IDENTIFICATION",
                           "Null": []},
                  "V3004":
                          {"Desc": "SAMPLE NUMBER",
                           "Null": []},
                  "V3005":
                          {"Desc": "SCRAMBLED CONTROL NUMBER",
                           "Null": []},
                  "V3006":
                          {"Desc": "HOUSEHOLD NUMBER",
                           "Null": [8]},
                  "V3007":
                          {"Desc": "LAST TWO DIGITS OF SCRAMBLED CONTROL NO. (END 2004 Q4)",
                           "Null": [-2]},
                  "V3008":
                          {"Desc": "PANEL AND ROTATION GROUP",
                           "Null": []},
                  "V3009":
                          {"Desc": "PERSON SEQUENCE NUMBER",
                           "Null": []},
                  "V3010":
                          {"Desc": "PERSON LINE NUMBER",
                           "Null": [98,99]},
                  "V3011":
                          {"Desc": "TYPE OF INTERVIEW",
                           "Null": [8,9]},
                  "V3012":
                          {"Desc": "RELATIONSHIP TO REFERENCE PERSON",
                           "Null": [98,99]},
                  "V3013":
                          {"Desc": "AGE (ORIGINAL)",
                           "Null": [98,99]},
                  "V3014":
                          {"Desc": "AGE (ALLOCATED)",
                           "Null": [98,99]},
                  "V3015":
                          {"Desc": "MARITAL STATUS (CURRENT SURVEY)",
                           "Null": [8,9]},
                  "V3016":
                          {"Desc": "MARITAL STATUS (PREVIOUS SURVEY)",
                           "Null": [8,9]},
                  "V3017":
                          {"Desc": "SEX (ORIGINAL)",
                           "Null": [8,9]},
                  "V3018":
                          {"Desc": "SEX (ALLOCATED)",
                           "Null": [8,9]},
                  "V3019":
                          {"Desc": "NOW AN ARMED FORCES MEMBER",
                           "Null": [8,9]},
                  "V3020":
                          {"Desc": "EDUCATIONAL ATTAINMENT",
                           "Null": [98,99]},
                  "V3021":
                          {"Desc": "EDUCATION COMPLETE YEAR (END 2002 Q4)",
                           "Null": [-2,8,9]},
                  "V3022":
                          {"Desc": "RACE (ORIGINAL) (END 2002 Q4)",
                           "Null": [-2,8,9]},
                  "V3023":
                          {"Desc": "RACE (ALLOCATED) (END 2002 Q4)",
                           "Null": [-2,8,9]},
                  "V3023A":
                          {"Desc": "RACE RECODE (START 2003 Q1)",
                           "Null": [-1,98,99]},
                  "V3024":
                          {"Desc": "HISPANIC ORIGIN",
                           "Null": [8,9]},
                  "V3024A":
                          {"Desc": "HISPANIC ORIGIN (ALLOCATED) (START 2014 Q1)",
                           "Null": [-1,8,9]},
                  "V3025":
                          {"Desc": "MONTH INTERVIEW COMPLETED",
                           "Null": [98,99]},
                  "V3026":
                          {"Desc": "DAY INTERVIEW COMPLETED",
                           "Null": [98,99]},
                  "V3027":
                          {"Desc": "YEAR INTERVIEW COMPLETED",
                           "Null": [9998,9999]},
                  "V3028":
                          {"Desc": "HOW OFTEN GONE SHOPPING (END 2002 Q2)",
                           "Null": [-2]},
                  "V3029":
                          {"Desc": "HOW OFTEN SPENT EVENING AWAY FROM HOME (END 2000 Q2)",
                           "Null": [-2]},
                  "V3030":
                          {"Desc": "HOW OFTEN RIDDEN PUBLIC TRANSPORTATION (END 2000 Q2)",
                           "Null": [-2]},
                  "V3031":
                          {"Desc": "HOW LONG AT THIS ADDRESS (MONTHS)",
                           "Null": [98,99]},
                  "V3032":
                          {"Desc": "HOW LONG AT THIS ADDRESS (YEARS)",
                           "Null": [98,99]},
                  "V3033":
                          {"Desc": "HOW MANY TIMES MOVED IN LAST 5 YEARS",
                           "Null": [98,99]},
                  "V3034":
                          {"Desc": "SOMETHING STOLEN OR ATTEMPT",
                           "Null": [3,8,9]},
                  "V3035":
                          {"Desc": "NO. TIMES SOMETHING STOLEN OR ATTEMPT",
                           "Null": [998,999]},
                  "V3036":
                          {"Desc": "BROKEN IN OR ATTEMPTED",
                           "Null": [3,8,9]},
                  "V3037":
                          {"Desc": "NO. TIMES BROKEN IN OR ATTEMPTED",
                           "Null": [998,999]},
                  "V3038":
                          {"Desc": "MOTOR VEHICLE THEFT",
                           "Null": [3,8,9]},
                  "V3039":
                          {"Desc": "NO. TIMES MOTOR VEHICLE THEFT",
                           "Null": [998,999]},
                  "V3040":
                          {"Desc": "ATTACK, THREAT, THEFT: LOCATION CUES",
                           "Null": [3,8,9]},
                  "V3041":
                          {"Desc": "NO. TIMES ATTACK, LOCATION CUES",
                           "Null": [998,999]},
                  "V3042":
                          {"Desc": "ATTACK, THREAT: WEAPON, ATTACK CUES",
                           "Null": [3,8,9]},
                  "V3043":
                          {"Desc": "NO. TIMES ATTACK, WEAPON CUES",
                           "Null": [998,999]},
                  "V3044":
                          {"Desc": "STOLEN, ATTACK, THREAT: OFFENDER KNOWN",
                           "Null": [3,8,9]},
                  "V3045":
                          {"Desc": "NO. TIMES ATTACK, OFFENDER KNOWN",
                           "Null": [998,999]},
                  "V3046":
                          {"Desc": "FORCED OR COERCED UNWANTED SEX",
                           "Null": [3,8,9]},
                  "V3047":
                          {"Desc": "NO. TIMES UNWANTED SEX",
                           "Null": [998,999]},
                  "V3048":
                          {"Desc": "CALL POLICE TO REPORT SOMETHING ELSE",
                           "Null": [3,8,9]},
                  "V3049":
                          {"Desc": "FIRST INCIDENT",
                           "Null": [29,98,99]},
                  "V3050":
                          {"Desc": "SECOND INCIDENT",
                           "Null": [29,98,99]},
                  "V3051":
                          {"Desc": "THIRD INCIDENT",
                           "Null": [29,98,99]},
                  "V3052":
                          {"Desc": "CHECK B: ATTACK, THREAT, THEFT",
                           "Null": [3,8,9]},
                  "V3053":
                          {"Desc": "NO. TIMES ATTACK, THREAT, THEFT",
                           "Null": [998,999]},
                  "V3054":
                          {"Desc": "THOUGHT CRIME BUT DIDN'T CALL POLICE",
                           "Null": [3,8,9]},
                  "V3055":
                          {"Desc": "FIRST INCIDENT",
                           "Null": [29,98,99]},
                  "V3056":
                          {"Desc": "SECOND INCIDENT",
                           "Null": [29,98,99]},
                  "V3057":
                          {"Desc": "THIRD INCIDENT",
                           "Null": [29,98,99]},
                  "V3058":
                          {"Desc": "CHECK C: ATTACK, THREAT, THEFT",
                           "Null": [3,8,9]},
                  "V3059":
                          {"Desc": "NO. TIMES ATTACK, THREAT, THEFT",
                           "Null": [998,999]},
                  "V3059A":
                          {"Desc": "LI USED COMPUTER IN LAST 6 MONTHS (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059B":
                          {"Desc": "C PERSONAL USE AT HOME (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059C":
                          {"Desc": "C PERSONAL USE AT WORK (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059D":
                          {"Desc": "C PERSONAL USE AT SCHOOL, LIBRARIES, ETC (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059E":
                          {"Desc": "C OPERATE HOME BUSINESS (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059F":
                          {"Desc": "C NONE OF ABOVE (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059G":
                          {"Desc": "RESIDUE: USED COMPUTER IN LAST 6 MONTHS (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059H":
                          {"Desc": "N COMPUTERS PERSONAL USE/HOME BUSINESS (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059I":
                          {"Desc": "INTERNET FOR PERSONAL/HOME BUSINESS (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059J":
                          {"Desc": "LI COMPUTER-RELATED INCIDENTS LAST 6 MONTHS (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059K":
                          {"Desc": "C FRAUD PURCHASE OVER INTERNET (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059L":
                          {"Desc": "C COMPUTER VIRUS ATTACK (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059M":
                          {"Desc": "C THREATS OF HARM/ATTACK ON-LINE (START 2001 Q3) (END 2004 Q2)",
                           "Null": []},
                  "V3059N":
                          {"Desc": "C OBSCENE MESSAGES ON-LINE (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059O":
                          {"Desc": "C SOFTWARE COPYRIGHT W HOME BUSINESS (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059P":
                          {"Desc": "C OTHER COMPUTER-RELATED CRIME (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059Q":
                          {"Desc": "C NO COMPUTER-RELATED INCIDENTS (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059R":
                          {"Desc": "RESIDUE: COMPUTER-RELATED INCIDENTS LAST 6 MONTHS (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059S":
                          {"Desc": "LOSSES FROM COMPUTER-RELATED INCIDENTS (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059T":
                          {"Desc": "AMOUNT OF LOSSES COMPUTER-RELATED INCIDENTS (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,99997,99998,99999]},
                  "V3059U":
                          {"Desc": "LI REPORT INCIDENTS (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059V":
                          {"Desc": "C LAW ENFORCEMENT (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059W":
                          {"Desc": "C INTERNET SERVICE PROVIDER (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059X":
                          {"Desc": "C WEBSITE ADMINISTRATOR (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059Y":
                          {"Desc": "C SYSTEMS ADMINISTRATOR (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059Z":
                          {"Desc": "C SOMEONE ELSE (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059AA":
                          {"Desc": "C NONE OF ABOVE (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3059AB":
                          {"Desc": "RESIDUE: REPORT INCIDENTS (START 2001 Q3) (END 2004 Q2)",
                           "Null": [-2,-1,8,9]},
                  "V3060":
                          {"Desc": "CHECK ITEM D(L): LI WHO PRESENT DURING SCREEN QUESTIONS",
                           "Null": [7,8,9]},
                  "V3061":
                          {"Desc": "CHECK ITEM D(1): C TELEPHONE INTERVIEW",
                           "Null": [8,9]},
                  "V3062":
                          {"Desc": "CHECK ITEM D(2): C NO ONE BESIDES RESPONDENT PRESENT",
                           "Null": [8,9]},
                  "V3063":
                          {"Desc": "CHECK ITEM D(3): C RESPONDENT'S SPOUSE",
                           "Null": [8,9]},
                  "V3064":
                          {"Desc": "CHECK ITEM D(4): C HH MEMBER(S) 12+, NOT SPOUSE",
                           "Null": [8,9]},
                  "V3065":
                          {"Desc": "CHECK ITEM D(5): C HH MEMBER(S) UNDER 12",
                           "Null": [8,9]},
                  "V3066":
                          {"Desc": "CHECK ITEM D(6): C NONHOUSEHOLD MEMBER(S)",
                           "Null": [8,9]},
                  "V3067":
                          {"Desc": "CHECK ITEM D(7): C SOMEONE PRESENT, CAN'T SAY WHO",
                           "Null": [8,9]},
                  "V3068":
                          {"Desc": "CHECK ITEM D(8): C DON'T KNOW IF SOMEONE ELSE PRESENT",
                           "Null": [8,9]},
                  "V3069":
                          {"Desc": "CHECK ITEM D(R): RESIDUE: WHO PRESENT DURING SCREEN",
                           "Null": [8,9]},
                  "V3070":
                          {"Desc": "CHECK ITEM E: DID SELECTED RESPONDENT HELP PROXY",
                           "Null": [3,8,9]},
                  "V3_V4526H3A":
                          {"Desc": "ARE YOU DEAF OR DO YOU HAVE SERIOUS DIFFICULTY HEARING? (START 2016 Q3)",
                           "Null": [-1,8,9]},
                  "V3_V4526H3B":
                          {"Desc": "ARE YOU BLIND OR DO YOU HAVE SERIOUS DIFFICULTY SEEING EVEN WHEN WEARING GLASSES (START 2016 Q3)",
                           "Null": [-1,8,9]},
                  "V3_V4526H5":
                          {"Desc": "DIFFICULT: LEARN, REMEMBER, CONCENTRATE (START 2016 Q3)",
                           "Null": [-1,8,9]},
                  "V3_V4526H4":
                          {"Desc": "LIMITS PHYSICAL ACTIVITIES (START 2016 Q3)",
                           "Null": [-1,8,9]},
                  "V3_V4526H6":
                          {"Desc": "DIFFICULT: DRESSING, BATHING, GET AROUND HOME (START 2016 Q3)",
                           "Null": [-1,8,9]},
                  "V3_V4526H7":
                          {"Desc": "DIFFICULT GO OUTSIDE HOME TO SHOP OR DR OFFICE (START 2016 Q3)",
                           "Null": [-1,8,9]},
                  "V3071":
                          {"Desc": "HAVE JOB OR WORK LAST WEEK",
                           "Null": [8,9]},
                  "V3072":
                          {"Desc": "HAVE JOB OR WORK IN LAST 6 MONTHS",
                           "Null": [8,9]},
                  "V3073":
                          {"Desc": "DID JOB/WORK LAST 2 WEEKS OR MORE",
                           "Null": [8,9]},
                  "V3074":
                          {"Desc": "WHICH BEST DESCRIBES YOUR JOB",
                           "Null": [98,99]},
                  "V3075":
                          {"Desc": "IS EMPLOYMENT PRIVATE, GOVT OR SELF",
                           "Null": [8,9]},
                  "V3076":
                          {"Desc": "IS WORK MOSTLY IN CITY, SUBURB, RURAL",
                           "Null": [8,9]},
                  "V3077":
                          {"Desc": "HOUSEHOLD RESPONDENT",
                           "Null": []},
                  "V3078":
                          {"Desc": "EMPLOYED BY A COLLEGE OR UNIVERSITY",
                           "Null": [8,9]},
                  "V3079":
                          {"Desc": "ATTENDING COLLEGE",
                           "Null": [8,9]},
                  "V3080":
                          {"Desc": "PERSON WEIGHT",
                           "Null": [0]},
                  "WGTPERCY":
                          {"Desc": "ADJUSTED PERSON WEIGHT - COLLECTION YEAR",
                           "Null": [0]},
                  "V3081":
                          {"Desc": "NUMBER OF CRIME INCIDENT REPORTS",
                           "Null": [98,99]},
                  "V3082":
                          {"Desc": "YEAR IDENTIFICATION (START 1999 Q3)",
                           "Null": [-1]},
                  "PER_TIS":
                          {"Desc": "PERSON TIME IN SAMPLE (START 2015 Q1)",
                           "Null": [-1]},
                  "PERINTVNUM":
                          {"Desc": "PERSON INTERVIEW NUMBER (START 2015 Q1)",
                           "Null": [-1]},
                  "PINTTYPE_TIS1":
                          {"Desc": "PERSON TYPE INTERVIEW CODE TIME IN SAMPLE 1 (START 2015 Q1)",
                           "Null": [-1,8,9]},
                  "PINTTYPE_TIS2":
                          {"Desc": "PERSON TYPE INTERVIEW CODE TIME IN SAMPLE 2 (START 2015 Q1)",
                           "Null": [-1,8,9]},
                  "PINTTYPE_TIS3":
                          {"Desc": "PERSON TYPE INTERVIEW CODE TIME IN SAMPLE 3 (START 2015 Q1)",
                           "Null": [-1,8,9]},
                  "PINTTYPE_TIS4":
                          {"Desc": "PERSON TYPE INTERVIEW CODE TIME IN SAMPLE 4 (START 2015 Q1)",
                           "Null": [-1,8,9]},
                  "PINTTYPE_TIS5":
                          {"Desc": "PERSON TYPE INTERVIEW CODE TIME IN SAMPLE 5 (START 2015 Q1)",
                           "Null": [-1,8,9]},
                  "PINTTYPE_TIS6":
                          {"Desc": "PERSON TYPE INTERVIEW CODE TIME IN SAMPLE 6 (START 2015 Q1)",
                           "Null": [-1,8,9]},
                  "PINTTYPE_TIS7":
                          {"Desc": "PERSON TYPE INTERVIEW CODE TIME IN SAMPLE 7 (START 2015 Q1)",
                           "Null": [-1,8,9]},
                  "PERBOUNDED":
                          {"Desc": "PERSON BOUNDED BY PREVIOUS TIME IN SAMPLE (START 2015 Q1)",
                           "Null": [-1]},
                  "VFLAG":
                          {"Desc": "HOUSEHOLD VICTIMIZATION FLAG",
                           "Null": [9]},
                  "VTYPE":
                          {"Desc": "TYPE OF VICTIMIZATION",
                           "Null": [9]},
                  "RECENTLY_MARRIED":
                          {"Desc": "MARRIED IN LAST YEAR",
                           "Null": []},
                  "RECENTLY_SINGLE":
                          {"Desc": "MARRIAGE ENDED IN LAST YEAR FOR ANY REASON",
                           "Null": []},
                  "RACE":
                          {"Desc": "RACE",
                           "Null": []}}

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
	return pickle.load(open('assets/model.sav', 'rb'))

def rprint(var):
    print(var)
    return var

def attempt(func, var):
    try:
        return func(var)
    except:
        print(f"failed to run: {func}({var})\n")
        return 0








