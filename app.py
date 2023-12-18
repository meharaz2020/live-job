import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import io
import requests
import dash_table

# Fetching data from GitHub
url = 'https://raw.githubusercontent.com/meharaz2020/ex/master/livejob.xlsx'
response = requests.get(url)
content = response.content
df = pd.read_excel(io.BytesIO(content))

app = dash.Dash(__name__)
server=app.server
# Create Dash layout
app.layout = html.Div([
    # Header
    html.H1("Live Job Data", style={'text-align': 'center', 'margin-top': '20px'}),

    html.Div([
    # Title for the filter
    html.H3("Filter by Job ID or JobTitle", style={'text-align': 'center', 'margin-bottom': '10px', 'color': 'navy'}),

    # Input field
    html.Div([
        dcc.Input(
        id='filter-input',
        type='text',
        placeholder='Enter JP_ID or JobTitle...',
        value='',  # Initial value of the input box
        style={'width': '80%', 'height': '50px', 'margin': '20px auto', 'padding': '5px', 'border-radius': '5px', 'border': '2px solid #ccc'},
        **{'autoComplete': 'off'}  # Disable autocomplete

        ),
    ], style={'text-align': 'center'})
]),

html.Div([
    # Title for the filter
    html.H3("Filter by Publish Date", style={'text-align': 'center', 'margin-bottom': '10px', 'color': 'navy'}),

    # Input field
    html.Div([
       # Date Range Picker for PublishDate
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=df['PublishDate'].min(),
        end_date=df['PublishDate'].max(),
        display_format='YYYY-MM-DD',
        style={'margin': '10px'}
    ),
    ], style={'text-align': 'center'})
]),
html.Div([
    # Title for the filter
    html.H3("Filter by CP ID", style={'text-align': 'center', 'margin-bottom': '10px', 'color': 'navy'}),

    # Input field
    html.Div([
        # Multi-Select box for CP_ID
        dcc.Dropdown(
            id='multi-select',
            options=[{'label': str(cp_id), 'value': cp_id} for cp_id in df['CP_ID'].unique()],
            value=[],  # Initial value of the multi-select box
            multi=True,  # Allow multiple selections
            placeholder='Select CP_ID...',
            style={'margin': '10px', 'width': '1000px', 'margin': '10px', 'display': 'inline-block'}
        ),
    ], style={'text-align': 'center', 'display': 'inline-block', 'width': '100%'})
]),


   html.Div([
    # Title for the filter
    html.H3("Filter by Regional JOB", style={'text-align': 'center', 'margin-bottom': '10px', 'color': 'navy'}),

    # Input field
    html.Div([
        # Multi-Select box for CP_ID
           # Slider for RegionalJob
    dcc.RangeSlider(
        id='regional-job-slider',
        min=df['RegionalJob'].min(),
        max=df['RegionalJob'].max(),
        step=1,
        marks={i: str(i) for i in range(df['RegionalJob'].min(), df['RegionalJob'].max() + 1)},
        value=[df['RegionalJob'].min(), df['RegionalJob'].max()],
        included=False,
        allowCross=False,
        className='regional-job-slider',
    ),

    ], style={'text-align': 'center', 'display': 'inline-block', 'width': '100%'})
]),
 
html.Div([
    # Title for the filter
    html.H3("Filter by Category", style={'text-align': 'center', 'margin-bottom': '10px', 'color': 'navy'}),

    # Input field
    html.Div([
        # html.Label('Filter by Category:', style={'font-weight': 'bold'}),
        dcc.Dropdown(
            id='cat-name-select',
            options=[{'label': str(cat), 'value': str(cat)} for cat in df['CAT_NAME'].unique()],
            value=[],  # Initial value of the CAT_NAME dropdown
            multi=True,  # Allow multiple selections
            placeholder='Select Category...',
            style={'margin': '10px', 'width': '1000px', 'margin': '10px', 'display': 'inline-block'}
        ),
    ], style={'text-align': 'center', 'display': 'inline-block', 'width': '100%'})
]),

 

html.Div([
    # Title for the filter
    html.H3("Filter by Language", style={'text-align': 'center', 'margin-bottom': '10px', 'color': 'navy'}),

    # Input field
    html.Div([
        # html.Label('Filter by Category:', style={'font-weight': 'bold'}),
         dcc.Checklist(
        id='job-lang-checkbox',
        options=[
            {'label': 'English Job', 'value': 'English'},
            {'label': 'Bangla Job', 'value': 'Bangla'}
        ],
        value=[],  # Initial value of the checkbox
        style={'margin': '10px'}
    ),
    ], style={'text-align': 'center', 'display': 'inline-block', 'width': '100%'})
]),
    # Checkbox for selecting Job Language
   

    # DataTable to display filtered data with pagination
    html.Div(
        dash_table.DataTable(
            id='table-container',
            columns=[{'name': col, 'id': col} for col in df.columns],
            page_size=10,  # Number of rows per page
            style_table={'overflowX': 'auto'},  # Horizontal scroll
            style_cell={
                'textAlign': 'left',
                'backgroundColor': 'rgb(245, 245, 245)',  # Light gray background
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'center',
            },
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',  # Lighter gray background for header
                'fontWeight': 'bold'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},  # Alternating row colors
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ]
        ),
        style={'margin': '20px'}
    )
])

# Callback to update DataTable based on input values
@app.callback(
    Output('table-container', 'data'),
    [Input('filter-input', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('multi-select', 'value'),
     Input('regional-job-slider', 'value'),
     Input('cat-name-select', 'value'),
     Input('job-lang-checkbox', 'value')]
)
def update_table(filter_value, start_date, end_date, selected_cp_ids, regional_job_range, selected_cat_names, job_lang):
    # Filter data based on input value for JP_ID or JobTitle
    if filter_value.isdigit():  # Check if input is a number for filtering by JP_ID
        filtered_data = df[df['JP_ID'] == int(filter_value)]
    else:  # If not a number, filter by JobTitle
        filtered_data = df[df['JobTitle'].str.contains(filter_value, case=False, na=False)]

    # Filter data based on date range for PublishDate
    filtered_data = filtered_data[
        (filtered_data['PublishDate'] >= start_date) &
        (filtered_data['PublishDate'] <= end_date)
    ]

    # Filter data based on selected CP_IDs
    if selected_cp_ids:
        filtered_data = filtered_data[filtered_data['CP_ID'].isin(selected_cp_ids)]

    # Filter data based on RegionalJob slider
    filtered_data = filtered_data[
        (filtered_data['RegionalJob'] >= regional_job_range[0]) &
        (filtered_data['RegionalJob'] <= regional_job_range[1])
    ]

    # Filter data based on selected CAT_NAMEs
    if selected_cat_names:
        filtered_data = filtered_data[filtered_data['CAT_NAME'].isin(selected_cat_names)]

    # Filter data based on Job Language
    if 'English' in job_lang:
        filtered_data = filtered_data[filtered_data['JobLang'] == 1]
    if 'Bangla' in job_lang:
        filtered_data = filtered_data[filtered_data['JobLang'] == 2]

    return filtered_data.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
