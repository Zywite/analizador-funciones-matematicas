# analizador.py
"""
Módulo para el análisis matemático de funciones.
Proporciona funciones para calcular dominio, recorrido, intersecciones y evaluar puntos,
con desarrollo paso a paso usando SymPy.
"""

import sympy as sp
import re
import math


class AnalizadorMatematico:
    """Clase para manejar el análisis matemático de funciones (paso a paso)."""
    
    def __init__(self):
        self.x = sp.symbols('x')
    
    def _to_safe_float(self, sym_val, decimals=4):
        """
        Convierte un valor SymPy a float de forma segura, limitando decimales.
        Devuelve (float_value, None) si OK, o (None, mensaje_error) si falla.
        """
        try:
            num = sp.N(sym_val, 15)
            if getattr(num, 'is_real', True) is False:
                return None, f"El valor es complejo: {num}"
            f = float(num)
            if not math.isfinite(f):
                return None, f"El valor no es finito: {num}"
            return round(f, decimals), None
        except Exception as e:
            return None, f"No se pudo convertir a float: {sym_val} ({e})"
    
    def _eval_relational(self, rel, val_x):
        """
        Evalúa si una relación (Relational) se cumple en val_x.
        Devuelve (bool_holds, error_msg_o_None).
        """
        try:
            lhs = rel.lhs.subs(self.x, val_x)
            rhs = rel.rhs.subs(self.x, val_x)
            lhs_n = sp.N(lhs, 10)
            rhs_n = sp.N(rhs, 10)
            if not (lhs_n.is_real and rhs_n.is_real):
                return False, "Valor complejo o indefinido en la restricción"
            l = float(lhs_n)
            r = float(rhs_n)
            op = rel.rel_op
            if op == '==':
                res = (l == r)
            elif op == '!=':
                res = (l != r)
            elif op == '>':
                res = (l > r)
            elif op == '>=':
                res = (l >= r)
            elif op == '<':
                res = (l < r)
            elif op == '<=':
                res = (l <= r)
            else:
                return False, f"Operador desconocido: {op}"
            return res, None
        except Exception as e:
            return False, str(e)
    
    def check_dominio_punto(self, val_x, restricciones):
        """
        Verifica si val_x satisface las restricciones del dominio.
        Devuelve (bool_in_domain, msg_o_None).
        """
        if not restricciones:
            return True, None
        violation_msgs = []
        for r in restricciones:
            holds, err = self._eval_relational(r, val_x)
            if not holds:
                if err:
                    violation_msgs.append(f"{str(r)}: {err}")
                else:
                    violation_msgs.append(str(r))
        if violation_msgs:
            msg = "; ".join(violation_msgs)
            return False, msg
        return True, None
    
    def validar_funcion(self, expresion):
        """
        Valida que la expresión sea una función válida y devuelve la expr SymPy.
        Devuelve (es_valida, funcion, mensaje).
        """
        try:
            expresion_limpia = self.limpiar_expresion(expresion)
            funcion = sp.sympify(expresion_limpia, evaluate=False)
            funcion = sp.simplify(funcion)
            return True, funcion, expresion_limpia
        except Exception as e:
            return False, None, f"Error en la función: {str(e)}"
    
    def limpiar_expresion(self, expresion):
        """
        Limpia y prepara la expresión para SymPy, permitiendo ingreso limpio.
        Soporta operadores como ^, ln, sen, etc., y corrige notación implícita.
        """
        expresion = expresion.replace('^', '**')
        expresion = expresion.replace('ln', 'log')
        expresion = expresion.replace('sen', 'sin')
        expresion = expresion.replace('tg', 'tan')
        expresion = expresion.replace('ctg', 'cot')
        expresion = expresion.replace('sec', 'sec')
        expresion = expresion.replace('csc', 'csc')
        expresion = expresion.replace('arcsin', 'asin')
        expresion = expresion.replace('arccos', 'acos')
        expresion = expresion.replace('arctan', 'atan')
        expresion = expresion.replace('sqrt', 'sqrt')
        expresion = expresion.replace('abs', 'Abs')
        
        # Corrige multiplicaciones implícitas (ej. 2x -> 2*x)
        expresion = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expresion)
        expresion = re.sub(r'([a-zA-Z\)])(\d)', r'\1*\2', expresion)
        expresion = re.sub(r'(\))(\()', r'\1*\2', expresion)
        expresion = re.sub(r'(\d)(\()', r'\1*\2', expresion)
        expresion = re.sub(r'(\))([a-zA-Z])', r'\1*\2', expresion)
        
        return expresion
    
    def calcular_dominio(self, funcion):
        """
        Calcula el dominio de la función.
        Devuelve (resumen_str, pasos_str, list_restricciones_sympy).
        """
        pasos = []
        restricciones = []
        try:
            pasos.append("Paso 1: Simplificamos la función para analizar numerador y denominador.")
            expr = sp.simplify(funcion)
            pasos.append(f"   Función simplificada: {expr}")
            
            expr_together = sp.together(expr)
            num, denom = expr_together.as_numer_denom()
            pasos.append(f"   Numerador: {num}")
            pasos.append(f"   Denominador: {denom}")
            
            if denom != 1:
                pasos.append("Paso 2: Encontramos valores donde el denominador es cero (no permitidos).")
                denom_fact = sp.factor(denom)
                pasos.append(f"   Denominador factorizado: {denom_fact}")
                ceros = sp.solve(sp.Eq(denom, 0), self.x)
                if ceros:
                    for z in ceros:
                        if z.is_real:
                            restr = sp.Ne(self.x, z)
                            restricciones.append(restr)
                            pasos.append(f"   Encontrado: x = {z} → restricción: x ≠ {z}")
            
            logs = list(funcion.find(sp.log))
            if logs:
                pasos.append("Paso 3: Analizamos logaritmos (el argumento debe ser positivo).")
                for L in logs:
                    arg = L.args[0]
                    restr = sp.Gt(arg, 0)
                    restricciones.append(restr)
                    pasos.append(f"   Logaritmo con argumento {arg} → restricción: {restr}")
            
            pow_exprs = list(funcion.find(sp.Pow))
            for p in pow_exprs:
                exp = p.exp
                base = p.base
                if exp.is_Rational and exp.q % 2 == 0:
                    restr = sp.Ge(base, 0)
                    restricciones.append(restr)
                    pasos.append(f"   Raíz de índice par: ({base})**({exp}) → restricción: {restr}")
            
            if not restricciones:
                dominio_resumen = "ℝ"
                pasos.append("Paso 4: No se encontraron restricciones, el dominio es todos los reales.")
            else:
                pasos.append("Paso 4: Combinamos las restricciones para definir el dominio.")
                restr_strings = [f"x ≠ {z}" for z in ceros if z.is_real]
                dominio_resumen = f"ℝ \\ {{ {', '.join(map(str, ceros))} }}"
            
            return dominio_resumen, "\n".join(pasos), restricciones
        
        except Exception as e:
            return f"No se pudo calcular el dominio: {e}", f"Error detallado: {e}", []
    
    def calcular_recorrido(self, funcion):
        """
        Determina el recorrido resolviendo y = f(x) algebraicamente.
        Devuelve (resumen_str, pasos_str).
        """
        pasos = []
        try:
            expr = sp.simplify(funcion)
            pasos.append(f"Paso 1: Simplificamos la función: {expr}")
            
            pasos.append("Paso 2: Intentamos expresar x en términos de y (resolviendo y = f(x)).")
            y = sp.symbols('y')
            try:
                eq = sp.Eq(expr, y)
                sol_x = sp.solve(eq, self.x)
                pasos.append(f"   Resolviendo y = f(x), obtenemos: x = {sol_x}")
                
                restr_y = []
                for s in sol_x:
                    denoms = s.as_numer_denom()[1]
                    if denoms != 1:
                        y_vals = sp.solve(sp.Eq(denoms, 0), y)
                        for yv in y_vals:
                            if yv.is_real:
                                restr_y.append(f"y ≠ {yv}")
                
                pasos.append(f"Paso 3: Encontramos restricciones en y: {', '.join(restr_y) if restr_y else 'ninguna'}")
                
                pasos.append("Paso 4: Verificamos que los valores de x obtenidos estén en el dominio.")
                _, _, restricciones_dominio = self.calcular_dominio(funcion)
                dominio_violado = False
                for s in sol_x:
                    for restr in restricciones_dominio:
                        try:
                            holds, err = self._eval_relational(restr, s)
                            if not holds:
                                pasos.append(f"   Restricción del dominio {restr} no se cumple para algunos y.")
                                dominio_violado = True
                        except Exception as e:
                            pasos.append(f"   No se pudo verificar restricción {restr}: {e}")
                            dominio_violado = True
                
                # Ajuste para funciones racionales lineales
                num, denom = expr.as_numer_denom()
                if num.is_polynomial(self.x) and denom.is_polynomial(self.x):
                    grado_num = sp.degree(num, self.x)
                    grado_den = sp.degree(denom, self.x)
                    if grado_num <= 1 and grado_den <= 1:
                        if restr_y:
                            resumen = f"ℝ \\ {{ {', '.join([str(yv) for yv in sp.solve(sp.Eq(denoms, 0), y) if yv.is_real])} }}"
                        else:
                            resumen = "ℝ"
                    else:
                        resumen = f"Todos los reales salvo {', '.join(restr_y)}" if restr_y else "ℝ"
                else:
                    resumen = f"Todos los reales salvo {', '.join(restr_y)}" if restr_y else "ℝ"
                
                return resumen, "\n".join(pasos)
            
            except Exception as e:
                pasos.append(f"   No se pudo resolver y = f(x): {e}")
                resumen = "ℝ (estimado, no se pudo determinar algebraicamente)"
                return resumen, "\n".join(pasos)
        
        except Exception as e:
            return f"No se pudo calcular el recorrido: {e}", f"Error detallado: {e}"
    
    def calcular_intersecciones(self, funcion):
        """
        Calcula intersecciones con los ejes.
        Devuelve (resumen_str, pasos_str).
        """
        pasos = []
        try:
            expr = sp.simplify(funcion)
            pasos.append(f"Paso 1: Simplificamos la función: {expr}")
            
            pasos.append("Paso 2: Calculamos la intersección con el eje Y (x = 0).")
            try:
                y0 = expr.subs(self.x, 0)
                y0_float, _ = self._to_safe_float(y0)
                inter_y = f"(0, {y0_float if y0_float is not None else y0})"
                pasos.append(f"   Sustituimos x = 0: f(0) = {y0}")
            except Exception as e:
                pasos.append(f"   No se puede evaluar en x=0: {e}")
                inter_y = "No definida en x=0"
            
            pasos.append("Paso 3: Calculamos las intersecciones con el eje X (f(x) = 0).")
            try:
                sols = sp.solve(sp.Eq(expr, 0), self.x)
                pasos.append(f"   Soluciones de f(x) = 0: {sols}")
                reales = []
                for s in sols:
                    if s.is_real:
                        s_float, _ = self._to_safe_float(s)
                        reales.append(f"({s_float if s_float is not None else s}, 0)")
                if reales:
                    inter_x = ", ".join(reales)
                else:
                    inter_x = "No hay intersecciones reales con el eje X."
            except Exception as e:
                pasos.append(f"   Error resolviendo f(x)=0: {e}")
                inter_x = "No se pudieron determinar las intersecciones con el eje X."
            
            resumen = f"Intersección con el eje Y: {inter_y}\nIntersecciones con el eje X: {inter_x}"
            return resumen, "\n".join(pasos)
        
        except Exception as e:
            return f"Error al calcular intersecciones: {e}", f"Error detallado: {e}"
    
    def evaluar_funcion_paso_a_paso(self, funcion, valor_x_sym, expresion_original, rompe_restricciones=False, detalles_rompe=None):
        """
        Evalúa la función en un punto paso a paso.
        Devuelve (pasos_str, valor_simpy, valor_float_opcional, error_msg_opcional).
        """
        pasos = []
        try:
            pasos.append(f"Paso 1: Función original: f(x) = {sp.simplify(funcion)}")
            x_float, _ = self._to_safe_float(valor_x_sym)
            x_display = x_float if x_float is not None else valor_x_sym
            pasos.append(f"Paso 2: Valor solicitado: x = {x_display}")
            
            if rompe_restricciones:
                pasos.append(f"ADVERTENCIA: Este valor de x ROMPE las restricciones del dominio: {detalles_rompe}")
            
            pasos.append(f"Paso 3: Sustituimos x = {x_display} en la función.")
            expr_sub = funcion.subs(self.x, valor_x_sym)
            pasos.append(f"   Resultado: f({x_display}) = {sp.N(expr_sub, 4)}")
            
            pasos.append("Paso 4: Simplificamos el resultado.")
            simpl = sp.simplify(expr_sub)
            pasos.append(f"   Resultado simplificado: {sp.N(simpl, 4)}")
            
            pasos.append("Paso 5: Intentamos obtener un valor numérico.")
            try:
                valor_num = sp.N(simpl, 15)
                pasos.append(f"   Valor numérico: {sp.N(valor_num, 4)}")
            except Exception as e:
                valor_num = simpl
                pasos.append(f"   No se pudo obtener un valor numérico: {e}")
            
            valor_float, err = self._to_safe_float(valor_num, decimals=4)
            if valor_float is None:
                pasos.append(f"Paso 6: No se pudo convertir a número decimal: {err}")
            else:
                pasos.append(f"Paso 6: Valor decimal: {valor_float}")
            
            pasos.append(f"Paso 7: Par ordenado: ({x_display}, {sp.N(valor_num, 4)})")
            return "\n".join(pasos), valor_num, valor_float, None
        
        except Exception as e:
            return f"Error en la evaluación: {e}", None, None, str(e)
    
    def validar_valor_x(self, valor_x_str):
        """Valida y convierte el valor de x a una expresión SymPy."""
        try:
            return sp.sympify(valor_x_str)
        except Exception as e:
            raise Exception(f"No se pudo interpretar el valor de x: {e}")
