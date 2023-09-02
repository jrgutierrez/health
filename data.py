import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import gspread
import streamlit as st


def get_raw_data():
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    spreadsheet = gc.open_by_key(st.secrets["sheet_id"])
    worksheet = spreadsheet.worksheet(st.secrets["sheet_name"])
    data = pd.DataFrame(worksheet.get_all_records())
    data['date'] = pd.to_datetime(data['date'])
    return data.set_index('date').sort_index()

def prepare_data(data):
    data = data[['weight', 'body_fat_rate', 'muscle_mass']]
    data['body_fat_rate'] = data['body_fat_rate'].apply(lambda x: x if x < 50 else round(x/10, 1))
    for i in range(len(data)-1):
        if abs(data['body_fat_rate'][i+1]/data['body_fat_rate'][i] - 1) > 0.1:
            if 21 <= data['body_fat_rate'][i+1] < 22:
                data['body_fat_rate'][i+1] = data['body_fat_rate'][i+1] + 6
    
    data = data.groupby(lambda x: x.date).aggregate({'weight': 'mean()', 'body_fat_rate': 'mean()', 'muscle_mass': 'mean()'})
    return data.reindex(pd.date_range(data.index[0], data.index[-1])).interpolate()

def get_data():
    data = get_raw_data()
    return prepare_data(data)