# Simulador de Máquina de Turing

Este proyecto implementa un simulador completo de Máquinas de Turing de una cinta, desarrollado en Python.

---

## Convenciones

### 1. Representación de enteros no negativos en la cinta

Se utiliza **notación unaria**: el entero no negativo `n` se representa mediante `n` símbolos `'1'` consecutivos en la cinta.

| Valor de n | Contenido de la cinta |
|:-----------:|:---------------------:|
| 0           | _(cinta vacía)_       |
| 1           | `1`                   |
| 2           | `11`                  |
| 3           | `111`                 |
| n           | `1` × n               |

El símbolo **blank** (`_`) representa una celda vacía y es el símbolo por defecto fuera de la entrada.

### 2. Interpretación de la respuesta en la cinta

Al finalizar la simulación de F(n), la cinta contiene la siguiente estructura:

```
[basura de trabajo] # [resultado en unario]
```

- Los símbolos a la **izquierda** del separador `#` son marcas de trabajo (`X`, `Y`) usadas durante el cómputo y no forman parte del resultado.
- Los símbolos `'1'` a la **derecha** del separador `#` representan el valor de F(n) en notación unaria.
- La cantidad de `'1'`s después del `#` es el resultado: **F(n)**.

**Ejemplos:**

| Entrada | F(n) | Cinta final      | Resultado |
|:-------:|:----:|:----------------:|:---------:|
| _(vacía)_ | F(0) | `_`            | 0         |
| `1`     | F(1) | `1_`             | 1         |
| `11`    | F(2) | `_1Y#1`          | 1 (`'1'` después del `#`) |
| `111`   | F(3) | `_1YY#11`        | 2 (`'11'` después del `#`) |
| `1111`  | F(4) | `_1YYY#111`      | 3         |

> **Nota:** Para los casos base F(0) y F(1), no se genera separador `#` porque la respuesta se deja directamente como la cantidad de `'1'`s en la cinta.

### 3. Símbolos auxiliares de la cinta

| Símbolo | Significado durante el cómputo |
|:-------:|:-------------------------------|
| `1`     | Unidad en notación unaria       |
| `X`     | Marca de contador (celda procesada del input) |
| `Y`     | Marca de iteración completada   |
| `#`     | Separador entre área de trabajo y resultado |
| `_`     | Blank (celda vacía)             |

---

## Características

- Simulación de Máquinas de Turing deterministas de **una cinta**
- Estado extendido con **memoria caché** — transición: `δ(estado, caché, símbolo)`
- Soporte para desplazamientos **R** (derecha), **L** (izquierda), **S** (quedarse)
- Configuración cargada desde archivos **YAML**
- Visualización de **descripciones instantáneas** con posición del cabezal en cada paso
- Detección automática de aceptación/rechazo
- Protección contra bucles infinitos (límite configurable de pasos)
- **Modo interactivo**: ingresa cadenas por teclado en tiempo de ejecución
- Análisis empírico con diagrama de dispersión y regresión polinomial

---

## Estructura del Proyecto

```
.
├── main.py                          # Programa principal (simulación + modo interactivo)
├── turing_machine.py                # Implementación de la clase TuringMachine
├── parser_yaml.py                   # Parser de archivos YAML
├── analisis.py                      # Análisis empírico y gráfica de regresión
├── diagrama.py                      # Generador del diagrama .dot desde el YAML
├── crear_yamls.py                   # Generador de ejemplos YAML
├── examples/
│   ├── fibonacci.yaml               # MT que calcula la sucesión de Fibonacci
│   ├── reconocedora.yaml            # MT reconocedora para {aⁿbⁿ}
│   └── alteradora.yaml              # MT alteradora (duplica cadenas)
├── diagramas/
│   ├── fibonacci.dot                # Diagrama de la MT de Fibonacci
│   ├── reconocedora.dot
│   └── alteradora.dot
└── resultados/
    ├── fibonacci_salida.txt         # Configuraciones paso a paso de Fibonacci
    ├── fibonacci_datos_analisis.csv # Datos de tiempos para regresión
    ├── grafica_fibonacci_final.png  # Gráfica de dispersión + regresión
    ├── reconocedora_salida.txt
    └── alteradora_salida.txt
```

---

## Instalación

1. **Clonar el repositorio** o descargar los archivos.

2. **Instalar dependencias**:
   ```bash
   pip install pyyaml pandas numpy matplotlib
   ```

---

## Uso

### Ejecutar la simulación de Fibonacci

```bash
python main.py examples/fibonacci.yaml
```

El programa:
1. Simula automáticamente todas las cadenas definidas en `simulation_strings` del YAML.
2. Entra al **modo interactivo** donde puedes ingresar cadenas adicionales por teclado.
3. Guarda todos los resultados en `resultados/`.

**Ejemplo de sesión interactiva:**
```
======================================================================
MODO INTERACTIVO
Alfabeto de entrada permitido: ['1']
Escribe una cadena y presiona Enter para simularla.
Escribe 'salir' o presiona Enter vacío para terminar.
======================================================================

Cadena de entrada: 11111
Paso 000: Cabeza:   0 | Estado: q_init | Cache: B | Cinta: ...
...
Cadena de entrada: salir
```

