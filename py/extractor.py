import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import bigquery

# Define as credenciais da conta de serviço.
credentials = service_account.Credentials.from_service_account_file('path/to/service_account.json')

# Define as informações do projeto e do conjunto de dados do BigQuery.
project_id = 'your-project-id'
dataset_id = 'your-dataset-id'

# Define o nome da tabela a ser criada no BigQuery.
table_name = 'your-table-name'

# Define o esquema da tabela.
table_schema = [
    bigquery.SchemaField('id', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('name', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('description', 'STRING'),
    bigquery.SchemaField('owner_id', 'STRING', mode='REQUIRED'),
]

# Cria o cliente do BigQuery.
bigquery_client = bigquery.Client(credentials=credentials, project=project_id)

# Cria o conjunto de dados, caso ainda não exista.
dataset_ref = bigquery_client.dataset(dataset_id)
try:
    bigquery_client.get_dataset(dataset_ref)
except HttpError as error:
    if error.resp.status == 404:
        dataset = bigquery.Dataset(dataset_ref)
        dataset = bigquery_client.create_dataset(dataset)
        print(f'Created dataset {dataset_id}.')
    else:
        raise

# Cria a tabela, caso ainda não exista.
table_ref = dataset_ref.table(table_name)
try:
    bigquery_client.get_table(table_ref)
except HttpError as error:
    if error.resp.status == 404:
        table = bigquery.Table(table_ref, schema=table_schema)
        table = bigquery_client.create_table(table)
        print(f'Created table {table_name}.')
    else:
        raise

# Extrai os dados do Google Classroom.
service = build('classroom', 'v1', credentials=credentials)
courses = []
next_page_token = None
while True:
    courses_request = service.courses().list(pageToken=next_page_token)
    courses_response = courses_request.execute()
    courses += courses_response['courses']
    next_page_token = courses_response.get('nextPageToken')
    if not next_page_token:
        break

# Transforma os dados em um DataFrame do Pandas.
data = []
for course in courses:
    row = {'id': course['id'], 'name': course['name'], 'description': course.get('description', ''), 'owner_id': course['ownerId']}
    data.append(row)
df = pd.DataFrame(data)

# Converte o DataFrame em uma lista de dicionários para inserir na tabela do BigQuery.
rows_to_insert = df.to_dict('records')

# Insere as linhas na tabela do BigQuery.
errors = bigquery_client.insert_rows(table_ref, rows_to_insert)
if errors:
    print(f'Encountered errors while inserting rows: {errors}.')
else:
    print(f'Successfully inserted {len(rows_to_insert)} rows into {table_name}.')
