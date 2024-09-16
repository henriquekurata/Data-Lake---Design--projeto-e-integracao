# 🚀 ***Construção de  Data Lake em nuvem: S3, AWS Lake Formation e Análise de dados com SQL acessando o Athena***


## **Descrição do Projeto:**
Este projeto visa construir um Data Lake na nuvem utilizando AWS S3 para armazenamento, AWS Lake Formation para gerenciamento de segurança e permissões, e Amazon Athena para análise de dados com SQL. O objetivo é criar um ambiente integrado que permita o armazenamento, gerenciamento e consulta de dados de forma eficiente e segura.

A construção do Data Lake inclui a configuração do bucket S3, a definição de permissões e administradores no Lake Formation, a criação de tabelas usando o Glue, e a execução de consultas SQL no Athena para análise dos dados armazenados.

## **Resumo das Funcionalidades**

### **1. Configuração de Acesso e Segurança**
- **Criação de Usuário e Grupo IAM:** Configura um usuário e um grupo com permissões adequadas para gerenciar o Data Lake.
- **Administração Segura:** Acessa a AWS com um usuário específico, evitando o uso do root.

### **2. Preparação da Fonte de Dados**
- **Configuração do Bucket S3:** Armazena o arquivo `bing_covid-19_data.parquet` no Amazon S3 como fonte de dados para o Data Lake.

### **3. Configuração do Data Lake com AWS Lake Formation**
- **Definição de Administradores:** Configura o administrador do Data Lake e os papéis de criação de banco de dados no AWS Lake Formation.
- **Configuração de Localizações de Dados:** Aponta o bucket S3 como fonte de dados no Lake Formation.
- **Gerenciamento de Acesso:** Define quais usuários terão privilégios de acesso ao bucket S3.

### **4. Criação e Configuração de Banco de Dados**
- **Criação do Banco de Dados:** Configura um banco de dados no Lake Formation usando os dados do S3.
- **Criação de Tabelas com Crawlers:** Utiliza Crawlers para criar e estruturar a tabela a partir dos dados no S3.

### **5. Análise de Dados com Amazon Athena**
- **Consulta SQL:** Acessa o Data Catalog e utiliza o Athena para executar consultas SQL nos dados do S3.
- **Criação de Bucket de Saída:** Configura um novo bucket no S3 para armazenar os resultados das consultas.
- **Execução de Queries:** Configura o Athena para usar o novo bucket como local de saída para os resultados das consultas SQL.




## 🛠️ **Ferramentas Utilizadas**
- **AWS S3:** Serviço de armazenamento de objetos para armazenar dados brutos.
- **AWS Lake Formation:** Serviço para configurar e gerenciar o Data Lake, incluindo segurança e permissões.
- **AWS Glue:** Serviço para catalogar dados e criar tabelas.
- **Amazon Athena:** Serviço de consulta interativo que permite executar consultas SQL diretamente no S3.



## 📋 **Descrição do Processo**

1. **Configuração do IAM:**
   - Acesse o IAM e crie um usuário e um grupo para gerenciar permissões e acessos ao Data Lake.


2. **Configuração do Usuário:**
   - Adicione o usuário ao grupo criado e faça login com esse usuário (evitando o uso do Root).

   - Deslogar da AWS e acessar o endereço https://010928218238.signin.aws.amazon.com/console do usuário criado (Cria-se outro usuário para evitar o uso do Root);

3. **Preparação da Fonte de Dados:**
   - Prepare o bucket S3 com o arquivo `bing_covid-19_data.parquet` para uso no Data Lake.

4. **Administração no Lake Formation:**
   - Defina o administrador do Data Lake e configure os papéis administrativos e criadores de banco de dados. No console do Aws Lake Formation (Administrative roles and tasks / Data lake administrators = dsadlp1 / Database creators = IAMAllowedPrincipals);


5. **Configuração do Lake Formation:**
   - Apontar o bucket S3 como fonte de dados no Lake Formation e definir permissões de acesso (Data lake locations);

   - Acessar Data locations para inferir qual usuário terá privilégio de acesso ao bucket s3;

6. **Criação de Banco de Dados:**
   - Crie um banco de dados no Lake Formation utilizando o arquivo no S3(Acessar Databases);

7. **Criação de Tabela com Glue:**
   - Utilize o Glue para criar a tabela a partir dos dados no S3 (Acessar o Crawlers na intrface do Lake formation e criar a tabela);

8. **Consulta de Dados com Athena:**
   - Acesse o Data Catalog e visualize os dados com Amazon Athena (Acessar Data Catalog > Tables no Aws Lake Formation > Actions > View Data (Vai abrir o Amazon Athena) para consultas SQL);

9. **Configuração de Saída de Dados:**
   - Crie um novo bucket S3 para armazenar os resultados das consultas;

10. **Execução de Consultas SQL:**
    - Configure o Athena para usar o novo bucket como destino para as consultas SQL e execute consultas sobre os dados.


---
## Contato

Se tiver dúvidas ou sugestões sobre o projeto, entre em contato comigo:

- 💼 [LinkedIn](https://www.linkedin.com/in/henrique-k-32967a2b5/)
- 🐱 [GitHub](https://github.com/henriquekurata?tab=overview&from=2024-09-01&to=2024-09-01)
