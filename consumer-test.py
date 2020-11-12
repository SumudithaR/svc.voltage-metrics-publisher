from kafka import KafkaConsumer

consumer = KafkaConsumer("raw-voltage-metrics", bootstrap_servers='walpola.tk:9094')
for message in consumer:
    print (message)