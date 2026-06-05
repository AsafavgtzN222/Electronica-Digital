import tkinter as tk
from tkinter import ttk
from converter import NumberConverter

class ConverterApp:
    """
    Clase que define la Interfaz Gráfica de Usuario (GUI) para la aplicación.
    Sigue una estética moderna y limpia en tema oscuro (Flat Dark Theme) y usa pestañas (Notebook).
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Conversor de Sistemas Numéricos")
        self.root.configure(bg="#121212")  # Fondo oscuro principal
        
        # Dimensiones y centrado de la ventana
        width = 850
        height = 680
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)

        # Historial en memoria para la sesión
        self.historial_datos = []

        # Estilo general para ttk
        self.style = ttk.Style()
        self.style.theme_use("default")
        
        # Configurar estilos de Combobox para tema oscuro
        self.style.configure("TCombobox", 
                             fieldbackground="#2C2C2C", 
                             background="#1E1E1E", 
                             foreground="#FFFFFF",
                             arrowcolor="#00ADB5")
        
        # Estilos para las pestañas del Notebook en tema oscuro
        self.style.configure("TNotebook", background="#121212", borderwidth=0)
        self.style.configure("TNotebook.Tab", 
                             background="#1E1E1E", 
                             foreground="#A0A0A0", 
                             padding=[18, 6],
                             font=("Segoe UI", 10, "bold"),
                             borderwidth=0)
        self.style.map("TNotebook.Tab",
                       background=[("selected", "#00ADB5"), ("active", "#2C2C2C")],
                       foreground=[("selected", "#FFFFFF"), ("active", "#FFFFFF")])
        
        self.crear_widgets()
        self.configurar_eventos()

    def crear_widgets(self):
        # --- HEADER ---
        header_frame = tk.Frame(self.root, bg="#1E1E1E", height=80)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, 
                               text="CONVERSOR DE SISTEMAS NUMÉRICOS", 
                               font=("Segoe UI", 16, "bold"), 
                               fg="#00ADB5", 
                               bg="#1E1E1E")
        title_label.pack(pady=(15, 2))
        
        subtitle_label = tk.Label(header_frame, 
                                  text="Herramienta Educativa de Conversión & Procedimientos", 
                                  font=("Segoe UI", 9, "italic"), 
                                  fg="#888888", 
                                  bg="#1E1E1E")
        subtitle_label.pack()

        # --- BARRA DE ESTADO / MENSAJES (Siempre visible abajo) ---
        self.lbl_estado = tk.Label(self.root, 
                                   text="Listo para convertir.", 
                                   font=("Segoe UI", 10), 
                                   fg="#888888", 
                                   bg="#121212", 
                                   anchor="w",
                                   padx=20)
        self.lbl_estado.pack(fill="x", side="bottom", pady=5)

        # --- PANEL DE PESTAÑAS (Notebook) ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=(10, 0))

        # Crear Frames para las pestañas
        self.tab_conversor = tk.Frame(self.notebook, bg="#121212")
        self.tab_explicacion = tk.Frame(self.notebook, bg="#121212")

        self.notebook.add(self.tab_conversor, text=" Conversor ")
        self.notebook.add(self.tab_explicacion, text=" Explicación del Proceso ")

        # =========================================================================
        # PESTAÑA 1: CONVERSOR (Interfaz Principal)
        # =========================================================================
        main_container = tk.Frame(self.tab_conversor, bg="#121212")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Fila Superior: Controles a la izquierda e Historial a la derecha
        top_row_frame = tk.Frame(main_container, bg="#121212")
        top_row_frame.pack(fill="x", side="top", pady=(0, 10))

        # --- SECCIÓN IZQUIERDA: CONTROLES ---
        left_frame = tk.LabelFrame(top_row_frame, 
                                   text=" Entrada de Datos ", 
                                   font=("Segoe UI", 11, "bold"), 
                                   fg="#00ADB5", 
                                   bg="#1E1E1E", 
                                   bd=1, 
                                   relief="flat",
                                   padx=15, 
                                   pady=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Entrada del Número
        lbl_num = tk.Label(left_frame, text="Número a convertir:", font=("Segoe UI", 10, "bold"), fg="#EEEEEE", bg="#1E1E1E")
        lbl_num.pack(anchor="w", pady=(0, 3))
        
        entry_border = tk.Frame(left_frame, bg="#3A3A3A", bd=1)
        entry_border.pack(fill="x", pady=(0, 10))
        self.entry_numero = tk.Entry(entry_border, 
                                     font=("Consolas", 12), 
                                     fg="#FFFFFF", 
                                     bg="#2C2C2C", 
                                     bd=0, 
                                     insertbackground="#FFFFFF",
                                     highlightthickness=0)
        self.entry_numero.pack(fill="x", padx=5, pady=5)
        self.entry_numero.focus()

        # Selección de Base
        lbl_base = tk.Label(left_frame, text="Base de origen:", font=("Segoe UI", 10, "bold"), fg="#EEEEEE", bg="#1E1E1E")
        lbl_base.pack(anchor="w", pady=(0, 3))

        self.combo_base = ttk.Combobox(left_frame, 
                                       values=["Binario", "Octal", "Decimal", "Hexadecimal"], 
                                       state="readonly", 
                                       font=("Segoe UI", 11))
        self.combo_base.set("Decimal")
        self.combo_base.pack(fill="x", pady=(0, 15))

        # Botones de Acción
        btn_frame = tk.Frame(left_frame, bg="#1E1E1E")
        btn_frame.pack(fill="x")

        self.btn_convertir = tk.Button(btn_frame, 
                                       text="Convertir", 
                                       font=("Segoe UI", 10, "bold"), 
                                       fg="#FFFFFF", 
                                       bg="#00ADB5", 
                                       activebackground="#008c92", 
                                       activeforeground="#FFFFFF",
                                       relief="flat", 
                                       cursor="hand2",
                                       bd=0,
                                       height=2,
                                       command=self.ejecutar_conversion)
        self.btn_convertir.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_limpiar = tk.Button(btn_frame, 
                                     text="Limpiar", 
                                     font=("Segoe UI", 10, "bold"), 
                                     fg="#FFFFFF", 
                                     bg="#393E46", 
                                     activebackground="#2e3238", 
                                     activeforeground="#FFFFFF",
                                     relief="flat", 
                                     cursor="hand2",
                                     bd=0,
                                     height=2,
                                     command=self.limpiar_campos)
        self.btn_limpiar.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # --- SECCIÓN DERECHA: HISTORIAL ---
        right_frame = tk.LabelFrame(top_row_frame, 
                                    text=" Historial de Conversiones ", 
                                    font=("Segoe UI", 11, "bold"), 
                                    fg="#00ADB5", 
                                    bg="#1E1E1E", 
                                    bd=1, 
                                    relief="flat",
                                    padx=15, 
                                    pady=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        list_container = tk.Frame(right_frame, bg="#1E1E1E")
        list_container.pack(fill="both", expand=True, pady=(0, 5))

        scrollbar = tk.Scrollbar(list_container, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.listbox_historial = tk.Listbox(list_container, 
                                            bg="#2C2C2C", 
                                            fg="#EEEEEE", 
                                            selectbackground="#00ADB5", 
                                            selectforeground="#FFFFFF",
                                            font=("Consolas", 9), 
                                            bd=0, 
                                            highlightthickness=0, 
                                            yscrollcommand=scrollbar.set)
        self.listbox_historial.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox_historial.yview)

        self.btn_borrar_historial = tk.Button(right_frame, 
                                              text="Borrar Historial", 
                                              font=("Segoe UI", 9), 
                                              fg="#A0A0A0", 
                                              bg="#2C2C2C", 
                                              activebackground="#3A3A3A", 
                                              activeforeground="#A0A0A0",
                                              relief="flat", 
                                              cursor="hand2",
                                              bd=0,
                                              command=self.limpiar_historial)
        self.btn_borrar_historial.pack(anchor="e")

        # --- SECCIÓN INFERIOR: RESULTADOS ---
        results_frame = tk.LabelFrame(main_container, 
                                      text=" Resultados de la Conversión ", 
                                      font=("Segoe UI", 11, "bold"), 
                                      fg="#00ADB5", 
                                      bg="#1E1E1E", 
                                      bd=1, 
                                      relief="flat",
                                      padx=20, 
                                      pady=10)
        results_frame.pack(fill="both", expand=True)

        results_grid = tk.Frame(results_frame, bg="#1E1E1E")
        results_grid.pack(fill="both", expand=True)

        results_grid.grid_columnconfigure(0, weight=1)
        results_grid.grid_columnconfigure(1, weight=3)
        results_grid.grid_columnconfigure(2, weight=1)

        self.salidas = {}
        bases_salida = [
            ("Binario", "Binario"),
            ("Octal", "Octal"),
            ("Decimal", "Decimal"),
            ("Hexadecimal", "Hexadecimal")
        ]

        for idx, (label_text, base_key) in enumerate(bases_salida):
            lbl = tk.Label(results_grid, 
                           text=f"{label_text}:", 
                           font=("Segoe UI", 10, "bold"), 
                           fg="#EEEEEE", 
                           bg="#1E1E1E",
                           anchor="w")
            lbl.grid(row=idx, column=0, sticky="w", pady=6, padx=(0, 10))
            if label_text == "Binario":
                self.lbl_binario = lbl

            entry_out_border = tk.Frame(results_grid, bg="#3A3A3A", bd=1)
            entry_out_border.grid(row=idx, column=1, sticky="ew", pady=6, padx=10)
            
            entry_out = tk.Entry(entry_out_border, 
                                 font=("Consolas", 11), 
                                 fg="#00ADB5", 
                                 bg="#2C2C2C", 
                                 bd=0,
                                 state="readonly",
                                 readonlybackground="#2C2C2C",
                                 highlightthickness=0)
            entry_out.pack(fill="x", padx=5, pady=4)
            self.salidas[base_key] = entry_out

            btn_copiar = tk.Button(results_grid, 
                                   text="Copiar 📋", 
                                   font=("Segoe UI", 9), 
                                   fg="#EEEEEE", 
                                   bg="#393E46", 
                                   activebackground="#2e3238", 
                                   activeforeground="#FFFFFF",
                                   relief="flat", 
                                   cursor="hand2",
                                   bd=0,
                                   padx=10,
                                   command=lambda key=base_key: self.copiar_resultado(key))
            btn_copiar.grid(row=idx, column=2, sticky="ew", pady=6, padx=(10, 0))


        # =========================================================================
        # PESTAÑA 2: EXPLICACIÓN DEL PROCESO
        # =========================================================================
        expl_container = tk.Frame(self.tab_explicacion, bg="#121212")
        expl_container.pack(fill="both", expand=True, padx=15, pady=15)

        # Barra superior con controles de la pestaña de explicación
        expl_top_bar = tk.Frame(expl_container, bg="#121212")
        expl_top_bar.pack(fill="x", side="top", pady=(0, 10))

        lbl_expl_title = tk.Label(expl_top_bar, 
                                  text="Desarrollo Matemático Paso a Paso", 
                                  font=("Segoe UI", 12, "bold"), 
                                  fg="#00ADB5", 
                                  bg="#121212")
        lbl_expl_title.pack(side="left")

        self.btn_copiar_expl = tk.Button(expl_top_bar, 
                                         text="Copiar Explicación Completa 📋", 
                                         font=("Segoe UI", 9, "bold"), 
                                         fg="#FFFFFF", 
                                         bg="#00ADB5", 
                                         activebackground="#008c92", 
                                         activeforeground="#FFFFFF",
                                         relief="flat", 
                                         cursor="hand2",
                                         bd=0,
                                         padx=15,
                                         pady=5,
                                         command=self.copiar_explicacion_completa)
        self.btn_copiar_expl.pack(side="right")

        # Widget de Texto y Scrollbar para la explicación
        txt_frame = tk.Frame(expl_container, bg="#3A3A3A", bd=1)
        txt_frame.pack(fill="both", expand=True)

        scrollbar_y = tk.Scrollbar(txt_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        self.txt_explicacion = tk.Text(txt_frame, 
                                      bg="#1E1E1E", 
                                      fg="#EEEEEE", 
                                      insertbackground="#FFFFFF", 
                                      font=("Consolas", 10), 
                                      bd=0, 
                                      wrap="none",  # Evita romper alineaciones de tablas
                                      yscrollcommand=scrollbar_y.set)
        self.txt_explicacion.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar_y.config(command=self.txt_explicacion.yview)

        # Scrollbar horizontal para no romper el formato de divisiones sucesivas
        scrollbar_x = tk.Scrollbar(expl_container, orient="horizontal")
        scrollbar_x.pack(fill="x", side="bottom")
        self.txt_explicacion.config(xscrollcommand=scrollbar_x.set)
        scrollbar_x.config(command=self.txt_explicacion.xview)

        # Mensaje por defecto en el visor de explicaciones
        self.actualizar_visor_explicacion("Realiza una conversión en la pestaña 'Conversor' para generar el proceso detallado.")

    def configurar_eventos(self):
        self.root.bind("<Return>", lambda event: self.ejecutar_conversion())
        self.listbox_historial.bind("<Double-Button-1>", self.cargar_desde_historial)

    def ejecutar_conversion(self):
        self.mostrar_mensaje("", es_error=False)

        num_original = self.entry_numero.get()
        base_origen = self.combo_base.get()

        es_valido, error_msg = NumberConverter.validar(num_original, base_origen)
        if not es_valido:
            self.mostrar_mensaje(error_msg, es_error=True)
            return

        num_limpio = NumberConverter.limpiar_entrada(num_original)

        try:
            # 1. Realizar conversión matemática
            resultados = NumberConverter.convertir(num_limpio, base_origen)
            
            for base, valor in resultados.items():
                if base == "Bits":
                    continue
                entry = self.salidas[base]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, valor)
                entry.config(state="readonly")

            self.lbl_binario.config(text=f"Binario ({resultados['Bits']} bits):")
            
            # 2. Generar explicación y cargar en la segunda pestaña
            explicacion_texto = NumberConverter.explicar_proceso(num_limpio, base_origen)
            self.actualizar_visor_explicacion(explicacion_texto)

            # 3. Guardar en Historial
            descripcion_historial = f"{base_origen}: {num_limpio} -> Bin:{resultados['Binario']} | Hex:{resultados['Hexadecimal']}"
            if not self.historial_datos or self.historial_datos[-1]["descripcion"] != descripcion_historial:
                historial_item = {
                    "descripcion": descripcion_historial,
                    "numero": num_limpio,
                    "base": base_origen
                }
                self.historial_datos.append(historial_item)
                self.listbox_historial.insert(tk.END, descripcion_historial)
                self.listbox_historial.see(tk.END)

            self.mostrar_mensaje("¡Conversión exitosa! El procedimiento paso a paso está en la pestaña 'Explicación del Proceso'.", es_error=False, es_exito=True)

        except Exception as e:
            self.mostrar_mensaje(f"Error inesperado al convertir: {str(e)}", es_error=True)

    def actualizar_visor_explicacion(self, texto: str):
        """
        Actualiza el contenido del widget de texto de explicación de manera segura.
        """
        self.txt_explicacion.config(state="normal")
        self.txt_explicacion.delete("1.0", tk.END)
        self.txt_explicacion.insert("1.0", texto)
        self.txt_explicacion.config(state="disabled")

    def copiar_resultado(self, base_key: str):
        entry = self.salidas[base_key]
        valor = entry.get()
        
        if not valor:
            self.mostrar_mensaje("No hay ningún resultado para copiar.", es_error=True)
            return

        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(valor)
            self.mostrar_mensaje(f"¡Copiado el valor de {base_key} ({valor}) al portapapeles!", es_error=False, es_exito=True)
        except Exception as e:
            self.mostrar_mensaje(f"Error al copiar al portapapeles: {str(e)}", es_error=True)

    def copiar_explicacion_completa(self):
        contenido = self.txt_explicacion.get("1.0", tk.END).strip()
        
        if not contenido or contenido.startswith("Realiza una conversión"):
            self.mostrar_mensaje("No hay ninguna explicación generada para copiar.", es_error=True)
            return

        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(contenido)
            self.mostrar_mensaje("¡Explicación matemática completa copiada al portapapeles!", es_error=False, es_exito=True)
        except Exception as e:
            self.mostrar_mensaje(f"Error al copiar al portapapeles: {str(e)}", es_error=True)

    def limpiar_campos(self):
        self.entry_numero.delete(0, tk.END)
        for entry in self.salidas.values():
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.config(state="readonly")
        
        self.lbl_binario.config(text="Binario:")
        self.actualizar_visor_explicacion("Realiza una conversión en la pestaña 'Conversor' para generar el proceso detallado.")
        self.mostrar_mensaje("Campos listos.", es_error=False)
        self.entry_numero.focus()

    def limpiar_historial(self):
        self.historial_datos.clear()
        self.listbox_historial.delete(0, tk.END)
        self.mostrar_mensaje("Historial borrado.", es_error=False)

    def cargar_desde_historial(self, event):
        seleccion = self.listbox_historial.curselection()
        if not seleccion:
            return
        
        indice = seleccion[0]
        if 0 <= indice < len(self.historial_datos):
            item = self.historial_datos[indice]
            self.entry_numero.delete(0, tk.END)
            self.entry_numero.insert(0, item["numero"])
            self.combo_base.set(item["base"])
            self.ejecutar_conversion()

    def mostrar_mensaje(self, mensaje: str, es_error: bool = False, es_exito: bool = False):
        """
        Muestra un mensaje informativo, de éxito o de error en la barra de estado inferior.
        """
        self.lbl_estado.config(text=mensaje)
        if es_error:
            self.lbl_estado.config(fg="#FF7675")
        elif es_exito:
            self.lbl_estado.config(fg="#55EFC4")
        else:
            self.lbl_estado.config(fg="#A0A0A0")
