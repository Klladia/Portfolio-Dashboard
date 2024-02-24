from dash import dcc, html, Dash, dash_table, callback, clientside_callback
from dash.dependencies import Output, Input, State

from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import webbrowser


#2022
excel_2022 = pd.read_excel(r"/content/exemplary2022.xlsx") 
excel_2022.replace('\xa0', np.nan, inplace=True)
excel_2022['Rating'].fillna('Not Rated', inplace=True)
excel_2022['Moodys_Rating'].fillna('Not Rated', inplace=True)
excel_2022['Risk_Color'].fillna('Not Flagged', inplace=True)
excel_2022['Year'] = '2022'

#2021
excel_2021 = pd.read_excel(r"/content/exemplary2021.xlsx")
excel_2021['Year'] = '2021'

#2020
excel_2020 = pd.read_excel(r"/content/exemplary2020.xlsx")
excel_2020['Year'] = '2020'

#2019
excel_2019 = pd.read_excel(r"/content/exemplary2019.xlsx")
excel_2019['Year'] = '2019'


joint_excel = pd.concat([excel_2022, excel_2021, excel_2020, excel_2019], ignore_index=True)
joint_excel.replace('\xa0', np.nan, inplace=True)
joint_excel['Rating'].fillna('Not Rated', inplace=True)
joint_excel['Moodys_Rating'].fillna('Not Rated', inplace=True)
joint_excel['Risk_Color'].fillna('Not Flagged', inplace=True)



year_names = joint_excel['Year'].unique()


order_moodys = ['Aaa','Aa1','Aa2','Aa3','A1','A2','A3','Baa1','Baa2','Baa3','Ba1','Ba2','Ba3','B1','B2','B3','Caa2','D','Not Rated',]
order_shortmoodys = ['Aaa','Aa', 'A', 'Baa', 'Ba', 'B','Caa','D']
IR = ['1', '2+', '2', '2-', '3+', '3', '3-', '4+', '4', '4-', '5+', '5', '5-', '6+', '6', '6-', '7', '8', 'Not Rated']
IR_Rank = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19']

color_palet = ['rgb(99, 190, 123)', 'rgb(143, 202, 125)', 'rgb(188, 215, 128)', 'rgb(232, 228, 130)', 'rgb(255, 217, 129)', 'rgb(252, 180, 122)', 'rgb(250, 143, 115)', 'rgb(248, 105, 107)']

ir_to_rank = {'1': 1, '2+': 2, '2': 3, '2-': 4, '3+': 5, '3': 6, '3-': 7, '4+': 8, '4': 9, '4-': 10,
              '5+': 11, '5': 12, '5-': 13, '6+': 14, '6': 15, '6-': 16, '7': 17, '8': 18, 'Not Rated': 19}
rank_to_shortmoodys = {1: 'Aaa', 2: 'Aa', 3: 'Aa', 4: 'Aa', 5: 'A', 6: 'A', 7: 'A', 8: 'Baa', 9: 'Baa', 10: 'Baa',
    11: 'Ba', 12: 'Ba', 13: 'Ba', 14: 'B', 15: 'B', 16: 'B', 17: 'Caa', 18: 'D', 19: 'Not Rated'}
shortmoodys_to_shortIR = {'Aaa':1, 'Aa':2, 'A':3, 'Baa':4, 'Ba':5, 'B':6, 'Caa':7, 'D':8, 'Not Rated':9}


joint_excel['Rating'] = joint_excel['Rating'].astype(str)
joint_excel['IR_Rank'] = joint_excel['Rating'].map(ir_to_rank)
joint_excel['Short_Moodys'] = joint_excel['IR_Rank'].map(rank_to_shortmoodys)
joint_excel['ShortIR'] = joint_excel['Short_Moodys'].map(shortmoodys_to_shortIR)

joint_excel_filtered = pd.DataFrame()
excel_2022_filtered = pd.DataFrame()


branches = sorted(excel_2022['Risk_Branch'].unique())
industry_names = sorted(excel_2022['Industry'].unique())
industry_options = sorted(excel_2022['Industry'].unique())
country_names = sorted(excel_2022['Country'].unique())


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
load_figure_template("MINTY")


app = Dash(__name__ , external_stylesheets=[dbc.themes.MINTY, dbc_css])


