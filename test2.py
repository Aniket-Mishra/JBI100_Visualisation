from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

index_layout = html.Div(
    [
        html.H1("Welcome to the Multi-Page App Demo"),
        html.A("Go to Page 1", href="/page-1", target="_blank"),
        html.Br(),
        html.A("Go to Page 2", href="/page-2", target="_blank"),
    ]
)

page_1_layout = html.Div(
    [
        html.H1("Page 1"),
        html.P("This is the content of Page 1."),
        html.Br(),
        html.A("Go to Page 2", href="/page-2", target="_blank"),
        html.Br(),
        html.A("Go back to home", href="/", target="_blank"),
    ]
)

page_2_layout = html.Div(
    [
        html.H1("Page 2"),
        html.P("This is the content of Page 2."),
        html.Br(),
        html.A("Go to Page 1", href="/page-1", target="_blank"),
        html.Br(),
        html.A("Go back to home", href="/", target="_blank"),
    ]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/page-1":
        return page_1_layout
    elif pathname == "/page-2":
        return page_2_layout
    else:
        return index_layout


if __name__ == "__main__":
    app.run_server(debug=False)
