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
			