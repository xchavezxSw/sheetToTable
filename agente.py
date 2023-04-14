import logging

# crea una instancia de logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# crea un archivo de registro
handler = logging.FileHandler('debug.log', mode='a')

# configura el formato del mensaje
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

# agrega el manejador de registro al logger
logger.addHandler(handler)
