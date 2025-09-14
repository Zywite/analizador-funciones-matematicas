# Analizador de Funciones Matemáticas
integrantes: 
-Joaquin Carrasco
-Benjamin Cabrera
-Renato Caceres
-Nicolas Castillo
## Descripción

El **Analizador de Funciones Matemáticas** es una aplicación Python con interfaz gráfica que permite analizar funciones matemáticas ingresadas por el usuario. Proporciona un análisis detallado paso a paso (dominio, recorrido, intersecciones con los ejes, evaluación en un punto) y genera un gráfico interactivo que muestra la función, sus intersecciones, el punto evaluado, y el dominio/recorrido en notación matemática.

### Características

- **Interfaz gráfica**:
  - Entrada de funciones matemáticas (ej. `(x+1)/(x-2)`, `x**2 - 4`, `sin(x)`).
  - Entrada opcional de un valor de \( x \) (decimales, fracciones, o constantes como `pi`).
  - Botones para analizar, limpiar campos, y cargar ejemplos.
  - Ventana de ejemplos seleccionables con funciones variadas (racionales, polinómicas, trigonométricas, logarítmicas, exponenciales, etc.).
- **Análisis matemático**:
  - **Dominio**: Calcula el dominio (ej. \( \mathbb{R} \setminus \{2\} \)) con pasos detallados.
  - **Recorrido**: Determina el recorrido (ej. \( \mathbb{R} \setminus \{1\} \)) para funciones racionales y otras.
  - **Intersecciones**: Calcula intersecciones con los ejes \( X \) y \( Y \).
  - **Evaluación**: Evalúa la función en un punto dado, mostrando pasos y resultados con 4 decimales.
- **Gráfico**:
  - Visualiza la función con Matplotlib, respetando el dominio (excluye discontinuidades).
  - Muestra intersecciones con los ejes (puntos verdes) y el punto evaluado (punto rojo).
  - Incluye texto con dominio y recorrido en notación matemática (ej. \( \mathbb{R} \setminus \{2\} \)).
  - Títulos, etiquetas, grilla, y leyenda claros.
- **Manejo de errores**:
  - Valida funciones y valores de \( x \), mostrando advertencias si \( x \) está fuera del dominio.
  - Soporta fracciones, decimales, y constantes como `pi`.
- **Ejemplos interactivos**:
  - Ventana con ejemplos seleccionables que se pueden cargar en los campos de entrada o copiar al portapapeles.
  - Incluye funciones como racionales, polinómicas, trigonométricas, logarítmicas, exponenciales, y más.

## Requisitos

- Python 3.8 o superior
- Bibliotecas:
  - `sympy>=1.12`
  - `matplotlib>=3.7`
  - `numpy>=1.24`

## Instalación

1. Clona el repositorio:
   ```bash
   git clone git push https://github.com/Zywite/analizador-funciones-matematicas
   cd analizador-funciones-matematicas
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

## Uso

1. **Iniciar la aplicación**:
   - Ejecuta `python main.py` para abrir la interfaz gráfica.
   - Los campos de entrada se inicializan con un ejemplo: \( f(x) = \frac{x+1}{x-2} \), \( x = 1.5 \).

2. **Ingresar una función**:
   - Escribe una función en términos de \( x \) en el campo "Función f(x)" (ej. `(x+1)/(x-2)`, `x**2 - 4`, `sin(x)`).
   - Soporta operadores como `**` (potencia), `sqrt`, `log`, `sin`, `cos`, `tan`, `Abs`, `exp`, etc.

3. **Ingresar un valor de \( x \)**:
   - Opcionalmente, ingresa un valor de \( x \) (ej. `1.5`, `3/2`, `pi`).
   - Si \( x \) está fuera del dominio, se mostrará una advertencia.

4. **Analizar**:
   - Presiona "Analizar Función" para obtener:
     - Análisis paso a paso (dominio, recorrido, intersecciones, evaluación).
     - Gráfico con la función, intersecciones, punto evaluado, y texto con dominio/recorrido.

5. **Cargar ejemplos**:
   - Presiona "Ver Ejemplos" para abrir una ventana con funciones soportadas.
   - Selecciona un ejemplo con clic o flechas, luego:
     - Haz doble clic o presiona "Cargar Ejemplo" para llenar los campos y analizar automáticamente.
     - Presiona `Ctrl+C` para copiar el ejemplo al portapapeles y pegarlo manualmente.

6. **Limpiar**:
   - Presiona "Limpiar Campos" para borrar los campos, el análisis, y el gráfico.

## Estructura del Proyecto

- `main.py`: Interfaz gráfica con Tkinter, coordina entrada de usuario y salida.
- `analizador.py`: Lógica para el análisis matemático (dominio, recorrido, intersecciones, evaluación).
- `graficos.py`: Generación de gráficos con Matplotlib.
- `requirements.txt`: Dependencias del proyecto.

## Ejemplo

**Entrada**:
- Función: `(x+1)/(x-2)`
- Valor de \( x \): `1.5`

**Salida**:
- **Análisis**:
  - Dominio: \( \mathbb{R} \setminus \{2\} \)
  - Recorrido: \( \mathbb{R} \setminus \{1\} \)
  - Intersección Y: \( (0, -0.5) \)
  - Intersección X: \( (-1.0, 0) \)
  - Evaluación: \( f(1.5) = -5.0 \), par ordenado: \( (1.5, -5.0) \)
- **Gráfico**:
  - Curva de la función con discontinuidad en \( x = 2 \).
  - Puntos verdes en intersecciones \( (0, -0.5) \), \( (-1.0, 0) \).
  - Punto rojo en \( (1.5, -5.0) \).
  - Texto: "Dominio: \( \mathbb{R} \setminus \{2\} \)", "Recorrido: \( \mathbb{R} \setminus \{1\} \)".

## Contribuir

1. Haz un fork del repositorio.
2. Crea una rama para tu cambio: `git checkout -b mi-rama`.
3. Realiza tus cambios y haz commit: `git commit -m "Descripción del cambio"`.
4. Sube los cambios: `git push origin mi-rama`.
5. Crea un Pull Request en GitHub.

Por favor, sigue las convenciones de código (PEP 8) y documenta tus cambios.

## Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE.txt).