app.layout = html.Div([
    dcc.Tabs(
            id="tabs",
            className="dbc",
            value="tab-1",
            style={"fontSize": 26},
            children=[
                dcc.Tab(
                    label="Portfolio Risk Profile",
                    value="tab-1",
                    children=[
                        html.Br(),
                        dbc.Card([
                            dbc.Row([
                                html.Br(),
                                html.Br(),
                                dbc.Col(html.H3("Branch", style={"font-size": "22px", "color": "#8b8b8b", "text-align": "center"}), width=4),
                                dbc.Col(html.H3("Industry", style={"font-size": "22px", "color": "#8b8b8b", "text-align": "center"}), width=4),
                                dbc.Col(html.H3("Country", style={"font-size": "22px", "color": "#8b8b8b", "text-align": "center"}), width=4),]),

                            dbc.Row([

                                dbc.Col([
                                    dcc.Checklist(
                                        id="branch-checklist",
                                        options=branches,
                                        value=branches,
                                        labelStyle={'display': 'block', 'margin': 10},
                                        style={'border':'2px solid #A1D6C7',
                                               "marginBottom": 10,
                                               "height": "120px",
                                               "background-color": "white",
                                               "border-radius": "5px"}),
                                     ],width = 4),
                                dbc.Col([
                                     dcc.Checklist(
                                        id="industry-checklist",
                                        value=industry_options,
                                        options= industry_options,
                                        labelStyle={'display': 'block', 'margin': 10},
                                        style={'border':'2px solid #A1D6C7',
                                               "marginBottom": 10,
                                               "height": "120px",
                                               "overflowY": "scroll",
                                               "background-color": "white",
                                               "border-radius": "5px"}),
                                     html.Button("Select All", id="select-all-industry-checklist", style={"border": "2px solid #A1D6C7", "border-radius": "5px"})],width = 4),

                                dbc.Col([
                                     dcc.Checklist(
                                        id="country-name",
                                        value= country_names,
                                        options= country_names,
                                        labelStyle={'display': 'block', 'margin': 10},
                                        style={'border':'2px solid #A1D6C7',
                                               "marginBottom": 10,
                                               "height": "120px",
                                               "overflowY": "scroll",
                                               "background-color": "white",
                                               "border-radius": "5px"}),
                                    html.Button("Select All", id="select-all-country", style={"border": "2px solid #A1D6C7", "border-radius": "5px"})],width = 4)

                            ]),
                                ],

                            style={"padding": "20px", "background-color": "rgb(231, 245, 241)", 'margin': '25px'},

                        ),
                        html.Br(),
                        dbc.Row(dbc.Card(dcc.Markdown("###  &nbsp;PORTFOLIO RISK PROFILE"),
                                        style={'width': '95%', 'background-color': '#B8E0D5', 'border-radius': '5'}),
                                justify="center",
                                align="center"),
                        html.Br(),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                     dcc.Markdown(f"### Current Portfolio Date: **{year_names[0]}**",
                                                 style={'fontSize': '20px', "text-align": "center", "border-radius": "5"},
                                                ),
                                     dcc.Markdown(id='exposure-value', style={'fontSize': '20px', "text-align": "center", "border-radius": "5"}),
                                     html.Br(),
                                     dcc.Graph(id="fig-av-rating"),
                                    ], width=5),
                            dbc.Col(dcc.Graph(id="fig-exp", style={"height": "100%"}), width=7),
                        ]),
                        html.Br(),
                        dbc.Row(
                            [dbc.Col(dcc.Graph(id="gauge-ptf"),width=4
                                    ),

                             dbc.Col(dcc.Graph(id="gauge-IG"),width=4
                                    ),

                             dbc.Col(dcc.Graph(id="gauge-flag"),width=4
                                    ),
                            ]
                        ),
                        html.Br(),
                        html.Br(),
                        dbc.Row(
                            [dbc.Col(dbc.Card(dcc.Markdown("###  &nbsp;&nbsp;Portfolio Quality"),
                                               style={'width': '90%', 'background-color': '#B8E0D5', 'border-radius': '5'}),
                                               className="text-center",

                                      style={'display': 'flex','justify-content': 'center','align-items': 'center','height': '100%', 'width': '6'},
                                    ),



                             dbc.Col(dbc.Card(dcc.Markdown("###  &nbsp;&nbsp;Rating Action Trend"),
                                              style={'width': '90%', 'background-color': '#B8E0D5', 'border-radius': '5'}),
                                              className="text-center",
                                     style={'display': 'flex','justify-content': 'center','align-items': 'center','height': '100%', 'width': '3'},
                                    ),
                            ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col(dcc.Graph(id="ptf-portfolio", style={"background-color": "white"}), width = 6),
                            dbc.Col(dcc.Graph(id="rating-change", style={"background-color": "white"}), width = 6)
                        ]),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        dbc.Row(
                            [dbc.Col(dbc.Card(dcc.Markdown("###  &nbsp;&nbsp;Exposure by Industry"),
                                               style={'width': '90%', 'background-color': '#B8E0D5', 'border-radius': '5'}),
                                               className="text-center",

                                      style={'display': 'flex','justify-content': 'center','align-items': 'center','height': '100%'},
                                    ),

                             dbc.Col(dbc.Card(dcc.Markdown("###  &nbsp;&nbsp;Exposure by Country"),
                                              style={'width': '90%', 'background-color': '#B8E0D5', 'border-radius': '5'}),
                                              className="text-center",
                                     style={'display': 'flex','justify-content': 'center','align-items': 'center','height': '100%'},
                                    ),

                             dbc.Col(dbc.Card(dcc.Markdown("###  &nbsp;&nbsp;Exposure by Branch"),
                                              style={'width': '90%', 'background-color': '#B8E0D5', 'border-radius': '5'}),
                                              className="text-center",
                                     style={'display': 'flex','justify-content': 'center','align-items': 'center','height': '100%'},
                                    ),
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [dbc.Col(dcc.Graph(id="pie-industry"),width=4
                                    ),

                             dbc.Col(dcc.Graph(id="pie-country"),width=4
                                    ),

                             dbc.Col(dcc.Graph(id="pie-branch"),width=4
                                    ),
                            ]
                        ),
                        ]
                        ),



                dcc.Tab(
                    label="Flagged and Rating Profile",
                    value="tab-2",
                    children=[
                        html.Div(id='merged_div', style={'display': 'none'}),
                        html.Br(),
                        html.Br(),
                        dbc.Row(dbc.Card(dcc.Markdown("###  &nbsp;PROFILE"),
                                        style={'width': '95%', 'background-color': '#B8E0D5', 'border-radius': '5'}),
                                justify="center",
                                align="center"),
                        html.Br(),
                        dbc.Row(
                            [dbc.Col(dbc.Card(dcc.Markdown(f"###  &nbsp;&nbsp;Risk Flagged in the Portfolio on {year_names[0]}"),
                                               style={'width': '90%', 'background-color': '#B8E0D5', 'border-radius': '5'}),
                                               className="text-center",

                                      style={'display': 'flex','justify-content': 'center','align-items': 'center','height': '100%', 'width': '6'},
                                    ),

                             dbc.Col(dbc.Card(dcc.Markdown("###  &nbsp;&nbsp;Trends in the Portfolio"),
                                              style={'width': '90%', 'background-color': '#B8E0D5', 'border-radius': '5'}),
                                              className="text-center",
                                     style={'display': 'flex','justify-content': 'center','align-items': 'center','height': '100%', 'width': '3'},
                                    ),
                            ]),
                        html.Br(),
                        html.Br(),
                        dbc.Row([
                            dbc.Col(dcc.Graph(id='pie-flagged'), width = 6),
                            dbc.Col(dcc.Graph(id='bar-flagged'), width = 6)
                        ]),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        dbc.Row(
                            [dbc.Col(dbc.Card(dcc.Markdown(f"###  &nbsp;&nbsp;Risk Concentration in the Portfolio by Industry on {year_names[0]}"),
                                               style={'width': '90%', 'background-color': '#B8E0D5', 'border-radius': '5'}),
                                               className="text-center",

                                      style={'display': 'flex','justify-content': 'center','align-items': 'center','height': '100%', 'width': '6'},
                                    ),



                             dbc.Col(dbc.Card(dcc.Markdown(f"###  &nbsp;&nbsp;Risk Concentration in the Portfolio by Country on {year_names[0]}"),
                                              style={'width': '90%', 'background-color': '#B8E0D5', 'border-radius': '5'}),
                                              className="text-center",
                                     style={'display': 'flex','justify-content': 'center','align-items': 'center','height': '100%', 'width': '3'},
                                    ),
                            ]),
                        html.Br(),
                        dbc.Row([dbc.Col(dcc.Graph(id="bar-con-industry"),width=6),
                                 dbc.Col(dcc.Graph(id="bar-con-country"),width=6),
                                ]),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        dbc.Row(dbc.Card(dcc.Markdown("###  &nbsp;RATING PROFILE"),
                                        style={'width': '95%', 'background-color': '#B8E0D5', 'border-radius': '5'}),
                                justify="center",
                                align="center"),
                        html.Br(),
                        html.Br(),

                        dbc.Row(
                            dbc.Col(dbc.Card(dcc.Markdown(f"###  &nbsp;&nbsp;Rating Distribution on {year_names[0]}"),
                                               style={'width': '90%', 'background-color': '#B8E0D5', 'border-radius': '5'}),
                                               className="text-center",

                                      style={'display': 'flex','justify-content': 'center','align-items': 'center','height': '100%'},
                                    ),

                            ),
                        html.Br(),
                        html.Br(),
                        dbc.Row(
                             dbc.Col(dcc.Graph(id='bar-distribution')),
                        ),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        dbc.Row(
                            [dbc.Col(dbc.Card(dcc.Markdown(f"###  &nbsp;&nbsp;Downgrades in the Portfolio by Industry on {year_names[1]}"),
                                               style={'width': '90%', 'background-color': '#B8E0D5', 'border-radius': '5'}),
                                               className="text-center",

                                      style={'display': 'flex','justify-content': 'center','align-items': 'center','height': '100%', 'width': '6'},
                                    ),



                             dbc.Col(dbc.Card(dcc.Markdown(f"###  &nbsp;&nbsp;Severity of Rating Change by Industry on {year_names[1]}"),
                                              style={'width': '90%', 'background-color': '#B8E0D5', 'border-radius': '5'}),
                                              className="text-center",
                                     style={'display': 'flex','justify-content': 'center','align-items': 'center','height': '100%', 'width': '3'},
                                    ),
                            ]),
                        html.Br(),
                        dbc.Row([dbc.Col(dcc.Graph(id="bar-downgrades"),width=6),
                                 dbc.Col(dcc.Graph(id="bar-severity"),width=6),
                                ]),
                        html.Br(),
                        html.Br(),

                    ]
                ),



                dcc.Tab(
                    label="Risk Portfolio by Country",
                    value="tab-3",
                    children=[
                        html.Br(),
                        dbc.Row(dcc.Graph(id="world-map",
                                          style={"background-color": "white", "border-radius": "5", 'height': '100vh', 'width': '100%'},
                                          clickData={'points': [{'location': 'Spain'}]}
                                         ),
                               ),
                        dcc.Store(id='scroll-pos', data=0),
                        html.Div(id='scroll-trigger', style={'display': 'none'}),
                        dbc.Row([dbc.Col(dcc.Graph(id='click-bar-exp'), width=6),
                                 dbc.Col(dcc.Graph(id='click-bar-ctp'), width=6)]),
                        html.Br(),
                        html.Br(),
                        html.Br(),

                                ]
                            ),

            ]
    )

])




