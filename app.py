import joblib
import datetime
import streamlit as st
from geopy.geocoders import Nominatim
import numpy as np

adress = st.text_input('Введите адрес.   Пример: Санкт-Петербург Фрунзе 25')

building_type = st.selectbox('Выберите тип здания', ['Монолитный','Кирпичный','Другой'])

level = st.slider('Этаж',min_value=1, max_value=50)

levels = st.slider('Всего этажей',min_value=1, max_value=50)

rooms = st.selectbox('Количество комнат', [1,2,3,4,5])

area = st.slider('Площадь',min_value=1, max_value=100)

kitchen_area = st.slider('Площадь кухни',min_value=1, max_value=50)

object_type = st.selectbox('Тип жилья', ['Новостройка','Вторичка'])

date = datetime.datetime.now()

month = date.month

year = date.year

geolocator = Nominatim(user_agent="my_request")
location = geolocator.geocode(adress)

if building_type == 'Монолитный':
  building_type = 2
elif building_type == 'Кирпичный':
  building_type = 3
else:
  building_type = 0

if object_type == 'Новостройка':
  object_type = 11
else:
  object_type = 1  

model = joblib.load("ml_rfr.pkl")
  

if st.button('Рассчитать стоимость'):
    geo_lat = location.latitude 
    geo_lon = location.longitude
    prediction_inp = np.array([geo_lat,geo_lon,building_type,level,levels,\
                 rooms,area,kitchen_area,object_type,month,year])
    cost = model.predict(prediction_inp.reshape(1, -1))
    st.write(f'### Приблизительная cтоимость жилья:\n ## {int(cost)}')
