# ***Configuração de ambiente Hadoop com Docker***

## Ferramentas: 

Docker e Hadoop.

## Passos:
* Download do Hadoop e JDK;
* Criar o container com o dockerfile;
* Fazer ajustes no container;
* Inicializar o namenode e os datanodes.

## 🖥️ Comandos:

### Preparação do NameNode

1. **Download e Configuração**:
   - Baixe o Apache Hadoop e o JDK 8.
   - Coloque os arquivos na pasta "binarios", descompacte-os e renomeie as pastas para "hadoop" e "jdk".
   
   **Obs:** Faça o download diretamente na documentação do Hadoop e Java.

   - Abra o terminal ou prompt de comando, navegue até a pasta do NameNode e execute o comando para criar a imagem:
   - 
     docker build . -t namenode:dsa
     

2. **Dockerfile para o NameNode**:

```
#https://hub.docker.com/_/ubuntu
FROM ubuntu:latest

#Updates e instalações
RUN \
  apt-get update && apt-get install -y \
  openssh-server \
  python3 \
  rsync \
  sudo \
  arp-scan \
  net-tools \
  iputils-ping \
  vim \
  && apt-get clean

#Cria usuário para a instalação do Hadoop
RUN useradd -m hduser && echo "hduser:supergroup" | chpasswd && adduser hduser sudo && echo "hduser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && cd /usr/bin/ && sudo ln -s python3 python

#Copia o arquivo de configuração do ssh
ADD ./config-files/ssh_config /etc/ssh/ssh_config

#Muda o usuário
USER hduser

#Pasta de trabalho
WORKDIR /home/hduser

#Cria a chave ssh
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && chmod 0600 ~/.ssh/authorized_keys

#Usuário de trabalho
ENV HDFS_NAMENODE_USER=hduser
ENV HDFS_DATANODE_USER=hduser
ENV HDFS_SECONDARYNAMENODE_USER=hduser
ENV YARN_RESOURCEMANAGER_USER=hduser
ENV YARN_NODEMANAGER_USER=hduser

#Copia os binários do JDK
ADD ./binarios/jdk ./jdk

#Variáveis de ambiente JDK
ENV JAVA_HOME=/home/hduser/jdk
ENV PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin

#Copia os binários do Hadoop
ADD ./binarios/hadoop ./hadoop

#Variáveis de ambiente do Hadoop
ENV HADOOP_HOME=/home/hduser/hadoop
ENV PATH=$PATH:$HADOOP_HOME
ENV PATH=$PATH:$HADOOP_HOME/bin
ENV PATH=$PATH:$HADOOP_HOME/sbin

#Pastas para os arquivos do NameNode
RUN mkdir /home/hduser/hdfs
RUN mkdir /home/hduser/hdfs/namenode

#Variáveis de ambiente
RUN echo "PATH=$PATH:$JAVA_HOME/bin" >> ~/.bashrc
RUN echo "PATH=$PATH:$HADOOP_HOME/bin" >> ~/.bashrc
RUN echo "PATH=$PATH:$HADOOP_HOME/sbin" >> ~/.bashrc

#Copia os arquivos de configuração
ADD ./config-files/hadoop-env.sh $HADOOP_HOME/etc/hadoop/
ADD ./config-files/core-site.xml $HADOOP_HOME/etc/hadoop/
ADD ./config-files/hdfs-site.xml $HADOOP_HOME/etc/hadoop/
ADD ./config-files/workers $HADOOP_HOME/etc/hadoop/

#Portas que poderão ser usadas
EXPOSE 50070 50075 50010 50020 50090 8020 9000 9864 9870 8030 8031 8032 8033 8040 8042 22

``` 

#### Documentação do `docker build`:
https://docs.docker.com/engine/reference/commandline/build/

3. **Precisaremos de uma rede. Verifique as redes disponíveis e então crie uma com as instruções abaixo:**

docker network ls

docker network create -d bridge dsa_dl_net

4. **Crie e inicialize o container com a instrução abaixo:**

docker run -it -d --net dsa_dl_net --hostname hdpmaster -p 9870:9870 -p 50030:50030 -p 8020:8020 --name namenode namenode:dsa 

#Documentação do docker run:
https://docs.docker.com/engine/reference/commandline/run/

5. **Acesse o container usando a CLI no Docker Desktop e execute os seguintes comandos:**

#Restart do serviço ssh

sudo service ssh restart

#Ajuste dos privilégios

sudo chown -R hduser:hduser /home/hduser/jdk

sudo chown -R hduser:hduser /home/hduser/hadoop

#Formate o NameNode (somente na primeira execução)

hdfs namenode -format

#Start do serviço do NameNode

hdfs --daemon start namenode

#Se precisar parar o serviço:

