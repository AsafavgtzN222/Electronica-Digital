import re

class NumberConverter:
    """
    Clase que encapsula la lógica de validación y conversión 
    entre diferentes sistemas numéricos (Binario, Octal, Decimal, Hexadecimal),
    y genera explicaciones detalladas del proceso matemático paso a paso.
    """

    BASES = {
        "Binario": 2,
        "Octal": 8,
        "Decimal": 10,
        "Hexadecimal": 16
    }

    # Expresiones regulares para validar los caracteres según la base
    VALIDATION_PATTERNS = {
        "Binario": re.compile(r"^[01]+$"),
        "Octal": re.compile(r"^[0-7]+$"),
        "Decimal": re.compile(r"^\d+$"),
        "Hexadecimal": re.compile(r"^[0-9a-fA-F]+$")
    }

    @staticmethod
    def limpiar_entrada(texto: str) -> str:
        """
        Limpia el texto de entrada removiendo espacios en blanco.
        """
        if not texto:
            return ""
        return texto.replace(" ", "").replace("\t", "").strip()

    @classmethod
    def validar(cls, texto: str, base_origen: str) -> tuple[bool, str]:
        """
        Valida que el número ingresado sea correcto para la base seleccionada.
        """
        limpio = cls.limpiar_entrada(texto)

        if not limpio:
            return False, "El campo no puede estar vacío."

        if base_origen not in cls.BASES:
            return False, f"Base de origen '{base_origen}' no soportada."

        pattern = cls.VALIDATION_PATTERNS[base_origen]
        if not pattern.match(limpio):
            if base_origen == "Binario":
                return False, "Un número binario solo puede contener 0 y 1."
            elif base_origen == "Octal":
                return False, "Un número octal solo puede contener dígitos del 0 al 7."
            elif base_origen == "Decimal":
                return False, "Un número decimal solo puede contener dígitos del 0 al 9."
            elif base_origen == "Hexadecimal":
                return False, "Un número hexadecimal solo puede contener dígitos del 0 al 9 y letras de la A a la F."

        return True, ""

    @classmethod
    def convertir(cls, texto: str, base_origen: str) -> dict[str, str]:
        """
        Convierte un número desde la base de origen a todas las demás bases.
        """
        limpio = cls.limpiar_entrada(texto)
        base_num = cls.BASES[base_origen]

        # Convertir a entero (sistema decimal interno)
        valor_decimal = int(limpio, base_num)

        binario_str = bin(valor_decimal)[2:]
        octal_str = oct(valor_decimal)[2:]
        decimal_str = str(valor_decimal)
        hexadecimal_str = hex(valor_decimal)[2:].upper()
        cantidad_bits = len(binario_str)

        return {
            "Binario": binario_str,
            "Octal": octal_str,
            "Decimal": decimal_str,
            "Hexadecimal": hexadecimal_str,
            "Bits": str(cantidad_bits)
        }

    @classmethod
    def explicar_proceso(cls, texto: str, base_origen: str) -> str:
        """
        Genera una explicación paso a paso de las conversiones en formato de texto estructurado.
        """
        limpio = cls.limpiar_entrada(texto)
        base_num = cls.BASES[base_origen]
        valor_decimal = int(limpio, base_num)

        explicacion = []
        explicacion.append("=" * 60)
        explicacion.append(f"EXPLICACIÓN DETALLADA DEL PROCESO DE CONVERSIÓN")
        explicacion.append(f"Entrada: {texto} (Base {base_origen})")
        explicacion.append("=" * 60 + "\n")

        # --- PASO 1: CONVERSIÓN A DECIMAL (si el origen no es Decimal) ---
        if base_origen != "Decimal":
            explicacion.append(f"1. CONVERSIÓN A DECIMAL (Base 10)")
            explicacion.append("-" * 35)
            explicacion.append("Se utiliza el método de expansión posicional. Multiplicamos cada dígito")
            explicacion.append(f"por la base ({base_num}) elevada a su posición (empezando desde 0 de derecha a izquierda):\n")

            digitos = list(limpio)
            n = len(digitos)
            terminos_formula = []
            terminos_valores = []
            suma = 0

            for i, digito in enumerate(digitos):
                posicion = n - 1 - i
                # Convertir dígito hex a valor entero si aplica
                if base_origen == "Hexadecimal":
                    val_digito = int(digito, 16)
                    letra_explicacion = f"'{digito}' ({val_digito})" if val_digito > 9 else f"'{digito}'"
                else:
                    val_digito = int(digito)
                    letra_explicacion = f"'{digito}'"

                terminos_formula.append(f"({val_digito} × {base_num}^{posicion})")
                val_calculado = val_digito * (base_num ** posicion)
                terminos_valores.append(str(val_calculado))
                suma += val_calculado

            explicacion.append(f"Fórmula: " + " + ".join(terminos_formula))
            explicacion.append(f"Valores: " + " + ".join(terminos_valores))
            explicacion.append(f"Suma:    {suma}\n")
            explicacion.append(f"Resultado en Decimal: {suma}₁₀\n")
        else:
            explicacion.append("1. VALOR EN DECIMAL (Base 10)")
            explicacion.append("-" * 35)
            explicacion.append(f"La entrada ya se encuentra en base Decimal: {valor_decimal}₁₀\n")

        # --- PASO 2: CONVERSIÓN DE DECIMAL A BINARIO (Base 2) ---
        if base_origen != "Binario":
            explicacion.append(f"2. CONVERSIÓN A BINARIO (Base 2)")
            explicacion.append("-" * 35)
            explicacion.append("Utilizamos el método de divisiones sucesivas entre 2.")
            explicacion.append("Dividimos el número decimal entre 2 consecutivamente y anotamos los residuos.")
            explicacion.append("El número binario se forma leyendo los residuos de abajo hacia arriba (último al primero):\n")
            
            explicacion.append(f"{'Dividendo':<12} | {'Divisor':<8} | {'Cociente':<10} | {'Residuo':<8}")
            explicacion.append("-" * 46)
            
            residuos = []
            temp = valor_decimal
            if temp == 0:
                explicacion.append(f"{0:<12} | {2:<8} | {0:<10} | {0:<8}")
                residuos.append(0)
            else:
                while temp > 0:
                    cociente = temp // 2
                    residuo = temp % 2
                    explicacion.append(f"{temp:<12} | {2:<8} | {cociente:<10} | {residuo:<8}")
                    residuos.append(residuo)
                    temp = cociente
            
            bin_final = "".join(map(str, reversed(residuos)))
            explicacion.append(f"\nLectura de residuos (abajo hacia arriba): {bin_final}")
            explicacion.append(f"Resultado en Binario: {bin_final}₂ ({len(bin_final)} bits)\n")
        else:
            explicacion.append(f"2. VALOR EN BINARIO (Base 2)")
            explicacion.append("-" * 35)
            explicacion.append(f"La entrada ya es Binario: {limpio}₂ ({len(limpio)} bits)\n")

        # --- PASO 3: CONVERSIÓN DE DECIMAL A OCTAL (Base 8) ---
        if base_origen != "Octal":
            explicacion.append(f"3. CONVERSIÓN A OCTAL (Base 8)")
            explicacion.append("-" * 35)
            explicacion.append("Utilizamos el método de divisiones sucesivas entre 8.")
            explicacion.append("Dividimos el número decimal entre 8 consecutivamente y anotamos los residuos:\n")
            
            explicacion.append(f"{'Dividendo':<12} | {'Divisor':<8} | {'Cociente':<10} | {'Residuo':<8}")
            explicacion.append("-" * 46)
            
            residuos = []
            temp = valor_decimal
            if temp == 0:
                explicacion.append(f"{0:<12} | {8:<8} | {0:<10} | {0:<8}")
                residuos.append(0)
            else:
                while temp > 0:
                    cociente = temp // 8
                    residuo = temp % 8
                    explicacion.append(f"{temp:<12} | {8:<8} | {cociente:<10} | {residuo:<8}")
                    residuos.append(residuo)
                    temp = cociente
            
            oct_final = "".join(map(str, reversed(residuos)))
            explicacion.append(f"\nLectura de residuos (abajo hacia arriba): {oct_final}")
            explicacion.append(f"Resultado en Octal: {oct_final}₈\n")
        else:
            explicacion.append(f"3. VALOR EN OCTAL (Base 8)")
            explicacion.append("-" * 35)
            explicacion.append(f"La entrada ya es Octal: {limpio}₈\n")

        # --- PASO 4: CONVERSIÓN DE DECIMAL A HEXADECIMAL (Base 16) ---
        if base_origen != "Hexadecimal":
            explicacion.append(f"4. CONVERSIÓN A HEXADECIMAL (Base 16)")
            explicacion.append("-" * 35)
            explicacion.append("Utilizamos el método de divisiones sucesivas entre 16.")
            explicacion.append("Dividimos el número decimal entre 16. Si el residuo es mayor a 9,")
            explicacion.append("lo mapeamos a su respectiva letra (10=A, 11=B, 12=C, 13=D, 14=E, 15=F):\n")
            
            explicacion.append(f"{'Dividendo':<12} | {'Divisor':<8} | {'Cociente':<10} | {'Residuo (Valor/Letra)':<22}")
            explicacion.append("-" * 58)
            
            residuos = []
            temp = valor_decimal
            hex_map = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
            
            if temp == 0:
                explicacion.append(f"{0:<12} | {16:<8} | {0:<10} | {0:<22}")
                residuos.append("0")
            else:
                while temp > 0:
                    cociente = temp // 16
                    residuo = temp % 16
                    if residuo > 9:
                        residuo_str = f"{residuo} -> {hex_map[residuo]}"
                        residuos.append(hex_map[residuo])
                    else:
                        residuo_str = str(residuo)
                        residuos.append(str(residuo))
                    explicacion.append(f"{temp:<12} | {16:<8} | {cociente:<10} | {residuo_str:<22}")
                    temp = cociente
            
            hex_final = "".join(reversed(residuos))
            explicacion.append(f"\nLectura de residuos (abajo hacia arriba): {hex_final}")
            explicacion.append(f"Resultado en Hexadecimal: {hex_final}₁₆")
        else:
            explicacion.append(f"4. VALOR EN HEXADECIMAL (Base 16)")
            explicacion.append("-" * 35)
            explicacion.append(f"La entrada ya es Hexadecimal: {limpio.upper()}₁₆")

        return "\n".join(explicacion)
