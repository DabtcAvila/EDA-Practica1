#!/usr/bin/env python3
"""
Script de benchmark para comparar el rendimiento de las dos implementaciones.
Genera gráficas comparativas del tiempo de ejecución.
"""

import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


def ejecutar_programa(programa, archivo_datos):
    """Ejecuta un programa y retorna el tiempo de ejecución."""
    try:
        resultado = subprocess.run(
            ['python3', programa, archivo_datos],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Extraer tiempo de las líneas de error
        for linea in resultado.stderr.split('\n'):
            if 'Tiempo de ejecución:' in linea:
                tiempo = float(linea.split(':')[1].strip().split()[0])
                return tiempo
        
        return None
    except subprocess.TimeoutExpired:
        print(f"Timeout ejecutando {programa} con {archivo_datos}")
        return None
    except Exception as e:
        print(f"Error ejecutando {programa}: {e}")
        return None


def generar_datos_prueba(tamaños, proporcion_duplicados=0.2):
    """Genera archivos de datos de diferentes tamaños."""
    archivos = []
    
    for tamaño in tamaños:
        archivo = f"datos_test_{tamaño}.txt"
        subprocess.run([
            'python3', 'generar_datos.py',
            archivo, str(tamaño), str(proporcion_duplicados)
        ])
        archivos.append(archivo)
    
    return archivos


def realizar_benchmark(tamaños, num_repeticiones=3):
    """Realiza el benchmark comparativo."""
    print("Generando datos de prueba...")
    archivos = generar_datos_prueba(tamaños)
    
    tiempos_array = []
    tiempos_hash_poly = []
    tiempos_hash_mult = []
    tiempos_hash_sha = []
    
    for i, archivo in enumerate(archivos):
        tamaño = tamaños[i]
        print(f"\nProbando con {tamaño} pacientes...")
        
        # Probar versión con arreglo
        tiempos = []
        for _ in range(num_repeticiones):
            t = ejecutar_programa('array_version.py', archivo)
            if t is not None:
                tiempos.append(t)
        tiempo_promedio = np.mean(tiempos) if tiempos else 0
        tiempos_array.append(tiempo_promedio)
        print(f"  Array: {tiempo_promedio:.6f}s")
        
        # Probar versión hash con función polinomial
        tiempos = []
        for _ in range(num_repeticiones):
            t = ejecutar_programa('hash_version.py', archivo)
            if t is not None:
                tiempos.append(t)
        tiempo_promedio = np.mean(tiempos) if tiempos else 0
        tiempos_hash_poly.append(tiempo_promedio)
        print(f"  Hash (polynomial): {tiempo_promedio:.6f}s")
        
        # Probar versión hash con función multiplicativa
        tiempos = []
        for _ in range(num_repeticiones):
            resultado = subprocess.run(
                ['python3', 'hash_version.py', archivo, 'multiplicative'],
                capture_output=True,
                text=True,
                timeout=60
            )
            for linea in resultado.stderr.split('\n'):
                if 'Tiempo de ejecución:' in linea:
                    t = float(linea.split(':')[1].strip().split()[0])
                    tiempos.append(t)
                    break
        tiempo_promedio = np.mean(tiempos) if tiempos else 0
        tiempos_hash_mult.append(tiempo_promedio)
        print(f"  Hash (multiplicative): {tiempo_promedio:.6f}s")
        
        # Probar versión hash con SHA256
        tiempos = []
        for _ in range(num_repeticiones):
            resultado = subprocess.run(
                ['python3', 'hash_version.py', archivo, 'sha256'],
                capture_output=True,
                text=True,
                timeout=60
            )
            for linea in resultado.stderr.split('\n'):
                if 'Tiempo de ejecución:' in linea:
                    t = float(linea.split(':')[1].strip().split()[0])
                    tiempos.append(t)
                    break
        tiempo_promedio = np.mean(tiempos) if tiempos else 0
        tiempos_hash_sha.append(tiempo_promedio)
        print(f"  Hash (SHA256): {tiempo_promedio:.6f}s")
    
    # Limpiar archivos temporales
    for archivo in archivos:
        if os.path.exists(archivo):
            os.remove(archivo)
    
    return tiempos_array, tiempos_hash_poly, tiempos_hash_mult, tiempos_hash_sha


def generar_graficas(tamaños, tiempos_array, tiempos_hash_poly, tiempos_hash_mult, tiempos_hash_sha):
    """Genera las gráficas comparativas."""
    
    # Gráfica 1: Comparación general
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(tamaños, tiempos_array, 'o-', label='Arreglo Lineal', linewidth=2, markersize=8)
    plt.plot(tamaños, tiempos_hash_poly, 's-', label='Hash (Polynomial)', linewidth=2, markersize=8)
    plt.plot(tamaños, tiempos_hash_mult, '^-', label='Hash (Multiplicative)', linewidth=2, markersize=8)
    plt.plot(tamaños, tiempos_hash_sha, 'd-', label='Hash (SHA256)', linewidth=2, markersize=8)
    plt.xlabel('Número de Pacientes')
    plt.ylabel('Tiempo (segundos)')
    plt.title('Comparación de Tiempo de Ejecución')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Gráfica 2: Escala logarítmica
    plt.subplot(1, 2, 2)
    plt.loglog(tamaños, tiempos_array, 'o-', label='Arreglo Lineal', linewidth=2, markersize=8)
    plt.loglog(tamaños, tiempos_hash_poly, 's-', label='Hash (Polynomial)', linewidth=2, markersize=8)
    plt.loglog(tamaños, tiempos_hash_mult, '^-', label='Hash (Multiplicative)', linewidth=2, markersize=8)
    plt.loglog(tamaños, tiempos_hash_sha, 'd-', label='Hash (SHA256)', linewidth=2, markersize=8)
    plt.xlabel('Número de Pacientes (log)')
    plt.ylabel('Tiempo (segundos, log)')
    plt.title('Comparación de Tiempo (Escala Log-Log)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('comparacion_tiempos.png', dpi=150, bbox_inches='tight')
    print("\nGráfica guardada como 'comparacion_tiempos.png'")
    
    # Gráfica 3: Análisis de complejidad
    plt.figure(figsize=(10, 6))
    
    # Calcular speedup
    speedup_poly = [ta/th if th > 0 else 0 for ta, th in zip(tiempos_array, tiempos_hash_poly)]
    speedup_mult = [ta/th if th > 0 else 0 for ta, th in zip(tiempos_array, tiempos_hash_mult)]
    speedup_sha = [ta/th if th > 0 else 0 for ta, th in zip(tiempos_array, tiempos_hash_sha)]
    
    plt.plot(tamaños, speedup_poly, 'o-', label='Hash Polynomial vs Array', linewidth=2, markersize=8)
    plt.plot(tamaños, speedup_mult, 's-', label='Hash Multiplicative vs Array', linewidth=2, markersize=8)
    plt.plot(tamaños, speedup_sha, '^-', label='Hash SHA256 vs Array', linewidth=2, markersize=8)
    plt.axhline(y=1, color='r', linestyle='--', alpha=0.5, label='Sin mejora')
    plt.xlabel('Número de Pacientes')
    plt.ylabel('Speedup (veces más rápido)')
    plt.title('Factor de Aceleración de Hash vs Arreglo')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('speedup_analysis.png', dpi=150, bbox_inches='tight')
    print("Gráfica de speedup guardada como 'speedup_analysis.png'")


def main():
    # Verificar que existen los programas necesarios
    programas = ['array_version.py', 'hash_version.py', 'generar_datos.py']
    for programa in programas:
        if not os.path.exists(programa):
            print(f"Error: No se encuentra el archivo {programa}")
            sys.exit(1)
    
    # Tamaños para el benchmark
    tamaños = [100, 500, 1000, 2000, 5000, 10000, 20000]
    
    print("Iniciando benchmark...")
    print(f"Tamaños a probar: {tamaños}")
    print(f"Repeticiones por prueba: 3")
    
    tiempos_array, tiempos_hash_poly, tiempos_hash_mult, tiempos_hash_sha = realizar_benchmark(tamaños)
    
    print("\n" + "="*50)
    print("RESULTADOS FINALES")
    print("="*50)
    print(f"{'Tamaño':<10} {'Array':<15} {'Hash(Poly)':<15} {'Hash(Mult)':<15} {'Hash(SHA)':<15}")
    print("-"*70)
    
    for i, tamaño in enumerate(tamaños):
        print(f"{tamaño:<10} {tiempos_array[i]:<15.6f} {tiempos_hash_poly[i]:<15.6f} "
              f"{tiempos_hash_mult[i]:<15.6f} {tiempos_hash_sha[i]:<15.6f}")
    
    generar_graficas(tamaños, tiempos_array, tiempos_hash_poly, tiempos_hash_mult, tiempos_hash_sha)


if __name__ == "__main__":
    main()