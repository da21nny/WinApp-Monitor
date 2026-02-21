import subprocess
import re

def verificar_actualizaciones():
    print("Analizando programas instalados y consultando repositorios en internet...")
    print("Esto puede tomar unos segundos...\n")
    
    try:
        # Ejecutamos winget de forma silenciosa para buscar actualizaciones en internet
        comando = ['winget', 'upgrade', '--accept-source-agreements']
        resultado = subprocess.run(
            comando, 
            capture_output=True, 
            text=True, 
            encoding='utf-8', 
            errors='ignore'
        )
        
        lineas = resultado.stdout.split('\n')
        leyendo_datos = False
        hay_actualizaciones = False
        
        for linea in lineas:
            linea = linea.strip()
            
            # Omitimos líneas vacías
            if not linea:
                continue
            
            # Detectamos la línea separadora "-------" que indica el inicio de la tabla
            if linea.startswith("---"):
                leyendo_datos = True
                continue
            
            if leyendo_datos:
                # Si llegamos a una línea de resumen de winget, paramos
                if "actualizaciones disponibles" in linea.lower() or linea.startswith(("-", " ")):
                    continue

                # Winget separa las columnas (Nombre, ID, Versión, Disponible, Origen) 
                # con múltiples espacios. Usamos expresiones regulares para dividir.
                columnas = re.split(r'\s{2,}', linea)
                
                # Si hay al menos 4 columnas identificadas, procesamos la información
                if len(columnas) >= 4:
                    hay_actualizaciones = True
                    nombre_app = columnas[0]
                    version_actual = columnas[2]
                    version_nueva = columnas[3]
                    
                    # Imprimir estrictamente en el formato solicitado
                    print(f"{nombre_app} - {version_actual} - {version_nueva}")

        if not hay_actualizaciones:
            print("Todos tus programas están actualizados o no se encontraron coincidencias en los repositorios.")

    except FileNotFoundError:
        print("Error crítico: 'winget' no está instalado o no se reconoce en tu sistema.")
        print("Este script está diseñado para Windows 10 o Windows 11.")
    except Exception as e:
        print(f"Ocurrió un error inesperado al ejecutar la automatización: {e}")

if __name__ == "__main__":
    verificar_actualizaciones()