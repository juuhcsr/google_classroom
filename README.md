# Extrator de dados do Classroom para o BigQuery :electron: :brazil:

Para extrair dados do Google Classroom e transferi-los para o Google BigQuery, a InnovateEDU criou uma ferramenta gratuita e de código aberto.

> Esse repositório possui uma atualização que corrige o erro ao importar para o Bigquery.

Para usar a ferramenta para extrair os dados do Google Classroom e carregá-los no Google BigQuery, siga as etapas a seguir:

1. Ativar as APIs;
2. Criar a conta de serviço
3. Dar permissão para a conta de serviço
4. Copiar o repositório;
5. Declarar as variáveis corretas;
6. Executar o docker;

## Pré requisitos

<details>
<summary> Ativando APIs </summary><br/>

Algumas APIs precisam ser ativadas no projeto do Google Cloud. Você pode ativá-las usando o console do Google Cloud ou comando no cloud shell

```shell
gcloud services enable classroom.googleapis.com
gcloud services enable admin.googleapis.com
```

</details>


<details>
<summary> Criar conta de serviço </summary><br/>

Uma conta de serviço é necessária para usar o conector.

para criar uma conta de serviço acesse seu projeto do Google Cloud , vá para IAM & Admin > Contas de serviço. Clique em Criar conta de serviço . 

Você também pode usar o link abaixo para ir direto para a página.

