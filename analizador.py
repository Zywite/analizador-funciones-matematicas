# analizador.py
"""
Módulo para el análisis matemático de funciones.
Proporciona cálculos de dominio, recorrido, intersecciones y evaluación paso a paso.
"""

import sympy as sp

class AnalizadorMatematico:
    """Clase para analizar funciones matemáticas usando SymPy."""
    
    def __init__(self):
        self.x = sp.Symbol('x')
    
    def _format_number(self, value):
        """Formatea un número con 2 decimales o en notación científica si es muy grande o pequeño."""
        try:
            value_float = float(value)
            if abs(value_float) > 10000 or (abs(value_float) < 0.0001 and value_float != 0):
                return f"{value_float:.1e}"
            return f"{value_float:.2f}"
        except (ValueError, TypeError):
            return str(value)
    
    def limpiar_expresion(self, expresion):
        """Limpia y estandariza la expresión de entrada."""
        expresion = expresion.replace('^', '**')
        expresion = expresion.replace('ln', 'log')
        return expresion
    
    def validar_funcion(self, expresion):
        """Valida si la expresión es una función válida en términos de x."""
        try:
            expresion_limpia = self.limpiar_expresion(expresion)
            funcion = sp.sympify(expresion_limpia)
            if not self.x in funcion.free_symbols:
                return False, None, "La expresión debe ser una función de x."
            return True, funcion, "Función válida."
        except Exception as e:
            return False, None, f"Error en la sintaxis de la función: {str(e)}"
    
    def _to_safe_float(self, valor, decimals=2):
        """Convierte un valor a float seguro, limitando a 2 decimales."""
        try:
            if valor.is_integer:
                return int(valor), None
            return round(float(valor), decimals), None
        except (ValueError, TypeError, OverflowError) as e:
            return None, f"No se pudo convertir a float: {str(e)}"
    
    def validar_valor_x(self, valor_x_str):
        """Valida y convierte el valor de x a un formato simbólico."""
        try:
            if '/' in valor_x_str:
                numer, denom = map(float, valor_x_str.split('/'))
                return sp.Rational(numer, denom)
            return sp.sympify(valor_x_str)
        except Exception as e:
            raise ValueError(f"Valor de x no válido: {str(e)}")
    
    def check_dominio_punto(self, valor_x, restricciones_dominio):
        """Verifica si un valor de x está en el dominio de la función."""
        for restriccion, valores in restricciones_dominio:
            for v in valores:
                try:
                    if sp.Eq(valor_x, v):
                        return False, f"x = {self._format_number(valor_x)} no está en el dominio ({restriccion})."
                except Exception:
                    continue
        return True, "x está en el dominio."
    
    def calcular_dominio(self, funcion):
        """Calcula el dominio de la función paso a paso."""
        try:
            pasos = []
            restricciones_dominio = []
            
            # Identificar denominadores
            if funcion.is_rational_function():
                _, den = funcion.as_numer_denom()
                if den != 1:
                    pasos.append(f"Paso 1: Identificar el denominador: {den}")
                    ceros = sp.solve(den, self.x)
                    if ceros:
                        restricciones_dominio.append((f"{den} != 0", ceros))
                        pasos.append(f"Paso 2: Encontrar valores donde {den} = 0")
                        pasos.append(f"Solución: {den} = 0 => x = {ceros}")
            
            # Identificar restricciones de logaritmos
            log_terms = funcion.find(sp.log)
            for log_term in log_terms:
                arg = log_term.args[0]
                pasos.append(f"Paso: Para log({arg}), el argumento debe ser positivo: {arg} > 0")
                sol = sp.solve(arg > 0, self.x)
                restricciones_dominio.append((f"{arg} > 0", sol))
                pasos.append(f"Solución: {arg} > 0 => x en {sol}")
            
            # Formatear dominio con notación científica
            dominio_resumen = "ℝ"
            if restricciones_dominio:
                exclusions = []
                for _, valores in restricciones_dominio:
                    formatted_vals = [self._format_number(float(val)) for val in valores]
                    exclusions.extend(formatted_vals)
                if exclusions:
                    dominio_resumen = f"ℝ \\ {{ {', '.join(exclusions)} \\}}"
            
            pasos.append(f"Dominio final: {dominio_resumen}")
            return dominio_resumen, "\n".join(pasos), restricciones_dominio
        except Exception as e:
            return "No se pudo calcular el dominio.", f"Error: {str(e)}", []
    
    def calcular_recorrido(self, funcion):
        """Calcula el recorrido de la función paso a paso."""
        try:
            pasos = []
            pasos.append("Paso 1: Intentar encontrar el recorrido resolviendo y = f(x) para x.")
            y = sp.Symbol('y')
            eq = sp.Eq(funcion, y)
            soluciones = sp.solve(eq, self.x)
            
            if not soluciones:
                pasos.append("Paso 2: No se pudo resolver y = f(x) para x. Analizando comportamiento.")
                if funcion.is_polynomial():
                    pasos.append("Paso 3: La función es un polinomio.")
                    grado = funcion.as_poly().degree()
                    if grado % 2 == 0:
                        pasos.append(f"Paso 4: Polinomio de grado par ({grado}).")
                        coef_lider = funcion.coeff(self.x**grado)
                        if coef_lider > 0:
                            min_y = funcion.subs(self.x, sp.solve(sp.diff(funcion, self.x), self.x)[0])
                            pasos.append(f"Paso 5: Mínimo en y = {self._format_number(min_y)}")
                            recorrido = f"[{self._format_number(min_y)}, ∞)"
                        else:
                            max_y = funcion.subs(self.x, sp.solve(sp.diff(funcion, self.x), self.x)[0])
                            pasos.append(f"Paso 5: Máximo en y = {self._format_number(max_y)}")
                            recorrido = f"(-∞, {self._format_number(max_y)}]"
                    else:
                        pasos.append(f"Paso 4: Polinomio de grado impar ({grado}).")
                        recorrido = "ℝ"
                else:
                    pasos.append("Paso 3: La función no es un polinomio. Analizando asíntotas.")
                    if funcion.is_rational_function():
                        num, den = funcion.as_numer_denom()
                        grado_num = num.as_poly(self.x).degree() if num.is_polynomial() else 0
                        grado_den = den.as_poly(self.x).degree() if den.is_polynomial() else 0
                        if grado_num == grado_den:
                            coef_num = num.coeff(self.x**grado_num) if grado_num > 0 else num
                            coef_den = den.coeff(self.x**grado_den) if grado_den > 0 else den
                            asintota = coef_num / coef_den
                            pasos.append(f"Paso 4: Asíntota horizontal en y = {self._format_number(asintota)}")
                            recorrido = f"ℝ \\ {{ {self._format_number(asintota)} \\}}"
                        elif grado_num < grado_den:
                            pasos.append("Paso 4: Asíntota horizontal en y = 0")
                            recorrido = f"ℝ \\ {{ {self._format_number(0)} \\}}"
                        else:
                            pasos.append("Paso 4: Sin asíntota horizontal (recorrido aproximado)")
                            recorrido = "ℝ"
                    else:
                        pasos.append("Paso 4: Análisis aproximado, requiere revisión")
                        recorrido = "ℝ"
            else:
                pasos.append(f"Paso 2: Solución para x = {soluciones}")
                # Calcular dominio de la inversa
                dominio_inversa, _, restricciones = self.calcular_dominio(soluciones[0]) if soluciones else ("ℝ", [], [])
                pasos.append(f"Paso 3: Identificar el denominador de la inversa: {soluciones[0].as_numer_denom()[1]}")
                ceros = sp.solve(soluciones[0].as_numer_denom()[1], y)
                if ceros:
                    pasos.append(f"Paso 4: Encontrar valores donde el denominador = 0")
                    pasos.append(f"Solución: y = {ceros}")
                    formatted_vals = [self._format_number(float(val)) for val in ceros]
                    dominio_inversa = f"ℝ \\ {{ {', '.join(formatted_vals)} \\}}"
                pasos.append(f"Paso 5: Dominio de la inversa (recorrido de f): {dominio_inversa}")
                recorrido = dominio_inversa
            
            pasos.append(f"Recorrido final: {recorrido}")
            return recorrido, "\n".join(pasos)
        except Exception as e:
            return "No se pudo calcular el recorrido.", f"Error: {str(e)}"
    
    def calcular_intersecciones(self, funcion):
        """Calcula las intersecciones con los ejes X y Y."""
        try:
            pasos = []
            inter_resumen = []
            
            pasos.append("Paso 1: Intersección con el eje Y (x = 0).")
            y_inter = funcion.subs(self.x, 0)
            y_inter_float, _ = self._to_safe_float(y_inter)
            inter_resumen.append(f"Intersección en Y: (0, {self._format_number(y_inter_float)})")
            pasos.append(f"Solución: f(0) = {y_inter} ≈ {self._format_number(y_inter_float)}")
            
            pasos.append("Paso 2: Intersección con el eje X (f(x) = 0).")
            x_inter = sp.solve(funcion, self.x)
            inter_x_float = []
            for xi in x_inter:
                xi_float, _ = self._to_safe_float(xi)
                if xi_float is not None:
                    inter_x_float.append(xi_float)
                    inter_resumen.append(f"Intersección en X: ({self._format_number(xi_float)}, 0)")
            pasos.append(f"Solución: f(x) = 0 => x = {inter_x_float}")
            
            return "\n".join(inter_resumen), "\n".join(pasos)
        except Exception as e:
            return "No se pudieron calcular las intersecciones.", f"Error: {str(e)}"
    
    def evaluar_funcion_paso_a_paso(self, funcion, valor_x, expresion_original, rompe_restricciones, detalles_rompe):
        """Evalúa la función en un valor de x, mostrando pasos."""
        pasos = []
        pasos.append(f"Paso 1: Evaluar f(x) = {expresion_original} en x = {self._format_number(valor_x)}")
        
        if rompe_restricciones:
            pasos.append(f"Paso 2: x = {self._format_number(valor_x)} NO está en el dominio.")
            pasos.append(f"Restricciones violadas: {detalles_rompe}")
            return "\n".join(pasos), None, None, "Valor de x fuera del dominio."
        
        try:
            pasos.append(f"Paso 2: Sustituir x = {self._format_number(valor_x)} en la función.")
            resultado = funcion.subs(self.x, valor_x)
            pasos.append(f"Paso 3: f({self._format_number(valor_x)}) = {resultado}")
            
            if resultado.is_algebraic:
                pasos.append("Paso 4: Simplificar el resultado algebraicamente.")
                resultado_simplificado = sp.simplify(resultado)
                pasos.append(f"Resultado simplificado: {resultado_simplificado}")
            else:
                resultado_simplificado = resultado
            
            pasos.append("Paso 5: Convertir a valor numérico.")
            valor_float, error = self._to_safe_float(resultado_simplificado)
            if error:
                pasos.append(f"Error: {error}")
                return "\n".join(pasos), None, None, error
            
            pasos.append(f"Valor decimal (2 decimales): {self._format_number(valor_float)}")
            pasos.append(f"Par ordenado: ({self._format_number(float(valor_x))}, {self._format_number(valor_float)})")
            
            return "\n".join(pasos), resultado_simplificado, valor_float, None
        except Exception as e:
            pasos.append(f"Error al evaluar: {str(e)}")
            return "\n".join(pasos), None, None, f"Error: {str(e)}"
