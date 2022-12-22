# -*- coding: utf-8 -*-
"""main.ipynb"

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d04dAKipodwhfzn9p3LbJk8naCUCOYLC

Итак, у нас есть данные с оценками услуг, предоставляемых Федеральными органами исполнительной власти

Наша задача заключалась в том, чтобы выяснить, какие из ФОИВ накручивают себе отзывы

Подключаем нужные нам библиотеки для работы, скачиваем датасет
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)


"""Загрузим данные из .xlxs файла и ознакомимся с данными:"""

data = pd.read_excel('Dataset.xlsx')

plt.hist(data['Уровень удовлетворенности'])
plt.show()

data.head()

"""Расшифровка некоторых параметров датасета:

|              	|                                                                          	|
|:------------:	|:-------------------------------------------------------------------------------:	|
| ФОИВ         	| Федеральный орган исполнительной власти                              	|
| cnt_1    	| количество оценок "1"                                       	|
| cnt_2     	| количество оценок "2"                                        	|
| cnt_3    	| количество оценок "3"                                                                  	|
| cnt_4     	| количество оценок "4"                    	|
| cnt_5   	| количество оценок "5"                                                          	|
| Оценки 	| общее количесиво оценок                                                     	|
| Уровень удовлетворенности      	| процентное соотношение оценок "4" и "5" к общему числу оценок                                                	|
"""

data.info()

"""Посмотрим на количество пропусков по столбцам:"""

data.isnull().sum()

"""Удалим строку, в которой есть пропущенное значение:"""

data['Факты'].replace('  ', np.nan, inplace=True)

data= data.dropna(subset=['Факты'])

"""Убедимся, что пропусков не осталось:"""

data.isnull().sum()

"""Корреляция данных:"""

plt.figure(figsize=(20,10))
sns.heatmap(data.corr())
plt.show()

"""Видно, что количество оценок коррелирует с количеством оценок "5", значит, существует много ФОИВ, работу которых оценивают исключительно на 5. 
Реже всего же пользователи ставят оценку "3"

И, вероятнее всего, данные, где все оценки являются оценками "5", были накручены

Будем считать 100% наивысших оценок аномально высоким показателем

Уберем такие строки из нашего датафрейма
"""

df = data[data['Оценки'] != data['cnt_5']]
df.head()

df.info()

"""Также, вероятнее всего, накрутокой являются те строки, в которых сумма оценок "1" и "5" равно общему количеству оценок данной услуги

Странно, что одну и ту же услугу в одном и том же месте пользователи оценивают так полярно, причем не ставя оценки "2", "3" и "4"

Найдем такие строки:
"""

df_n = df[df['Оценки'] == df['cnt_5'] + df['cnt_1']]
df_tn = df_n[df_n['Оценки'] != df_n['cnt_1']]
df_tn.head()

df_tn.info()

"""Их оказалось 1269, уберем их из нашего датафрейма:"""

df = df[df['Оценки'] != df['cnt_5'] + df['cnt_1']]
df.head()

"""Также удалось заметить, что оценки не везде соответствуют сумме оценок по баллам

Является ли это просто ошибкой или накруткой - неизвестно, но в любом случае такие строки тоже нужно убрать
"""

df = df[df['Оценки'] == df['cnt_1'] + df['cnt_2'] + df['cnt_3'] + df['cnt_4'] + df['cnt_5']]
df.head()

df.info()

"""Таким образом, по нашим расчетам, получился датасет без накруток

Скачаем его, чтобы посторить диаграммы общей статистики теперь для данных без накрутки для сравнения с исходными данными
"""


df.to_excel('new_df.xlsx')
files.download('new_df.xlsx')
