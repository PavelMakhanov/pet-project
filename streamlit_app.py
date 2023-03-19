import joblib
import datetime
import streamlit as st
from geopy.geocoders import Nominatim
import numpy as np


st.title('Рассчитайте стоимость недвижимости')
st.image('interer.jpeg')

st.sidebar.title('Заполните параметры')

adress = st.sidebar.text_input('Введите адрес.   Пример: Санкт-Петербург Фрунзе 25')

building_type = st.sidebar.selectbox('Выберите тип здания', ['Панельный', 'Монолитный','Кирпичный','Блочный','Деревянный','Другой'])

level = st.sidebar.slider('Этаж',min_value=1, max_value=50)

levels = st.sidebar.slider('Всего этажей',min_value=1, max_value=50)

rooms = st.sidebar.selectbox('Количество комнат', [1,2,3,4,5])

area = st.sidebar.slider('Площадь',min_value=1, max_value=100)

kitchen_area = st.sidebar.slider('Площадь кухни',min_value=1, max_value=50)

object_type = st.sidebar.selectbox('Тип жилья', ['Новостройка','Вторичка'])

date = datetime.datetime.now()

month = date.month

year = date.year

geolocator = Nominatim(user_agent="my_request")
location = geolocator.geocode(adress)
if building_type == 'Панельный':
  building_type = 1
elif building_type == 'Монолитный':
  building_type = 2  
elif building_type == 'Кирпичный':
  building_type = 3
elif building_type == 'Блочный':
  building_type = 4 
elif building_type == 'Деревянный':
  building_type = 5   
else:
  building_type = 0

if object_type == 'Новостройка':
  object_type = 11
else:
  object_type = 1  

model = joblib.load("model_xgb.pkl")
  

if st.sidebar.button('Рассчитать стоимость'):
    try:
        geo_lat = location.latitude 
        geo_lon = location.longitude
        prediction_inp = np.array([geo_lat,geo_lon,building_type,level,levels,\
                    rooms,area,kitchen_area,object_type,month,year])
        cost = model.predict(prediction_inp.reshape(1, -1))
        cost = '{0:,}'.format(int(cost)).replace(',', ' ')

        st.write(f'### Приблизительная cтоимость жилья:\n ## {cost}')
    except:
        st.write(f'#### ⚠ Проверьте правильность введенных данных, все ячейки должны быть заполнены согласно примерам') 
