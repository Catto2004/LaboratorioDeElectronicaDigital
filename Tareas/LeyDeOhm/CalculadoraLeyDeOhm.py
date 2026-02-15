# Laboratorio de Electronica Digital: Calculadora de Ley de Ohm by JDRB
# Codigo Principal

# ############ Importaciones ############
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Input, Button, Static, Label, Footer, Header
from textual.reactive import reactive
import os

import tcss

os.system("cls")

# ################## Aplicación ##################
class CalculadoraLeyDeOhm(App):
    """
    Aplicación basada en Textual para calcular el valor faltante en la Ley de Ohm (V = I * R).
    Permite ingresar dos de los tres valores (Voltaje, Corriente, Resistencia) y calcula el tercero.
    """

    # ################## Declaración De Variables
    CSS = tcss.CSS
    TITLE = "Ω - Calculadora de Ley de Ohm - Ω"
    BINDINGS = [("^q", "quit", "Salir"),        # Cerrar la aplicación
                ("^c", "clear", "Limpiar"),     # Limpiar los campos
                ("^s", "solve", "Calcular")]    # Calcular el valor faltante
    Voltaje = reactive(0)                       # Voltaje (V)
    Corriente = reactive(0)                     # Corriente (I)
    Resistencia = reactive(0)                   # Resistencia (R)

    def on_mount(self) -> None:
        self.theme = "flexoki"
        self.notify("Bienvenido a la Calculadora de Ley de Ohm. Ingrese dos valores para calcular el tercero.", severity="information")

    # ################## Interface
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with Vertical(id="PanelPrincipal"):
            yield Label("Calculadora de Ley de Ohm", id="Titulo")
            yield Input(placeholder="Voltaje (V)", id="InputVoltaje")
            yield Label("", id="Espacio1")
            yield Input(placeholder="Corriente (I)", id="InputCorriente")
            yield Label("", id="Espacio2")
            yield Input(placeholder="Resistencia (R)", id="InputResistencia")
            yield Label("", id="Espacio3")
            yield Button("Calcular", id="BotonCalcular")

    # ################## Manejo de Botones
    def on_button_pressed(self, event: Button.Pressed) -> None:
        boton = event.button
        if boton.id == "BotonCalcular":
            self.action_solve()

    # ################## Manejo de Acciones
    def action_clear(self) -> None: # Limpiar los campos de entrada
        self.query_one("#InputVoltaje", Input).value = ""
        self.query_one("#InputCorriente", Input).value = ""
        self.query_one("#InputResistencia", Input).value = ""
        self.notify("Campos limpiados.", severity="success")

    def action_solve(self) -> None: # Calcular el valor faltante usando la Ley de Ohm
        try:
            V = self.query_one("#InputVoltaje", Input).value
            I = self.query_one("#InputCorriente", Input).value
            R = self.query_one("#InputResistencia", Input).value

            # Convertir a float o mantener como None si no se ingresó
            V = float(V) if V and V != "Voltaje (V)" else None
            I = float(I) if I and I != "Corriente (I)" else None
            R = float(R) if R and R != "Resistencia (R)" else None

            # Calcular el valor faltante usando la Ley de Ohm
            if V is not None and I is not None: # Calcular R
                R = V / I
                self.query_one("#InputResistencia", Input).value = f"{R:.2f}"
                self.notify(f"Resistencia calculada: {R:.2f} Ω", severity="information")
            elif V is not None and R is not None: # Calcular I
                I = V / R
                self.query_one("#InputCorriente", Input).value = f"{I:.2f}"
                self.notify(f"Corriente calculada: {I:.2f} A", severity="information")
            elif I is not None and R is not None: # Calcular V
                V = I * R
                self.query_one("#InputVoltaje", Input).value = f"{V:.2f}"
                self.notify(f"Voltaje calculado: {V:.2f} V", severity="information")
            else:
                self.notify("Por favor, ingrese al menos dos valores para calcular el tercero.", severity="error")
                
        except ValueError as e:
            # Mostrar un mensaje de error en caso de entrada inválida
            self.push_screen(Static(str(e), id="ErrorMensaje"))
    
# ################## Ejecución ##################
if __name__ == "__main__":
    app = CalculadoraLeyDeOhm()
    app.run()