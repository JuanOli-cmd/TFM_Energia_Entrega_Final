from datetime import datetime, timedelta
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import glob
import shutil
import argparse
import sys

# Rutas
base_dir = os.path.dirname(__file__)
proyecto_dir = os.path.abspath(os.path.join(base_dir, ".."))
download_dir = os.path.abspath(os.path.join(proyecto_dir, "data_download"))
tmp_dir = os.path.join(download_dir, "tmp")

# Comprobamos si existe y si no lo creamos
os.makedirs(download_dir, exist_ok=True)
os.makedirs(tmp_dir, exist_ok=True)

# Firefox Profile 
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.dir", tmp_dir)
profile.set_preference("browser.download.useDownloadDir", True)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/csv,application/octet-stream")
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.manager.scanWhenDone", False)

# Opciones
options = Options()
options.add_argument("-headless")
options.profile = profile

# Creamos el driver
driver = webdriver.Firefox(options=options)

# Función para descarga los ficheros de REEs segun la tabla que queramos cargar
def descargar_csv(driver, url, tabla):
    """Descarga CSV desde la URL y devuelve la ruta del fichero descargado."""

    # Antes del clic snapshot de ficheros existentes
    prev_files = set(glob.glob(os.path.join(tmp_dir, "*.csv")))

    # Cargar la URL
    driver.get(url)

    # Refrescamos para evitar fallos por cache detectados
    driver.refresh()

    # Esperar elemento y hacer clic
    wait = WebDriverWait(driver, 15)

    # Ponemos como sacar cada fichero en función de la tabla
    match tabla:
        case "tabla_demanda":
            selector_css = "#tabla_evolucion > thead:nth-child(1) > tr:nth-child(1) > th:nth-child(1) > span:nth-child(2)"
        case "tabla_generacion":   
            selector_css = "#tabla_generacion > thead:nth-child(1) > tr:nth-child(1) > th:nth-child(1) > div:nth-child(1) > span:nth-child(2)"
        case "tabla_emision":
            selector_css = "#tabla_emision > thead:nth-child(1) > tr:nth-child(1) > th:nth-child(1) > span:nth-child(2)"
        case "tabla_almacenamiento":
            selector_css = "#tabla_almacenamiento > thead:nth-child(1) > tr:nth-child(1) > th:nth-child(1) > div:nth-child(1) > span:nth-child(2)"
    

    # Esperamos a que este disponible para hacer click
    elemento = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, selector_css)
        ))

    # Hacemos el clic
    elemento.click()
    print(f"Clic hecho en {url}")

    # Esperamos un nuevo fichero
    timeout = 60
    start = time.time()
    new_file = None
    while time.time() - start < timeout:
        files = [f for f in glob.glob(os.path.join(tmp_dir, "*.csv")) if f not in prev_files]
        files = [f for f in files if not os.path.exists(f + ".part")]
        if files:
            new_file = files[0]
            break
        time.sleep(1)

    # Controlamos error si no se descarga
    if not new_file:
        raise RuntimeError("No se detectó el nuevo fichero descargado")

    # Indicamos que se cargo y devolvemos el fichero
    print(f"Descarga completada: {new_file}")
    return new_file



def descarga_ree (fecha_inicio = '2020-01-01', fecha_fin = '0'):
    # Controlamos que no haya errores
    try:

        # Tratamos los parametros de fechas de la función
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")

        if fecha_fin == '0':
            fecha_fin = datetime.strptime(str(datetime.today().date()), "%Y-%m-%d")
        else:
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        
        fecha_fin -= timedelta(days=1)

        current_date = fecha_inicio

        # Recorremos todas las fechas hasta llegar a la fecha_fin declarada
        while current_date <= fecha_fin:
            
            # Variables de fecha pasadas a string para las rutas
            fecha_str = current_date.strftime("%Y-%m-%d")
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Recorremos cada tabla con su codigo para la url
            for sufijo, tabla in [("1", "tabla_demanda"), ("2", "tabla_generacion"), ("3", "tabla_emision"), ("4", "tabla_almacenamiento")]:

                # Construimos patrón de búsqueda
                pattern = os.path.join(download_dir, tabla, f"{tabla}_{fecha_str}_*.csv")
                
                # Verificamos si ya hay un fichero para esa tabla y fecha
                ya_descargado = glob.glob(pattern)
                if ya_descargado:
                    print(f"Ya descargado: {tabla} {fecha_str}, se omite.")
                    continue
                
                # Comprobamos fechas que no estamos en las fechas que hemos detectado que tiene otra url a la estandar
                if fecha_str not in ('2021-05-13','2021-05-14','2021-05-15','2021-05-16'):
                    url = f"https://demanda.ree.es/visiona/peninsula/nacionalau/tablas/{fecha_str}/{sufijo}"
                
                # Solamente para dias entre el 2021-05-13 y el 2025-05-16
                else:
                    url = f"https://demanda.ree.es/visiona/peninsula/demandaau/tablas/{fecha_str}/{sufijo}" 
                
                # Descargamos el CSV de la tabla
                csv_path = descargar_csv(driver, url, tabla)

                # Movemos CSV a data_download con nombre único
                os.makedirs(os.path.join(download_dir, tabla), exist_ok=True)
                final_csv_name = f"{tabla}_{fecha_str}_{timestamp_str}.csv"
                final_csv_path = os.path.join(download_dir, tabla, final_csv_name)
                shutil.move(csv_path, final_csv_path)

            # recorremos al día siguiente
            current_date += timedelta(days=1)

    # Si falla salimos del driver
    finally:
        driver.quit()



if __name__ == "__main__":

    fecha_inicio_default = '2020-01-01'
    fecha_fin_default = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Definimos los argumentos desde terminal (son opcionales y si no los cogen ponemos los default anteriores)
    parser = argparse.ArgumentParser(description="Recorrer fechas entre dos rangos")
    parser.add_argument("--fecha_inicio", type=str, help="Fecha de inicio (YYYY-MM-DD)")
    parser.add_argument("--fecha_fin", type=str, help="Fecha de fin (YYYY-MM-DD)")
    args = parser.parse_args()

    # Vemos si usar las fechas introducidas o metemos los valores por defecto
    if not args.fecha_inicio:
        fecha_inicio = fecha_inicio_default
    else:
        fecha_inicio = args.fecha_inicio

    if not args.fecha_fin:
        fecha_fin = fecha_fin_default
    else:
        fecha_fin = args.fecha_fin

    if fecha_fin < fecha_inicio:
        print("La fecha de inicio no puede ser posterior a la fecha de fin")
        sys.exit(1)
    
    descarga_ree(fecha_inicio, fecha_fin)







