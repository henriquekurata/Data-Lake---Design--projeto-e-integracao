# ***Processamento de dados com Amazon EMR***

## Ferramentas:

AWS S3 e EMR.

## Passos:
* Criar bucket S3 com pasta para "dados" e "jobs"
* Carregar os dados e o script Pyspark nas pastas organizadas;
* Criar Cluster no menu do EMR (Aplicativos - Spark , configuração cluster, VPC - usar o automático, encerramento do cluster, Logs de cluster - Adicionar o bucket criado para gravação no item anterior, Configuração de segurança e par de chaves do EC2 - Criar par de chaves tipo RSA e .ppk para Windows para liberar o acesso via máquina local, Perfis do Identity and Access Management (IAM) para conversação entre serviços AWS- Criar automaticamente, Perfil de instância do EC2 para o Amazon EMR para liberar o acesso de leitura e escrita da instancia ao bucket S3- Criar automaticamente);
* Ajustar no menu do cluster EMR "EC2 security groups (firewall)": Primary node > inbound role > add rule > SSH > 0.0.0.0./0 > para o terminal da máquina local conseguir acessar o cluster na nuvem AWS;
* Acessar o cluster EMR via linha de comando: Para Windows basta fazer a conexão com o putty.exe
* Com a conexão relizada, basta acessar a aba "steps" do cluster criado e adicionar um Spark application > Cluster mode > Application location (job.py) bucket S3 > Argumentos (adicionar a URI: --data_source s3://p3-dsa-dl-hk/dados/dataset.csv e --output_uri s3://p3-dsa-dl-hk/saida) em linhas separadas, pois no script Spark há argumentos na função def); 
* Processamento de dados com PySpark será realizado após configurações do "steps".

## Comandos:

### Dados (dataset):
name,inspection_result,inspection_closed_business,violation_type,violation_points
100 LB CLAM,Incomplete,FALSE,,0
100 LB CLAM,Unsatisfactory,FALSE,BLUE,5
100 LB CLAM,Unsatisfactory,FALSE,RED,5
100 LB CLAM,Unsatisfactory,FALSE,RED,10
100 LB CLAM,Unsatisfactory,FALSE,RED,5
100 LB CLAM,Complete,FALSE,,0
100 LB CLAM,Complete,FALSE,,0
100 PERCENT NUTRICION,Unsatisfactory,FALSE,BLUE,5
100 PERCENT NUTRICION,Unsatisfactory,FALSE,BLUE,5
100 PERCENT NUTRICION,Unsatisfactory,FALSE,RED,10
100 PERCENT NUTRICION,Unsatisfactory,FALSE,RED,5
1000 SPIRITS,Satisfactory,FALSE,BLUE,5
1000 SPIRITS,Satisfactory,FALSE,,0
1000 SPIRITS,Unsatisfactory,FALSE,RED,5
1000 SPIRITS,Complete,FALSE,,0
1000 SPIRITS,Satisfactory,FALSE,BLUE,5
1000 SPIRITS,Satisfactory,FALSE,,0
1000 SPIRITS,Unsatisfactory,FALSE,BLUE,5


### Job:

```
import argparse

from pyspark.sql import SparkSession

def calculate_red_violations(data_source, output_uri):

    with SparkSession.builder.appName("Job Projeto 3 DSA").getOrCreate() as spark:
        
        # Carrega os dados
        if data_source is not None:
            restaurants_df = spark.read.option("header", "true").csv(data_source)

        # Cria um DataFrame in-memory para executar a consulta
        restaurants_df.createOrReplaceTempView("restaurant_violations")

        # Cria um DataFrame com os Top 10 Restaurantes com mais "red violations"
        top_red_violation_restaurants = spark.sql("""SELECT name, count(*) AS total_red_violations 
          FROM restaurant_violations 
          WHERE violation_type = 'RED' 
          GROUP BY name 
          ORDER BY total_red_violations DESC LIMIT 10""")

        # Grava os resultados
        top_red_violation_restaurants.write.option("header", "true").mode("overwrite").csv(output_uri)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_source', help="A URI para o arquivo de origem no Data Lake.")
    parser.add_argument('--output_uri', help="A URI para salvar o resultado.")
    args = parser.parse_args()

    calculate_red_violations(args.data_source, args.output_uri)
			
```

