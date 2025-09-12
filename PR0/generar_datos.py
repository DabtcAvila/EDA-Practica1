#!/usr/bin/env python3
"""
Generador de datos de prueba para el análisis de pacientes.
Genera archivos con diferentes tamaños y proporciones de duplicados.
"""

import random
import sys


def generar_datos(n, num_estudios=10, max_valor=10000000, proporcion_duplicados=0.1):
    """
    Genera datos de pacientes con estudios de laboratorio.
    
    n: número de pacientes
    num_estudios: número de estudios por paciente (default 10)
    max_valor: valor máximo para cada estudio
    proporcion_duplicados: proporción de registros duplicados (0.0 a 1.0)
    """
    pacientes = []
    num_duplicados = int(n * proporcion_duplicados)
    num_unicos = n - num_duplicados
    
    # Generar registros únicos
    registros_unicos = []
    for _ in range(num_unicos):
        registro = [random.randint(0, max_valor) for _ in range(num_estudios)]
        registros_unicos.append(registro)
    
    pacientes.extend(registros_unicos)
    
    # Generar duplicados si es necesario
    if num_duplicados > 0 and registros_unicos:
        for _ in range(num_duplicados):
            registro_a_duplicar = random.choice(registros_unicos)
            pacientes.append(registro_a_duplicar[:])
    
    # Mezclar aleatoriamente
    random.shuffle(pacientes)
    
    return pacientes


def guardar_datos(archivo, pacientes):
    """Guarda los datos en un archivo."""
    with open(archivo, 'w') as f:
        f.write(f"{len(pacientes)}\n")
        for paciente in pacientes:
            f.write(" ".join(map(str, paciente)) + "\n")


def main():
    if len(sys.argv) < 3:
        print("Uso: python generar_datos.py <archivo_salida> <num_pacientes> [proporcion_duplicados]")
        print("Ejemplo: python generar_datos.py datos_100.txt 100 0.2")
        sys.exit(1)
    
    archivo = sys.argv[1]
    n = int(sys.argv[2])
    proporcion_duplicados = float(sys.argv[3]) if len(sys.argv) > 3 else 0.1
    
    pacientes = generar_datos(n, proporcion_duplicados=proporcion_duplicados)
    guardar_datos(archivo, pacientes)
    
    print(f"Archivo '{archivo}' generado con {n} pacientes")
    print(f"Proporción de duplicados: {proporcion_duplicados:.1%}")


if __name__ == "__main__":
    main()