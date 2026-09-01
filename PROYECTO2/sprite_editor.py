"""
Editor de Sprites (8x8 bits) con Flet
--------------------------------------
Proyecto: Electrónica Digital - Ingeniería de Sistemas

Convierte una cuadrícula de 64 píxeles (8x8) hacia/desde un código
hexadecimal de 16 caracteres, pasando siempre por una cadena binaria
intermedia de 64 bits.
"""

import flet as ft

FILAS = 8
COLUMNAS = 8
TOTAL_PIXELES = FILAS * COLUMNAS  # 64

COLOR_APAGADO = "#2b2b2b"   # gris oscuro
COLOR_ENCENDIDO = "#39d353"  # verde brillante


def main(page: ft.Page):
    page.title = "Editor de Sprites 8x8"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 480
    page.window.height = 750
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Estado interno: 64 valores booleanos, uno por píxel (False = apagado)
    estado_pixeles = [False] * TOTAL_PIXELES

    # Referencias a los contenedores visuales de cada píxel
    contenedores_pixeles: list[ft.Container] = []

    # ---------- Fase 3: de la cuadrícula al código hexadecimal ----------
    def actualizar_hex_desde_pixeles():
        """Recorre los 64 píxeles, arma la cadena binaria y la convierte a hex."""
        cadena_binaria = "".join(
            "1" if encendido else "0" for encendido in estado_pixeles
        )
        # 64 bits -> 16 caracteres hexadecimales
        valor_hex = f"{int(cadena_binaria, 2):016X}"
        texto_hex.value = valor_hex
        page.update()

    # ---------- Fase 2: manejo del clic en cada píxel ----------
    def pixel_clicado(e):
        indice = e.control.data  # guardamos el índice del píxel en 'data'
        estado_pixeles[indice] = not estado_pixeles[indice]
        e.control.bgcolor = COLOR_ENCENDIDO if estado_pixeles[indice] else COLOR_APAGADO
        actualizar_hex_desde_pixeles()

    # ---------- Construcción de la cuadrícula (Fase 1) ----------
    grid = ft.GridView(
        expand=False,
        runs_count=COLUMNAS,
        max_extent=45,
        child_aspect_ratio=1.0,
        spacing=3,
        run_spacing=3,
        width=8 * 48,
        height=8 * 48,
    )

    # Bucle anidado: filas x columnas, como pide la guía
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            indice = fila * COLUMNAS + columna
            pixel = ft.Container(
                width=40,
                height=40,
                bgcolor=COLOR_APAGADO,
                border_radius=4,
                data=indice,
                on_click=pixel_clicado,
            )
            contenedores_pixeles.append(pixel)
            grid.controls.append(pixel)

    # ---------- Fase 4: de código hexadecimal a la cuadrícula ----------
    def cargar_hex(e):
        entrada = campo_hex.value.strip().upper()

        # Validación: máximo 16 caracteres hexadecimales válidos (no exige exactos 16)
        if len(entrada) == 0 or len(entrada) > 16 or not all(c in "0123456789ABCDEF" for c in entrada):
            mensaje_error.value = "Debe ingresar máximo 16 caracteres hexadecimales (0-9, A-F)."
            page.update()
            return

        mensaje_error.value = ""

        # Hex -> binario de 64 bits, rellenando ceros a la izquierda si es necesario
        cadena_binaria = f"{int(entrada, 16):064b}"

        for i in range(TOTAL_PIXELES):
            encendido = cadena_binaria[i] == "1"
            estado_pixeles[i] = encendido
            contenedores_pixeles[i].bgcolor = COLOR_ENCENDIDO if encendido else COLOR_APAGADO

        texto_hex.value = f"{int(entrada, 16):016X}"
        page.update()

    def limpiar_todo(e):
        for i in range(TOTAL_PIXELES):
            estado_pixeles[i] = False
            contenedores_pixeles[i].bgcolor = COLOR_APAGADO
        campo_hex.value = ""
        mensaje_error.value = ""
        actualizar_hex_desde_pixeles()

    # ---------- Controles de texto y entrada ----------
    campo_hex = ft.TextField(
        label="Código Hex (máx. 16 caracteres)",
        max_length=16,
        width=280,
    )

    boton_cargar = ft.ElevatedButton(
        "Cargar Hex",
        icon=ft.Icons.UPLOAD,
        on_click=cargar_hex,
    )

    boton_limpiar = ft.FilledButton(
        "Limpiar",
        icon=ft.Icons.DELETE_OUTLINE,
        on_click=limpiar_todo,
    )

    texto_hex = ft.Text(
        value="0000000000000000",
        size=26,
        weight=ft.FontWeight.BOLD,
        font_family="Consolas",
    )

    mensaje_error = ft.Text(value="", color=ft.Colors.RED_400, size=12)

    # ---------- Layout final ----------
    page.add(
        ft.Text("Editor de Sprites 8x8", size=22, weight=ft.FontWeight.BOLD),
        ft.Text("Haz clic en los píxeles para dibujar tu sprite", size=12, italic=True),
        ft.Container(content=grid, alignment=ft.Alignment.CENTER),
        ft.Divider(),
        ft.Text("Valor hexadecimal actual:", size=14),
        texto_hex,
        ft.Row(
            controls=[campo_hex, boton_cargar],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        mensaje_error,
        ft.Row(controls=[boton_limpiar], alignment=ft.MainAxisAlignment.CENTER),
    )


if __name__ == "__main__":
    ft.run(main)