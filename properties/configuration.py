
# DATABASE
DATABASE = {
    "DB_PASSWORD" : "oracle12c",
    "DB_USER" : "postgres",
    "DB_SERVICE" : "db_taller_sistemas",
    "DB_HOST" : "127.0.0.1"
    # "DB_PASSWORD" : "modulo4",
    # "DB_USER" : "modulo4",
    # "DB_HOST" : "161.35.60.197",
    # "DB_SERVICE" : "tcs7"
}

#SITIO-COMPUTRABAJO
COMPUTRABAJO = {
    "WS_PORTAL_LABORAL" : "computrabajo",
    "WS_PORTAL_LABORAL_URL" : "https://www.computrabajo.com.pe/",
    "WS_PAGINAS" : 2,  # 500 CANTIDAD DE PAGINAS A SCRAPEAR
    "WS_PAGINA_INICIAL" : 1,  # NUMERO DE PAGINA DESDE DONDE SE EMPEZARA A SCRAPEAR
    "WS_OFERTAS" : None,  # CANTIDAD DE OFERTAS POR PAGINA A SCRAPEAR (None: Sin limite)
    "WS_AREA" : None,  # FILTRO DE AREA PARA REALIZAR LA BUSQUEDA (None: Sin filtro)
}

#SITIO-INDEED
INDEED= {
    "WS_PORTAL_LABORAL" : "indeed",
    "WS_PORTAL_LABORAL_URL" : "https://pe.indeed.com",
    "WS_PAGINAS" : 1,  # 500 CANTIDAD DE PAGINAS A SCRAPEAR
    "WS_PAGINA_INICIAL" : 1,  # NUMERO DE PAGINA DESDE DONDE SE EMPEZARA A SCRAPEAR
    "WS_OFERTAS" : None,  # CANTIDAD DE OFERTAS POR PAGINA A SCRAPEAR (None: Sin limite)
    "WS_AREA" : None,  # FILTRO DE AREA PARA REALIZAR LA BUSQUEDA (None: Sin filtro)
}

#SITIO-INDEED
GOOGLE_JOBS= {
    "WS_PORTAL_LABORAL" : "google jobs",
    "WS_PORTAL_LABORAL_URL" : "https://google.com",
    "WS_PAGINAS" : 5,  # 500 CANTIDAD DE PAGINAS A SCRAPEAR
    "WS_PAGINA_INICIAL" : 1,  # NUMERO DE PAGINA DESDE DONDE SE EMPEZARA A SCRAPEAR
    "WS_OFERTAS" : None,  # CANTIDAD DE OFERTAS POR PAGINA A SCRAPEAR (None: Sin limite)
    "WS_AREA" : None,  # FILTRO DE AREA PARA REALIZAR LA BUSQUEDA (None: Sin filtro)
}














