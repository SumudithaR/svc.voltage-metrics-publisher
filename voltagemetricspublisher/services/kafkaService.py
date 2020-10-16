import configparser
from pykafka import KafkaClient, Topic

class KafkaService():
    def __init__(self):  
        self.config = configparser.ConfigParser()
        #self.config.read('../../config/voltagemetricspublisher.ini')
        kafkaHost = "127.0.0.1:9092" 
        #self.config["kafka_settings"]["host"]
        
        try: 
            
            self.kafkaClient = KafkaClient(hosts=kafkaHost) 
            
            if self.kafkaClient is None:
                print("Failed to instantiate Kafka Client.")

        except Exception as ex:

            print('Failed to connect to Kafka Host. Host: %s' % kafkaHost)
            print(ex)
    
    def publishToTopic(self, topicName, item):
        if topicName is None:
            print('Provided Topic Name is invalid. TopicName: %s' % topicName)

        if item is None:
            print('Provided Data item is invalid.')

        rawVoltageMetricsTopic = self.kafkaClient.topics['raw-voltage-metrics']
        
        try:
        
            if rawVoltageMetricsTopic is None:
                self.kafkaClient.topics._create_topic('raw-voltage-metrics')
                rawVoltageMetricsTopic = self.kafkaClient.topics['raw-voltage-metrics']
        
            with rawVoltageMetricsTopic.get_sync_producer() as producer:
                producer.produce(item)
        
        except Exception as ex:
            
            print('Failed to publish to Kafka topic. TopicName: %s' % topicName)
            print(ex)