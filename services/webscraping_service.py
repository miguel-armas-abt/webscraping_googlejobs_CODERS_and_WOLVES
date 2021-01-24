from time import sleep
import random
import re
from unicodedata import normalize
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller

from properties.configuration import *
from utils import util
import hashlib

from services import oferta_service
from services import oferta_detalle_service
from services import keyword_search_service

from models import webscraping
from models import oferta as ofertaModelo
from models import oferta_detalle

from dao import webscraping_dao


class WebScrapingService():

    def __init__(self):
        self.__wscraping_dao = webscraping_dao.WebscrapingDao()
        self.__of_service = oferta_service.OfertaService()
        self.__of_detalle_service = oferta_detalle_service.OfertaDetalleService()
        self.__key_service = keyword_search_service.KeywordSearchService()

    def insert_then_return_latest_row(self, webscraping: webscraping.WebScraping):
        return self.__wscraping_dao.insert_then_return_latest_row(webscraping)

    def iterar_scrape(self):
        ksearchs = self.__key_service.select_keyword_search()
        for ksearch in ksearchs:
            cadena_limpia = util.Utils().limpiar_cadena(ksearch[1])
            self.scrape_request(cadena_limpia, ksearch[0])

    def scrape_request(self, cadena_busqueda, id_keyword):
        pagina_web = GOOGLE_JOBS["WS_PORTAL_LABORAL"]               ## google jobs
        numero_paginas = GOOGLE_JOBS["WS_PAGINAS"]                  ## 0
        url_pagina = GOOGLE_JOBS["WS_PORTAL_LABORAL_URL"]           ## https://google.com

        ## incrusto mi keyword search en la url
        url_busqueda = "/search?q="+cadena_busqueda+"&ibp=htl;jobs#htivrt=jobs"
        url_busqueda = url_pagina + url_busqueda

        ## inserto el registro de webscraping
        wscraping = webscraping.WebScraping(
            None,                       # busqueda
            None,                       # busqueda_area
            pagina_web,                 # pagina_web
            url_pagina,                 # url_pagina
            url_busqueda,               # url_busqueda
            id_keyword                  # id_keyword
        )
        id_webscraping_insert = self.insert_then_return_latest_row(wscraping)
        self.scrape(url_busqueda, numero_paginas, id_webscraping_insert)


    def scrape(self, url_pagina, numero_paginas, id_webscraping):

        chromedriver_autoinstaller.install()

        # inicio el driver
        # driver = webdriver.Chrome('./chromedriver.exe')
        driver = webdriver.Chrome()
        driver.get(url_pagina)

        # scroll
        scroll_empleos = driver.find_element_by_class_name("vWdgBe")  # lista de empleos
        for x in range(0, numero_paginas):
            scroll_empleos.send_keys(Keys.END)
            sleep(0.5)
        scroll_empleos.send_keys(Keys.UP)

        # obtengo los campos del modelo oferta
        titulos = driver.find_elements_by_class_name("BjJfJf")  # items

        for titulo in titulos:
            item_detalle = driver.find_element_by_class_name("jolnDe")  # item contenedor
            titulo.click()
            sleep(random.uniform(0.5, 1))
            etiquetas = item_detalle.find_elements_by_class_name("sMzDkb")
            url_oferta = item_detalle.find_element_by_class_name("pMhGee").get_attribute('href')
            detalle = item_detalle.find_element_by_class_name("HBvzbc")
            tiempo_publicado = item_detalle.find_element_by_class_name("SuWscb").text

            try:
                masInfo = item_detalle.find_element_by_class_name("cVLgvc")
                masInfo.click()

            except:
                pass

            empresa = ""
            lugar = ""
            try:
                empresa = etiquetas[0].text
                lugar = etiquetas[1].text
                # empresa = item_detalle.find_element_by_class_name("nJlQNd").text
                # lugar = item_detalle.find_element_by_class_name("tJ9zfc").text
            except:
                pass

            id_anuncioempleo = hashlib.md5(str(detalle.text).encode()).hexdigest()
            ofer = ofertaModelo.Oferta(
                id_webscraping,                 # id_webscraping
                titulo.text,                    # titulo
                empresa,                        # empresa
                lugar,                          # lugar
                tiempo_publicado,               # tiempo publicado
                None,                           # salario
                None,                           # modalidad de trabajo
                None,                           # subarea
                url_oferta,                     # url oferta
                url_pagina,                     # url pagina
                None,                           # area
                datetime.now(),                 # fecha creacion
                datetime.now(),                 # fecha modificacion
                detalle.text,                   # detalle
                None,                           # fecha publicacion
                id_anuncioempleo                # id_anuncioempleo
            )

            id_oferta_insert = self.__of_service.insert_then_return_latest_row(ofer)
            parrafo = detalle.text.splitlines()
            self.limpiarParrafo(parrafo, id_oferta_insert)

    def limpiarParrafo(self, parrafo, id_oferta):
        for linea_descripcion in parrafo:
            linea_descripcion = linea_descripcion.strip()
            if (len(linea_descripcion) > 0):
                if (not linea_descripcion[0].isalpha()):
                    linea_descripcion = linea_descripcion[1:]
                linea_descripcion = linea_descripcion.strip().upper()
                linea_descripcion = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
                              normalize("NFD", linea_descripcion), 0, re.I)
                if (not linea_descripcion == ""):
                    # inserto cada linea en oferta_detalle
                    self.__of_detalle_service.insert_then_return_latest_row(
                    oferta_detalle.OfertaDetalle(
                        id_oferta,                          # id_oferta
                        linea_descripcion,                  # descripcion
                        None,                               # descripcion normalizada
                        None,                               # ind_activo            (entero)
                        None,                               # modo_inactivo         (entero)
                        datetime.now(),                     # fecha_creacion        (fecha)
                        datetime.now(),                     # fecha_modificacion    (fecha)
                        None                                # ofertaperfil_id       (entero)
                    ))

WebScrapingService().iterar_scrape()