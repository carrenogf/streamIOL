import streamlit as st
import pandas as pd
import IOL2

with st.form(key='my_form'):
    st.write("### Login IOL")
    st.write("Es necesario tener habilitada la API de IOL")
    usr = st.text_input("Usuario IOL:",value="", type="password")
    pwd = st.text_input("Contraseña IOL:", value="", type="password")
    submit_button = st.form_submit_button(label='Ingresar')
    if usr and pwd:
        try:
            iol = IOL2.IOL(usr,pwd)
            if iol.tk:
                st.write("Logueado exitosamente")
        except:
            st.warning("Error al loguearse")
        

with st.form(key='my_form_op'):
    st.write("### Buscar Ticker")
    ticker = st.text_input("Ticker: ")
    sb_op=st.form_submit_button(label="buscar")

if iol.tk:
    if ticker:
        try:
            df_op = iol.opcionesDe(ticker=ticker)
            st.dataframe(df_op)
        except:
            st.warning("ticker no encontrado")

