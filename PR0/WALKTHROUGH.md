# Walkthrough Técnico - Sistema de Detección de Registros Médicos Duplicados

## Autores

**Estudiante:** David Fernando Avila Díaz  
**Clave Única:** 197851

**Estudiante:** José Gerardo Malfavaun Gorostizaga  
**Clave Única:** 213398

Instituto Tecnológico Autónomo de México (ITAM)  
Estructuras de Datos y Algoritmos

## Índice
1. [Arquitectura General](#arquitectura-general)
2. [Implementación con Arreglo Lineal](#implementación-con-arreglo-lineal)
3. [Implementación con Tabla Hash](#implementación-con-tabla-hash)
4. [Funciones Hash Detalladas](#funciones-hash-detalladas)
5. [Sistema de Benchmark](#sistema-de-benchmark)
6. [Optimizaciones y Decisiones de Diseño](#optimizaciones-y-decisiones-de-diseño)
7. [Casos Edge y Manejo de Errores](#casos-edge-y-manejo-de-errores)
8. [Análisis de Complejidad Detallado](#análisis-de-complejidad-detallado)

---

## Arquitectura General

### Estructura de Datos del Problema
Cada paciente tiene un registro con exactamente 10 estudios de laboratorio:
```python
registro = [estudio1, estudio2, ..., estudio10]  # Cada valor: 0 ≤ x ≤ 10,000,000
```

### Definición de "Pacientes Idénticos"
Dos pacientes son idénticos si sus 10 valores coinciden exactamente en el mismo orden. Por ejemplo:
- `[1,2,3,4,5,6,7,8,9,10]` == `[1,2,3,4,5,6,7,8,9,10]` ✓
- `[1,2,3,4,5,6,7,8,9,10]` != `[10,9,8,7,6,5,4,3,2,1]` ✗

---

## Implementación con Arreglo Lineal

### Algoritmo Principal (`array_version.py`)

```python
def buscar_duplicados_array(pacientes):
    registros_vistos = []      # Lista de registros ya procesados
    duplicados = set()         # Registros que aparecen más de una vez
    indices_duplicados = set() # Índices de TODOS los pacientes duplicados
```

### Flujo de Ejecución Paso a Paso

1. **Iteración sobre cada paciente**:
   ```python
   for i, registro in enumerate(pacientes):
   ```

2. **Búsqueda en registros previos**:
   ```python
   for j, registro_visto in enumerate(registros_vistos):
       if registro == registro_visto:  # Comparación O(10) = O(1)
   ```
   
   **Nota clave**: La comparación de listas en Python compara elemento por elemento hasta encontrar una diferencia.

3. **Manejo de duplicados encontrados**:
   ```python
   if registro == registro_visto:
       duplicados.add(tuple(registro))  # Convertir a tupla (hasheable)
       indices_duplicados.add(i)        # Paciente actual
       indices_duplicados.add(j)        # Paciente previo idéntico
       break                            # No seguir buscando
   ```

4. **Registro del paciente actual**:
   ```python
   registros_vistos.append(registro)
   ```

### Ejemplo de Traza

Entrada:
```
3
100 200 300 400 500 600 700 800 900 1000  # Paciente 0
101 201 301 401 501 601 701 801 901 1001  # Paciente 1  
100 200 300 400 500 600 700 800 900 1000  # Paciente 2 (duplicado de 0)
```

Ejecución:
```
i=0: registros_vistos=[], no hay duplicado, agregar P0
i=1: registros_vistos=[P0], P1≠P0, agregar P1
i=2: registros_vistos=[P0,P1], P2==P0, marcar índices 0 y 2 como duplicados
Resultado: 2 pacientes idénticos (índices 0 y 2)
```

### Complejidad Temporal
- **Peor caso**: O(n²) - Todos los registros son únicos
- **Mejor caso**: O(n) - Todos los registros son idénticos
- **Caso promedio**: O(n²) - Distribución aleatoria

---

## Implementación con Tabla Hash

### Estructura de la Clase `TablaHash`

```python
class TablaHash:
    def __init__(self, size=10007, hash_function='polynomial'):
        self.size = size                    # Tamaño de la tabla (primo)
        self.tabla = [[] for _ in range(size)]  # Lista de listas (chaining)
        self.hash_function = hash_function
        self.colisiones = 0
```

### Manejo de Colisiones: Separate Chaining

Cada posición de la tabla es una lista (bucket) que puede contener múltiples registros:
```python
tabla[hash_value] = [
    (registro1, [índice1, índice2]),  # Registro con sus índices
    (registro2, [índice3]),
    ...
]
```

### Proceso de Inserción

```python
def insertar(self, registro, indice_paciente):
    hash_value = self.hash(registro)  # Calcular posición
    bucket = self.tabla[hash_value]   # Obtener bucket
    
    # Buscar si el registro ya existe en el bucket
    for reg, indices in bucket:
        if reg == registro:
            indices.append(indice_paciente)  # Agregar índice al existente
            return True  # Era duplicado
    
    # No existía, agregar nuevo
    bucket.append((registro, [indice_paciente]))
    return False
```

### Ejemplo de Estado de la Tabla

Después de insertar 3 pacientes (con hash_value simplificado):
```python
tabla = [
    [],                                    # índice 0: vacío
    [(registro_A, [0, 2])],               # índice 1: pacientes 0 y 2 idénticos
    [],                                    # índice 2: vacío
    [(registro_B, [1])],                  # índice 3: paciente 1 único
    ...
]
```

---

## Funciones Hash Detalladas

### 1. Hash Polinomial (Rolling Hash)

```python
def _hash_polynomial(self, registro):
    p = 31          # Primo pequeño (buena distribución)
    m = self.size   # Módulo (tamaño de tabla)
    hash_value = 0
    p_pow = 1       # p^i
    
    for valor in registro:
        hash_value = (hash_value + (valor + 1) * p_pow) % m
        p_pow = (p_pow * p) % m
```

**Matemáticamente**:
```
h(x) = (Σ(xi + 1) * p^i) mod m
```

**¿Por qué funciona bien?**
- El `+1` evita que valores 0 no contribuyan al hash
- La base prima 31 minimiza patrones repetitivos
- El módulo con primo grande distribuye uniformemente

**Ejemplo de cálculo**:
```python
registro = [100, 200, 300]
p = 31, m = 10007

hash = ((100+1)*1 + (200+1)*31 + (300+1)*961) % 10007
     = (101 + 6231 + 289261) % 10007
     = 295593 % 10007
     = 5510
```

### 2. Hash Multiplicativo (Método de Knuth)

```python
def _hash_multiplicative(self, registro):
    A = 0.6180339887  # (√5 - 1)/2 - Proporción áurea
    hash_sum = sum(registro)
    return int(self.size * ((hash_sum * A) % 1))
```

**Matemáticamente**:
```
h(x) = ⌊m * fractional_part(sum(x) * A)⌋
```

**¿Por qué la proporción áurea?**
- Distribuye los valores de manera óptima en [0,1)
- Minimiza clustering para valores consecutivos
- Probado matemáticamente por Knuth

**Ejemplo**:
```python
registro = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
sum = 5500
hash = floor(10007 * ((5500 * 0.6180339887) % 1))
     = floor(10007 * (3399.1869385 % 1))
     = floor(10007 * 0.1869385)
     = 1870
```

### 3. Hash SHA256

```python
def _hash_sha256(self, registro):
    str_registro = '-'.join(map(str, registro))  # "100-200-300-..."
    hash_obj = hashlib.sha256(str_registro.encode())
    hash_hex = hash_obj.hexdigest()
    return int(hash_hex, 16) % self.size
```

**Ventajas**:
- Distribución perfectamente uniforme
- Imposible predecir colisiones
- Determinista (mismo input = mismo output)

**Desventajas**:
- Más costoso computacionalmente (~10x más lento)
- Overkill para este problema

---

## Sistema de Benchmark

### Generación de Datos Controlados

```python
def generar_datos(n, proporcion_duplicados=0.1):
    num_duplicados = int(n * proporcion_duplicados)
    num_unicos = n - num_duplicados
    
    # Fase 1: Crear registros únicos
    registros_unicos = [generar_registro_aleatorio() for _ in range(num_unicos)]
    
    # Fase 2: Duplicar algunos registros
    for _ in range(num_duplicados):
        registro_a_duplicar = random.choice(registros_unicos)
        pacientes.append(registro_a_duplicar[:])  # Copia
    
    random.shuffle(pacientes)  # Mezclar para simular datos reales
```

### Medición Precisa de Tiempos

```python
start_time = time.perf_counter()  # Alta resolución (nanosegundos)
# ... ejecutar algoritmo ...
end_time = time.perf_counter()
tiempo_ejecucion = end_time - start_time
```

**¿Por qué `perf_counter`?**
- Monotónico (no afectado por ajustes del reloj)
- Mayor resolución que `time.time()`
- Ideal para benchmarks

### Análisis Estadístico

El benchmark ejecuta cada prueba 3 veces y promedia:
```python
tiempos = []
for _ in range(num_repeticiones):
    t = ejecutar_programa(programa, archivo)
    tiempos.append(t)
tiempo_promedio = np.mean(tiempos)
desviacion = np.std(tiempos)  # Para verificar consistencia
```

---

## Optimizaciones y Decisiones de Diseño

### 1. Tamaño de Tabla Hash como Primo

```python
def siguiente_primo(n):
    def es_primo(num):
        if num < 2: return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0: return False
        return True
    
    while not es_primo(n):
        n += 1
    return n

tabla_size = max(len(pacientes) * 2, 10007)  # Factor de carga ~0.5
tabla_size = siguiente_primo(tabla_size)
```

**Razón**: Los números primos minimizan patrones en la función módulo, distribuyendo mejor los valores.

### 2. Factor de Carga Óptimo

```python
factor_carga = num_elementos / tamaño_tabla
# Objetivo: mantener factor_carga ≈ 0.5
```

**Trade-off**:
- Factor bajo (< 0.5): Menos colisiones, más memoria desperdiciada
- Factor alto (> 0.75): Más colisiones, degradación a O(n)

### 3. Uso de Sets para Índices

```python
indices_duplicados = set()  # En lugar de lista
```

**Ventajas**:
- Inserción O(1) vs O(n) de lista
- Automáticamente evita duplicados
- Operación `len()` sigue siendo O(1)

### 4. Early Exit en Búsqueda Lineal

```python
if registro == registro_visto:
    # ... procesar duplicado ...
    break  # No seguir buscando
```

Ahorra comparaciones innecesarias una vez encontrado el duplicado.

---

## Casos Edge y Manejo de Errores

### 1. Archivo Vacío o Malformado

```python
try:
    n = int(f.readline().strip())
    if n < 1 or n > 100000:
        raise ValueError("N fuera de rango")
except ValueError as e:
    print(f"Error en formato de archivo: {e}")
    sys.exit(1)
```

### 2. Registros con Menos de 10 Valores

```python
registro = list(map(int, line.split()))
if len(registro) != 10:
    print(f"Error: Registro con {len(registro)} valores, esperados 10")
    continue  # O manejar según requerimientos
```

### 3. Valores Fuera de Rango

```python
for valor in registro:
    if valor < 0 or valor > 10_000_000:
        raise ValueError(f"Valor {valor} fuera de rango permitido")
```

### 4. Memoria Insuficiente

Para datasets muy grandes (n > 1,000,000):
```python
import resource
# Limitar memoria para evitar swap excesivo
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, -1))  # 2GB máximo
```

---

## Análisis de Complejidad Detallado

### Arreglo Lineal

**Tiempo**:
```
T(n) = Σ(i=1 to n) i = n(n+1)/2 = O(n²)
```

**Espacio**:
```
S(n) = n * 10 * sizeof(int) + overhead = O(n)
```

### Tabla Hash

**Tiempo (promedio)**:
```
T(n) = n * O(1) = O(n)
```

**Tiempo (peor caso - todas las colisiones)**:
```
T(n) = n * O(n) = O(n²)
```

**Probabilidad de peor caso**:
```
P(todas_colisiones) = (1/m)^n  donde m = tamaño_tabla
Para m = 10007, n = 1000: P ≈ 10^-4000 (prácticamente imposible)
```

### Comparación Práctica

| n | Array (seg) | Hash (seg) | Speedup |
|---|------------|------------|---------|
| 100 | 0.0002 | 0.0016 | 0.125x |
| 1,000 | 0.010 | 0.003 | 3.3x |
| 10,000 | 1.028 | 0.024 | 42.8x |
| 100,000 | ~100 | ~0.25 | ~400x |

### Punto de Inflexión

El hash se vuelve más eficiente a partir de:
```
n ≈ 250 pacientes (considerando overhead de inicialización)
```

---

## Preguntas Frecuentes de Entrevista

### P1: ¿Por qué no usar un diccionario de Python directamente?

**R**: El ejercicio requiere implementar la tabla hash para entender:
- Manejo de colisiones
- Funciones hash
- Trade-offs de diseño

Python dict() usa una implementación optimizada en C que ocultaría estos detalles.

### P2: ¿Cómo mejorarías el rendimiento para 100M de registros?

**R**: Varias estrategias:
1. **Bloom Filter** preliminar para descartar no-duplicados
2. **Hash distribuido** (sharding por primeros dígitos)
3. **Procesamiento paralelo** con multiprocessing
4. **Base de datos** con índices (PostgreSQL, Redis)
5. **Streaming** para no cargar todo en memoria

### P3: ¿Qué pasa si los registros pueden tener valores NULL?

**R**: Modificar la representación:
```python
# Opción 1: Valor centinela
NULL = -1  # Fuera del rango válido

# Opción 2: Tuplas con flag
registro = [(valor, es_null) for valor in datos]

# Opción 3: Hash especial para NULL
if valor is None:
    hash_component = HASH_NULL_CONSTANT
```

### P4: ¿Cómo detectarías registros "casi idénticos"?

**R**: Usar LSH (Locality-Sensitive Hashing):
```python
def lsh_hash(registro, tolerancia=0.05):
    # Dividir valores en buckets
    buckets = [int(v / (max_val * tolerancia)) for v in registro]
    return hash(tuple(buckets))
```

### P5: ¿Por qué la función hash SHA256 es más lenta pero tiene mejor distribución?

**R**: SHA256 hace múltiples rondas de operaciones bit a bit para garantizar:
- **Avalanche effect**: Un bit de cambio altera ~50% del hash
- **Distribución uniforme**: Cada bit de salida tiene P(0)=P(1)=0.5
- **No reversibilidad**: Imposible deducir input del hash

El costo es ~64 rondas de operaciones vs 1 operación aritmética simple.

---

## Conclusión

Este sistema demuestra claramente por qué las tablas hash son fundamentales en ciencias de la computación. La diferencia entre O(n²) y O(n) se vuelve crítica con datasets reales, y entender las implementaciones permite tomar decisiones informadas sobre:

- Cuándo vale la pena el overhead de una estructura compleja
- Cómo elegir funciones hash según los datos
- Trade-offs entre memoria y tiempo
- Importancia de benchmarks con datos realistas

El código está diseñado para ser extensible, permitiendo agregar nuevas funciones hash o métodos de resolución de colisiones sin modificar la estructura base.