# SELECT ALL BUTTONS


@app.callback(
    Output("industry-checklist", "value"),
    Input("select-all-industry-checklist", "n_clicks"),
    State("industry-checklist", "value"),
    prevent_initial_call=True)

def select_all_risk_industry(n_clicks, current_values):
    if n_clicks:
        if set(current_values) == set(industry_names):
            return []
        else:
            return industry_names

@app.callback(
    Output("country-name", "value"),
    Input("select-all-country", "n_clicks"),
    State("country-name", "value"),
    prevent_initial_call=True)

def select_all_country_name(n_clicks, current_values):
    if n_clicks:
        if set(current_values) == set(country_names):
            return []
        else:
            return country_names





@app.callback(
    [
    Output('industry-checklist', 'options'),
    Output('country-name', 'options'),
    Output('exposure-value', 'children'),
    Output("fig-av-rating", "figure"),
    Output("fig-exp", "figure"),
    Output("gauge-IG", "figure"),
    Output("gauge-ptf", "figure"),
    Output("gauge-flag", "figure"),
    Output("ptf-portfolio", "figure"),
    Output("rating-change", "figure"),
    Output("pie-industry", "figure"),
    Output("pie-country", "figure"),
    Output("pie-branch", "figure"),
    Output("pie-flagged", "figure"),
    Output("bar-flagged", "figure"),
    Output("bar-con-industry", "figure"),
    Output("bar-con-country", "figure"),
    Output("bar-distribution", "figure"),
    Output("bar-downgrades", "figure"),
    Output("bar-severity", "figure"),
    Output("world-map", "figure")],
    [
    Input("branch-checklist", "value"),
    Input("industry-checklist", "value"),
    Input("country-name", "value")],
    [
    State("industry-checklist", "options"),
    State("country-name", "options"),
    ]
)



