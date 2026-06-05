# Conversor de Sistemas Numéricos

Este es un programa de escritorio desarrollado en Python utilizando la biblioteca gráfica nativa `tkinter`. Su objetivo principal es servir como una herramienta educativa y práctica para estudiantes y profesionales en **Informática, Electrónica Digital y Arquitectura de Computadoras**, facilitando la conversión rápida de números entre diferentes bases.

## Características

* **Soporte Multibase**: Convierte entre Binario (Base 2), Octal (Base 8), Decimal (Base 10) y Hexadecimal (Base 16).
* **Validación en Tiempo Real**: Valida si los caracteres son aptos para la base seleccionada antes de realizar la conversión y muestra errores amigables (ej: ingresar un `9` en octal o una `G` en hexadecimal).
* **Tema Oscuro Profesional**: Interfaz limpia, plana (flat design) y moderna, optimizada para reducir la fatiga visual.
* **Copiado al Portapapeles**: Botones individuales para copiar rápidamente cada resultado con un solo clic.
* **Historial de Conversiones**: Mantiene un registro de las conversiones de la sesión. Permite volver a cargar una conversión previa haciendo doble clic en el historial.
* **Conteo de Bits**: Muestra automáticamente la cantidad de bits del resultado binario.
* **Fácil de Usar**: Permite realizar la conversión simplemente presionando la tecla `Enter`.

## Estructura del Código

La aplicación sigue principios de programación orientada a objetos (POO) y separa la lógica de la interfaz gráfica:

1. `converter.py`: Contiene la lógica matemática, funciones de validación de caracteres (expresiones regulares) y limpieza de entradas.
2. `gui.py`: Define el diseño de la interfaz de usuario, los estilos modernos y los enlaces de eventos de la aplicación.
3. `main.py`: Punto de entrada principal que inicializa y arranca la interfaz gráfica.

## Cómo Ejecutar

Para ejecutar el conversor, asegúrate de tener Python 3 instalado y corre el siguiente comando en la terminal:

```bash
python main.py
```
