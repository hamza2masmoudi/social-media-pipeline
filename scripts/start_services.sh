#!/bin/bash

# Start Hadoop
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

# Start Kafka
$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties &
sleep 5
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties &

# Start Hive Metastore
hive --service metastore &