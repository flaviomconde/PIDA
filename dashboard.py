import pandas as pd
import yfinance as yf
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

#cargamos una imagen
st.image('https://assets.soyhenry.com/henry-landing/assets/Henry/logo-white.png')

# le ponemos titulo
st.title('Porque invertir en Microsoft (MSFT)')
#le agregamos un espacio de separacion
st.markdown('##')

##Datos de la empresa
col1, col2 = st.columns(2)

with col1:
    st.subheader(':moneybag: Cap. Mercado:')
    st.write('2.081T U$D')
    st.subheader(':dollar: Ventas:')
    st.write('198.27M U$D')
    st.subheader(':top: G/A en el 2022:')
    st.write('19.72%')

    
with col2:
    st.subheader(':bar_chart: Precio De La Accion:')
    st.write('280.60 U$D')
    st.subheader(':money_with_wings: Ingresos :')
    st.write('198.09B U$D')
    st.subheader(':chart: Dividendos %:')
    st.write('2.60%')

st.image('https://i0.wp.com/fourweekmba.com/wp-content/uploads/2023/01/microsoft-business-model.png?resize=1536%2C1158&ssl=1')

st.markdown('##')

#traemos el dataset a trabajar
msft = pd.read_csv('./msft.csv')
msft.set_index("Date", inplace=True)

#KPI porcentaje de cambio en el precio de cierre
change_pct = (msft["Adj Close"][-1] - msft["Adj Close"][0]) / msft["Adj Close"][0] * 100
st.subheader(f":chart_with_upwards_trend: Porcentaje de cambio en el precio de cierre:")
st.write(f"{change_pct:.2f}%")
#-------------------------------------------------------------------------------------------
#KPI precio promedio al cierre
avg_close_price = msft["Adj Close"].mean()
st.subheader(f":money_with_wings: Precio promedio de cierre:")
st.write(f"{avg_close_price:.2f} U$D")
#-------------------------------------------------------------------------------------------
# KPI Volatilidad de la acción de msft en comparación con otras empresas del sector tecnologico
# Obtener los datos de las empresas del sector
tickers = ["MSFT", "AMZN", "GOOG", "ADBE", "ROP"]  #tickers de las empresas que deseas comparar
technologies_sector = yf.download(tickers, start='2000-01-01', end='2023-03-26', group_by='ticker')

# Calcular la desviación estándar del precio de cierre ajustado de cada empresa
std_MSFT = technologies_sector["MSFT"]["Adj Close"].std()
std_AMZN = technologies_sector["AMZN"]["Adj Close"].std()
std_GOOG = technologies_sector["GOOG"]["Adj Close"].std()
std_ADBE = technologies_sector["ADBE"]["Adj Close"].std()
std_ROP = technologies_sector["ROP"]["Adj Close"].std()

# Crear un DataFrame con los resultados
data = {"Ticker": ["MSFT", "AMZN", "GOOG", "ADBE", "ROP"],
        "Desviación estándar del precio de cierre ajustado": [std_MSFT, std_AMZN, std_GOOG, std_ADBE, std_ROP]}
df = pd.DataFrame(data)

# Mostrar el DataFrame en Streamlit
st.subheader(":fire: Volatilidad de la acción de MSFT comparado con otras empresas del sector tecnologico :fire:")
st.write(df)
#--------------------------------------------------------------------------------------------

#MOSTRAMOS EL VALOR DE SP500
msft = pd.read_csv('./msft.csv')
msft.set_index("Date", inplace=True)

st.header('Grafica de la accion SP500:chart_with_upwards_trend:')
st.line_chart(msft.Close)
#-------------------------------------------------------------------------------------------

#MOSTRAMOS EL VALOR DEL SECTOR TECNOLOGICO
sec_tec = pd.read_csv('./tecnologicas.csv')
sec_tec.set_index("Date", inplace=True)

st.header('Grafica del sector tecnologico:chart_with_upwards_trend:')
st.line_chart(sec_tec.Close)
#------------------------------------------------------------------------------------------

## 1. VALOR DE MICROSOFT
#Gráfico de líneas
st.header('Grafica de la accion MSFT:chart_with_upwards_trend:')
st.line_chart(msft.Close)
#------------------------------------------------------------------------------------------

# Gráfico de empresas históricos: Un gráfico que muestre los precios de cierre históricos de Microsoft, el XLK desde el 2000.
#  Esto podría ayudar a ilustrar cómo ha evolucionado el precio de Chevron en comparación con el sector energético específicamente.

st.header('Relacion entre los precios de Microsoft y el XLK (Indice del sector tecnologico)')