### Generar la gráfica de análisis empírico

Después de ejecutar la simulación de Fibonacci:
```bash
python analisis.py
```

Produce `resultados/grafica_fibonacci_final.png` con el diagrama de dispersión y la curva de regresión polinomial.

---

### Formato del archivo YAML

```yaml
states:
  - 'q0'
  - 'q1'
  - 'q_final'

initial_state: 'q0'
final_states:
  - 'q_final'

input_alphabet:
  - 'a'
  - 'b'

tape_alphabet:
  - 'a'
  - 'b'
  - 'X'
  - !!null 'null'     # símbolo blank

blank: !!null 'null'

delta:
  - params:
      initial_state: 'q0'
      mem_cache_value: !!null 'null'   # caché vacío
      tape_input: 'a'
    output:
      final_state: 'q1'
      mem_cache_value: 'a'             # guardar 'a' en caché
      tape_output: 'X'
      tape_displacement: 'R'           # R, L o S

simulation_strings:
  - 'aabb'
  - 'ab'
```

---

## Máquina de Turing: Sucesión de Fibonacci

### Estados

| Estado    | Rol |
|-----------|-----|
| `q_init`  | Estado inicial; detecta el caso base F(0) |
| `q_base_1`| Maneja F(1) y prepara n > 1 |
| `q_setup` | Convierte el input en marcas `X` (contador de iteraciones) |
| `q_loop`  | Bucle principal; decide si quedan iteraciones |
| `q_copy`  | Viaja al final de la cinta a agregar un `'1'` |
| `q_back`  | Regresa al inicio para la siguiente iteración |
| `q_final` | Estado de aceptación |

### Descripción del algoritmo

- **F(0):** cinta vacía → acepta sin modificar (cinta final: `_`).
- **F(1):** una sola `'1'` → acepta dejando `1_` en la cinta.
- **F(n), n ≥ 2:**
  1. `q_setup` transforma cada `'1'` del input en `'X'`, dejando `n-1` marcas X.
  2. El bucle `q_loop → q_copy → q_back` itera `n-1` veces.
  3. En cada iteración, `q_copy` escribe un `'1'` al final (acumulando el resultado tras el `#`).
  4. Cuando no quedan `'X'` sin procesar, `q_loop` transita a `q_final`.

La complejidad resulta **O(n²)** porque por cada una de las `n-1` iteraciones el cabezal recorre la cinta de extremo a extremo (longitud proporcional a n).

---

## Descripción Instantánea

Cada paso de la simulación muestra:

```
Paso 003: Cabeza:   2 | Estado: q_setup | Cache: B | Cinta: ['1', 'X'][q_setup, B][None]
```

| Campo    | Descripción |
|----------|-------------|
| `Cabeza` | Posición numérica del cabezal (0-indexado) |
| `Estado` | Estado actual de la máquina |
| `Cache`  | Valor en memoria caché (`B` = blank) |
| `Cinta`  | Contenido completo; el símbolo bajo el cabezal es el primero del bloque derecho |

---

## Análisis Empírico

El script `analisis.py` lee `resultados/fibonacci_datos_analisis.csv` y:

1. Grafica los puntos experimentales (n símbolos de entrada vs. pasos ejecutados).
2. Ajusta una **regresión polinomial de grado 2**.
3. Imprime la ecuación ajustada y la conclusión asintótica.

**Salida esperada:**
```
Ecuación del tiempo: T(n) = 4.00n² + 2.00n + 1.00
Conclusión: La complejidad asintótica es O(n²)
```

---

## Componentes

### `turing_machine.py`
Clase `TuringMachine` con estado dual (estado + caché).  
Función de transición: `δ(estado, caché, símbolo) → (nuevo_estado, nuevo_caché, escribir, dirección)`.

### `parser_yaml.py`
Convierte el archivo YAML al diccionario de transiciones y configuración que consume `TuringMachine`.

### `main.py`
Punto de entrada. Corre cadenas predefinidas del YAML y, a continuación, habilita ingreso interactivo por teclado. Todo se guarda en `resultados/`.

### `analisis.py`
Análisis empírico: gráfica de dispersión y regresión polinomial sobre los datos del CSV.

### `diagrama.py`
Genera el archivo `.dot` del diagrama de estados a partir del YAML.

---

## Arquitectura

```
┌─────────────────┐
│   main.py       │  ← Punto de entrada
└────────┬────────┘
         │
         ├─► parser_yaml.py      ← Carga configuración desde YAML
         │
         └─► turing_machine.py   ← Simula la máquina
                 │
                 ├─► load_tape()
                 ├─► step()
                 └─► get_configuration()

analisis.py  ← Lee el CSV y genera la gráfica de regresión
diagrama.py  ← Lee el YAML y genera el .dot
```

---

## Video de Demostración

https://github.com/user-attachments/assets/02395b92-c56d-4ef4-b60f-c568200c2238

https://youtu.be/bjJKKkm5I0A

