# graficos.py
"""
Módulo para la generación de gráficos de funciones matemáticas.
Utiliza Matplotlib para graficar funciones SymPy, incluyendo dominio, recorrido,
intersecciones y puntos evaluados.
"""

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from analizador import AnalizadorMatematico


class GeneradorGraficos:
    """Clase para generar gráficos de funciones con Matplotlib."""
    
    def __init__(self):
        self.x = sp.symbols('x')
        self.analizador = AnalizadorMatematico()
    
    def generar_grafico(self, funcion, valor_x=None, valor_y=None, expresion_original=""):
        """
        Genera el gráfico de una función SymPy, incluyendo dominio, recorrido,
        intersecciones y puntos evaluados.
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        try:
            # Convertir la función SymPy a una función numérica
            f_lambd = sp.lambdify(self.x, funcion, modules=['numpy'])
            
            # Obtener dominio, recorrido e intersecciones
            dominio_resumen, _, restricciones_dominio = self.analizador.calcular_dominio(funcion)
            recorrido_resumen, _ = self.analizador.calcular_recorrido(funcion)
            inter_resumen, _ = self.analizador.calcular_intersecciones(funcion)
            
            # Determinar puntos excluidos del dominio
            excluidos = []
            for restr in restricciones_dominio:
                if restr.rel_op == '!=':
                    try:
                        punto = float(restr.rhs)
                        if -10 <= punto <= 10:  # Solo dentro del rango visible
                            excluidos.append(punto)
                    except:
                        pass
            
            # Definir el rango del dominio, evitando discontinuidades
            x = []
            if not excluidos:
                x = np.linspace(-10, 10, 1000)
            else:
                puntos = sorted([-10] + excluidos + [10])
                for i in range(len(puntos)-1):
                    start = puntos[i]
                    end = puntos[i+1]
                    if end - start > 0.1:  # Evitar intervalos demasiado pequeños
                        x_mid = np.linspace(start, end, int(1000 * (end - start) / 20))
                        x = np.concatenate([x, x_mid[:-1]]) if len(x) > 0 else x_mid[:-1]
            
            # Calcular valores de y
            y = f_lambd(x)
            y = np.where(np.abs(y) > 1e6, np.nan, y)
            
            # Ajustar límites de y dinámicamente
            y_finite = y[np.isfinite(y)]
            if len(y_finite) > 0:
                y_min, y_max = np.min(y_finite), np.max(y_finite)
                y_range = y_max - y_min
                y_min -= 0.1 * y_range
                y_max += 0.1 * y_range
                ax.set_ylim(max(-10, y_min), min(10, y_max))
            else:
                ax.set_ylim(-10, 10)
            
            # Graficar la función
            ax.plot(x, y, label=f"f(x) = {expresion_original}", color='blue')
            
            # Graficar intersecciones
            try:
                # Intersección con el eje Y
                if "No definida" not in inter_resumen:
                    y_inter = eval(inter_resumen.split(":")[1].split("\n")[0].strip()[1:-1].split(",")[1])
                    y_inter_rounded = round(float(sp.N(y_inter, 4)), 4)
                    ax.plot(0, y_inter, 'go', label=f"Intersección Y (0, {y_inter_rounded})")
                
                # Intersecciones con el eje X
                x_inters = inter_resumen.split("Intersecciones con el eje X:")[1].strip()
                if "No hay" not in x_inters:
                    for inter in x_inters.split(", "):
                        x_val = eval(inter[1:-1].split(",")[0])
                        x_val_rounded = round(float(sp.N(x_val, 4)), 4)
                        ax.plot(x_val, 0, 'go', label=f"Intersección X ({x_val_rounded}, 0)")
            except:
                pass
            
            # Graficar el punto evaluado
            if valor_x is not None and valor_y is not None:
                valor_x_rounded = round(float(sp.N(valor_x, 4)), 4)
                valor_y_rounded = round(float(sp.N(valor_y, 4)), 4)
                ax.plot(valor_x, valor_y, 'ro', label=f"Punto ({valor_x_rounded}, {valor_y_rounded})")
            
            # Mostrar dominio y recorrido como texto en el gráfico
            ax.text(0.02, 0.98, f"Dominio: {dominio_resumen}", 
                    transform=ax.transAxes, fontsize=10, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            ax.text(0.02, 0.92, f"Recorrido: {recorrido_resumen}", 
                    transform=ax.transAxes, fontsize=10, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            # Configurar el gráfico
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.set_title(f"Gráfico de f(x) = {expresion_original}")
            ax.grid(True)
            ax.legend(loc='best')
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)
            
            # Ajustar límites de x
            ax.set_xlim(-10, 10)
            
            return fig
        except Exception as e:
            print(f"Error al generar el gráfico: {e}")
            ax.text(0.5, 0.5, f"Error al generar gráfico:\n{str(e)}",
                    ha='center', va='center', transform=ax.transAxes)
            return fig