# Tickers de Microsoft y del sector tecnologico
chevron = msft
tech = sec_tec

# Creación de un DataFrame con los precios de Microsoft y del sector tecnologico
prices_df = pd.DataFrame({"Microsoft": msft["Adj Close"], "XLK": tech["Adj Close"]})

# Creación del gráfico de líneas
fig = px.line(prices_df, title="Relación entre los precios de Microsoft y del XLK")

# Agregar las series de datos para Microsoft y del sector tecnologico
fig.add_scatter(x=prices_df.index, y=prices_df["Microsoft"], name="Microsoft")
fig.add_scatter(x=prices_df.index, y=prices_df["XLK"], name="XLK")

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

#-------------------------------------------------------------------------------

# COMPARACION CON OTRAS EMPRESAS DEL SECTOR
st.header('Comparacion con otras empresas :bar_chart:')
tickers = ('AMZN','AAPL','MSFT','ROP','GOOG')
dropdown = st.multiselect('Elija sus acciones',
                          tickers)

start = st.date_input('Start', value = pd.to_datetime('2000-01-01'))
end = st.date_input('End',value = pd.to_datetime('today'))

def relativeret(df):
    rel = df.pct_change()
    cumret= (1+rel).cumprod() - 1
    cumret = cumret.fillna(0)
    return cumret

if len(dropdown) > 0:
    #df = yf.download(dropdown, start,end)['Adj Close']
    df = relativeret(yf.download(dropdown,start,end)['Close'])
    st.header('seleccionaste{}'.format(dropdown))
    st.line_chart(df)

#------------------------------------------------------------------------------------------



# MEJOR DIA PARA INVERTIR
msft2 = pd.read_csv('./msft2.csv')
#msft2.set_index("Date", inplace=True)

st.header('Mejor dia de la semana que podemos invertir en MSFT')

order_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

msft2["Date"] = pd.to_datetime(msft2["Date"])
msft2["Weekday"] = msft2["Date"].dt.day_name()

# Calcular el rendimiento diario
msft2["Daily Return"] = msft2["Adj Close"].pct_change()

# Añadir una columna que contenga el día de la semana correspondiente a cada fecha
msft2["Weekday"] = msft2["Date"].dt.day_name()

# Convertir la columna Weekday en una categoría con un orden personalizado de días de la semana
msft2["Weekday"] = pd.Categorical(msft2["Weekday"], categories=order_day, ordered=True)

# Agrupar los datos por día de la semana y calcular el rendimiento promedio
mean_return = msft2.groupby("Weekday")["Daily Return"].mean().reset_index()

# Visualizar los resultados en una gráfica de barras
figG = px.bar(mean_return, x="Weekday", y="Daily Return", color="Weekday",
             color_discrete_sequence=px.colors.qualitative.Pastel)
figG.update_layout(title="Rendimiento promedio diario de la acción de Microsoft (MSFT) por día de la semana")
st.plotly_chart(figG)

#-----------------------------------------------------------------------------------------


# comparacion con otras empresas del sector tecnologico
comp = pd.read_csv('./comparacion.csv')
comp.set_index("Date", inplace=True)
st.header('Relacion entre los precios de Microsoft y 4 empresas importantes del sector tecnologico')

# Seleccionar solo los precios de cierre
precios_cierre = comp.filter(regex='_Close')

# Renombrar las columnas eliminando el sufijo "_Close"
nombres_empresas = [nombre[:-6] for nombre in precios_cierre.columns]
precios_cierre.columns = nombres_empresas

# Crear el DataFrame para el gráfico
df = precios_cierre.reset_index()

# Convertir la columna "Date" en índice
df = df.set_index('Date')

# Crear el gráfico de líneas
fig = px.line(df, title="Relación entre los precios de cierre de las empresas AAPL, MSFT, GOOG, ROP y AMZN")

# Agregar las series de datos para cada empresa
for empresa in nombres_empresas:
    fig.add_scatter(x=df.index, y=df[empresa], name=empresa)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

#-----------------------------------------------------------------

#imagen de relacion open ia y microsoft
st.image('https://i.blogs.es/875a99/1366_2000/1366_2000.webp')

#-----------------------------------------------------------------
#estimacion para la ccion de microsoft
st.header('Estimacion futura entre 2023 al 2027 de la accion de Microsoft')

st.subheader(':moneybag: BPA 2027:')
st.write('15.35 U$D')
st.subheader(':dollar: PER:')
st.write('29 X')
st.subheader(':top: Precio objetivo 2027:')
st.write('445 U$D')


st.balloons()