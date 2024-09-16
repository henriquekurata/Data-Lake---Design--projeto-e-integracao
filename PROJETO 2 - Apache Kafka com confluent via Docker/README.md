# 🚀 ***Camada de Mensagens Kafka - Criando um Ambiente com KSQLDB para Execução de Queries SQL***

## **Descrição do Projeto:**
Este projeto configura um ambiente Kafka utilizando Docker e KSQLDB para executar consultas SQL em dados de streaming. O objetivo é criar um cluster Kafka, configurar tópicos e conectores, e usar o KSQLDB para consultar e transformar dados em tempo real.

O projeto configura um ambiente Kafka com KSQLDB para processar e consultar dados em tempo real. Utilizando Docker, você pode iniciar um cluster Kafka, criar tópicos, e executar consultas SQL sobre streams e tabelas com o KSQLDB, permitindo o processamento e análise de dados dinâmicos e em tempo real.

## 🛠️ **Ferramentas Utilizadas**
**Kafka (Confluent)**: Plataforma de mensagens distribuídas para processamento de dados em tempo real.

**KSQLDB**: Banco de dados SQL para processamento de fluxo de dados em tempo real, baseado em Kafka.

## Funcionalidades da Camada de Mensagens Kafka com KSQLDB
### **Criação e Configuração de Serviços**
- **Kafka Broker:** Gerencia comunicação e armazenamento de dados.
- **Zookeeper:** Coordena e gerencia o cluster Kafka.
- **Schema Registry:** Armazena e valida esquemas de dados.
- **Connect:** Gerencia integração de dados com Kafka.
- **Control Center:** Interface web para monitoramento e gerenciamento.
- **KSQLDB Server:** Executa consultas SQL sobre dados em Kafka.
- **KSQLDB CLI:** Interface de linha de comando para interações.
- **Rest Proxy:** Interage com Kafka via HTTP.

### **Manipulação de Dados com KSQLDB**
- **Criação de Streams:** Representa tópicos de Kafka para consultas contínuas.
- **Criação de Tabelas:** Armazena dados com atualizações e agregações.
- **Consultas e Transformações:** Visualiza, filtra e transforma dados.
- **Joins e Agregações:** Combina e agrega dados, com suporte a janelas temporais.

### **Exemplos de Consultas**
- **Seleção de Dados:** Visualização de dados em streams e tabelas.
- **Filtros e Joins:** Combinação e refinamento de dados.
- **Aggregações:** Contagem de eventos e outras funções de agregação.


## 📋 **Descrição do Processo**
1. **Configuração do Ambiente com Docker:**
   - Acesse a pasta do projeto e execute o docker-compose extraído do git direto no terminal da máquina local para criar e iniciar os containers:
     ```bash
     docker-compose up -d
     ```

2. **Acesso ao Control Center:**
   - Com os containers em execução, acesse o Control Center através do navegador em `http://localhost:9021`.

3. **Criação de Topics e Conectores:**
   - Utilize o Control Center para criar tópicos e conectores conforme necessário.
   - Acesse o KSQLDB para executar queries SQL sobre os dados.



## 🖥️ **Comandos:**

### Docker Compose para Criação de Imagens e Containers Kafka

