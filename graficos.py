# graficos.py
"""
Módulo para generar gráficos de funciones matemáticas utilizando Matplotlib.
Maneja funciones simbólicas, evalúa puntos, y muestra dominio, recorrido, intersecciones
y puntos evaluados en el gráfico. Usa notación científica para valores grandes/pequeños.
"""

import matplotlib.pyplot as plt
from sympy import lambdify
import math


class GeneradorGraficos:
    """Clase para generar gráficos de funciones matemáticas con Matplotlib."""
    
    def _format_number(self, value):
        """Formatea un número con 2 decimales o en notación científica si es muy grande o pequeño."""
        try:
            value_float = float(value)
            if abs(value_float) > 10000 or (abs(value_float) < 0.0001 and value_float != 0):
                return f"{value_float:.1e}"
            return f"{value_float:.2f}"
        except (ValueError, TypeError):
            return str(value)
    
    def generar_grafico(self, funcion, valor_x=None, valor_y=None, expresion_original="f(x)"):
        """
        Genera un gráfico de la función dada, marcando intersecciones, puntos evaluados,
        y mostrando dominio y recorrido en notación científica cuando corresponda.
        
        Args:
            funcion: Función simbólica (SymPy) a graficar.
            valor_x: Valor de x a evaluar (opcional).
            valor_y: Valor de f(x) correspondiente (opcional).
            expresion_original: Expresión de la función como string para la leyenda.
        
        Returns:
            fig: Objeto de figura de Matplotlib.
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Generar puntos para el eje x (-10 a 10, 1000 puntos)
        x_min, x_max, num_puntos = -10, 10, 1000
        x = [x_min + i * (x_max - x_min) / (num_puntos - 1) for i in range(num_puntos)]
        
        # Convertir la función simbólica a una función numérica
        f = lambdify('x', funcion, 'math')
        
        # Evaluar la función en los puntos x, manejando valores no finitos
        y = []
        for x_val in x:
            try:
                y_val = f(x_val)
                if math.isinf(y_val) or math.isnan(y_val):
                    y.append(None)  # Usar None para discontinuidades
                else:
                    y.append(float(y_val))
            except (ValueError, ZeroDivisionError, OverflowError):
                y.append(None)  # Discontinuidades o errores
        
        # Graficar la función
        ax.plot(x, y, label=f"f(x) = {expresion_original}", color='blue')
        
        # Marcar el punto evaluado (si se proporciona)
        if valor_x is not None and valor_y is not None:
            try:
                x_float = float(valor_x)
                y_float = float(valor_y)
                ax.plot(x_float, y_float, 'ro', markersize=8, label=f"Punto ({self._format_number(x_float)}, {self._format_number(y_float)})")
            except (ValueError, TypeError):
                pass
        
        # Obtener intersecciones (puntos en el eje x y y)
        from analizador import AnalizadorMatematico
        analizador = AnalizadorMatematico()
        inter_resumen, _ = analizador.calcular_intersecciones(funcion)
        
        inter_x, inter_y = [], []
        # Parseo robusto de inter_resumen
        for inter in inter_resumen.split('\n'):
            if not inter.strip():
                continue
            try:
                if "Intersección en X" in inter:
                    x_val_str = inter.split('(')[1].split(',')[0].strip()
                    x_val = float(x_val_str)
                    inter_x.append(x_val)
                elif "Intersección en Y" in inter:
                    y_val_str = inter.split(',')[1].split(')')[0].strip()
                    y_val = float(y_val_str)
                    inter_y.append((0, y_val))
            except (ValueError, IndexError) as e:
                print(f"Error al parsear intersección: {inter}, {str(e)}")
                continue
        
        # Graficar intersecciones con formato adecuado
        for x_val in inter_x:
            ax.plot(x_val, 0, 'go', markersize=8, label=f"Intersección X ({self._format_number(x_val)}, 0)")
        for _, y_val in inter_y:
            ax.plot(0, y_val, 'go', markersize=8, label=f"Intersección Y (0, {self._format_number(y_val)})")
        
        # Configurar el dominio y recorrido como texto
        dominio_resumen, _, _ = analizador.calcular_dominio(funcion)
        recorrido_resumen, _ = analizador.calcular_recorrido(funcion)
        
        ax.text(0.02, 0.98, f"Dominio: {dominio_resumen}", transform=ax.transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        ax.text(0.02, 0.90, f"Recorrido: {recorrido_resumen}", transform=ax.transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Configurar el gráfico
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.set_title(f"Gráfico de f(x) = {expresion_original}")
        ax.grid(True)
        
        # Manejar leyenda para evitar duplicados
        handles, labels = ax.get_legend_handles_labels()
        unique_labels = dict(zip(labels, handles))
        ax.legend(unique_labels.values(), unique_labels.keys())
        
        # Ajustar límites
        y_valid = [v for v in y if v is not None and not math.isinf(v)]
        if y_valid:
            ax.set_ylim(min(y_valid) - 1, max(y_valid) + 1)
        
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        
        return fig