def filtered(branch, industry, country, industry_options, country_names):
    global excel_2022_filtered
    global joint_excel_filtered

    excel_2022_filtered = excel_2022[
        (excel_2022['Risk_Branch'].isin(branch)) &
        (excel_2022['Industry'].isin(industry)) &
        (excel_2022['Country'].isin(country))
    ]


    joint_excel_filtered = joint_excel[
        (joint_excel['Risk_Branch'].isin(branch)) &
        (joint_excel['Industry'].isin(industry)) &
        (joint_excel['Country'].isin(country))
    ]

    df_filtering = joint_excel_filtered.copy()
    industry_options = sorted(df_filtering['Industry'].unique())
    country_names = sorted(df_filtering['Country'].unique())

    sum_exposure_latest = int(round(excel_2022_filtered['Borrowed'].sum(),0))

    ##################################################################################################################################################################
    ## TAB 1
    ##################################################################################################################################################################



    # EXPOSURE BY INDUSTRY


    pie_exposure = excel_2022_filtered.groupby('Industry')['Borrowed'].sum().reset_index()
    pie_exposure2 = pie_exposure.sort_values(by='Borrowed', ascending=False)


    if pie_exposure2.empty:
        fig_pie_industry = px.scatter()
        fig_pie_industry.update_layout(
            annotations=[
                dict(
                    text='No data available for Exposure by Industry',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        TotalSum = sum(pie_exposure2['Borrowed'])
        pie_exposure2.loc[:, "Total"] = ((pie_exposure2['Borrowed'] / TotalSum)*100).round(1)
        top = pie_exposure2.head(10)
        totalforindustry = top['Total'].sum()
        fig_pie_industry = px.pie(top, values='Borrowed', hole=.3, names='Industry')
        fig_pie_industry.update_traces(direction ='clockwise',
                          customdata=top['Total'],
                          texttemplate = '%{label}: <b>%{customdata:.0f}</b>%',
                          textposition='inside',
                          insidetextorientation='radial',
                          hovertemplate='<b>%{label}</b><br>Percentage Share: <b>%{customdata:.0f}</b>%',
                          marker=dict(line=dict(color='#000000', width=2)))
        fig_pie_industry.update_layout(title=f'{totalforindustry:.0f}% of the portfolio in the Top 10 Industries',
                          title_font=dict(family="Verdana", size=16),
                          title_x=0.5,
                          showlegend=False,
        )




    # EXPOSURE BY COUNTRY


    TotalSum2 = sum(excel_2022_filtered['Borrowed'])

    pie_country = excel_2022_filtered.groupby('Country')['Borrowed'].sum().reset_index()
    pie_country2 = pie_country.sort_values(by='Borrowed', ascending=False)


    if pie_country2.empty:
        fig_pie_country = px.scatter()
        fig_pie_country.update_layout(
            annotations=[
                dict(
                    text='No data available for Exposure by Country',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        pie_country2.loc[:, "Total"] = ((pie_country2['Borrowed'] / TotalSum2)*100).round(1)
        top2 = pie_country2.head(10)
        totalfortitle = top2['Total'].sum()
        fig_pie_country = px.pie(top2, values='Borrowed', hole=.3, names='Country')
        fig_pie_country.update_traces(direction ='clockwise',
                          customdata=top2['Total'],
                          texttemplate = '%{label}: <b>%{customdata:.0f}</b>%',
                          textposition='inside',
                          insidetextorientation='radial',
                          hovertemplate='<b>%{label}</b><br>Percentage Share: <b>%{customdata:.0f}</b>%',
                          marker=dict(line=dict(color='#000000', width=2)))
        fig_pie_country.update_layout(title=f'{totalfortitle:.0f}% of the portfolio in the Top 10 Countries',
                          title_font=dict(family="Verdana", size=16),
                          title_x=0.5,
                          showlegend=False,
        )






    # EXPOSURE BY BRANCH


    pie_branch = excel_2022_filtered.groupby('Risk_Branch')['Borrowed'].sum().reset_index()
    pie_branch2 = pie_branch.sort_values(by='Borrowed', ascending=False)


    if pie_branch2.empty:
        fig_pie_branch = px.scatter()
        fig_pie_branch.update_layout(
            annotations=[
                dict(
                    text='No data available for Exposure by Branch',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        TotalSum3 = sum(pie_branch2['Borrowed'])
        pie_branch2.loc[:, "Total"] = ((pie_branch2['Borrowed'] / TotalSum3)*100).round(1)
        fig_pie_branch = px.pie(pie_branch2, values='Borrowed', hole=.3, names='Risk_Branch')
        fig_pie_branch.update_traces(direction ='clockwise',
                          customdata=pie_branch2['Total'],
                          texttemplate = '%{label}: <b>%{customdata:.0f}</b>%',
                          textposition='inside',
                          insidetextorientation='radial',
                          hovertemplate='<b>%{label}</b><br>Percentage Share: <b>%{customdata:.0f}</b>%',
                          marker=dict(line=dict(color='#000000', width=2)))
        fig_pie_branch.update_layout(title=f'{pie_branch2.values[0][2]:.0f}% of the portfolio is in {pie_branch2.values[0][0]}',
                          title_font=dict(family="Verdana", size=16),
                          title_x=0.5,
                          showlegend=False,
        )



    # GAUGE IG/NonIG


    excel_2022_filtered['IG/nonIG'] = excel_2022_filtered['Moodys_Rating'].apply(lambda x: 'IG' if x in ['Aaa', 'Aa1', 'Aa2', 'Aa3', 'A1', 'A2', 'A3', 'Baa1', 'Baa2', 'Baa3'] else ('NonIG' if x in ['Ba1', 'Ba2', 'Ba3', 'B1', 'B2', 'B3', 'Caa1', 'Caa2', 'Caa3', 'D'] else 'Missing data'))
    IG_count = excel_2022_filtered[excel_2022_filtered['IG/nonIG'] != 'Missing data']
    IG_count = IG_count.groupby('IG/nonIG')['Borrowed'].sum().reset_index()

    IG_count['Share IG'] = (IG_count['Borrowed'][0] / (IG_count['Borrowed'][0] + IG_count['Borrowed'][1])) * 100
    IG_count['Share NonIG'] = (IG_count['Borrowed'][1] / (IG_count['Borrowed'][0] + IG_count['Borrowed'][1])) * 100

    if IG_count.empty:
        IG_value = None
    else:
        if len(IG_count['IG/nonIG'].values) > 1:
            IG_count['Share IG'] = (IG_count['Borrowed'][0] / (IG_count['Borrowed'][0] + IG_count['Borrowed'][1])) * 100
            IG_count['Share NonIG'] = (IG_count['Borrowed'][1] / (IG_count['Borrowed'][0] + IG_count['Borrowed'][1])) * 100

            IG_value = IG_count['Share IG'][0]
            NonIG_value = IG_count['Share NonIG'][0]
        else:
            if IG_count['IG/nonIG'].values[0] == "NonIG":
                IG_value = 0
            else:
                IG_value = 100


    if IG_value is None:
        gauge_IG = px.scatter()
        gauge_IG.update_layout(
            annotations=[
                dict(
                    text='No data available for IG value',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        gauge_IG = go.Figure()
        gauge_IG.add_trace(go.Indicator(
            mode = "gauge+number",
            value=IG_value,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [0, 100]},
                   'steps': [
                       {'range': [0, IG_value], 'color': "green"},
                       {'range': [IG_value, 100], 'color': "red"}]},
            number={'suffix': "%"},
        ))

        gauge_IG.add_annotation(
        text=f"IG / NonIG %",
        x=0.5,
        y=1.2,
        font=dict(size=24),
        showarrow=False)





    # GAUGE AVERAGE PORTFOLIO RATING


    av = excel_2022_filtered[excel_2022_filtered['Rating'] != 'Not Rated']
    av['Rating'] = av['Rating'].astype(str)

    av['IR_Rank'] = av['Rating'].map(ir_to_rank)
    av['Short_Moodys'] = av['IR_Rank'].map(rank_to_shortmoodys)
    av['ShortIR'] = av['Short_Moodys'].map(shortmoodys_to_shortIR)

    if av.empty:
        av_short_moodys = None
    else:
        weighted_average = (av['IR_Rank'] * av['Borrowed']).sum() / av['Borrowed'].sum()
        average_value = round(weighted_average,0)

        av_moodys = joint_excel.loc[joint_excel['IR_Rank'] == average_value, 'Moodys_Rating'].iloc[0]
        av_short_moodys = joint_excel.loc[joint_excel['IR_Rank'] == average_value, "ShortIR"].iloc[0]


    num_ranges = len(color_palet)
    steps = []
    for i in range(num_ranges):
        step = {
            'range': [i + 1, i + 2],
            'color': color_palet[i]}
        steps.append(step)


    if av_short_moodys is None:
        gauge_avg = px.scatter()
        gauge_avg.update_layout(
            annotations=[
                dict(
                    text='No data available for Average Portfolio Rating',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        gauge_avg = go.Figure(go.Indicator(
            value=av_short_moodys,
            mode="gauge",
            gauge={'axis': {'range': [1, len(order_shortmoodys)], 'tickvals': list(range(1, len(order_shortmoodys) + 1)), 'ticktext': order_shortmoodys},
                   'steps': steps},
        ))

        gauge_avg.add_annotation(
            text=av_moodys,
            x=0.5,
            y=0,
            showarrow=False,
            font=dict(size=80)
        )

        gauge_avg.add_annotation(
            text=f"Average Portfolio Rating*",
            x=0.5,
            y=1.2,
            font=dict(size=24),
            showarrow=False)
        gauge_avg.add_annotation(
            text=r"*Average over the rated universe",
            x=0.5,
            y=(-0.1),
            font=dict(size=16))
        gauge_avg.update_annotations(showarrow=False)




    # GAUGE FLAG


    flagged = excel_2022_filtered.groupby('Risk_Color')['Borrowed'].sum().reset_index()
    if flagged.empty:
        share_flagged = None
    else:
        sum_flagged = flagged[flagged['Risk_Color'] != 'Not Flagged']['Borrowed'].sum()
        notflagged_value = flagged.loc[flagged['Risk_Color'] == 'Not Flagged', 'Borrowed'].values[0]
        share_flagged = round((sum_flagged/(notflagged_value + sum_flagged))*100,1)

    if share_flagged is None:
        gauge_flag = px.scatter()
        gauge_flag.update_layout(
            annotations=[
                dict(
                    text='No data available for flagged portfolio',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        gauge_flag = go.Figure()
        gauge_flag.add_trace(go.Indicator(
            mode = "gauge+number",
            value=share_flagged,
            gauge={'axis': {'range': [0, 100], 'tickvals': [10,30,100]},
                   'steps': [
                       {'range': [0, 10], 'color': "rgb(99, 190, 123)"},
                       {'range': [10, 30], 'color': "rgb(252, 180, 122)"},
                       {'range': [30, 100], 'color': "rgb(248, 105, 107)"},
                   ]},
            number={'suffix': "%"}))

        gauge_flag.add_annotation(
        text=f"% of Portfolio Flagged",
        x=0.5,
        y=1.2,
        font=dict(size=24),
        showarrow=False)

        gauge_flag.add_annotation(
            text=f"<br>of the filtered portoflio was flagged</br>",
            x=0.5,
            y=(-0.1),
            font=dict(size=16))
        gauge_flag.update_annotations(showarrow=False)




    # PORTFOLIO QUALITY


    sum_per_year = joint_excel_filtered.groupby(['Year', 'Short_Moodys'])['Borrowed'].sum().reset_index()

    if sum_per_year.empty:
        fig_ptf_quality = px.scatter()
        fig_ptf_quality.update_layout(
            annotations=[
                dict(
                    text='No data available for Portfolio Quality',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        sum_per_year = sum_per_year[sum_per_year['Short_Moodys'] != 'Not Rated']
        total_sum = round(sum_per_year[sum_per_year['Year'] == year_names[0]]['Borrowed'].sum(),2)
        below_IG = sum_per_year[sum_per_year['Year'] == year_names[0]][sum_per_year['Short_Moodys'].isin(['Ba', 'B', 'Caa', 'D'])]
        below_sum = round(below_IG['Borrowed'].sum(),2)
        ratio_IG =  round((below_sum / total_sum) * 100,0)

        fig_ptf_quality = px.bar(
            sum_per_year,
            x="Year",
            y="Borrowed",
            color="Short_Moodys",
            category_orders={"Short_Moodys": order_shortmoodys},
            color_discrete_sequence=color_palet,
            text="Borrowed",
        )
        fig_ptf_quality.update_layout(
            title=dict(
                text=f"{ratio_IG:.0f}% of the portfolio is rated below investment grade (on {year_names[0]})",
                x=0.5),
            yaxis_title="Exposure (in millions of dollars)",
            legend=dict(
                orientation="h",
                yanchor="top",
                title=None,
                x=0.1)
        )
        fig_ptf_quality.update_traces(
            texttemplate='<b>%{text:,.0f}</b> $',
            textposition='inside',
            textangle=0,
            insidetextanchor='middle',
            hovertemplate='<br>'.join([
                'Rating: <b>%{fullData.name}</b>',
                'Exposure: <b>%{text:,.0f}</b> M$',
                "<extra></extra>"])
        )
        fig_ptf_quality.update_xaxes(title_text=None)

        overall_portfolio = sum_per_year.groupby('Year')['Borrowed'].sum().reset_index()
        for i, row in overall_portfolio.iterrows():
            fig_ptf_quality.add_trace(
                go.Scatter(
                    x=[row['Year']],
                    y=[row['Borrowed']],
                    mode='text',
                    textposition="top center",
                    text=[f'<b>{row["Borrowed"]:,.0f} $</b>'],
                    showlegend=False,
                    hoverinfo='none'
                )
            )





    # AVERAGE RATING BAR CHART


        results = []

    for year in year_names:
        av = joint_excel_filtered[joint_excel_filtered['Year'] == year]

        # weighted average
        weighted_average = (av['IR_Rank'] * av['Borrowed']).sum() / av['Borrowed'].sum()
        average_value = round(weighted_average, 0)

        av_rating = av[av['IR_Rank'] == average_value]

        if not av_rating.empty:
            av_moodys = av_rating.iloc[0]["Moodys_Rating"]
            av_short_moodys = av_rating.iloc[0]["ShortIR"]
            av_short = av_rating.iloc[0]["Short_Moodys"]

            result = {
                'Year': year,
                'Weighted Average': weighted_average,
                'AverageValue': average_value,
                'MoodyInternalRating': av_moodys,
                'ShortMoodyInternalRating': av_short_moodys,
                'Short Moodys': av_short
            }
            results.append(result)
            result_df = pd.DataFrame(results)
        else:
            result_df = None



    if result_df is None:
        fig_av_rating = px.scatter()
        fig_av_rating.update_layout(
            annotations=[
                dict(
                    text='No data available for Average Rating',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        fig_av_rating = px.bar(
            result_df,
            x="Year",
            y="Weighted Average",
            text="MoodyInternalRating",
            color="Short Moodys",
            category_orders={"Short Moodys": order_shortmoodys},
            color_discrete_sequence=color_palet,
            title="Average Portfolio Rating for Different Years"
        )

        fig_av_rating.update_xaxes(categoryorder='category ascending', title=None)
        fig_av_rating.update_traces(hovertemplate="<b>%{x}</b><br>Weighted Average: <b>%{y:.2f}</b><br>Rating: <b>%{text}</b><extra></extra>",
                                      texttemplate="<b>%{text}</b>",
                                      showlegend=False)
        fig_av_rating.update_layout(title="Average Portfolio Rating for Different Years",
                          title_font=dict(family="Verdana", size=24),
                          title_x=0.5)




    # PORTFOLIO SIZE & DEFAULT RATE RED


    # DEFAULT RATE Red

    FLAG_df = joint_excel_filtered.groupby(['Year', 'Risk_Color'])['Borrowed'].sum().reset_index()
    total_exp = FLAG_df.groupby('Year')['Borrowed'].sum().reset_index()
    total_exp.rename(columns={'Borrowed': 'Total Exposure'}, inplace=True)
    result = FLAG_df.merge(total_exp, on='Year')

    red_total = result[result['Risk_Color'] == 'Red']
    red_total['Red_percentage'] = (red_total['Borrowed'] / red_total['Total Exposure']) * 100

    # PORTFOLIO SIZE
    sum_portfolio = joint_excel_filtered.groupby('Year')['Borrowed'].sum().reset_index()


    if sum_portfolio.empty:
        fig_sum_trend = px.scatter()
        fig_sum_trend.update_layout(
            annotations=[
                dict(
                    text='No data available for the selected category',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        if len(sum_portfolio) > 1:
            fig_sum = go.Figure(data=go.Scatter(x=sum_portfolio['Year'], y=sum_portfolio['Borrowed'], text=sum_portfolio['Borrowed'], mode="lines+text", line=dict(color='#B8E0D5')))
        else:
            fig_sum = go.Figure(data=go.Scatter(x=sum_portfolio['Year'], y=sum_portfolio['Borrowed'], text=sum_portfolio['Borrowed'], mode="text", line=dict(color='#B8E0D5')))

        fig_sum.update_xaxes(showline=False, showgrid=False, zeroline=False, showticklabels=False)
        fig_sum.update_yaxes(showline=False, showgrid=False, zeroline=False, showticklabels=False)
        fig_sum.update_traces(texttemplate='<b>%{text:,.0f} M$</b>', textfont=dict(size=15))
        #
        y_max_sum = sum_portfolio['Borrowed'].max()
        y_sum_range = [0, y_max_sum + 10000]
        fig_sum.update_yaxes(range=y_sum_range)

        if len(red_total) > 1:
            fig_trend = go.Figure(data=go.Scatter(x=red_total['Year'], y=red_total['Red_percentage'], text=red_total['Red_percentage'], mode="lines+text", line=dict(color='#B8E0D5')))
        else:
            fig_trend = go.Figure(data=go.Scatter(x=red_total['Year'], y=red_total['Red_percentage'], text=red_total['Red_percentage'], mode="text", line=dict(color='#B8E0D5')))
        fig_trend.update_xaxes(showline=False, showgrid=False, zeroline=False, showticklabels=False)
        fig_trend.update_yaxes(showline=False, showgrid=False, zeroline=False, showticklabels=False)
        fig_trend.update_traces(texttemplate='<b>%{text:,.2f} %</b>', textfont=dict(size=15))

        y_red_sum = red_total['Red_percentage'].max()
        y_red_range = [0, y_red_sum + 1]
        fig_trend.update_yaxes(range=y_red_range)

        fig_sum_trend = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
        fig_sum_trend.add_trace(fig_sum.data[0], row=1, col=1)
        fig_sum_trend.add_trace(fig_trend.data[0], row=2, col=1)

        fig_sum_trend.update_layout(
            title_font=dict(family="Verdana", size=24),
            title={
                'text': "Portfolio Size & Red Default Rate",
                'x': 0.5},
            showlegend=False)
        fig_sum_trend.update_traces(hoverinfo='skip')




    # RATING ACTION TREND

    rating_change_df = joint_excel_filtered.copy()
    rating_change_df = rating_change_df[rating_change_df['Moodys_Rating'] != 'Not Rated']

    rating_change_df.sort_values(['Company_ID', 'Year'], inplace=True)

    value_counts = rating_change_df['Company_ID'].value_counts()
    values_to_keep = value_counts[value_counts > 1].index
    rating_change_df = rating_change_df[rating_change_df['Company_ID'].isin(values_to_keep)]

    rating_change_df['Rating_Difference'] = rating_change_df.groupby('Company_ID')['IR_Rank'].diff()
    rating_change_df = rating_change_df[rating_change_df['Rating_Difference'].notna()]
    rating_change_df['Rating_Difference'] = rating_change_df['Rating_Difference'].astype(int)
    rating_change_df['Change Type'] = rating_change_df['Rating_Difference'].apply(lambda x: 'Affirmed' if x == 0 else ('Downgraded' if x < 0 else 'Upgraded'))


    def dd_group(group):
        return group.drop_duplicates(subset=['Company_ID'])
    rating_trend = rating_change_df.groupby('Year', group_keys=False).apply(dd_group).reset_index(drop=True)


    if rating_trend.empty:
        fig_bar_trend = px.scatter()
        fig_bar_trend.update_layout(
            annotations=[
                dict(
                    text='No data available for the selected category',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:#here 
        rating_trend = rating_trend[rating_trend['Change Type'] != 'Missing data']
        rating_trend = rating_trend.groupby('Year')['Change Type'].value_counts().reset_index(name='count')
        ratios_df = rating_trend[rating_trend['Change Type'].isin(['Upgraded', 'Downgraded'])]

        if not ratios_df.empty:
            pivot_table = pd.pivot_table(ratios_df, values='count', index='Year', columns='Change Type', aggfunc='sum', fill_value=0)
            if len(pivot_table.columns) > 1:
                pivot_table['Ratio'] =  pivot_table['Upgraded'] / pivot_table['Downgraded']
                pivot_table.reset_index(inplace=True)
                ratio_title = pivot_table[pivot_table['Year'] == list(pivot_table['Year'].unique())[-1]]['Ratio'].values[0]
                fig_bar_trend = px.bar(
                    rating_trend,
                    x="Year",
                    y="count",
                    color="Change Type",
                    color_discrete_map={
                        "Affirmed": "rgb(192,192,192)",
                        "Downgraded": "rgb(248,105,107)",
                        "Upgraded": "rgb(143,202,125)"})
                if np.isnan(ratio_title) or not np.isfinite(ratio_title):
                    fig_bar_trend.update_layout(yaxis_title = 'Number of Counterparts'),
                else:
                    fig_bar_trend.update_layout(yaxis_title = 'Number of Counterparts',
                                            title=dict(text=f"{ratio_title:.1f}x more upgrades than downgrades (on {year_names[0]})",x=0.5),
                                            legend=dict(
                                                orientation="h",
                                                yanchor="top",
                                                title=None,
                                                x=0.1))
                fig_bar_trend.update_layout(xaxis=dict(tickvals=rating_trend['Year'].unique()))
                fig_bar_trend.update_xaxes(title_text=None)
                yaxis2 = go.layout.YAxis(overlaying="y", side="right")
                if len(list(filter(lambda x: np.isfinite(x), pivot_table['Ratio'].dropna()))) > 1:
                    fig_bar_trend.add_trace(go.Scatter(x=pivot_table['Year'], y=pivot_table['Ratio'],  text=pivot_table['Ratio'].apply(lambda x: f'<b>{x:.1f}</b> x'), mode='lines+markers+text', line=dict(color='yellow'), name='Upgrades/Downgrades Ratio', yaxis="y2"))
                else:
                    fig_bar_trend.add_trace(go.Scatter(x=pivot_table['Year'], y=pivot_table['Ratio'],  text=pivot_table['Ratio'].apply(lambda x: f'<b>{x:.1f}</b> x'), mode='markers+text', line=dict(color='yellow'), name='Upgrades/Downgrades Ratio', yaxis="y2"))
                fig_bar_trend.update_layout(
                    barmode='stack',
                    yaxis=dict(title='Number of Counterparts'),
                    yaxis2=yaxis2
                )
                fig_bar_trend.update_traces(
                    hovertemplate='<br>'.join([
                        '<b>%{fullData.name}</b>',
                        'Number of ctp: <b>%{y:.0f}</b>',
                        "<extra></extra>"]),)

                fig_bar_trend.update_traces(
                    text=pivot_table['Ratio'].apply(lambda x: f'<b>{x:.1f}</b>'),
                    selector=dict(type='scatter'),
                    textfont=dict(size=14, color='black'),
                    texttemplate='<b>%{y:.1f}</b>',
                    textposition='top center',
                    hoverinfo='text',
                    hovertemplate='<br>'.join([
                        '<b>%{fullData.name}</b>',
                        "<extra></extra>"]),
                )
            else:
                pivot_table.reset_index(inplace=True)
                fig_bar_trend = px.bar(
                    rating_trend,
                    x="Year",
                    y="count",
                    color="Change Type",
                    color_discrete_map={
                        "Affirmed": "rgb(192,192,192)",
                        "Downgraded": "rgb(248,105,107)",
                        "Upgraded": "rgb(143,202,125)"})
                fig_bar_trend.update_layout(yaxis_title = 'Number of Counterparts',
                                        legend=dict(
                                            orientation="h",
                                            yanchor="top",
                                            title=None,
                                            x=0.1))
                fig_bar_trend.update_layout(xaxis=dict(tickvals=rating_trend['Year'].unique()))
                fig_bar_trend.update_xaxes(title_text=None)
                yaxis2 = go.layout.YAxis(overlaying="y", side="right")
                fig_bar_trend.update_layout(
                    barmode='stack',
                    yaxis=dict(title='Number of Counterparts'),
                    yaxis2=yaxis2
                )
                fig_bar_trend.update_traces(
                    hovertemplate='<br>'.join([
                        '<b>%{fullData.name}</b>',
                        'Number of ctp: <b>%{y:.0f}</b>',
                        "<extra></extra>"]),)
        else:
            fig_bar_trend = px.scatter()
            fig_bar_trend.update_layout(
                annotations=[
                    dict(
                        text='No data available for the selected category',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.5,
                        y=0.5
                    )])





    ##################################################################################################################################################################
    ## TAB 2
    ##################################################################################################################################################################


    ## PIE FLAGGED


    flagged = excel_2022_filtered.copy()

    flagged = flagged.groupby('Risk_Color')['Borrowed'].sum().reset_index()
    flagged['Total Exposure'] = flagged['Borrowed'].sum()
    flagged['share'] = round((flagged['Borrowed'] / flagged['Total Exposure'])*100, 2)

    if any(flagged['Risk_Color'] == 'Red') is False:
        red_share = 0.0
    else:
        red_share = round(flagged[flagged['Risk_Color'] == 'Red']['share'], 2).to_string(index=False)

    flagged_share = round(flagged[flagged['Risk_Color'] != 'Not Flagged']['share'].sum(), 2)

    if flagged.empty:
        pie_flagged = px.scatter()
        pie_flagged.update_layout(
            annotations=[
                dict(
                    text='No data available for Flagged Portfolio',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        pie_flagged = px.pie(flagged, values='share', hole=.5, names='Risk_Color', color = 'Risk_Color',
                             color_discrete_map={'Not Flagged':'lightgray',
                                                 'Green':'rgb(99, 190, 123)',
                                                 'Orange':'rgb(252, 180, 122)',
                                                 'Red':'rgb(248, 105, 107)',
                                                 },)
        pie_flagged.update_traces(direction ='clockwise',
                          texttemplate='<b>%{value:.1f}</b>%',
                          textposition='inside',
                          insidetextorientation='horizontal',
                          marker=dict(line=dict(color='#000000', width=2)),
                          pull=[0, 0.1, 0.05, 0, 0],
                          hovertemplate='<b>%{label}</b><br>Percentage Share: <b>%{value:.2f}</b>%'
                                 )
        pie_flagged.update_layout(title=f'<br>{flagged_share}% of the portfolio is flagged</br>{red_share}% of the portfolio is Red flagged',
                          title_font=dict(family="Verdana", size=16),
                          title_x=0.5,
                          title_y=0.1,
                          showlegend=False)

        pie_flagged.update_layout(
            showlegend=False,
            font=dict(
                size=18)
        )



    ## BAR FLAGGED


    flagged_order = ['Green', 'Orange', 'Red']

    flagged_bar_df = joint_excel_filtered.copy()

    flagged_bar_df = flagged_bar_df[flagged_bar_df['Risk_Color'] != 'Not Flagged'].groupby(['Year','Risk_Color'])['Borrowed'].sum().reset_index()
    flagged_bar_df['Borrowed'] = round(flagged_bar_df['Borrowed'],0)

    flagged_order33 = [value for value in flagged_order if value in flagged_bar_df['Risk_Color'].unique()]

    flagged_bar_df['Risk_Color'] = pd.Categorical(flagged_bar_df['Risk_Color'], categories=flagged_order33, ordered=True)
    sorted_flagged = flagged_bar_df.sort_values(by=['Year', 'Risk_Color'])


    if sorted_flagged.empty:
        bar_flagged = px.scatter()
        bar_flagged.update_layout(
            annotations=[
                dict(
                    text='No data available for Flagged Portfolio',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        bar_flagged = px.bar(
            sorted_flagged,
            x="Year",
            y="Borrowed",
            color="Risk_Color",
            color_discrete_map={
                'Green':'rgb(99, 190, 123)',
                'Risk_Color':'rgb(252, 180, 122)',
                'Red':'rgb(248, 105, 107)',
                },
            text="Borrowed",
        )
        bar_flagged.update_layout(
            yaxis_title="Exposure (in millions of dollars)",
            legend=dict(
                orientation="h",
                yanchor="top",
                title=None,
                y=1.1,
                x=0.25)
        )
        bar_flagged.update_traces(
            texttemplate='<b>%{text:,.0f}</b> $',
            textposition='inside',
            hovertemplate=' Exposure: <b>%{y:,.0f}</b> $<extra></extra>'
        )



    ## RISK CONCENTRATION INDUSTRY


    reversed_flagged_order = flagged_order[::-1]

    risk_con = excel_2022_filtered[excel_2022_filtered['Risk_Color'] != 'Not Flagged'].groupby(['Industry', 'Risk_Color'])['Borrowed'].sum().reset_index()
    risk_con['Total Exposure'] = risk_con.groupby('Industry')['Borrowed'].transform('sum')

    reversed_flagged_order33 = [value for value in reversed_flagged_order if value in risk_con['Risk_Color'].unique()]

    risk_con['Risk_Color'] = pd.Categorical(risk_con['Risk_Color'], categories=reversed_flagged_order33, ordered=True)
    risk_con_sorted = risk_con.sort_values(by=['Total Exposure', 'Risk_Color'], ascending=False)

    top_con = risk_con_sorted['Industry'].unique()[:14]

    if risk_con_sorted.empty:
        bar_con_industry = px.scatter()
        bar_con_industry.update_layout(
            annotations=[
                dict(
                    text='No data available for Risk Concentration per Industry',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        bar_con_industry = px.bar(
            risk_con_sorted[risk_con_sorted['Industry'].isin(top_con)],
            x="Borrowed",
            y="Industry",
            color="Risk_Color",
            color_discrete_map={
                'Green':'rgb(99, 190, 123)',
                'Orange':'rgb(252, 180, 122)',
                'Red':'rgb(248, 105, 107)',
                },
            text="Borrowed",
            category_orders={"Industry": top_con},
        )
        bar_con_industry.update_traces(
            texttemplate='<b>%{text:,.0f}</b> $',
            textangle=0,
            textposition='inside',
            insidetextanchor='middle',
            hovertemplate='%{y}:<b> %{x:,.0f} </b>$<extra></extra>'

        )
        bar_con_industry.update_layout(
            xaxis_title="Exposure in millions of $",
            yaxis_title=None,
            legend=dict(
                orientation="h",
                yanchor="top",
                title=None,
                y=1.1,
                x=0.1)
        )



    ## BAR RISK CONCENTRATION COUNTRY


    risk_con_country = excel_2022_filtered[excel_2022_filtered['Risk_Color'] != 'Not Flagged'].groupby(['Country', 'Risk_Color'])['Borrowed'].sum().reset_index()
    risk_con_country['Total Exposure'] = risk_con_country.groupby('Country')['Borrowed'].transform('sum')
    risk_con_country['Risk_Color'] = pd.Categorical(risk_con_country['Risk_Color'], categories=reversed_flagged_order, ordered=True)

    risk_country_sorted = risk_con_country.sort_values(by=['Total Exposure', 'Risk_Color'], ascending=False)
    top_10 = risk_country_sorted['Country'].unique()[:10]
    top_countries = risk_country_sorted[risk_country_sorted['Country'].isin(top_10)]

    other_countries = risk_country_sorted[~risk_country_sorted['Country'].isin(top_10)]
    other_countries2 = other_countries.groupby('Risk_Color')['Borrowed'].sum().reset_index()
    other_countries2['Total Exposure'] = other_countries2['Borrowed'].sum()
    other_countries2['Country'] = 'Other'
    combined_df = pd.concat([top_countries, other_countries2], ignore_index=True)
    top_10 = np.append(top_10, 'Other')

    if combined_df.empty:
        bar_con_country = px.scatter()
        bar_con_country.update_layout(
            annotations=[
                dict(
                    text='No data available for Risk Concentration per Country',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:

        bar_con_country = px.bar(
            combined_df,
            x="Borrowed",
            y="Country",
            color="Risk_Color",
            color_discrete_map={
                'Green':'rgb(99, 190, 123)',
                'Orange':'rgb(252, 180, 122)',
                'Red':'rgb(248, 105, 107)',
                },
            text="Borrowed",
            category_orders={"Country": top_10}
        )
        bar_con_country.update_traces(
            texttemplate='<b>%{text:,.0f}</b> $',
            textangle=0,
            textposition='inside',
            insidetextanchor='middle',
            hovertemplate='%{y}:<b> %{x:,.0f} </b>$<extra></extra>'

        )
        bar_con_country.update_layout(
            xaxis_title="Exposure in millions of $",
            yaxis_title=None,
            legend=dict(
                orientation="h",
                yanchor="top",
                title=None,
                y=1.1,
                x=0.25)
        )



    ## RATING DISTRIBUTION

    flagged_order22 = ['Not Flagged', 'Green', 'Orange', 'Red']

    rat_dist = excel_2022_filtered.groupby(["Moodys_Rating",'Risk_Color'])['Borrowed'].sum().reset_index()
    rat_dist = rat_dist.dropna()

    flagged_order4 = [value for value in flagged_order22 if value in rat_dist['Risk_Color'].unique()]

    rat_dist['Risk_Color'] = pd.Categorical(rat_dist['Risk_Color'], categories=flagged_order4, ordered=True)
    rat_dist["Moodys_Rating"] = pd.Categorical(rat_dist["Moodys_Rating"], categories=order_moodys[::-1], ordered=True)
    rat_dist = rat_dist.sort_values(by=["Moodys_Rating", 'Risk_Color'], ascending=False)



    if rat_dist.empty:
        fig_rat_dist = px.scatter()
        fig_rat_dist.update_layout(
            annotations=[
                dict(
                    text='No data available for Rating Distribution',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        fig_rat_dist = px.bar(
            rat_dist,
            x="Moodys_Rating",
            y="Borrowed",
            color="Risk_Color",
            color_discrete_map={
                     'Not Flagged':'rgb(173, 216, 230)',
                     'Green':'rgb(99, 190, 123)',
                     'Orange':'rgb(252, 180, 122)',
                     'Red':'rgb(248, 105, 107)',
                     },
            category_orders={"Moodys_Rating": order_moodys},
            text='Borrowed'
        )
        fig_rat_dist.update_layout(
            plot_bgcolor='white',
            yaxis_title="Exposure (in millions of dollars)",
            legend=dict(
                orientation="h",
                yanchor="top",
                title=None,
                x=0.3,
                y = 1.1)
        )
        fig_rat_dist.update_traces(
            textangle=0,
            texttemplate='<b>%{text:,.0f} $</b>',
            textposition='inside',
            insidetextanchor='middle',
            hovertemplate='<br>'.join([
                'Rating: <b>%{fullData.name}</b>',
                'Exposure: <b>%{text:,.0f}</b> M$',
                "<extra></extra>"]),

        )
        fig_rat_dist.update_xaxes(title_text=None)

        overall_moodys = rat_dist.groupby("Moodys_Rating")['Borrowed'].sum().reset_index()
        for i, row in overall_moodys.iterrows():
            fig_rat_dist.add_trace(
                go.Scatter(
                    x=[row["Moodys_Rating"]],
                    y=[row['Borrowed']],
                    mode='text',
                    textposition="top center",
                    text=[f'<b>{row["Borrowed"]:,.0f} $</b>'],
                    showlegend=False,
                    hoverinfo='none'
                )
            )



    ## DOWNGRADES IN THE PORTFOLIO


    grouped_downgrades = rating_change_df[rating_change_df['Year'] == year_names[1]]

    if grouped_downgrades.empty:
        downgrades_counts = None
    else:
        def dd_group(group):
            return group.drop_duplicates(subset=['Company_ID'])
        grouped_downgrades = grouped_downgrades.groupby('Industry', group_keys=False).apply(dd_group)
        grouped_downgrades = grouped_downgrades.groupby('Industry')['Change Type'].value_counts().reset_index(name='count')#here

        downgrades_counts = grouped_downgrades[grouped_downgrades["Change Type"]=='Downgraded']
        downgrades_counts = downgrades_counts.sort_values(by='count', ascending=True)


    if downgrades_counts is None:
        fig_downgrades = px.scatter()
        fig_downgrades.update_layout(
            annotations=[
                dict(
                    text='No data available for Downgrades in the Portfolio',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        fig_downgrades = px.bar(downgrades_counts.tail(14), y='Industry',
                     x='count',
                     orientation='h',
                     height=500)

        fig_downgrades.update_yaxes(title_text='')
        fig_downgrades.update_xaxes(title_text='Number of Companies Downgraded')
        fig_downgrades.update_layout(title=dict(x=0.5), legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.35, title_text=''))
        fig_downgrades.update_traces(textposition='inside',hovertemplate='<b>%{y}</b><br>Downgraded: %{x}<extra></extra>', texttemplate='<b>%{x}</b>', textangle=0, insidetextanchor='middle')



    ## SEVERITY BAR


    severity = rating_change_df[rating_change_df['Year'] == year_names[1]]

    if severity.empty:
        severity = None
    else:
        def dd_group(group):
            return group.drop_duplicates(subset=['Company_ID'])
        severity = severity.groupby('Industry', group_keys=False).apply(dd_group)
        severity = severity.groupby(['Rating_Difference', 'Industry']).size().reset_index(name='Count')
        severity = severity[severity['Rating_Difference'] != 0]   # filter out Affirmed


    if severity is None:
        fig_severity = px.scatter()
        fig_severity.update_layout(
            annotations=[
                dict(
                    text='No data available for Severity of Rating Change',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        fig_severity = px.bar(
            severity,
            x="Rating_Difference",
            y="Count",
            color="Industry",
        )
        fig_severity.update_yaxes(title_text='Number of Companies')
        fig_severity.update_xaxes(title_text='Rating Action: Number of notches (excluding ratings Affirmed)')
        fig_severity.update_layout(legend=dict(title_text=''))
        fig_severity.update_traces(textposition='inside', texttemplate='<b>%{y}</b>', textangle=0, hovertemplate='<b>%{fullData.name}</b><br>Number of Cnpt: %{y}<extra></extra>')



    ##################################################################################################################################################################
    ## TAB 3
    ##################################################################################################################################################################

    df_map = excel_2022_filtered.copy()

    df_map = df_map.groupby('Country')['Borrowed'].sum().reset_index()
    df_map = df_map.sort_values(by='Borrowed', ascending=False)

    fig_world_map = px.choropleth(
        df_map,
        locations="Country",
        color="Borrowed",
        locationmode="country names",
        scope="world",
        hover_name="Country",
    )
    fig_world_map.update_traces(hovertemplate="<b>%{location}</b><br>Exposure in M of $: %{z:,.0f}<extra></extra>")
    fig_world_map.update_layout(
        title=f"Exposure over the World (in millions of dollars) on {year_names[0]}",
        title_x=0.5,
        height=1200,
        title_font=dict(size=24),
        geo=dict(showframe=False, center=dict(lat=10)),
        coloraxis=dict(colorbar=dict(yanchor='top', xanchor='center', orientation='h', title=None)),
    )




    return industry_options, country_names, f"### Portfolio Size: **{sum_exposure_latest:,.0f} M$**", fig_av_rating, fig_sum_trend, gauge_avg, gauge_IG, gauge_flag, fig_ptf_quality, fig_bar_trend, fig_pie_industry, fig_pie_country, fig_pie_branch, pie_flagged, bar_flagged, bar_con_industry, bar_con_country, fig_rat_dist, fig_downgrades, fig_severity, fig_world_map






@app.callback(
    Output('scroll-trigger', 'children'),
    Input("world-map", "clickData"),
    prevent_initial_call=True
)
def trigger_scroll(click_data):
    if click_data:
        return 1
    else:
        return 0





@app.callback(
    Output("click-bar-exp", "figure"),
    Output("click-bar-ctp", "figure"),
    Input("world-map", "clickData"))


    ### CLICK BAR EXPOSURE


def generate_clicked_bar_chart(click_data):

    country_name = click_data["points"][0]["location"]
    click_df = joint_excel_filtered.copy()
    click_df = click_df.query("Country == @country_name")
    click_dfff = click_df.groupby(['Year', 'Short_Moodys'])['Borrowed'].sum().reset_index()


    if click_dfff.empty:
        fig_click_exp = px.scatter()
        fig_click_exp.update_layout(
            annotations=[
                dict(
                    text='No data available for Exposure of the Country',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5
                )
            ]
        )
    else:
        fig_click_exp = px.bar(
            click_dfff,
            x="Year",
            y="Borrowed",
            color="Short_Moodys",
            category_orders={"Short_Moodys": order_shortmoodys},
            color_discrete_sequence=color_palet,
            text="Borrowed",
            title=f"<span style='font-size:40px'>{country_name}<br><span style='font-size:20px'>Exposure for Different Years</span>",
        )
        fig_click_exp.update_layout(
            yaxis_title='Exposure in Millions of Dollars',
            xaxis_title=None,
            height=460
        )
        fig_click_exp.update_traces(
            texttemplate='%{text:,.0f} $',
            textposition='inside',
            textangle=0,
            insidetextanchor='middle',
            hovertemplate='<br>'.join([
                'Rating: <b>%{fullData.name}</b>',
                'Exposure: <b>%{text:,.0f}</b> M$',
                "<extra></extra>"])
        )
        fig_click_exp.update_xaxes(title_text=None)

        overall_values = click_df.groupby('Year')['Borrowed'].sum().reset_index()
        for i, row in overall_values.iterrows():
            fig_click_exp.add_trace(
                go.Scatter(
                    x=[row['Year']],
                    y=[row['Borrowed']],
                    mode='text',
                    textposition="top center",
                    text=[f'<b>{row["Borrowed"]:,.0f} $</b>'],
                    showlegend=False,
                    hoverinfo='none'
                )
            )





    ### CLICK LINE COUNT


    click_df3 = click_df.copy()
    click_df3 = click_df3.groupby(['Year', 'Country'])['Company_ID'].nunique().reset_index()
    click_df3 = click_df3.rename(columns={'Company_ID': 'All CTP'})

    count_flagged = click_df[click_df['Risk_Color'] != 'Not Flagged']
    count_flagged2 = count_flagged.groupby(['Year', 'Country'])['Company_ID'].nunique().reset_index()
    count_flagged2 = count_flagged2.rename(columns={'Company_ID': 'All Flagged'})



    fig_click_ctp = px.line(
        count_flagged2,
        x="Year",
        y="All Flagged",
        title = "Number of <span style='font-size:16px;color:#42AD90;'>All the Companies</span> and the <span style='font-size:16px;color:red;'>Companies Flagged</span>",
        category_orders={"Year": year_names},
    ).update_traces(line=dict(color='red'))


    fig_click_ctp.add_trace(
        px.line(
            click_df3,
            x="Year",
            y="All CTP",
        ).update_traces(line=dict(color='#42AD90')).data[0]
    )


    for i, row in count_flagged2.iterrows():
        fig_click_ctp.add_trace(
            go.Scatter(
                x=[row['Year']],
                y=[row['All Flagged']],
                mode='text',
                textposition="top center",
                text=[f'<b>{row["All Flagged"]}</b>'],
                showlegend=False,
                hoverinfo='none'
            )
        )


    for i, row in click_df3.iterrows():
        fig_click_ctp.add_trace(
        go.Scatter(
            x=[row['Year']],
            y=[row['All CTP']],
            mode='text',
            textposition="top center",
            text=[f'<b>{row["All CTP"]}</b>'],
            showlegend=False,
            hoverinfo='none'
        )
    )


    fig_click_ctp.update_xaxes(showline=False, showgrid=False)
    fig_click_ctp.update_yaxes(showline=False, showgrid=False)
    fig_click_ctp.update_layout(yaxis_title='Number of Companies', xaxis_title=None, height=460)



    return fig_click_exp, fig_click_ctp





app.clientside_callback(
    """
    function scrollToGeneratedGraph(trigger) {
        console.log('Trigger:', trigger);
        if (trigger === 1) {
            var element = document.getElementById('click-bar-exp');
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
                console.log('Scrolling to element');
            } else {
                console.log('Element not found');
            }
        }
        return 0;
    }
    """,
    Output('scroll-pos', 'data'),
    Input('scroll-trigger', 'children'),
)




def open_browser():
    webbrowser.open_new_tab('http://127.0.0.1:8309')

if __name__ == '__main__':
    app.title = "Portfolio Risk"
    import threading
    threading.Timer(1, open_browser).start()
    app.run_server(port=8309, debug=False)

