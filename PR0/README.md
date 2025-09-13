# Práctica 1: Tablas de Hash - Comparación de Estructuras de Datos

Autores
Estudiante: David Fernando Avila Díaz
Clave Única: 197851

Estudiante: José Gerardo Malfavaun Gorostizaga
Clave Única: 213398


## Descripción del Proyecto

Este proyecto implementa dos soluciones para detectar pacientes con registros médicos idénticos en un centro de salud:
1. **Versión con arreglo lineal**: Búsqueda secuencial O(n²)
2. **Versión con tabla hash**: Búsqueda optimizada O(n) en promedio

## Estructura de Archivos

```
PR0/
├── array_version.py       # Implementación con arreglo lineal
├── hash_version.py        # Implementación con tabla hash
├── generar_datos.py       # Generador de datos de prueba
├── benchmark.py           # Script de comparación y análisis
├── datos_ejemplo.txt      # Archivo de ejemplo con 10 pacientes
├── README.md             # Este archivo
├── comparacion_tiempos.png    # Gráfica comparativa (generada)
└── speedup_analysis.png      # Análisis de aceleración (generada)
```

## Requisitos

- Python 3.6+
- matplotlib (para generar gráficas)
- numpy (para análisis estadístico)

Instalar dependencias:
```bash
pip install matplotlib numpy
```

## Instrucciones de Compilación y Ejecución

### 1. Ejecutar versión con arreglo lineal

```bash
python3 array_version.py datos_ejemplo.txt
```

### 2. Ejecutar versión con tabla hash

```bash
# Con función hash polinomial (default)
python3 hash_version.py datos_ejemplo.txt

# Con función hash multiplicativa
python3 hash_version.py datos_ejemplo.txt multiplicative

# Con función hash SHA256
python3 hash_version.py datos_ejemplo.txt sha256
```

### 3. Generar datos de prueba

```bash
# Generar archivo con 1000 pacientes y 20% de duplicados
python3 generar_datos.py datos_1000.txt 1000 0.2
```

### 4. Ejecutar benchmark completo

```bash
python3 benchmark.py
```

Este comando:
- Genera datos de prueba de diferentes tamaños (100 a 20,000 pacientes)
- Ejecuta ambas versiones múltiples veces
- Genera gráficas comparativas
- Muestra tabla de resultados

## Formato de Entrada

El archivo de entrada debe tener el siguiente formato:
- Primera línea: número entero `n` (1 ≤ n ≤ 100,000)
- Siguientes `n` líneas: 10 enteros separados por espacios (0 ≤ valor ≤ 10,000,000)

Ejemplo:
```
3
100 200 300 400 500 600 700 800 900 1000
101 201 301 401 501 601 701 801 901 1001
100 200 300 400 500 600 700 800 900 1000
```

## Formato de Salida

- Si no hay duplicados: `"no hay dos pacientes con registros idénticos"`
- Si hay duplicados: `"se encontraron m pacientes idénticos"` donde m es el número de pacientes con registros duplicados

## Análisis de Complejidad

### Versión con Arreglo Lineal
- **Complejidad temporal**: O(n²)
  - Para cada paciente, comparamos con todos los anteriores
  - En el peor caso: n + (n-1) + ... + 1 = n(n+1)/2 comparaciones
- **Complejidad espacial**: O(n)
  - Almacenamos todos los registros en memoria

### Versión con Tabla Hash
- **Complejidad temporal**: 
  - Caso promedio: O(n)
  - Peor caso: O(n²) (todas las colisiones en el mismo bucket)
- **Complejidad espacial**: O(n)
  - Tabla hash de tamaño proporcional a n
  - Factor de carga óptimo ≈ 0.5

### Funciones Hash Implementadas

1. **Polinomial Hash**: 
   - Usa rolling hash con base prima 31
   - Buena distribución para datos numéricos estructurados
   - h(x) = (∑ xi * p^i) mod m

2. **Multiplicative Hash**:
   - Método de Knuth con constante φ (golden ratio)
   - h(x) = ⌊m * ((sum(x) * A) mod 1)⌋
   - Rápida pero puede tener más colisiones

3. **SHA256 Hash**:
   - Distribución uniforme garantizada
   - Mayor costo computacional
   - Ideal para minimizar colisiones

## Resultados Experimentales

Los benchmarks muestran que:

1. **Para datasets pequeños (< 1000 registros)**:
   - Diferencia mínima entre ambos métodos
   - El overhead de la tabla hash puede hacer que sea ligeramente más lenta

2. **Para datasets medianos (1000-10000 registros)**:
   - La tabla hash empieza a mostrar ventajas significativas
   - Speedup de 5x-20x dependiendo de la distribución de datos

3. **Para datasets grandes (> 10000 registros)**:
   - La tabla hash es claramente superior
   - Speedup puede superar 100x
   - La diferencia crece cuadráticamente con el tamaño

### Comparación de Funciones Hash

| Función | Velocidad | Colisiones | Uso Recomendado |
|---------|-----------|------------|-----------------|
| Polynomial | Alta | Bajas | General, datos estructurados |
| Multiplicative | Muy Alta | Medias | Datos uniformes |
| SHA256 | Baja | Mínimas | Cuando las colisiones son críticas |

## Conclusiones

1. **Eficiencia**: La tabla hash es significativamente más eficiente para conjuntos de datos medianos y grandes, con una mejora de rendimiento que crece cuadráticamente.

2. **Escalabilidad**: Mientras el arreglo lineal se vuelve impráctico para n > 10,000, la tabla hash mantiene tiempos de respuesta razonables incluso con 100,000 registros.

3. **Trade-offs**: 
   - El arreglo lineal es más simple y puede ser suficiente para datasets pequeños
   - La tabla hash requiere más memoria y tiene overhead de inicialización
   - La elección de función hash afecta significativamente el rendimiento

4. **Recomendaciones**:
   - Para n < 100: Cualquier método es aceptable
   - Para n < 1000: Considerar simplicidad vs rendimiento
   - Para n > 1000: Usar tabla hash es altamente recomendado
   - Para datos con patrones conocidos: Optimizar función hash específicamente

## Autores

**Estudiante:** David Fernando Avila Díaz  
**Clave Única:** 197851

**Estudiante:** José Gerardo Malfavaun Gorostizaga  
**Clave Única:** 213398

Desarrollado para el curso de Estructuras de Datos y Algoritmos  
Instituto Tecnológico Autónomo de México (ITAM)
