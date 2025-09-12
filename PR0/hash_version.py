#!/usr/bin/env python3
"""
Versión con tabla hash para detectar pacientes con registros idénticos.
Utiliza una tabla hash con diferentes funciones hash opcionales para minimizar colisiones.
"""

import sys
import time
import hashlib


class TablaHash:
    def __init__(self, size=10007, hash_function='polynomial'):
        """
        Inicializa la tabla hash.
        size: tamaño de la tabla (primo para mejor distribución)
        hash_function: tipo de función hash a usar ('polynomial', 'multiplicative', 'sha256')
        """
        self.size = size
        self.tabla = [[] for _ in range(size)]
        self.hash_function = hash_function
        self.colisiones = 0
        
    def _hash_polynomial(self, registro):
        """Función hash polinomial para mejor distribución."""
        p = 31
        m = self.size
        hash_value = 0
        p_pow = 1
        
        for valor in registro:
            hash_value = (hash_value + (valor + 1) * p_pow) % m
            p_pow = (p_pow * p) % m
            
        return hash_value
    
    def _hash_multiplicative(self, registro):
        """Función hash multiplicativa."""
        A = 0.6180339887  # Constante de Knuth
        hash_sum = sum(registro)
        return int(self.size * ((hash_sum * A) % 1))
    
    def _hash_sha256(self, registro):
        """Función hash usando SHA-256 para distribución uniforme."""
        str_registro = '-'.join(map(str, registro))
        hash_obj = hashlib.sha256(str_registro.encode())
        hash_hex = hash_obj.hexdigest()
        return int(hash_hex, 16) % self.size
    
    def hash(self, registro):
        """Aplica la función hash seleccionada."""
        if self.hash_function == 'polynomial':
            return self._hash_polynomial(registro)
        elif self.hash_function == 'multiplicative':
            return self._hash_multiplicative(registro)
        elif self.hash_function == 'sha256':
            return self._hash_sha256(registro)
        else:
            return self._hash_polynomial(registro)
    
    def insertar(self, registro, indice_paciente):
        """Inserta un registro en la tabla hash."""
        hash_value = self.hash(registro)
        bucket = self.tabla[hash_value]
        
        if len(bucket) > 0:
            self.colisiones += 1
        
        for reg, indices in bucket:
            if reg == registro:
                indices.append(indice_paciente)
                return True
        
        bucket.append((registro, [indice_paciente]))
        return False
    
    def buscar_duplicados(self):
        """Cuenta el número total de pacientes con registros duplicados."""
        total_duplicados = 0
        
        for bucket in self.tabla:
            for registro, indices in bucket:
                if len(indices) > 1:
                    total_duplicados += len(indices)
        
        return total_duplicados
    
    def obtener_estadisticas(self):
        """Retorna estadísticas sobre la tabla hash."""
        buckets_ocupados = sum(1 for bucket in self.tabla if len(bucket) > 0)
        max_bucket_size = max(len(bucket) for bucket in self.tabla)
        promedio_bucket = sum(len(bucket) for bucket in self.tabla) / buckets_ocupados if buckets_ocupados > 0 else 0
        
        return {
            'colisiones': self.colisiones,
            'buckets_ocupados': buckets_ocupados,
            'max_bucket_size': max_bucket_size,
            'promedio_bucket': promedio_bucket
        }


def leer_datos(archivo):
    """Lee los datos del archivo de entrada."""
    with open(archivo, 'r') as f:
        n = int(f.readline().strip())
        pacientes = []
        for _ in range(n):
            registro = list(map(int, f.readline().strip().split()))
            pacientes.append(registro)
    return pacientes


def buscar_duplicados_hash(pacientes, hash_function='polynomial'):
    """
    Busca pacientes con registros idénticos usando una tabla hash.
    Retorna el número de pacientes idénticos encontrados.
    """
    tabla_size = max(len(pacientes) * 2, 10007)
    tabla_size = siguiente_primo(tabla_size)
    
    tabla = TablaHash(tabla_size, hash_function)
    
    for i, registro in enumerate(pacientes):
        tabla.insertar(registro, i)
    
    return tabla.buscar_duplicados(), tabla.obtener_estadisticas()


def siguiente_primo(n):
    """Encuentra el siguiente número primo mayor o igual a n."""
    def es_primo(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True
    
    while not es_primo(n):
        n += 1
    return n


def main():
    if len(sys.argv) < 2:
        print("Uso: python hash_version.py <archivo_entrada> [hash_function]")
        print("hash_function puede ser: polynomial (default), multiplicative, sha256")
        sys.exit(1)
    
    archivo = sys.argv[1]
    hash_function = sys.argv[2] if len(sys.argv) > 2 else 'polynomial'
    
    start_time = time.perf_counter()
    
    pacientes = leer_datos(archivo)
    num_duplicados, estadisticas = buscar_duplicados_hash(pacientes, hash_function)
    
    end_time = time.perf_counter()
    tiempo_ejecucion = end_time - start_time
    
    if num_duplicados == 0:
        print("no hay dos pacientes con registros idénticos")
    else:
        print(f"se encontraron {num_duplicados} pacientes idénticos")
    
    print(f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos", file=sys.stderr)
    print(f"Función hash: {hash_function}", file=sys.stderr)
    print(f"Estadísticas: {estadisticas}", file=sys.stderr)


if __name__ == "__main__":
    main()