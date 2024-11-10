import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Button("Toggle Modal", id="button"),
        dbc.Modal(
            [
                dbc.ModalHeader("This modal's content is really high!"),
                dbc.ModalBody(
                    html.Div(
                        "Hi "*10000
                    )
                ),
            ],
            id="modal",
            scrollable=True,
        ),
    ],
    className="p-5",
)


@app.callback(
    Output("modal", "is_open"),
    [Input("button", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)
