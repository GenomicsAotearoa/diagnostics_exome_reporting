import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

from dash.dependencies import Input, Output



#app = dash.Dash(__name__ , external_stylesheets=external_stylesheets)Aa

dataDirectory="/blue/project/vulval/data/lists/"

sampleName="/vulval01"

tier0df = pd.read_csv(dataDirectory + sampleName +  sampleName + "_tier0.csv")
tier1df = pd.read_csv(dataDirectory + sampleName +  sampleName + "_tier1.csv")
tier2df = pd.read_csv(dataDirectory + sampleName +  sampleName + "_tier2.csv")



def generate_table(sampleName, tier, selectedColumns, max_rows=10):
    dataframe = pd.read_csv(dataDirectory + sampleName +  sampleName + "_" + tier + ".csv")
    return dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in selectedColumns
        ],
        data=dataframe.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        #column_selectable="single",
        #row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 30,
        #fixed_rows={ 'headers': True, 'data': 0 },
		style_table={'overflowX': 'scroll'},
		style_cell={
     	    'minWidth': '140px' ,
        	'whiteSpace': 'normal',
			'font_family': 'Gravitas One',
            'font_size': '18px',
            'text_align': 'center',
            'textOverflow': 'ellipsis',
            'overflow': 'hidden',
            'maxWidth': 0
    	},
        style_data_conditional=[
            {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        export_format='xlsx',
        export_headers='display',
        
    )
#    return html.Table(
#        [html.Tr([html.Th(col) for col in selectedColumns])] +
#        
#        # Body
#        [html.Tr([
#            html.Td(dataframe.iloc[i][col]) for col in selectedColumns
#        ]) for i in range(min(len(dataframe), max_rows))],
#    )


def generateColumns(dataframe):
    columnNames=list(dataframe.columns.values)
    optionList=list()
    for item in columnNames:
        itemDict={"label":item, "value":item}
        optionList.append(itemDict)

    return dcc.Checklist(
        id="selectedColumns",
        options=optionList,
        value=["Main_gene", "REF", "ALT", "altDepth", "refDepth", "Total_Depth", "QUAL"],
        labelStyle={'display': 'block'}
    )   

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
tabs_styles = {
    'height': '44px'
}

sampleSelect = dcc.Dropdown(
    id='sampleName',
    options=[
        {'label': 'vulval01', 'value': '/vulval01'},
        {'label': 'vulval02', 'value': '/vulval02'},
        {'label': 'vulval03', 'value': '/vulval03'}
    ],
    value='/vulval01'
    )


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__)

server = app.server


app.layout = html.Div(children=[
    html.H1(children='DART - dash version 0.1'),
    html.Div(children='''Annotated variants for vulval samples'''),
    html.Tr([
		html.Td(children=[sampleSelect ,generateColumns(tier0df)]),
		html.Td([
            dcc.Tabs(id="tabs", value='tab-0',   children=[
            dcc.Tab(label='Tier 0', value='tab-0'),
        	dcc.Tab(label='Tier 1', value="tab-1"),
        	dcc.Tab(label='Tier 2', value='tab-2')
   			],style=tabs_styles),
            html.Div(id='tabs-content'),
            ], style={"width":80}),
	])

    ], className='row' )



#app.css.append_css({
#    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#})



@app.callback(Output('tabs-content', 'children'), [Input('sampleName','value'),Input('tabs', 'value'),Input('selectedColumns', 'value')])

def render_content(sampleName, tab, selectedColumns):
    if tab == 'tab-1':
        return html.Div([
			generate_table(sampleName, "tier1", selectedColumns)
        ])
    elif tab == 'tab-2':
        return html.Div([
			generate_table(sampleName, "tier2",selectedColumns)
        ])
    elif tab == 'tab-0':
        return html.Div([
            generate_table(sampleName, "tier0",selectedColumns)
        ])


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0")