hdfs --daemon stop namenode

#Acesse: http://localhost:9870/

#### Obs: Para mais informações sobre os arquivos de configurações do hadoop, basta acessar o site http://apache.github.io/hadoop/ na aba configuration


### Preparação dos DataNodes

1. **Faça o download do Apache Hadoop e do JDK 8, coloque na pasta "binarios", descompacte os arquivos e renomeie as pastas. O procedimento é o mesmo do namenode.**

2. **Abra o terminal ou prompt de comando, navegue até a pasta do DataNode e execute a instrução abaixo para criar a imagem:**
docker build . -t datanode:dsa

#Arquivo de Configuração do DataNode no Cluster HDFS

#O sistema operacional será o Ubuntu na versão mais atual

#https://hub.docker.com/_/ubuntu
FROM ubuntu:latest

```
#Updates e instalações
RUN \
  apt-get update && apt-get install -y \
  openssh-server \
  python3 \
  rsync \
  sudo \
  arp-scan \
  net-tools \
  iputils-ping \
  vim \
  && apt-get clean

#Cria usuário para a instalação do Hadoop
RUN useradd -m hduser && echo "hduser:supergroup" | chpasswd && adduser hduser sudo && echo "hduser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && cd /usr/bin/ && sudo ln -s python3 python

#Copia o arquivo de configuração do ssh
ADD ./config-files/ssh_config /etc/ssh/ssh_config

#Muda o usuário
USER hduser

#Pasta de trabalho
WORKDIR /home/hduser

#Usuário de trabalho
ENV HDFS_NAMENODE_USER=hduser
ENV HDFS_DATANODE_USER=hduser
ENV HDFS_SECONDARYNAMENODE_USER=hduser
ENV YARN_RESOURCEMANAGER_USER=hduser
ENV YARN_NODEMANAGER_USER=hduser

#Copia os binários do JDK
ADD ./binarios/jdk ./jdk

#Variáveis de ambiente JDK
ENV JAVA_HOME=/home/hduser/jdk
ENV PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin

#Copia os binários do Hadoop
ADD ./binarios/hadoop ./hadoop

#Variáveis de ambiente do Hadoop
ENV HADOOP_HOME=/home/hduser/hadoop
ENV PATH=$PATH:$HADOOP_HOME
ENV PATH=$PATH:$HADOOP_HOME/bin
ENV PATH=$PATH:$HADOOP_HOME/sbin

#Pastas para os arquivos do DataNode
RUN mkdir /home/hduser/hdfs
RUN mkdir /home/hduser/hdfs/datanode

#Copia os arquivos de configuração
ADD ./config-files/hadoop-env.sh $HADOOP_HOME/etc/hadoop/
ADD ./config-files/core-site.xml $HADOOP_HOME/etc/hadoop/
ADD ./config-files/hdfs-site.xml $HADOOP_HOME/etc/hadoop/
ADD ./config-files/workers $HADOOP_HOME/etc/hadoop/

#Portas que poderão ser usadas
EXPOSE 22

```

#Documentação do `docker build`:
https://docs.docker.com/engine/reference/commandline/build/

3. **Precisaremos de uma rede. Verifique se a rede `dsa_dl_net` criada no capítulo anterior está criada:**
docker network ls

4. **Crie e inicialize o container de cada datanode (criaremos 2) com cada instrução abaixo:**
docker run -it -d --net dsa_dl_net --hostname datanode1 --name datanode1 datanode:dsa

docker run -it -d --net dsa_dl_net --hostname datanode2 --name datanode2 datanode:dsa

#Documentação do docker run:
https://docs.docker.com/engine/reference/commandline/run/

5. **Acesse cada container usando a CLI no Docker Desktop e execute as instruções abaixo:**

##### Restart do serviço ssh

sudo service ssh restart

##### Ajuste dos privilégios

sudo chown -R hduser:hduser /home/hduser/jdk

sudo chown -R hduser:hduser /home/hduser/hadoop

##### Crie a pasta ~/.ssh

mkdir ~/.ssh

##### Crie o arquivo ~/.ssh/authorized_keys

touch ~/.ssh/authorized_keys

##### Ajuste o privilégio

chmod 600 ~/.ssh/authorized_keys

##### Copie a chave que está em /home/hduser/.ssh/authorized_keys no NameNode para o mesmo arquivo em cada datanode.

####Start do serviço do DataNode

hdfs --daemon start datanode

##### Se precisar parar o serviço:

hdfs --daemon stop datanode

##### Acesse o painel de gestão pelo navegador

Obs: Se não funcionar o endereço 0.0.0.0 use localhost

Obs: Para inicializar o datanode é necessário limpar a pasta /home/hduser/hdfs/datanode/ (sudo rm -rf *)

