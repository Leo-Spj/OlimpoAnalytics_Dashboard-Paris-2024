\
import csv
import ast # Para convertir la representación de cadena de la lista en una lista real

def generar_csv_codigos_equipos_atletas():
    # Paso 1: Leer atletas.tsv y crear un mapeo de nombre a código de atleta
    atletas_map = {}
    with open('atletas.tsv', 'r', encoding='utf-8') as f_atletas:
        reader_atletas = csv.DictReader(f_atletas, delimiter='\t')
        for row in reader_atletas:
            # Normalizar el nombre del atleta para la búsqueda
            # El formato en atletas.tsv es "APELLIDO Nombre" o "APELLIDO Nombre1 Nombre2"
            nombre_atleta_normalizado = row['name'].strip()
            atletas_map[nombre_atleta_normalizado] = row['code']

    # Paso 2: Leer equipos.tsv y procesar
    datos_para_csv = []
    with open('equipos.tsv', 'r', encoding='utf-8') as f_equipos:
        reader_equipos = csv.DictReader(f_equipos, delimiter='\t')
        for row_equipo in reader_equipos:
            codigo_equipo = row_equipo['code']
            
            # La columna 'athletes' es una cadena que representa una lista, ej: "['KAO Wenchao', 'LI Zhongyuan']"
            # Usamos ast.literal_eval para convertirla de forma segura a una lista de Python
            try:
                nombres_atletas_equipo_str = row_equipo['athletes']
                # Asegurarse de que la cadena esté correctamente formateada para ast.literal_eval
                # A veces los nombres pueden tener comillas simples internas si hay apóstrofes,
                # pero el formato general de la lista es con comillas simples.
                # Si los nombres mismos contienen comillas dobles, ast.literal_eval debería manejarlos.
                nombres_atletas_equipo = ast.literal_eval(nombres_atletas_equipo_str)
            except (ValueError, SyntaxError) as e:
                print(f"Error al parsear atletas para el equipo {codigo_equipo}: {row_equipo['athletes']}. Error: {e}")
                continue # Saltar este equipo si hay un error de parseo

            codigos_atletas_equipo = []
            for nombre_atleta_equipo in nombres_atletas_equipo:
                # Normalizar el nombre del atleta del equipo para la búsqueda
                # El formato en equipos.tsv parece ser "APELLIDO Nombre" o "APELLIDO Nombre1 Nombre2"
                nombre_atleta_equipo_normalizado = nombre_atleta_equipo.strip()
                
                codigo_atleta = atletas_map.get(nombre_atleta_equipo_normalizado)
                if codigo_atleta:
                    # En lugar de agregar a una lista para luego unir,
                    # agregamos directamente una fila por cada atleta del equipo.
                    datos_para_csv.append({
                        'codigo_equipo': codigo_equipo,
                        'codigo_atleta': codigo_atleta  # Campo individual para el código del atleta
                    })
                else:
                    # Intentar una coincidencia más laxa si no se encuentra directamente
                    # Por ejemplo, si el nombre en equipos.tsv tiene comillas dobles internas que no están en atletas.tsv
                    # O si hay variaciones menores.
                    # Esta es una heurística simple, podría necesitar ser más robusta.
                    encontrado_alternativo = False
                    for nombre_map, cod_map in atletas_map.items():
                        if nombre_atleta_equipo_normalizado.lower() == nombre_map.lower():
                            datos_para_csv.append({ # Agregar fila si se encuentra alternativo
                                'codigo_equipo': codigo_equipo,
                                'codigo_atleta': cod_map
                            })
                            encontrado_alternativo = True
                            break
                    if not encontrado_alternativo:
                        print(f"Advertencia: No se encontró el código para el atleta '{nombre_atleta_equipo_normalizado}' del equipo '{codigo_equipo}'.")
            
            # Ya no se unen los códigos de los atletas aquí, se agregan individualmente arriba.
            # Ya no es necesario:
            # datos_para_csv.append({
            #     'codigo_equipo': codigo_equipo,
            #     'codigos_atletas': ','.join(codigos_atletas_equipo)
            # })

    # Paso 3: Escribir los resultados en un nuevo archivo CSV
    nombre_archivo_salida = 'equipos_atletas_codigos_normalizado.csv' # Cambiado nombre de archivo para reflejar el cambio
    with open(nombre_archivo_salida, 'w', newline='', encoding='utf-8') as f_salida:
        if datos_para_csv: # Asegurarse de que hay datos para escribir
            campos = ['codigo_equipo', 'codigo_atleta'] # Campos actualizados para la salida normalizada
            writer = csv.DictWriter(f_salida, fieldnames=campos)
            writer.writeheader()
            writer.writerows(datos_para_csv)
        else:
            print("No se generaron datos para escribir en el CSV.")

    print(f"Archivo '{nombre_archivo_salida}' generado exitosamente.")

if __name__ == '__main__':
    generar_csv_codigos_equipos_atletas()
