# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 16:44:05 2021

@author: Francisco Carreño
"""
import pandas as pd
import requests
import datetime as dt
class IOL():
    tk = ""
    def __init__(self,usr,pwd):
        #id = open(txt)
        #username = id.readline()
        #password = id.readline()
        #id.close()
        #self.username = username[::2].replace('\n','')
        #self.password = password[::2].replace('\n','')
        self.username = usr
        self.password = pwd
        self.tk = self.pedirToken()
        
    
    def pedirToken(self):
        url = 'https://api.invertironline.com/token'
        data = {"username":self.username,"password":self.password,"grant_type":"password"}
        r = requests.post(url=url,data=data).json()
        return r

    def checkToken(self):
        exp = dt.datetime.strptime(self.tk[".expires"], '%a, %d %b %Y %H:%M:%S GMT')
        ahora = dt.datetime.utcnow()
        tiempo = exp-ahora
        return tiempo
    
    def actualizarToken(self):
        #comprobar si está expirado
        if self.checkToken().days == 0:
            tokenOk = self.tk
        else:
            tokenOk = self.pedirToken()
        return tokenOk
    
    def getHist(self,ticker,FROM,TO, Aj = True):
      self.tk = self.actualizarToken()
      url_base = 'https://api.invertironline.com/api/v2/'
      if Aj:
        endpoint = 'bCBA/titulos/'+ticker+'/cotizacion/seriehistorica/'
        endpoint += FROM +'/'+ TO +'/ajustada'
      else:
        endpoint = 'bCBA/titulos/'+ticker+'/cotizacion/seriehistorica/'
        endpoint += FROM +'/'+ TO +'/sinAjustar'
      
      url = url_base + endpoint
      headers = {"Authorization" : "Bearer " + self.tk['access_token']}
    
      #llamado a la API
      data = requests.get(url = url, headers=headers).json()
      return (data)
    
    def getFCI(self):
        self.tk = self.actualizarToken()
        # config de la llamada a la api
        url_base = 'https://api.invertironline.com/api/v2/'
        endpoint = 'Titulos/FCI'
        url = url_base + endpoint
        headers = {"Authorization" : "Bearer " + self.tk['access_token']}
        # llamada a la api
        data = requests.get(url = url, headers=headers).json()
    
        #acomodamos la tabla
        tabla = pd.DataFrame(data)
        return(tabla)
    
    def titulo(self,ticker):
        self.tk = self.actualizarToken()
        #configuracion de la llamada a la api
        url_base = 'https://api.invertironline.com/api/v2/'
        endpoint = 'bcba/Titulos/'+ticker
        url = url_base + endpoint
        headers = {"Authorization" : "Bearer " + self.tk['access_token']}   
        # llamada a la api
        data = requests.get(url=url,headers=headers).json()
    
        return (data)
    
    def panel(self,instrumento, panel, pais):
        self.tk = self.actualizarToken()
        #configuracion de la llamada a la api
        url_base = 'https://api.invertironline.com/api/v2/'
        endpoint = 'Cotizaciones/'+instrumento+'/'+panel+'/'+pais
        url = url_base + endpoint
        headers = {"Authorization" : "Bearer " + self.tk['access_token']}   
        # llamada a la api
        data = requests.get(url=url,headers=headers).json()['titulos']
        tabla = pd.DataFrame(data).set_index('simbolo')
        return (tabla)
    
    def precio(self,ticker, mercado = 'bcba'):
        #configuracion de la llamada a la api
        url_base = 'https://api.invertironline.com/api/v2/'
        endpoint = mercado+'/Titulos/'+ticker+'/Cotizacion'
        url = url_base + endpoint
        headers = {"Authorization" : "Bearer " + self.tk['access_token']}   
        # llamada a la api
        data = requests.get(url=url,headers=headers).json()
        return (data)
    
    def opcionesDe(self,ticker):
        self.tk = self.actualizarToken()
        #configuracion de la llamada a la api
        url_base = 'https://api.invertironline.com/api/v2/'
        endpoint = 'bcba/Titulos/'+ticker+'/Opciones'
        url = url_base + endpoint
        headers = {"Authorization" : "Bearer " + self.tk['access_token']}   
        # llamada a la api
        data = requests.get(url=url,headers=headers).json()
    
        opciones = []
        for i in range(len(data)):
          opcion = data[i]['cotizacion']
          opcion['simbolo'] = data[i]['simbolo']
          opcion['tipo'] = data[i]['tipoOpcion']
          opcion['vencimiento'] = data[i]['fechaVencimiento']
          opcion['descripcion'] = data[i]['descripcion']
          opciones.append(opcion)
        tabla = pd.DataFrame(opciones).set_index('simbolo')
        return (tabla)
    
    def cuenta(self):
        self.tk = self.actualizarToken()
        #configuracion de la llamada a la api
        url_base = 'https://api.invertironline.com/api/v2/'
        endpoint = 'estadocuenta'
        url = url_base + endpoint
        headers = {"Authorization" : "Bearer " + self.tk['access_token']}   
        # llamada a la api
        data = requests.get(url=url,headers=headers).json()['cuentas']
        df = pd.DataFrame(data)
        return (df)
    
    def portafolio(self,pais='Argentina'):
        self.tk = self.actualizarToken()
        #configuracion de la llamada a la api
        url_base = 'https://api.invertironline.com/api/v2/'
        endpoint = 'portafolio/'+pais
        url = url_base + endpoint
        headers = {"Authorization" : "Bearer " + self.tk['access_token']}   
        # llamada a la api
        data = requests.get(url=url,headers=headers).json()['activos']
        df = pd.DataFrame(data)
        titulos = df['titulo']
        simbolo = []
        descripcion = []
        for i in range(len(titulos)):
          ticker = titulos[i]['simbolo']
          descrip = titulos[i]['descripcion']
          simbolo.append(ticker)
          descripcion.append(descrip)
        df['simbolo'] = simbolo
        df['descripcion'] = descripcion
        
        return (df.set_index('simbolo'))
    
    def operaciones(self):
        self.tk = self.actualizarToken()
        #configuracion de la llamada a la api
        url_base = 'https://api.invertironline.com/api/v2/'
        endpoint = 'operaciones/'
        url = url_base + endpoint
        headers = {"Authorization" : "Bearer " + self.tk['access_token']}   
        # llamada a la api
        data = requests.get(url=url,headers=headers).json()
        df = pd.DataFrame(data)
        return (df)
    
    def comprar(self,ticker, q=0,  precio=0,  monto = 0, plazo = 't2'):
        self.tk = self.actualizarToken()
        vigencia = dt.datetime.now() + dt.timedelta(days=1)
        vigencia_str = dt.datetime.strftime(vigencia, '%Y-%m-%d')
        if precio ==0:
            punta = self.puntas(ticker)
            precio = punta['precioVenta'][0]
        if monto != 0:
            q = int(round(monto/precio,0))
        params = {
          "mercado":"bCBA",
          "simbolo":ticker,
          "cantidad":q,
          "precio":precio,
          "plazo":plazo,
          "validez":vigencia_str
          }
        #configuracion de la llamada a la api
        url_base = 'https://api.invertironline.com/api/v2/'
        endpoint = 'operar/comprar/'
        url = url_base + endpoint
        headers = {"Authorization" : "Bearer " + self.tk['access_token']}   
        # llamada a la api
        data = requests.post(url=url,headers=headers, json = params).json()
        return (data)
    
    def vender(self,ticker, q,  precio=0, plazo = 't2'):
        self.tk = self.actualizarToken()
        vigencia = dt.datetime.now() + dt.timedelta(days=1)
        vigencia_str = dt.datetime.strftime(vigencia, '%Y-%m-%d')
        if precio ==0:
            punta = self.puntas(ticker)
            precio = punta['precioCompra'][0]
        params = {
          "mercado":"bCBA",
          "simbolo":ticker,
          "cantidad":q,
          "precio":precio,
          "plazo":plazo,
          "validez":vigencia_str
          }
        #configuracion de la llamada a la api
        url_base = 'https://api.invertironline.com/api/v2/'
        endpoint = 'operar/vender/'
        url = url_base + endpoint
        headers = {"Authorization" : "Bearer " + self.tk['access_token']}   
        # llamada a la api
        data = requests.post(url=url,headers=headers, json = params).json()
        return (data)
    
    def operacion(self,numero):
        self.tk = self.actualizarToken()
        #configuracion de la llamada a la api
        url_base = 'https://api.invertironline.com/api/v2/'
        endpoint = 'operaciones/'+str(numero)
        url = url_base + endpoint
        headers = {"Authorization" : "Bearer " + self.tk['access_token']}   
        # llamada a la api
        data = requests.get(url=url,headers=headers, json = params).json()
        return (data)
    
    def cancelar(self,numero):
        self.tk = self.actualizarToken()
        #configuracion de la llamada a la api
        url_base = 'https://api.invertironline.com/api/v2/'
        endpoint = 'operaciones/'+str(numero)
        url = url_base + endpoint
        headers = {"Authorization" : "Bearer " + self.tk['access_token']}   
        # llamada a la api
        data = requests.delete(url=url,headers=headers, json = params).json()
        return (data)
    
    def puntas(self,ticker, mercado= 'bcba'):
        data = self.precio(ticker, mercado)
        df = pd.DataFrame(data['puntas'])
        return df
    
    def resultado(self):
        data = self.portafolio()
        data['ganDiariaDinero'] = data.valorizado-(data.valorizado/(data.variacionDiaria/100+1))
        data['ten%']= data.valorizado/sum(data.valorizado)*100
        rtoDiarioTotal = sum(data.ganDiariaDinero)
        variacionDiariaTotal = sum(data.ganDiariaDinero)/sum(data.valorizado-data.ganDiariaDinero)*100
        gananciaPorcentaje = (sum(data.valorizado)/sum(data.valorizado-data.gananciaDinero)-1)*100
        gananciaDinero = sum(data.gananciaDinero)
        porcentajeTotal = sum(data['ten%'])
        valorizadoTotal = sum(data.valorizado)
        data = data.loc[:,['variacionDiaria','ganDiariaDinero','gananciaPorcentaje','gananciaDinero','ten%','valorizado']]
        data.loc['TOTAL'] = [variacionDiariaTotal, rtoDiarioTotal, gananciaPorcentaje, gananciaDinero,porcentajeTotal, valorizadoTotal]
        return (data)