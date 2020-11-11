import os
import configparser
from pykafka import KafkaClient, Topic

class KafkaService():
    def __init__(self):  
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(os.path.dirname(__file__), '../config', 'voltagemetricspublisher.ini'))
        kafkaHost = self.config["kafka_settings"]["host"]
        
        try: 
            print("Starting Kafka Service.")
            
            print("Kafka Host: %s" % kafkaHost)
            self.kafkaClient = KafkaClient(hosts=kafkaHost) 

            if self.kafkaClient is None:
                print("Failed to instantiate Kafka Client.")

        except Exception as ex:

            print('Failed to connect to Kafka Host. Host: %s' % kafkaHost)
            print(ex)
            raise ex
    
    def publishToTopic(self, topicName, item):
        
        print("Publishing Metrics to Kafka topic.")
        
        if topicName is None:
            print('Provided Topic Name is invalid. TopicName: %s' % topicName)

        if item is None:
            print('Provided Data item is invalid.')

        rawVoltageMetricsTopic = self.kafkaClient.topics[topicName]
        
        try:
        
            if rawVoltageMetricsTopic is None:
                self.kafkaClient.topics._create_topic(topicName)
                rawVoltageMetricsTopic = self.kafkaClient.topics[topicName]
        
            with rawVoltageMetricsTopic.get_sync_producer() as producer:
                producer.produce(item)
        
        except Exception as ex:
            
            print('Failed to publish to Kafka topic. TopicName: %s' % topicName)
            print(ex)