[Criar conta de serviço](https://console.cloud.google.com/iam-admin/serviceaccounts/create)

- Crie um nome para sua conta de serviço. Por exemplo, **Classroom Connector**;
- Clique em Criar;
- Atribua a esta conta a função **BigQuery Admin**; (Proprietário)
- Clique em criar;

Depois de ter criado a conta de serviço 

- CLique nos **3 pontos** ( Ações) > **Gerenciar chaves**
- Clique em **Adicionar chave** > **Criar nova chave** e baixe o arquivo JSON que contém a chave privada para esta conta de serviço;
- Clique em Concluído.

> Guarde esse arquivo para fazer o upload nos próximos passos 
</details>


<details>
<summary> Dar permissão para a conta de serviço </summary><br/>

Para a conta de serviço ser utilizada como conector é necessário você dar permissões pra ela no **Google Admin Console**. Cada conta de serviço tem um ID exclusivo. Selecione a conta de serviço recém-criada em seu console Cloud e anote o ID exclusivo associado.
  
![image](https://user-images.githubusercontent.com/110038530/232064617-39607621-afd1-4a04-acf6-ac165e86abd1.png)

  [Exibir contas de serviço](https://console.cloud.google.com/iam-admin/serviceaccounts)

No console de admin vá até **Segurança** > **Controle de dados e acesso** > **Controles de API** > Role a página e vá em **Gerenciar delegação em todo o domínio**

- Clique em Adicionar novo
- Cole o ID exclusivo de suas contas de serviço
- Copie e cole o texto abaixo na caixa de escopos oAuth
- Clique em **Autorizar**

```
https://www.googleapis.com/auth/admin.directory.orgunit,
https://www.googleapis.com/auth/admin.reports.usage.readonly,
https://www.googleapis.com/auth/classroom.announcements,
https://www.googleapis.com/auth/classroom.courses,
https://www.googleapis.com/auth/classroom.coursework.students,
https://www.googleapis.com/auth/classroom.guardianlinks.students,
https://www.googleapis.com/auth/classroom.profile.emails,
https://www.googleapis.com/auth/classroom.rosters,
https://www.googleapis.com/auth/classroom.student-submissions.students.readonly,
https://www.googleapis.com/auth/classroom.topics
```
<details>
<summary> O que cada uma dessas permissões faz  </summary><br/>
  
  
| API | Descrição|
|-----|-----|
| admin.directory.orgunit     | Permite ler e gerenciar unidades organizacionais no Google Workspace.|
| admin.reports.usage.readonly| Permite ler os relatórios de uso do Google Workspace, como a atividade do Gmail, do Google Drive e do Google Meet.|
| classroom.announcements     | Permite visualizar e gerenciar anúncios no Google Sala de Aula.  |
| classroom.courses           | Permite ver, editar, criar e excluir turmas no Google Sala de Aula. |
| classroom.coursework.students| Permite gerenciar o trabalho do curso e as notas dos alunos nas turmas do Google Sala de Aula em que você é o professor.|
| classroom.guardianlinks.students| Permite visualizar e gerenciar os responsáveis pelos alunos nas turmas do Google Sala de Aula em que você é o professor.|
| classroom.profile.emails    | Permite visualizar o endereço de e-mail de pessoas em suas turmas no Google Sala de Aula.|
| classroom.rosters           | Permite gerenciar as listas de alunos nas turmas do Google Sala de Aula em que você é o professor.|
| classroom.student-submissions.students.readonly| Permite visualizar o trabalho do curso e as notas dos alunos nas turmas do Google Sala de Aula em que você é o professor ou administrador. |
| classroom.topics            | Permite ver, criar e editar tópicos nas turmas do Google Sala de Aula.|

  
  
  
(Lista de todas as permissões)[https://developers.google.com/resources/api-libraries/documentation/classroom/v1/cpp/latest/classgoogle__classroom__api_1_1ClassroomService_1_1SCOPES.html]
</details>
</details>

## Deploy da ferramenta

<details>
<summary> Copiando o repositório </summary><br/>

Para começar, você precisará de um projeto do Google Cloud para executar o script e ter acesso de administrador do Google. Em seguida, acesse o Cloud Shell e execute o comando 

```shell
gcloud config set project <<PROJECT_ID>>
```
para configurar seu projeto. Em seguida, clone o repositório do GitHub usando o comando 
```
git clone https://github.com/InnovateEDU-NYC/google_classroom.git
```
  
</details>

<details>
<summary> Declarando variáveis </summary><br/>

No editor de arquivos do Google Shell, clique em "Exibir → Alternar arquivos ocultos" para mostrar o arquivo .env-sample na pasta do projeto. 

Crie um novo arquivo chamado .env na raiz do projeto e configure as variáveis:
```shell
mv .env-sample .env
```  
>Caso você prefira, edite os arquivos com o **nano**
  
Adicione dados as seguintes variáveis:
  
```
ACCOUNT_EMAIL =
STUDENT_ORG_UNIT =
SCHOOL_YEAR_START =
DB =
DB_SCHEMA = 
```
Descrição das variáveis:

**ACCOUNT_EMAIL** = E-mail da conta de administrador que será usada para extrair dados.

**STUDENT_ORG_UNIT** = Define a OU ou deixe em branco para obter todos os alunos

**SCHOOL_YEAR_START**= data de início da sua escola usando o formato AAAA-MM-DD (ano - mês - dia).

**DB** = defina como o ID do seu projeto do Google Cloud.

**DB_SCHEMA** = Conjunto de dados do BigQuery em que você deseja que o conector crie as tabelas do Google Sala de Aula.
</details>

<details>
<summary> Exportar service.json </summary><br/>
  
> Antes de executar o docker clique nas 3 bolinhas no menu superior do cloud shell e faça o upload do JSON da conta de serviço recém-criada. **Renomeie o arquivo para service.json**
{.is-info}

```shell
mv <nome_arquivo> service.json
```
Mais um passo é dar permissão para os arquivos .env e services.json
```shell
chmod +x .env
chmod +x service.json
```

  
</details>


<details>
<summary> Executar o docker </summary><br/>
  
  Os comandos abaixo mostrarão como criar sua imagem do Docker e executar o script. Ao usar o Cloud Shell, essas duas etapas devem ser concluídas sempre que você quiser atualizar os dados no BigQuery.

o primeiro passo é construir a imagem docker, na pasta do repositório execute o comando: 
```shell
docker build -t google_classroom .
```


Recomendamos que você primeiro execute este script com o  sinalizador **--course** para puxar apenas um subconjunto de  dados do Classroom. Isso permitirá que você verifique se tudo foi instalado e configurado corretamente.

```shell
docker run --rm -it google_classroom --courses
```
Se você receber um erro, tente adicionar o sinalizador **--debug** ao comando acima. Isso fará com que o script registre informações adicionais que podem ajudar na solução do erro.

Se o comando acima for bem-sucedido, você estará pronto para buscar dados de todos os endpoints da Classroom API.

```shell
docker run --rm -it google_classroom --all
```
> Para executar testes, execute o seguinte comando: 
```shell
docker run --rm -it google_classroom --test
```  
<details>
<summary> Lista de tags para usar com o comando  </summary><br/>
  
Abaixo estão todos os sinalizadores disponíveis para este script.
```shell
--all
--usage
--courses
--topics
--coursework
--students
--teachers
--guardians
--submissions
--invites
--aliases
--invitations
--announcements
```
  
</details>
</details>

## Opcional
  
<details>
<summary> Usando Data studio para viualizar dados </summary><br/>
  
A innovateedu também publicou um modelo de relatório do Data Studio que facilita a visualização desses dados. Depois de criar as tabelas do Google Classroom em seu BigQuery, siga as etapas abaixo para copiar nosso relatório em seu Data Studio.


### Copiar a fonta de dados 
  
Antes de poder copiar o próprio relatório, você precisará copiar a fonte de dados para sua instância do Data Studio.

[Copiar fonte de dados](https://lookerstudio.google.com/u/0/datasources/1J_nWVVc9MpiEqJGdiAN757U4j9-Oqynd)

- No canto superior direito, clique em copiar;![image](https://user-images.githubusercontent.com/110038530/232074171-2d7f0f96-4895-4c78-b5c6-fcfb14135ead.png)
- Na caixa de diálogo de confirmação, clique em Copiar fonte de dados;
- Para selecionar a sua tabela, vá em **Projetos recentes** e selecione o seu **projeto** > **conjunto de dados** > **tabela**;
- Clique em **Reconectar** > aplicar .

### Modelo de relatório

[Copiar modelo de relatório](https://lookerstudio.google.com/u/0/reporting/1_BpTpJnFGNgXBGQ3WhbgDIqDziHCNw6O/page/rUWQB/preview)
  
- Clique em **Usar meus próprios dados**;
- Selecione o seu dataset do BigQuery , vá em **Projetos recentes** e selecione o seu **projeto** > **conjunto de dados** > **tabela**;
- Clique em **Adicionar**.


É isso! Agora você pode fazer qualquer modificação que desejar no SQL por trás da fonte de dados ou no próprio relatório do Data Studio.
  
</details>

<details>
<summary> Links relacionados </summary><br/>
 
Para verificar mais projetos da landing zone [Clique aqui](https://www.landingzone.org/);

Para verificar o relatório original [Clique aqui](https://innovateedu-nyc.github.io/google_classroom/index.html);

Para acessar o Repositório github [Clique aqui](https://github.com/InnovateEDU-NYC/google_classroom).  
  
</details>  
