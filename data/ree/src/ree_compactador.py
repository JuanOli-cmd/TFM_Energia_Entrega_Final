import pandas as pd
import os
import re
import sys
import shutil
from datetime import datetime, timedelta
import argparse
from tqdm import tqdm


def compactador_ree (fecha_inicio = '2020-01-01', fecha_fin = '0'):
    ''' Función para compactar los datos de REE descargados '''

    # Tratamos los parametros de fechas de la función
    fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")

    if fecha_fin == '0':
        fecha_fin_dt = datetime.strptime(str(datetime.today().date()), "%Y-%m-%d")
    else:
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
    
    

    print(f"Se va cargar en parquet desde {fecha_inicio_dt.date()} hasta {fecha_fin_dt.date()}")

    # Carpeta con los CSV
    carpeta_csv = "../data_download"

    # Carpeta de salida para los Parquet
    carpeta_parquet = "../data_parquet"
    os.makedirs(carpeta_parquet, exist_ok=True)

    # Regex para extraer tipo_tabla, fecha_datos
    patron_archivo = re.compile(r"tabla_(\w+)_((\d{4})-(\d{2})-(\d{2}))_")

    list_tabla = ['tabla_demanda','tabla_generacion','tabla_almacenamiento','tabla_emision']

    # Recorremos todas los ficheros cargando los de cada tabla
    for tabla in tqdm(list_tabla, colour='green'):
        print(f"Cargando tabla {tabla}")
        path_tabla_csv = os.path.join(carpeta_csv,tabla)
        if not os.path.isdir(path_tabla_csv):
            print("El directorio NO existe. No hay nada que cargar")
            sys.exit(1)
        list_df = []
        for archivo in tqdm(sorted(os.listdir(path_tabla_csv)), colour='red'):
            if archivo.endswith(".csv"):
                match = patron_archivo.search(archivo)
                if match:
                    tipo_tabla, date, year, month, day = match.groups()

                    # Vamos a comprobar que el fichero esta en el rango de fechas a compactar
                    date_dt = datetime.strptime(date, "%Y-%m-%d")

                    if fecha_inicio_dt > date_dt:
                        continue

                    if fecha_fin_dt < date_dt:
                        break

                    ruta_csv = os.path.join(path_tabla_csv, archivo)

                    # Tenemos que abrir cada fichero y añadirle a las cabeceras una , al final si los datos lo tienen, para que encajen las columnas, aprovechamos y lo guardamos sin el titulo inicial
                    with open(ruta_csv, "r", encoding="latin-1") as f:
                        lineas = f.readlines()

                    # Verifica si hay inconsistencia de última columna vacía
                    header = lineas[2].strip()
                    primer_dato = lineas[3].strip()
                    if primer_dato.endswith(",") and not header.endswith(","):
                        lineas[2] = header + ",\n"

                    # Guardar archivo temporal corregido
                    ruta_temp = os.path.join(path_tabla_csv, "temp_" + archivo)

                    with open(ruta_temp, "w", encoding="utf-8") as f:
                        # quitamos el titulo
                        f.writelines(lineas[2:])

                    # Leemos el CSV
                    df = pd.read_csv(
                        ruta_temp,
                        encoding='utf8',
                        header=0,
                        quotechar='"',
                        skipinitialspace=True,
                        engine='python'
                    )

                    # La columna final que se crea la eliminamos al solo tener NaN
                    if df.columns[-1] == '' or df.columns[-1].startswith('Unnamed'):
                        df = df.iloc[:, :-1]

                    # Hay ficheros que tienen la hora 02 como 2A y/o 2B, por ello nos quedamos si hay las dos nos quedamos con una y prevale el 2A por seguir mejor la serie en los analizados
                    tiene_2A = df["Hora"].str.contains("2A:", na=False)
                    tiene_2B = df["Hora"].str.contains("2B:", na=False)

                    # Si hay 2A, lo normalizamos y eliminamos 2B si hay tambien
                    if tiene_2A.any():
                        df.loc[tiene_2A, "Hora"] = df.loc[tiene_2A, "Hora"].str.replace("2A:", "02:", regex=False)
                        df = df[~tiene_2B]

                    # Si no hay 2A pero sí hay 2B, lo normalizamos
                    elif tiene_2B.any():
                        df.loc[tiene_2B, "Hora"] = df.loc[tiene_2B, "Hora"].str.replace("2B:", "02:", regex=False)


                    df["Hora"] = pd.to_datetime(df["Hora"])

                    # Filtramos por la fecha del archivo
                    fecha_datos = pd.to_datetime(date)
                    df = df[df["Hora"].dt.date == fecha_datos.date()]

                    # Añadir columna 'year'
                    df["year"] = year

                    list_df.append(df)

                    # Borramos el fichero temporal creado
                    os.remove(ruta_temp)

        #  Unimos los dataframes de la tabla y guardamos como Parquet particionando por año
        df_tabla = pd.concat(list_df, ignore_index=True)

        # Si existe la carpeta de la tabla la borramos para que no haya datos repetidos
        carpeta_tabla_parquet = os.path.join(carpeta_parquet, tipo_tabla)
        print(f"Guardando tabla {tipo_tabla} en formato parquet en {carpeta_tabla_parquet}")
        print(f"Eliminando carpeta si existe de  {carpeta_tabla_parquet}")
        if os.path.exists(carpeta_tabla_parquet):
            shutil.rmtree(carpeta_tabla_parquet)

        df_tabla.to_parquet(os.path.join(carpeta_parquet, tipo_tabla), index=False, compression='snappy', partition_cols=['year'])

    print(f"Finalizado")


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


    compactador_ree(fecha_inicio, fecha_fin)