```
---yaml
version: '2'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.3.2
    hostname: zookeeper
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  broker:
    image: confluentinc/cp-server:7.3.2
    hostname: broker
    container_name: broker
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
      - "9101:9101"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://broker:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_METRIC_REPORTERS: io.confluent.metrics.reporter.ConfluentMetricsReporter
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_CONFLUENT_LICENSE_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_CONFLUENT_BALANCER_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_JMX_PORT: 9101
      KAFKA_JMX_HOSTNAME: localhost
      KAFKA_CONFLUENT_SCHEMA_REGISTRY_URL: http://schema-registry:8081
      CONFLUENT_METRICS_REPORTER_BOOTSTRAP_SERVERS: broker:29092
      CONFLUENT_METRICS_REPORTER_TOPIC_REPLICAS: 1
      CONFLUENT_METRICS_ENABLE: 'true'
      CONFLUENT_SUPPORT_CUSTOMER_ID: 'anonymous'

  schema-registry:
    image: confluentinc/cp-schema-registry:7.3.2
    hostname: schema-registry
    container_name: schema-registry
    depends_on:
      - broker
    ports:
      - "8081:8081"
    environment:
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: 'broker:29092'
      SCHEMA_REGISTRY_LISTENERS: http://0.0.0.0:8081

  connect:
    image: cnfldemos/cp-server-connect-datagen:0.5.3-7.1.0
    hostname: connect
    container_name: connect
    depends_on:
      - broker
      - schema-registry
    ports:
      - "8083:8083"
    environment:
      CONNECT_BOOTSTRAP_SERVERS: 'broker:29092'
      CONNECT_REST_ADVERTISED_HOST_NAME: connect
      CONNECT_GROUP_ID: compose-connect-group
      CONNECT_CONFIG_STORAGE_TOPIC: docker-connect-configs
      CONNECT_CONFIG_STORAGE_REPLICATION_FACTOR: 1
      CONNECT_OFFSET_FLUSH_INTERVAL_MS: 10000
      CONNECT_OFFSET_STORAGE_TOPIC: docker-connect-offsets
      CONNECT_OFFSET_STORAGE_REPLICATION_FACTOR: 1
      CONNECT_STATUS_STORAGE_TOPIC: docker-connect-status
      CONNECT_STATUS_STORAGE_REPLICATION_FACTOR: 1
      CONNECT_KEY_CONVERTER: org.apache.kafka.connect.storage.StringConverter
      CONNECT_VALUE_CONVERTER: io.confluent.connect.avro.AvroConverter
      CONNECT_VALUE_CONVERTER_SCHEMA_REGISTRY_URL: http://schema-registry:8081
      # CLASSPATH required due to CC-2422
      CLASSPATH: /usr/share/java/monitoring-interceptors/monitoring-interceptors-7.3.2.jar
      CONNECT_PRODUCER_INTERCEPTOR_CLASSES: "io.confluent.monitoring.clients.interceptor.MonitoringProducerInterceptor"
      CONNECT_CONSUMER_INTERCEPTOR_CLASSES: "io.confluent.monitoring.clients.interceptor.MonitoringConsumerInterceptor"
      CONNECT_PLUGIN_PATH: "/usr/share/java,/usr/share/confluent-hub-components"
      CONNECT_LOG4J_LOGGERS: org.apache.zookeeper=ERROR,org.I0Itec.zkclient=ERROR,org.reflections=ERROR

  control-center:
    image: confluentinc/cp-enterprise-control-center:7.3.2
    hostname: control-center
    container_name: control-center
    depends_on:
      - broker
      - schema-registry
      - connect
      - ksqldb-server
    ports:
      - "9021:9021"
    environment:
      CONTROL_CENTER_BOOTSTRAP_SERVERS: 'broker:29092'
      CONTROL_CENTER_CONNECT_CONNECT-DEFAULT_CLUSTER: 'connect:8083'
      CONTROL_CENTER_KSQL_KSQLDB1_URL: "http://ksqldb-server:8088"
      CONTROL_CENTER_KSQL_KSQLDB1_ADVERTISED_URL: "http://localhost:8088"
      CONTROL_CENTER_SCHEMA_REGISTRY_URL: "http://schema-registry:8081"
      CONTROL_CENTER_REPLICATION_FACTOR: 1
      CONTROL_CENTER_INTERNAL_TOPICS_PARTITIONS: 1
      CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC_PARTITIONS: 1
      CONFLUENT_METRICS_TOPIC_REPLICATION: 1
      PORT: 9021

  ksqldb-server:
    image: confluentinc/cp-ksqldb-server:7.3.2
    hostname: ksqldb-server
    container_name: ksqldb-server
    depends_on:
      - broker
      - connect
    ports:
      - "8088:8088"
    environment:
      KSQL_CONFIG_DIR: "/etc/ksql"
      KSQL_BOOTSTRAP_SERVERS: "broker:29092"
      KSQL_HOST_NAME: ksqldb-server
      KSQL_LISTENERS: "http://0.0.0.0:8088"
      KSQL_CACHE_MAX_BYTES_BUFFERING: 0
      KSQL_KSQL_SCHEMA_REGISTRY_URL: "http://schema-registry:8081"
      KSQL_PRODUCER_INTERCEPTOR_CLASSES: "io.confluent.monitoring.clients.interceptor.MonitoringProducerInterceptor"
      KSQL_CONSUMER_INTERCEPTOR_CLASSES: "io.confluent.monitoring.clients.interceptor.MonitoringConsumerInterceptor"
      KSQL_KSQL_CONNECT_URL: "http://connect:8083"
      KSQL_KSQL_LOGGING_PROCESSING_TOPIC_REPLICATION_FACTOR: 1
      KSQL_KSQL_LOGGING_PROCESSING_TOPIC_AUTO_CREATE: 'true'
      KSQL_KSQL_LOGGING_PROCESSING_STREAM_AUTO_CREATE: 'true'

  ksqldb-cli:
    image: confluentinc/cp-ksqldb-cli:7.3.2
    container_name: ksqldb-cli
    depends_on:
      - broker
      - connect
      - ksqldb-server
    entrypoint: /bin/sh
    tty: true

  ksql-datagen:
    image: confluentinc/ksqldb-examples:7.3.2
    hostname: ksql-datagen
    container_name: ksql-datagen
    depends_on:
      - ksqldb-server
      - broker
      - schema-registry
      - connect
    command: "bash -c 'echo Waiting for Kafka to be ready... && \
                       cub kafka-ready -b broker:29092 1 40 && \
                       echo Waiting for Confluent Schema Registry to be ready... && \
                       cub sr-ready schema-registry 8081 40 && \
                       echo Waiting a few seconds for topic creation to finish... && \
                       sleep 11 && \
                       tail -f /dev/null'"
    environment:
      KSQL_CONFIG_DIR: "/etc/ksql"
      STREAMS_BOOTSTRAP_SERVERS: broker:29092
      STREAMS_SCHEMA_REGISTRY_HOST: schema-registry
      STREAMS_SCHEMA_REGISTRY_PORT: 8081

  rest-proxy:
    image: confluentinc/cp-kafka-rest:7.3.2
    depends_on:
      - broker
      - schema-registry
    ports:
      - 8082:8082
    hostname: rest-proxy
    container_name: rest-proxy
    environment:
      KAFKA_REST_HOST_NAME: rest-proxy
      KAFKA_REST_BOOTSTRAP_SERVERS: 'broker:29092'
      KAFKA_REST_LISTENERS: "http://0.0.0.0:8082"
      KAFKA_REST_SCHEMA_REGISTRY_URL: 'http://schema-registry:8081'

```
---

