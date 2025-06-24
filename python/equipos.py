\
import csv
import ast

def procesar_datos_atletas_equipos(path_atletas, path_equipos, path_salida_relacion, path_salida_no_registrados):
    """
    Procesa los archivos de atletas y equipos para generar relaciones y listas de atletas no registrados.
    """
    atletas_existentes = {}
    try:
        with open(path_atletas, 'r', encoding='utf-8') as f_atletas:
            lector_atletas = csv.reader(f_atletas, delimiter='\t')
            next(lector_atletas)  # Omitir encabezado
            for fila in lector_atletas:
                if len(fila) == 2:
                    atletas_existentes[fila[0].strip()] = fila[1].strip()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {path_atletas}")
        return
    except Exception as e:
        print(f"Error al leer {path_atletas}: {e}")
        return

    relacion_equipo_atleta = []
    atletas_no_registrados_dict = {} # Usar un diccionario para evitar duplicados y facilitar la búsqueda

    try:
        with open(path_equipos, 'r', encoding='utf-8') as f_equipos:
            lector_equipos = csv.reader(f_equipos, delimiter='\t')
            encabezado_equipos = next(lector_equipos)  # Guardar encabezado
            
            # Encontrar los índices de las columnas relevantes
            try:
                idx_codigo_equipo = encabezado_equipos.index('code')
                idx_nombres_atletas = encabezado_equipos.index('athletes')
                idx_codigos_atletas = encabezado_equipos.index('athletes_codes')
            except ValueError as e:
                print(f"Error: Falta una columna esperada en {path_equipos}. Columnas encontradas: {encabezado_equipos}. Error: {e}")
                return

            for fila_equipo in lector_equipos:
                if len(fila_equipo) < max(idx_codigo_equipo, idx_nombres_atletas, idx_codigos_atletas) + 1:
                    # print(f"Advertencia: Fila incompleta en equipos.tsv: {fila_equipo}")
                    continue

                codigo_equipo = fila_equipo[idx_codigo_equipo].strip()
                
                try:
                    nombres_atletas_str = fila_equipo[idx_nombres_atletas]
                    codigos_atletas_str = fila_equipo[idx_codigos_atletas]

                    # Usar ast.literal_eval para convertir las cadenas de listas en listas reales
                    nombres_atletas = ast.literal_eval(nombres_atletas_str)
                    codigos_atletas = ast.literal_eval(codigos_atletas_str)
                except (SyntaxError, ValueError) as e:
                    # print(f"Advertencia: Error al procesar datos de atletas para el equipo {codigo_equipo}: {e}. Fila: {fila_equipo}")
                    continue # Saltar esta fila si el formato no es el esperado

                if len(nombres_atletas) != len(codigos_atletas):
                    # print(f"Advertencia: Discrepancia en la cantidad de nombres y códigos para el equipo {codigo_equipo}. Nombres: {len(nombres_atletas)}, Códigos: {len(codigos_atletas)}")
                    continue

                for i, codigo_atleta in enumerate(codigos_atletas):
                    codigo_atleta_limpio = codigo_atleta.strip()
                    relacion_equipo_atleta.append((codigo_equipo, codigo_atleta_limpio))

                    if codigo_atleta_limpio not in atletas_existentes:
                        nombre_atleta = nombres_atletas[i].strip() if i < len(nombres_atletas) else "Nombre Desconocido"
                        # Solo añadir si no está ya en el diccionario para evitar duplicados en el archivo de salida
                        if codigo_atleta_limpio not in atletas_no_registrados_dict:
                             atletas_no_registrados_dict[codigo_atleta_limpio] = nombre_atleta
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {path_equipos}")
        return
    except Exception as e:
        print(f"Error al leer {path_equipos}: {e}")
        return

    # Escribir archivo de relación equipo-atleta
    try:
        with open(path_salida_relacion, 'w', newline='', encoding='utf-8') as f_salida_rel:
            escritor_rel = csv.writer(f_salida_rel, delimiter=',') # Cambiado a coma
            escritor_rel.writerow(['codigo_equipo', 'codigo_atleta']) # Encabezado
            escritor_rel.writerows(relacion_equipo_atleta)
        print(f"Archivo de relación equipo-atleta guardado en: {path_salida_relacion}")
    except IOError as e:
        print(f"Error al escribir el archivo {path_salida_relacion}: {e}")


    # Escribir archivo de atletas no registrados
    atletas_no_registrados_lista = list(atletas_no_registrados_dict.items()) # Convertir el diccionario a lista de tuplas

    try:
        with open(path_salida_no_registrados, 'w', newline='', encoding='utf-8') as f_salida_no_reg:
            escritor_no_reg = csv.writer(f_salida_no_reg, delimiter=',') # Cambiado a coma
            escritor_no_reg.writerow(['codigo_atleta', 'nombre_atleta']) # Encabezado
            escritor_no_reg.writerows(atletas_no_registrados_lista)
        print(f"Archivo de atletas no registrados guardado en: {path_salida_no_registrados}")
    except IOError as e:
        print(f"Error al escribir el archivo {path_salida_no_registrados}: {e}")


if __name__ == "__main__":
    # Rutas a los archivos (ajusta según sea necesario)
    ruta_base = "c:\\\\Users\\\\Leo\\\\OneDrive - Universidad Tecnologica del Peru\\\\CODIGO\\\\CoderHouse\\\\Data_Analytics\\\\Avance proyecto\\\\equipos\\\\"
    
    archivo_atletas = ruta_base + "atletas.tsv"
    archivo_equipos = ruta_base + "equipos.tsv"
    
    archivo_salida_relacion = ruta_base + "equipo_atleta_relacion.csv" # Cambiado a .csv
    archivo_salida_no_registrados = ruta_base + "atletas_no_registrados.csv" # Cambiado a .csv
    
    procesar_datos_atletas_equipos(archivo_atletas, archivo_equipos, archivo_salida_relacion, archivo_salida_no_registrados)
