# 🚀 ***Multi-Broker Kafka Cluster com Docker: Producer e Consumer com Linguagem Python***

## **Descrição do Projeto:**
Este projeto configura um cluster Kafka multi-broker utilizando Docker e integra produtores e consumidores de dados escritos em Python. O objetivo é criar um cluster Kafka com múltiplos brokers, configurar tópicos e streams, e utilizar scripts em Python para produzir e consumir dados.

## **Resumo das Funcionalidades**

### **1. Configuração do Cluster Kafka**
- **Criação de Containers:** Configura um cluster Kafka com múltiplos brokers e um Zookeeper usando Docker.
- **Containers Utilizados:**
  - **Zookeeper:** Gerencia o cluster Kafka.
  - **Brokers Kafka:** Armazenam e gerenciam mensagens.

### **2. Gerenciamento de Tópicos**
- **Criação de Tópicos:** Define e gerencia tópicos onde as mensagens são publicadas e consumidas.
- **Verificação de Tópicos:** Confirma a existência e as características dos tópicos criados.

### **3. Produção e Consumo de Dados**
- **Produzindo Dados:**
  - **Producer (Python):** Script que publica mensagens em um tópico Kafka.
  - **Integração:** Envia registros de dados e confirma a entrega.
- **Consumindo Dados:**
  - **Consumer (Python):** Script que lê e processa mensagens de um tópico Kafka.
  - **Integração:** Recebe e exibe mensagens consumidas.

### **4. Testes e Validações**
- **Testes de Integração:** Verifica a comunicação entre diferentes brokers e a integridade da transmissão de mensagens.
- **Execução de Scripts:** Executa scripts Python em containers para testar a produção e o consumo de mensagens.

### **5. Ambiente de Desenvolvimento**
- **Setup do Container Cliente:**
  - **Ambiente Python:** Instala dependências necessárias e configura scripts para teste.
  - **Execução dos Scripts:** Rodar scripts de producer e consumer para verificar o funcionamento do cluster Kafka.


## 🛠️ **Ferramentas Utilizadas**
- **Docker:** Plataforma para criar e gerenciar containers.
- **Kafka:** Sistema de mensagens distribuídas.
- **Python:** Linguagem de programação para criar os scripts de producer e consumer.

## 📋 **Descrição do Processo**
* Criar container zookeeper e brocker;
* Criar tópico e streams para producer e consumer;
* Acessar terminal externo do container broker e verificar a integração da camada de mensagens;
* Criar container cliente;
* Criar arquivos para producer e consumer;
* Acessar o terminal externo do container cliente e verificar a integração da camada de mensagens (executar `python producer.py` e `python consumer.py`).



## 📋 **Comandos:**

### Criando container zookeeper

1. *Abra o prompt de comando ou terminal e execute o comando abaixo para criar o container do Zookeeper, o gerenciador do cluster Kafka.*

docker run -d --name zookeeper2 --network dsa_dl_net -e ZOOKEEPER_CLIENT_PORT=2181 confluentinc/cp-zookeeper:latest

#Criando containers brockers

2. *Abra o prompt de comando ou terminal e execute os comandos abaixo para criar os containers Kafka, os brokers do cluster.*

docker run -d --name kafka-1 --network dsa_dl_net -p 9092:9092 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka-1:9092 -e KAFKA_BROKER_ID=1 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=2 -e KAFKA_ZOOKEEPER_CONNECT=zookeeper2:2181 confluentinc/cp-kafka:latest

docker run -d --name kafka-2 --network dsa_dl_net -p 9093:9092 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka-2:9092 -e KAFKA_BROKER_ID=2 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=2 -e KAFKA_ZOOKEEPER_CONNECT=zookeeper2:2181 confluentinc/cp-kafka:latest

---

### Criando Tópico no Kafka

1. *Acesse o terminal de um dos containers Kafka e execute os comandos abaixo:*

bash

cd /usr/bin

ls -la kafka*

./kafka-topics --create --bootstrap-server kafka-1:9092 --replication-factor 2 --partitions 1 --topic lab6

./kafka-topics --list --bootstrap-server kafka-1:9092

./kafka-topics --describe --bootstrap-server kafka-1:9092 --topic lab6

---

### Acessando o Tópico do Segundo Broker Kafka

1. *Acesse o terminal do outro container Kafka e execute os comandos abaixo:*

bash
cd /usr/bin

ls -la kafka*

./kafka-topics --list --bootstrap-server kafka-2:9092

./kafka-topics --describe --bootstrap-server kafka-2:9092 
--topic lab6

---

### Produzindo Streams de Dados Para o Kafka

1. *Acesse o terminal do container kafka-1 e execute os comandos abaixo:*

bash
cd /usr/bin

./kafka-console-producer --bootstrap-server kafka-1:9092 --topic lab6

---

### Consumindo Streams de Dados do Kafka

1. *Acesse o terminal do container kafka-2 e execute os comandos abaixo:*

bash

cd /usr/bin

./kafka-console-consumer --bootstrap-server kafka-2:9092 --topic lab6 --from-beginning

---

### Produzindo e Consumindo Stream de Dados do Cluster Kafka com Linguagem Python

1. *Acesse o terminal da sua máquina e execute o comando abaixo para criar o container cliente:*

docker run -dit --name cliente --network dsa_dl_net ubuntu

2. *Execute o terminal do container e execute os comandos abaixo para preparar o ambiente:*

apt-get update

apt install wget curl vim nano default-jdk

cd ~

mkdir Lab6

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

bash Minicondpython

pip install confluent-kafka

---

### Crie os scripts `producer.py` e `consumer.py` na pasta Lab6

#Producer

```
#Producer
from confluent_kafka import Producer

def delivery_report(err, msg):
    if err is not None:
        print('Entrega da mensagem falhou: {}'.format(err))
    else:
        print('Mensagem entregue com sucesso no tópico [{}]'.format(msg.topic()))

bootstrap_servers = '172.19.0.3:9092,172.19.0.4:9092'
topic = 'lab6'

conf = {'bootstrap.servers': bootstrap_servers}
producer = Producer(conf)

for i in range(10):
    message = f'registro_maquina {i}'
    producer.produce(topic, key=str(i), value=message, callback=delivery_report)
    producer.poll(0)

producer.flush()

```

# Consumer
```
# Consumer
from confluent_kafka import Consumer, KafkaError

bootstrap_servers = '172.19.0.3:9092,172.19.0.4:9092'
group_id = 'test_group'
topic = 'lab6'

conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest',
}

consumer = Consumer(conf)
consumer.subscribe([topic])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print('Erro ao consumir a mensagem: {}'.format(msg.error()))
    else:
        print('Mensagem recebida: {}'.format(msg.value().decode('utf-8')))

```

### Inicialize a leitura dos arquivos de producer e consumer em terminais diferentes: 
1. *Abra um terminal externo e execute:*
   
   python producer.py

2. *Em outro terminal externo, execute:*

python consumer.py


---
## Contato

Se tiver dúvidas ou sugestões sobre o projeto, entre em contato comigo:

- 💼 [LinkedIn](https://www.linkedin.com/in/henrique-k-32967a2b5/)
- 🐱 [GitHub](https://github.com/henriquekurata?tab=overview&from=2024-09-01&to=2024-09-01)
