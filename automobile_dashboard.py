"""
Final Assignment Part 2: Create Dashboard using Plotly and Dash
-----------------------------------------------------------------
Analyzing the Impact of Recession on Automobile Sales — XYZAutomotives

Run with:  python automobile_dashboard.py
Then open the URL printed in the terminal (usually http://127.0.0.1:8050).
"""

import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
# Replace this URL/path with the exact dataset link given in your lab
# instructions if it differs from the one below.
URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/"
    "historical_automobile_sales.csv"
)
data = pd.read_csv(URL)

# ---------------------------------------------------------------------------
# TASK 2.1: Create a Dash application and give it a meaningful title
# ---------------------------------------------------------------------------
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

# ---------------------------------------------------------------------------
# TASK 2.2: Add drop-down menus with appropriate titles and options
# ---------------------------------------------------------------------------
dropdown_options = [
    {"label": "Yearly Statistics", "value": "Yearly Statistics"},
    {"label": "Recession Period Statistics", "value": "Recession Period Statistics"},
]

year_list = [i for i in range(data["Year"].min(), data["Year"].max() + 1)]

app.layout = html.Div(
    [
        html.H1(
            "Automobile Sales Statistics Dashboard",
            style={"textAlign": "center", "color": "#503D36", "fontSize": 28},
        ),
        html.Div(
            [
                html.Label("Select Statistics:"),
                dcc.Dropdown(
                    id="dropdown-statistics",
                    options=dropdown_options,
                    value="Yearly Statistics",
                    placeholder="Select a report type",
                    style={"width": "80%", "padding": "3px", "fontSize": "20px"},
                ),
            ],
            style={"width": "48%", "margin": "auto"},
        ),
        html.Div(
            dcc.Dropdown(
                id="select-year",
                options=[{"label": i, "value": i} for i in year_list],
                value=year_list[-1],
                placeholder="Select a year",
                style={"width": "60%", "padding": "3px", "fontSize": "20px"},
            ),
            id="select-year-div",
            style={"width": "48%", "margin": "auto", "marginTop": "10px"},
        ),
        # -------------------------------------------------------------
        # TASK 2.3: Division for output display with id and className
        # -------------------------------------------------------------
        html.Div(
            id="output-container",
            className="chart-grid",
            style={
                "display": "flex",
                "flexDirection": "column",
                "marginTop": "20px",
            },
        ),
    ]
)


# ---------------------------------------------------------------------------
# TASK 2.4: Callback to update the input container based on the selected
# statistics type (disable the Year dropdown unless "Yearly Statistics"
# is selected).
# ---------------------------------------------------------------------------
@app.callback(Output("select-year", "disabled"), Input("dropdown-statistics", "value"))
def update_input_container(selected_statistics):
    return selected_statistics != "Yearly Statistics"


# ---------------------------------------------------------------------------
# Main callback that builds and returns the output graphs
# ---------------------------------------------------------------------------
@app.callback(
    Output("output-container", "children"),
    [Input("dropdown-statistics", "value"), Input("select-year", "value")],
)
def update_output_container(selected_statistics, input_year):

    # -----------------------------------------------------------------
    # TASK 2.5: Graphs for Recession Report Statistics
    # -----------------------------------------------------------------
    if selected_statistics == "Recession Period Statistics":
        recession_data = data[data["Recession"] == 1]

        # Plot 1: Average automobile sales fluctuation over the recession period
        yearly_rec = recession_data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                title="Average Automobile Sales Fluctuation over Recession Period",
            )
        )

        # Plot 2: Average number of vehicles sold by vehicle type during recession
        avg_sales = recession_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index()
        chart2 = dcc.Graph(
            figure=px.bar(
                avg_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title="Average Vehicles Sold by Vehicle Type during Recession",
            )
        )

        # Plot 3: Total advertisement expenditure share by vehicle type
        exp_rec = recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"].sum().reset_index()
        chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Total Advertisement Expenditure Share by Vehicle Type during Recession",
            )
        )

        # Plot 4: Effect of unemployment rate on vehicle type and sales
        unemp_data = (
            recession_data.groupby(["unemployment_rate", "Vehicle_Type"])["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x="unemployment_rate",
                y="Automobile_Sales",
                color="Vehicle_Type",
                labels={
                    "unemployment_rate": "Unemployment Rate",
                    "Automobile_Sales": "Average Automobile Sales",
                },
                title="Effect of Unemployment Rate on Vehicle Type and Sales",
            )
        )

        return [
            html.Div(
                className="chart-item",
                children=[
                    html.Div(children=chart1, style={"width": "48%"}),
                    html.Div(children=chart2, style={"width": "48%"}),
                ],
                style={"display": "flex", "justifyContent": "space-around"},
            ),
            html.Div(
                className="chart-item",
                children=[
                    html.Div(children=chart3, style={"width": "48%"}),
                    html.Div(children=chart4, style={"width": "48%"}),
                ],
                style={"display": "flex", "justifyContent": "space-around"},
            ),
        ]

    # -----------------------------------------------------------------
    # TASK 2.6: Graphs for Yearly Report Statistics
    # -----------------------------------------------------------------
    elif input_year and selected_statistics == "Yearly Statistics":
        yearly_data = data[data["Year"] == input_year]

        # Plot 1: Yearly average automobile sales across the whole dataset
        yas = data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        chart1 = dcc.Graph(
            figure=px.line(yas, x="Year", y="Automobile_Sales", title="Yearly Average Automobile Sales")
        )

        # Plot 2: Total monthly automobile sales for the selected year
        mas = yearly_data.groupby("Month")["Automobile_Sales"].sum().reset_index()
        chart2 = dcc.Graph(
            figure=px.line(
                mas, x="Month", y="Automobile_Sales", title=f"Total Monthly Automobile Sales in {input_year}"
            )
        )

        # Plot 3: Average vehicles sold by vehicle type in the selected year
        avr_vdata = yearly_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index()
        chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title=f"Average Vehicles Sold by Vehicle Type in {input_year}",
            )
        )

        # Plot 4: Total advertisement expenditure by vehicle type in the selected year
        exp_data = yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"].sum().reset_index()
        chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title=f"Total Advertisement Expenditure by Vehicle Type in {input_year}",
            )
        )

        return [
            html.Div(
                className="chart-item",
                children=[
                    html.Div(children=chart1, style={"width": "48%"}),
                    html.Div(children=chart2, style={"width": "48%"}),
                ],
                style={"display": "flex", "justifyContent": "space-around"},
            ),
            html.Div(
                className="chart-item",
                children=[
                    html.Div(children=chart3, style={"width": "48%"}),
                    html.Div(children=chart4, style={"width": "48%"}),
                ],
                style={"display": "flex", "justifyContent": "space-around"},
            ),
        ]

    else:
        return None


# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
