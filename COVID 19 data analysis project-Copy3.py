#!/usr/bin/env python
# coding: utf-8

# In[136]:


# imports
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

import folium

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')

import math
import random

import warnings
warnings.filterwarnings('ignore')

#colour pallets 
cnf = '#393e46'
dth = '#ff2e63'
rec = '#21bf73'
act = '#fe9801'


# #  Data preparation

# In[137]:


import plotly as py
py.offline.init_notebook_mode(connected =True)


# In[138]:


df = pd.read_csv('C:/Users/Dhruv Kushalkar/OneDrive/Desktop/Covid-19-Preprocessed-Dataset-master (3)/Covid-19-Preprocessed-Dataset-master/preprocessed/covid_19_data_cleaned.csv', parse_dates=['Date'])

country_daywise = pd.read_csv('C:/Users/Dhruv Kushalkar/OneDrive/Desktop/Covid-19-Preprocessed-Dataset-master (3)/Covid-19-Preprocessed-Dataset-master/preprocessed/country_daywise.csv', parse_dates=['Date'])

countrywise = pd.read_csv('C:/Users/Dhruv Kushalkar/OneDrive/Desktop/Covid-19-Preprocessed-Dataset-master (3)/Covid-19-Preprocessed-Dataset-master/preprocessed/countrywise.csv',)

daywise = pd.read_csv('C:/Users/Dhruv Kushalkar/OneDrive/Desktop/Covid-19-Preprocessed-Dataset-master (3)/Covid-19-Preprocessed-Dataset-master/preprocessed/daywise.csv', parse_dates=['Date'])


# In[139]:


df['Province/State'] = df['Province/State'].fillna("")
df.head()


# In[140]:


country_daywise


# In[141]:


countrywise


# In[142]:


daywise


# In[143]:


confirmed = df.groupby('Date').sum()['Confirmed'].reset_index()
recovered = df.groupby('Date').sum()['Recovered'].reset_index()
deaths = df.groupby('Date').sum()['Deaths'].reset_index()

deaths.head()
#recovered
#confirmed


# In[144]:


df.isnull().sum() #No null values present in this frame


# In[145]:


df.info()


# In[146]:


#check all the cases in india till date

df.query('Country == "India"') 


# #  Worldwide Total Confirmed, Recovered, and Deaths

# In[147]:


#initial confirmed cases

confirmed.head()


# In[148]:


#latest confirmed cases
confirmed.tail()


# In[149]:


recovered.tail()


# In[150]:


deaths.tail()


# In[151]:


fig = go.Figure()
fig.add_trace(go.Scatter(x = confirmed['Date'],y=confirmed['Confirmed'],mode = 'lines+markers', name = 'Confirmed', line = dict(color = "Orange", width=6)))
fig.add_trace(go.Scatter(x = recovered['Date'],y=recovered['Recovered'],mode = 'lines+markers', name = 'Recovered', line = dict(color = "Green", width=6)))
fig.add_trace(go.Scatter(x = deaths['Date'],y=deaths['Deaths'],mode = 'lines+markers', name = 'Deaths', line = dict(color = "Red", width=6)))
fig.update_layout(title = 'Worldwide COVID-19 Cases', xaxis_tickfont_size = 14, yaxis=dict(title = 'Number of Cases'))


fig.show()


# #  Cases Density Animation on World Map

# In[152]:


df.info()


# In[153]:


df['Date']= df['Date'].astype(str)


# In[154]:


df.info()


# In[155]:


df.head()


# In[156]:


fig = px.density_mapbox(df, lat = 'Lat', lon = 'Long', hover_name ='Country', hover_data = ['Confirmed', 'Recovered', 'Deaths'], animation_frame = 'Date',  radius = 7, zoom = 0, height= 700)
fig.update_layout(title = 'Worldwide Covid-19 Cases with Time Lapse')
fig.update_layout(mapbox_style = 'open-street-map', mapbox_center_lon =0)

fig.show()


# #  Cases over the time with Area Plot

# In[157]:


temp = df.groupby('Date')['Confirmed','Deaths','Recovered','Active'].sum().reset_index()
temp = temp[temp['Date']==max(temp['Date'])].reset_index(drop = True)
temp


# In[158]:


tm = temp.melt(id_vars = 'Date', value_vars = ['Active', 'Deaths', 'Recovered'])
fig = px.treemap(tm, path = ['variable'], values = 'value', height =250, width = 800, color_discrete_sequence=[act, rec, dth])

fig.data[0].textinfo = 'label+text+value'
fig.show()


# In[159]:


temp =df.groupby('Date')['Recovered','Deaths','Active'].sum().reset_index()
temp = temp.melt(id_vars = 'Date', value_vars = ['Recovered','Deaths','Active'], var_name = 'Case', value_name = 'Count')
temp


# In[160]:


fig = px.area(temp, x = 'Date', y = 'Count', color = 'Case', height = 400, title = 'Cases over time', color_discrete_sequence=[rec, dth, act])
fig.update_layout(xaxis_rangeslider_visible=True)
fig.show()


# #  Folium maps

# In[161]:


# Worldwide Cases on folium Maps


# In[162]:


temp = df[df['Date']==max(df['Date'])]
temp


# In[163]:


m = folium.Map(location=[0,0], tiles ='cartodbpositron', min_zoom=1, max_zoom=4, zoom_start=1)


for i in range(0,len(temp)):
    folium.Circle(location=[temp.iloc[i]['Lat'],temp.iloc[i]['Long']], color = 'crimson', fill = 'crimson',
                 tooltip = '<li><bold> Country: ' + str(temp.iloc[i]['Country'])+
                            '<li><bold> Province: ' + str(temp.iloc[i]['Province/State'])+
                                '<li><bold> Cofirmed: ' + str(temp.iloc[i]['Confirmed'])+
                                     '<li><bold> Deaths: ' + str(temp.iloc[i]['Deaths']),
                  radius=int(temp.iloc[i]['Confirmed'])**0.5).add_to(m)
    
m


# #  Confirmed Cases with Choropleth Map

# In[164]:


country_daywise.head()


# In[165]:


fig = px.choropleth(country_daywise, locations= 'Country', locationmode = 'country names', color = np.log(country_daywise['Confirmed']),
                   hover_name = 'Country', animation_frame=country_daywise['Date'].dt.strftime('%Y-%m-%d'),
                   title='Cases over time')

fig.update(layout_coloraxis_showscale = True)
fig.show()


# #  Deaths and Recoveries per 100 cases

# In[166]:


daywise.head()


# In[167]:


fig_c = px.bar(daywise, x = 'Date', y = 'Confirmed', color_discrete_sequence=[act])
fig_d = px.bar(daywise, x = 'Date', y = 'Deaths', color_discrete_sequence=[dth])

fig = make_subplots(rows = 1, cols = 2, shared_xaxes=False, horizontal_spacing=0.1,
                   subplot_titles=('Confirmed Cases', 'Deaths Cases'))

fig.add_trace(fig_c['data'][0], row=1,col=1)
fig.add_trace(fig_d['data'][0], row=1,col=2)

fig.update_layout(height = 400)

fig.show()


# #  Confirmed and Death Cases with Static Color Map

# In[168]:


fig_c =px.choropleth(countrywise, locations='Country', locationmode='country names',
                    color = np.log(countrywise['Confirmed']), hover_name = 'Country',
                    hover_data = ['Confirmed'])
temp = countrywise[countrywise['Deaths']>0]

fig_d =px.choropleth(temp, locations='Country', locationmode='country names',
                    color = np.log(temp['Deaths']), hover_name = 'Country',
                    hover_data = ['Deaths'])

fig = make_subplots(rows = 1,cols = 2, subplot_titles= ['Confirmed','Deaths'],
                   specs = [[{'type': 'choropleth'}, {'type': 'choropleth'}]])

fig.add_trace(fig_c['data'][0], row=1, col= 1)
fig.add_trace(fig_d['data'][0], row=1, col= 2)


fig.update(layout_coloraxis_showscale = False)

fig.show()


# # New cases and number of countries

# In[169]:


fig_c = px.bar(daywise,x='Date',y='Confirmed', color_discrete_sequence=[act])
fig_d = px.bar(daywise,x='Date',y='No. of Countries', color_discrete_sequence=[dth])

fig = make_subplots(rows=1,cols=2, shared_xaxes=False, horizontal_spacing=0.1,
                   subplot_titles=('No. of New Cases per Day', 'No of Countries'))

fig.add_trace(fig_c['data'][0],row=1,col=1)
fig.add_trace(fig_d['data'][0],row=1,col=2)

fig.show()


# # Top 15 Countries Cases

# In[170]:


countrywise.columns


# In[171]:


top=15

fig_c = px.bar(countrywise.sort_values('Confirmed').tail(top), x='Confirmed', y='Country',
              text = 'Confirmed', orientation='h', color_discrete_sequence=[cnf])

fig_d = px.bar(countrywise.sort_values('Deaths').tail(top), x='Deaths', y='Country',
              text = 'Deaths', orientation='h', color_discrete_sequence=[dth])

