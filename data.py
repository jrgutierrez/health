from PIL import Image
from pytesseract import pytesseract
import os
import re
from datetime import datetime
import pandas as pd
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

def update_data():
    print('Updating data...')
    if not os.path.exists('result/data.csv'):
        os.makedirs('result/', exist_ok = True)
        df = pd.DataFrame(columns = ['weight', 'bmi', 'body_fat_rate', 'subcutaneous_fat',
                                     'heart_rate', 'heart_index', 'visceral_fat', 'body_water',
                                     'skeletal_muscle_rate', 'muscle_mass', 'bone_mass', 'protein',
                                     'bmr', 'body_age'])

        df.to_csv('result/data.csv')

    data = pd.read_csv('result/data.csv').set_index('Unnamed: 0')

    path_to_tesseract = '/usr/local/bin/tesseract'
    images_path = 'images/'

    images = [images_path + img for img in os.listdir(images_path) if img.endswith('.jpeg')]
    n_images = 0
    for image in tqdm(images):
        try:
            # Opening the image & storing it in an image object
            img = Image.open(image).crop((0, 500, 900, 3100))
            # Providing the tesseract executable
            # location to pytesseract library
            pytesseract.tesseract_cmd = path_to_tesseract

            # Passing the image object to image_to_string() function
            # This function will extract the text from the image
            text = pytesseract.image_to_string(img)

            # Displaying the extracted text
            text = text.split('\n')
            date, img_data = text[0], text[1:]
            date = datetime.strptime(date, '%H:%M %b.%d,%Y')
            if str(date) in list(data.index): continue
            img_data = [x for x in img_data if x]
            aux_data = {}
            for img_val in img_data:
                val = re.split(r'(\d+)', img_val)
                aux_data[val[0].lower().strip().replace(' ', '_')] = ''.join(val[1:-1])
            data = data.append(pd.DataFrame(aux_data, index = [date]))
            n_images+=1
        except: continue
    data.to_csv('result/data.csv')
    print(f'{n_images} images updated!')
    
def get_raw_data():
    data = pd.read_csv('result/data.csv').rename(columns = {'Unnamed: 0': 'date'})
    data['date'] = pd.to_datetime(data['date'])
    return data.set_index('date').sort_index()

def prepare_data(data):
    data = data[['weight', 'body_fat_rate', 'muscle_mass']]
    data['body_fat_rate'] = data['body_fat_rate'].apply(lambda x: x if x < 50 else round(x/10, 1))
    for i in range(len(data)-1):
        if abs(data['body_fat_rate'][i+1]/data['body_fat_rate'][i] - 1) > 0.1:
            if 21 <= data['body_fat_rate'][i+1] < 22:
                data['body_fat_rate'][i+1] = data['body_fat_rate'][i+1] + 6
    
    data = data.groupby(lambda x: x.date).aggregate({'weight': 'mean', 'body_fat_rate': 'mean',
                                                 'muscle_mass': 'mean'})
    return data.reindex(pd.date_range(data.index[0], data.index[-1])).interpolate()

def get_data(update = False):
    if update: update_data()
    data = get_raw_data()
    data = prepare_data(data)
    return data