# main.py
"""
Punto de entrada principal para el Analizador de Funciones Matemáticas.
Coordina la interfaz gráfica, el análisis matemático y la generación de gráficos.
Utiliza módulos 'analizador' y 'graficos' para mantener una arquitectura modular.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from analizador import AnalizadorMatematico
from graficos import GeneradorGraficos


class InterfazGrafica:
    """Clase principal para la interfaz gráfica del analizador de funciones."""
    
    def __init__(self):
        self.analizador = AnalizadorMatematico()
        self.graficador = GeneradorGraficos()
        self.funcion_actual = None
        self.expresion_original = ""
        
        self.ventana = tk.Tk()
        self.ventana.title("Analizador de Funciones Matemáticas")
        self.ventana.geometry("1200x800")
        self.ventana.configure(bg='#f0f0f0')
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz gráfica."""
        main_frame = ttk.Frame(self.ventana, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Analizador de Funciones Matemáticas", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de entrada
        entrada_frame = ttk.LabelFrame(main_frame, text="Entrada de Datos", padding="10")
        entrada_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        entrada_frame.columnconfigure(1, weight=1)
        
        ttk.Label(entrada_frame, text="Función f(x):").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.entry_funcion = ttk.Entry(entrada_frame, font=('Arial', 12), width=50)
        self.entry_funcion.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Label(entrada_frame, text="Valor de x (opcional):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.entry_x = ttk.Entry(entrada_frame, font=('Arial', 12), width=20)
        self.entry_x.grid(row=1, column=1, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        # Botones
        self.btn_analizar = ttk.Button(entrada_frame, text="Analizar Función", 
                                      command=self.analizar_funcion, style='Accent.TButton')
        self.btn_analizar.grid(row=0, column=2, rowspan=2, padx=(10, 5))
        
        self.btn_ejemplos = ttk.Button(entrada_frame, text="Ver Ejemplos", 
                                      command=self.mostrar_ejemplos)
        self.btn_ejemplos.grid(row=2, column=0, pady=(10, 0))
        
        self.btn_limpiar = ttk.Button(entrada_frame, text="Limpiar Campos", 
                                     command=self.limpiar_campos)
        self.btn_limpiar.grid(row=2, column=1, sticky=tk.W, pady=(10, 0))
        
        # Frame de resultados
        resultados_frame = ttk.Frame(main_frame)
        resultados_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.columnconfigure(1, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        
        analisis_frame = ttk.LabelFrame(resultados_frame, text="Análisis Matemático", padding="10")
        analisis_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        analisis_frame.rowconfigure(0, weight=1)
        analisis_frame.columnconfigure(0, weight=1)
        
        self.text_analisis = scrolledtext.ScrolledText(analisis_frame, height=25, width=60, 
                                                      font=('Courier', 10), wrap=tk.WORD)
        self.text_analisis.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        grafico_frame = ttk.LabelFrame(resultados_frame, text="Gráfico", padding="10")
        grafico_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        grafico_frame.rowconfigure(0, weight=1)
        grafico_frame.columnconfigure(0, weight=1)
        
        self.canvas_frame = ttk.Frame(grafico_frame)
        self.canvas_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)
        
        self.mostrar_instrucciones()
        
        self.entry_funcion.insert(0, "(x+1)/(x-2)")
        self.entry_x.insert(0, "1.5")
    
    def mostrar_instrucciones(self):
        """Muestra las instrucciones iniciales en el cuadro de texto."""
        instrucciones = """
ANALIZADOR DE FUNCIONES MATEMÁTICAS

1. Ingresa una función en términos de x (ejemplo: (x+1)/(x-2) o x**2 - 4).
2. Opcionalmente, ingresa un valor de x (fracción como '3/2', 'pi', o decimal '1.5').
3. Haz clic en "Analizar Función" para ver el análisis paso a paso.
4. Usa "Ver Ejemplos" para cargar ejemplos de funciones soportadas.
5. Usa "Limpiar Campos" para restablecer los campos.

Nota: Si el valor de x no está en el dominio, aparecerá una advertencia.
        """
        self.text_analisis.delete(1.0, tk.END)
        self.text_analisis.insert(1.0, instrucciones.strip())
    
    def mostrar_ejemplos(self):
        """Muestra una ventana con ejemplos seleccionables de funciones."""
        # Lista de ejemplos con función, valor de x y descripción
        ejemplos = [
            {"funcion": "(x+1)/(x-2)", "x": "1.5", "desc": "Función racional (x≠2)"},
            {"funcion": "x**2 - 4", "x": "3/2", "desc": "Polinomio cuadrático"},
            {"funcion": "sqrt(x**2 + 1)", "x": "3", "desc": "Función con raíz cuadrada"},
            {"funcion": "log(x + 1)", "x": "1", "desc": "Función logarítmica (x>-1)"},
            {"funcion": "sin(x) + cos(x)", "x": "pi/2", "desc": "Función trigonométrica"},
            {"funcion": "Abs(x - 2)", "x": "3", "desc": "Función con valor absoluto"},
            {"funcion": "exp(x) - 1", "x": "0", "desc": "Función exponencial"},
            {"funcion": "1/(1 + exp(-x))", "x": "2", "desc": "Función sigmoide"},
            {"funcion": "x**3 - 2*x", "x": "1", "desc": "Polinomio cúbico"},
            {"funcion": "tan(x)", "x": "pi/4", "desc": "Función tangente (x≠π/2 + kπ)"}
        ]
        
        # Crear ventana emergente
        ventana_ejemplos = tk.Toplevel(self.ventana)
        ventana_ejemplos.title("Ejemplos de Funciones")
        ventana_ejemplos.geometry("600x400")
        ventana_ejemplos.transient(self.ventana)
        ventana_ejemplos.grab_set()
        
        # Frame principal
        frame = ttk.Frame(ventana_ejemplos, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        # Listbox para mostrar ejemplos
        listbox = tk.Listbox(frame, height=15, width=80, font=('Arial', 10))
        listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Llenar el Listbox con los ejemplos
        for ej in ejemplos:
            listbox.insert(tk.END, f"f(x) = {ej['funcion']} | x = {ej['x']} | {ej['desc']}")
        
        # Función para cargar el ejemplo seleccionado
        def cargar_ejemplo_seleccionado(event=None):
            seleccion = listbox.curselection()
            if seleccion:
                idx = seleccion[0]
                ejemplo = ejemplos[idx]
                self.entry_funcion.delete(0, tk.END)
                self.entry_funcion.insert(0, ejemplo['funcion'])
                self.entry_x.delete(0, tk.END)
                self.entry_x.insert(0, ejemplo['x'])
                self.analizar_funcion()  # Ejecutar análisis automáticamente
                ventana_ejemplos.destroy()
        
        # Botón para cargar el ejemplo
        btn_cargar = ttk.Button(frame, text="Cargar Ejemplo", command=cargar_ejemplo_seleccionado)
        btn_cargar.grid(row=1, column=0, padx=5, pady=5)
        
        # Botón para cerrar la ventana
        btn_cerrar = ttk.Button(frame, text="Cerrar", command=ventana_ejemplos.destroy)
        btn_cerrar.grid(row=1, column=1, padx=5, pady=5)
        
        # Permitir cargar con doble clic
        listbox.bind('<Double-1>', cargar_ejemplo_seleccionado)
        
        # Permitir copiar el texto seleccionado
        def copiar_seleccion(event=None):
            seleccion = listbox.curselection()
            if seleccion:
                idx = seleccion[0]
                ejemplo = ejemplos[idx]
                texto = f"f(x) = {ejemplo['funcion']}, x = {ejemplo['x']}"
                self.ventana.clipboard_clear()
                self.ventana.clipboard_append(texto)
                messagebox.showinfo("Copiado", "Ejemplo copiado al portapapeles.")
        
        listbox.bind('<Control-c>', copiar_seleccion)
    
    def limpiar_campos(self):
        """Limpia los campos de entrada y el cuadro de análisis."""
        self.entry_funcion.delete(0, tk.END)
        self.entry_x.delete(0, tk.END)
        self.text_analisis.delete(1.0, tk.END)
        self.mostrar_instrucciones()
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
    
    def analizar_funcion(self):
        """Función principal de análisis."""
        try:
            expresion = self.entry_funcion.get().strip()
            if not expresion:
                messagebox.showerror("Error", "Por favor ingrese una función")
                return
            
            es_valida, funcion, mensaje = self.analizador.validar_funcion(expresion)
            if not es_valida:
                messagebox.showerror("Error en la función", mensaje)
                return
            
            self.funcion_actual = funcion
            self.expresion_original = expresion
            
            resultados = []
            resultados.append("=" * 60)
            resultados.append("ANÁLISIS DE LA FUNCIÓN (PASO A PASO)")
            resultados.append("=" * 60)
            resultados.append(f"Función: f(x) = {expresion}")
            resultados.append("")
            
            dominio_resumen, dominio_pasos, restricciones_dominio = self.analizador.calcular_dominio(funcion)
            resultados.append("DOMINIO (resumen):")
            resultados.append(dominio_resumen)
            resultados.append("")
            resultados.append("DOMINIO (pasos):")
            resultados.append(dominio_pasos)
            resultados.append("")
            
            recorrido_resumen, recorrido_pasos = self.analizador.calcular_recorrido(funcion)
            resultados.append("RECORRIDO (resumen):")
            resultados.append(recorrido_resumen)
            resultados.append("")
            resultados.append("RECORRIDO (pasos):")
            resultados.append(recorrido_pasos)
            resultados.append("")
            
            inter_resumen, inter_pasos = self.analizador.calcular_intersecciones(funcion)
            resultados.append("INTERSECCIONES (resumen):")
            resultados.append(inter_resumen)
            resultados.append("")
            resultados.append("INTERSECCIONES (pasos):")
            resultados.append(inter_pasos)
            resultados.append("")
            
            valor_x_str = self.entry_x.get().strip()
            valor_y_num = None
            valor_x_num_for_plot = None
            rompe_restricciones = False
            detalles_rompe = None
            
            if valor_x_str:
                try:
                    valor_x_sym = self.analizador.validar_valor_x(valor_x_str)
                except Exception as e:
                    resultados.append(f"ERROR: No se pudo interpretar el valor de x: {e}")
                    messagebox.showerror("Error", f"No se pudo interpretar el valor de x: {e}")
                    valor_x_sym = None
                
                if valor_x_sym is not None:
                    in_domain, check_msg = self.analizador.check_dominio_punto(valor_x_sym, restricciones_dominio)
                    if not in_domain:
                        rompe_restricciones = True
                        detalles_rompe = check_msg
                        messagebox.showwarning(
                            "Valor de x no válido",
                            f"El valor x = {valor_x_sym} ROMPE las restricciones del dominio de la función.\nRestricciones violadas: {check_msg}"
                        )
                        resultados.append(f"ADVERTENCIA: x = {valor_x_sym} ROMPE las restricciones del dominio de la función.")
                        resultados.append(f"Detalles: {check_msg}")
                        resultados.append("")
                    
                    pasos_eval, valor_sym_result, valor_float_for_plot, err = self.analizador.evaluar_funcion_paso_a_paso(
                        funcion, valor_x_sym, expresion, rompe_restricciones, detalles_rompe)
                    
                    resultados.append("=" * 60)
                    resultados.append("EVALUACIÓN PASO A PASO")
                    resultados.append("=" * 60)
                    resultados.append(pasos_eval)
                    resultados.append("")
                    
                    valor_y_num = valor_sym_result
                    vx, errx = self.analizador._to_safe_float(valor_x_sym)
                    if vx is not None:
                        valor_x_num_for_plot = vx
                    else:
                        resultados.append(f"Aviso: No se pudo usar x = {valor_x_sym} para el gráfico: {errx}")
            
            self.text_analisis.delete(1.0, tk.END)
            self.text_analisis.insert(1.0, "\n".join(resultados))
            
            self.generar_y_mostrar_grafico(valor_x_num_for_plot, valor_y_num)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def generar_y_mostrar_grafico(self, valor_x=None, valor_y=None):
        """Genera y muestra el gráfico en la interfaz."""
        try:
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            fig = self.graficador.generar_grafico(
                self.funcion_actual, valor_x, valor_y, self.expresion_original)
            
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            plt.close(fig)
        except Exception as e:
            error_label = ttk.Label(self.canvas_frame, text=f"Error al generar gráfico:\n{str(e)}")
            error_label.grid(row=0, column=0)
    
    def ejecutar(self):
        """Ejecuta la aplicación."""
        self.ventana.mainloop()


def main():
    """Función principal para iniciar la aplicación."""
    try:
        app = InterfazGrafica()
        app.ejecutar()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {str(e)}")
        input("Presione Enter para salir...")


if __name__ == "__main__":
    main()
