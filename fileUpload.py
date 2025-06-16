from shiny import App, ui, render, reactive
import pandas as pd
from io import BytesIO

app_ui = ui.page_fluid(
    ui.h2("Excel Upload & Download App"),
    ui.input_file("file", "Upload an Excel file (.xlsx)", accept=[".xlsx"]),
    ui.output_table("preview"),
    ui.download_button("download", "Download Processed Excel"),
    ui.output_text("error_msg"),
)

def server(input, output, session):
    @reactive.Calc
    def uploaded_df():
        file = input.file()
        if not file:
            return None
        try:
            return pd.read_excel(file[0]["datapath"], engine="openpyxl")
        except Exception as e:
            # Save error message to reactive output
            session._outputs["error_msg"].set(str(e))
            return None

    @output
    @render.table
    def preview():
        df = uploaded_df()
        if df is None:
            return None
        return df.iloc[:5, :5]

    @session.download(filename="processed.xlsx")
    def download():
        df = uploaded_df()
        if df is None:
            return None

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Sheet1", index=False)
        buffer.seek(0)
        return buffer.read()

app = App(app_ui, server)
