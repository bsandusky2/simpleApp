# app.py
from shiny import App, ui, render

app_ui = ui.page_fluid(
    ui.input_numeric("number", "Enter a number", value=1),
    ui.output_text("result")
)

def server(input, output, session):
    @output
    @render.text
    def result():
        return f"The square is: {input.number() ** 2}"

app = App(app_ui, server)
