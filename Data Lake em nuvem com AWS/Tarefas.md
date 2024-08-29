# ***Construção de  Data Lakeem nuvem: S3 com AWS Lake Formation e Análise de dados com SQL acessando o Athena***

## Ferramentas:

AWS S3, Lake Formation, Glue e Athena.

## Comandos:
Já estão listados junto com os passos.

## Passos:

### 1- Acessar IAM e criar usuário e grupo;

### 2- Adicionar o usuário ao grupo criado;

### 3- Deslogar da AWS e acessar o endereço https://010928218238.signin.aws.amazon.com/console do usuário criado (Cria-se outro usuário para evitar o uso do Root);

### 4- Preparar a fonte de dados (Bucket S3) com o arquivo bing_covid-19_data.parquet;

### 5- Definir o adminstrador do Data Lake no console do Aws Lake Formation (Administrative roles and tasks / Data lake administrators = dsadlp1 / Database creators = IAMAllowedPrincipals);

### 6- Apontar a fonte de dados (S3) para o Lake Formation (Data lake locations);

### 7- Acessar Data locations para inferir qual usuário terá privilégio de acesso ao bucket s3;

### 8- Acessar Databases e criar o banco de dados com o arquivo do S3;

### 9- Acessar o Crawlers na intrface do Lake formation e criar a tabela;

### 10- Acessar Data Catalog > Tables no Aws Lake Formation > Actions > View Data (Vai abrir o Amazon Athena) para consultas SQL;

### 11- Criar no S3 um novo Bucket para a saída dos dados (p1-dsa-dl-saida > saída);

### 12- Acessar novamente o Athena e configurar a saída de dados com a execução de Querys da tabela.