fig_a = px.bar(countrywise.sort_values('Active').tail(top), x='Active', y='Country',
              text = 'Active', orientation='h', color_discrete_sequence=[act])


fig_dc = px.bar(countrywise.sort_values('Deaths / 100 Cases').tail(top), x='Deaths / 100 Cases', y='Country',
              text = 'Deaths / 100 Cases', orientation='h', color_discrete_sequence=['#f84351'])



fig=make_subplots(rows=5,cols=2, shared_xaxes=False, horizontal_spacing=0.14, 
                  vertical_spacing=0.1,
                  subplot_titles=('Confirmed Cases','Deaths Reported','Active Cases',
                                  'Deaths / 100 Cases'))

fig.add_trace(fig_c['data'][0], row=1,col=1)
fig.add_trace(fig_d['data'][0], row=1,col=2)


fig.add_trace(fig_a['data'][0], row=2,col=1)

fig.add_trace(fig_dc['data'][0], row=2,col=2)


fig.update_layout(height=4000)
fig.show()


# # Scatter Plot for Deaths vs Confirmed Cases

# In[172]:


top=15
fig=px.scatter(countrywise.sort_values('Deaths', ascending=False).head(top),
              x='Confirmed',y='Deaths',color='Country',size='Confirmed',height=700,
              text='Country',log_x=True,log_y=True, title='Deaths vs Confirmed Cases (Cases are on Log10 scale)')

fig.update_traces(textposition='top center')
fig.update_layout(showlegend=True)
fig.update_layout(xaxis_rangeslider_visible=True)

fig.show()


# # Confirmed and Deaths
# # Barplot

# In[173]:


#fig = px.bar(country_daywise, x='Date',y='Confirmed', color='Country', height=600,
     #       title='Confirmed', color_discrete_sequence=px.colors.cyclical.mygbm)

#fig.show()


# In[174]:


#fig = px.bar(country_daywise, x='Date',y='Deaths', color='Country', height=600,
 #           title='Deaths', color_discrete_sequence=px.colors.cyclical.mygbm)

#fig.show()


# # Line Plot

# In[175]:


fig = px.line(country_daywise,x='Date', y='Confirmed',color='Country',height=600,
             title='Confirmed',color_discrete_sequence=px.colors.cyclical.mygbm)
fig.show()

fig = px.line(country_daywise,x='Date', y='Deaths',color='Country',height=600,
             title='Deaths',color_discrete_sequence=px.colors.cyclical.mygbm)
fig.show()


# # Tree Map Analysis

# # Confirmed

# In[176]:


full_latest=df[df['Date']==max(df['Date'])]

fig=px.treemap(full_latest.sort_values(by='Confirmed', ascending=False).reset_index(drop=True),
              path=['Country','Province/State'],values='Confirmed',height=700,
              title='Number of Confirmed Cases',
              color_discrete_sequence = px.colors.qualitative.Dark2)
fig.data[0].textinfo = 'label+text+value'
fig.show()


# In[177]:


full_latest=df[df['Date']==max(df['Date'])]

fig=px.treemap(full_latest.sort_values(by='Deaths', ascending=False).reset_index(drop=True),
              path=['Country','Province/State'],values='Deaths',height=700,
              title='Number of Deaths',
              color_discrete_sequence = px.colors.qualitative.Dark2)
fig.data[0].textinfo = 'label+text+value'
fig.show()


# # Covid 19 vs Other Similar Epidemics

# In[178]:


full_latest


# In[179]:


#wikipedia Source

epidemics = pd.DataFrame({
    'epidemic' : ['COVID-19','SARS','EBOLA','MERS','H1N1'],
    'start_year' : [2019, 2002, 2013, 2012, 2009],
    'end_year' : [2020, 2004, 2016, 2020, 2010],
    'confirmed' : [full_latest['Confirmed'].sum(), 8422, 28646, 2519, 6724149],
    'deaths' : [full_latest['Deaths'].sum(),813, 11323, 866, 19654]
})

epidemics['mortality']=round((epidemics['deaths']/epidemics['confirmed'])*100, 2)

epidemics.head()


# In[180]:


temp = epidemics.melt(id_vars='epidemic', value_vars=['confirmed', 'deaths', 'mortality'],
                     var_name='Case', value_name='Value')
fig = px.bar(temp, x='epidemic',y='Value',color='epidemic',text='Value',facet_col='Case',
            color_discrete_sequence=px.colors.qualitative.Bold)

fig.update_traces(textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
fig.update_yaxes(showticklabels=False)
fig.layout.yaxis2.update(matches=None)
fig.layout.yaxis3.update(matches=None)
fig.show()


# # Thank you