### Dentro do Kafka: localhost:9021

Criar os topics e os connects (datagen connects > name > kafka.topic (tópico) / quickstart (igual ao name))

---

### Agora é acessar o menu KsqlDB para execução de querys SQL:

```
#Crie um stream para um tópico específico no KSQLDB
#Criar um stream (objeto imutável) para um dos tópicos
CREATE STREAM pageviews_stream WITH (KAFKA_TOPIC='pageviews', VALUE_FORMAT='AVRO');

#Execute uma consulta para visualizar os dados do stream:
#Consulta ao Stream:
SELECT * FROM pageviews_stream EMIT CHANGES;

#Cria uma tabela (objeto mutável) para um dos tópicos
#Crie uma tabela para um tópico específico no KSQLDB:
CREATE TABLE users_table (id VARCHAR PRIMARY KEY) WITH (KAFKA_TOPIC='users', VALUE_FORMAT='AVRO');

#Execute uma consulta para visualizar os dados da tabela
#Select da tabela
SELECT * FROM USERS_TABLE EMIT CHANGES;

#Realize um join entre o stream e a tabela para criar um novo stream com dados combinados:
#Join do stream com a tabela
CREATE STREAM user_pageviews
  AS SELECT users_table.id AS userid, pageid, regionid, gender
    FROM pageviews_stream
    LEFT JOIN users_table ON pageviews_stream.userid = users_table.id
EMIT CHANGES;

#Execute uma consulta para visualizar os dados do novo stream:
#Select
SELECT * FROM user_pageviews EMIT CHANGES;

#Crie um novo stream filtrando dados baseados em condições específicas
#Filtrando o stream
CREATE STREAM pageviews_region_like_89
  WITH (KAFKA_TOPIC='pageviews_filtered_r8_r9', VALUE_FORMAT='AVRO')
    AS SELECT * FROM user_pageviews
    WHERE regionid LIKE '%_8' OR regionid LIKE '%_9'
EMIT CHANGES;

#Execute uma consulta para visualizar os dados do stream filtrado:
#Select
SELECT * FROM pageviews_region_like_89 EMIT CHANGES;

#Crie uma tabela para agregar dados com base em uma janela de tempo:
#Window
CREATE TABLE pageviews_per_region_89 WITH (KEY_FORMAT='JSON')
  AS SELECT userid, gender, regionid, COUNT(*) AS numusers
    FROM pageviews_region_like_89
    WINDOW TUMBLING (SIZE 30 SECOND)
    GROUP BY userid, gender, regionid
    HAVING COUNT(*) > 1
EMIT CHANGES;


#Execute uma consulta para visualizar os dados agregados
#Select
SELECT * FROM pageviews_per_region_89 EMIT CHANGES;

```

---
## Contato

Se tiver dúvidas ou sugestões sobre o projeto, entre em contato comigo:

- 💼 [LinkedIn](https://www.linkedin.com/in/henrique-k-32967a2b5/)
- 🐱 [GitHub](https://github.com/henriquekurata?tab=overview&from=2024-09-01&to=2024-09-01)