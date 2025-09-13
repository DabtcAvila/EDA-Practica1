#!/usr/bin/env python3
"""
Versión con arreglo lineal para detectar pacientes con registros idénticos.
Almacena cada registro de paciente y busca duplicados mediante comparación lineal.

Estudiante: David Fernando Avila Díaz - Clave Única: 197851
Estudiante: José Gerardo Malfavaun Gorostizaga - Clave Única: 213398
Instituto Tecnológico Autónomo de México (ITAM)
Estructuras de Datos y Algoritmos
"""

import sys
import time


def leer_datos(archivo):
    """Lee los datos del archivo de entrada."""
    with open(archivo, 'r') as f:
        n = int(f.readline().strip())
        pacientes = []
        for _ in range(n):
            registro = list(map(int, f.readline().strip().split()))
            pacientes.append(registro)
    return pacientes


def buscar_duplicados_array(pacientes):
    """
    Busca pacientes con registros idénticos usando un arreglo lineal.
    Retorna el número de pacientes idénticos encontrados.
    """
    registros_vistos = []
    duplicados = set()
    indices_duplicados = set()
    
    for i, registro in enumerate(pacientes):
        for j, registro_visto in enumerate(registros_vistos):
            if registro == registro_visto:
                duplicados.add(tuple(registro))
                indices_duplicados.add(i)
                indices_duplicados.add(j)
                break
        registros_vistos.append(registro)
    
    return len(indices_duplicados)


def main():
    if len(sys.argv) != 2:
        print("Uso: python array_version.py <archivo_entrada>")
        sys.exit(1)
    
    archivo = sys.argv[1]
    
    start_time = time.perf_counter()
    
    pacientes = leer_datos(archivo)
    num_duplicados = buscar_duplicados_array(pacientes)
    
    end_time = time.perf_counter()
    tiempo_ejecucion = end_time - start_time
    
    if num_duplicados == 0:
        print("no hay dos pacientes con registros idénticos")
    else:
        print(f"se encontraron {num_duplicados} pacientes idénticos")
    
    print(f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos", file=sys.stderr)


if __name__ == "__main__":
    main()