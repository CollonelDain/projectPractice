import dash
from dash import html, dcc
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import requests

# Функция получения данных из NocoDB
def get_nocodb_data():
    url = "https://bookish-carnival-4jqq5q7r96p2jr6-8000.app.github.dev/nocodb-data/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(response)
            data = response.json()
            print(2)
            records = data.get('records', [])
            print(3)
            print("Полученные данные:", records)
            print(4)
            cleaned_records = [
                {k: v for k, v in record.items() if not k.startswith('_nc_m2m_')}
                for record in records
            ]
            return pd.DataFrame(cleaned_records)
        else:
            print("Ошибка при получении данных:", response.status_code)
            return pd.DataFrame()
    except Exception as e:
        print(f"Ошибка соединения: {e}")
        return pd.DataFrame()

# Инициализация приложения Dash
app = dash.Dash(__name__)

# Базовый макет приложения
app.layout = html.Div([
    html.H1('User Dashboard'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # обновление каждую секунду при первой загрузке
        n_intervals=0,
        max_intervals=1   # выполняется только один раз при загрузке
    ),
    html.Div(id='dashboard-content')
])

# Callback для обновления содержимого при загрузке
@app.callback(
    Output('dashboard-content', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_dashboard(n):
    # Получаем данные
    df = get_nocodb_data()

    # Проверяем, что DataFrame не пустой
    if df.empty:
        return html.P('Нет данных для отображения. Проверьте соединение с NocoDB.')
    
    # Преобразуем даты
    if 'CreatedAt' in df.columns:
        df['CreatedAt'] = pd.to_datetime(df['CreatedAt'])
    if 'UpdatedAt' in df.columns:
        df['UpdatedAt'] = pd.to_datetime(df['UpdatedAt'], errors='coerce')

    # Создаем визуализации
    log_columns = [col for col in ['virtual_machines', 'audit_logs', 'vm_deletion_logs'] if col in df.columns]
    if log_columns:
        fig_logs = px.bar(df, 
                         x='Id', 
                         y=log_columns,
                         title='Количество логов по типам',
                         barmode='group')
    else:
        fig_logs = px.bar(title='Нет данных о логах')

    if 'CreatedAt' in df.columns:
        fig_timeline = px.scatter(df, 
                                x='CreatedAt', 
                                y='Id',
                                hover_data=['username', 'email'] if 'username' in df.columns and 'email' in df.columns else [],
                                title='Временная шкала создания пользователей')
    else:
        fig_timeline = px.scatter(title='Нет данных о времени создания')

    # Определяем колонки для таблицы
    table_columns = [
        {'name': 'ID', 'id': 'Id'},
        {'name': 'Username', 'id': 'username'} if 'username' in df.columns else {'name': 'Username', 'id': 'username', 'hidden': True},
        {'name': 'Email', 'id': 'email'} if 'email' in df.columns else {'name': 'Email', 'id': 'email', 'hidden': True},
        {'name': 'Role', 'id': 'role'} if 'role' in df.columns else {'name': 'Role', 'id': 'role', 'hidden': True},
        {'name': 'Status', 'id': 'status'} if 'status' in df.columns else {'name': 'Status', 'id': 'status', 'hidden': True},
        {'name': 'Created', 'id': 'CreatedAt'} if 'CreatedAt' in df.columns else {'name': 'Created', 'id': 'CreatedAt', 'hidden': True},
    ]

    # Возвращаем содержимое dashboard
    return [
        html.Div([
            html.H3('Общая статистика'),
            html.P(f"Всего пользователей: {len(df)}"),
            html.P(f"Активных audit logs: {df['audit_logs'].sum() if 'audit_logs' in df.columns else 'N/A'}"),
            html.P(f"VM deletions: {df['vm_deletion_logs'].sum() if 'vm_deletion_logs' in df.columns else 'N/A'}"),
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        html.Div([
            dcc.Graph(figure=fig_logs),
            dcc.Graph(figure=fig_timeline),
        ], style={'width': '65%', 'display': 'inline-block'}),
        
        html.Div([
            html.H3('Детальная информация'),
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=table_columns,
                style_table={'overflowX': 'auto'},
            )
        ])
    ]

# Запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)