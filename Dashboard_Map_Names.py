from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

#configure credentials for engine
engine = create_engine('postgresql://postgres:(password)@(Name):(Port)/(Name db)')
df = pd.read_sql_query('Select "Name", "State", Sum("Count") as "Count" '
                       'from "StateNames" '
                       'Where "Name" in (SELECT "Name" from "StateNames"'
                       ' Group by "Name" Order by Sum("Count") desc Limit 10) '
                       'Group by "Name", "State";', engine)

df_Names = df['Name'].drop_duplicates()

app = Dash(__name__)

# # ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Dashboard - TOP 10 NAMES", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_name",
                 options=[{'label': i, 'value': i} for i in df_Names.values],
                 multi=False,
                 value="David",
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_map', component_property='figure')],
    [Input(component_id='slct_name', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The name chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Name"] == option_slctd]

    #
    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='State',
        scope="usa",
        color='Count',
        hover_data=['State', 'Count'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        # labels={'****': '% !!!!!!'},
        template='plotly_dark'
    )
    #
    # Plotly Graph Objects (GO)
    fig = go.Figure(
        data=[go.Choropleth(
            locationmode='USA-states',
            locations=dff['State'],
            z=dff["Count"].astype(float),
            colorscale='Reds',
        )]
    )

    fig.update_layout(
        title_text="Babies USA",
        title_xanchor="center",
        title_font=dict(size=24),
        title_x=0.5,
        geo=dict(scope='usa'),
    )

    return container, fig


# # ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
