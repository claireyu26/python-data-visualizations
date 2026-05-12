from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv("Invasive_Species.csv")

DATE_COL = "ObservationDate"
SPECIES_COL = "InvasiveName"
LOCATION_COL = "Town"
AREA_COL = "InfestedArea"

df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")

df = df.dropna(subset=[DATE_COL])

locations = sorted(df[LOCATION_COL].dropna().unique())

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("Invasive Species Dashboard", style={"textAlign": "center"}),

        html.Label("Select a Town:"),
        dcc.Dropdown(
            id="town-dropdown",
            options=[{"label": loc, "value": loc} for loc in locations],
            value=locations[0],
            clearable=False
        ),

        html.Br(),

        dcc.Graph(id="species-bar-chart"),
        dcc.Graph(id="time-line-chart"),
    ]
)

@app.callback(
    Output("species-bar-chart", "figure"),
    Input("town-dropdown", "value")
)
def update_species_chart(town):
    dff = df[df[LOCATION_COL] == town]

    species_area = (
        dff.groupby(SPECIES_COL)[AREA_COL]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        species_area,
        x=SPECIES_COL,
        y=AREA_COL,
        title=f"Total Infestation by Species in {town}",
        hover_data=[AREA_COL]
    )

    fig.update_layout(
        xaxis_title="Species",
        yaxis_title="Infested Area"
    )

    return fig

# line chart, infestation trend over time
@app.callback(
    Output("time-line-chart", "figure"),
    Input("town-dropdown", "value")
)
def update_time_chart(town):
    dff = df[df[LOCATION_COL] == town]

    time_series = (
        dff.groupby(DATE_COL)[AREA_COL]
        .sum()
        .reset_index()
        .sort_values(DATE_COL)
    )

    fig = px.line(
        time_series,
        x=DATE_COL,
        y=AREA_COL,
        markers=True,
        title=f"Infestation Over Time in {town}",
        hover_data=[AREA_COL]
    )

    fig.update_layout(
        xaxis_title="Date Observed",
        yaxis_title="Infested Area"
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)