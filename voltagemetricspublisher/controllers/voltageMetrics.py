from ..core.version import get_version
import threading
from ..services.extractionService import ExtractionService
from ..services.kafkaService import KafkaService
import click_config_file
import configparser

VERSION_BANNER = """Console Application to publish Voltage Metrics to Kafka. %s """ % (get_version(),)

class VoltageMetrics():
    class Meta:
        label = 'Voltage Metrics'

        # text displayed at the top of --help output
        #description = 'Console Application to publish Voltage Metrics to Kafka.'

        # text displayed at the bottom of --help output
        #epilog = 'Usage: voltagemetricspublisher command1 --foo bar'

        # controller level arguments. ex: 'voltagemetricspublisher --version'
        # arguments = [
        #     # add a version banner
        #     (['-v', '--version'],
        #      {'action': 'version',
        #         'version': VERSION_BANNER}),
        # ]

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('../../config/voltagemetricspublisher.ini')
        self.kafkaService = KafkaService()
        self.extractionService = ExtractionService()

    
    def start(self):
        """Starting Voltage Metrics Publish."""
        threading.Timer(1.0, self.start).start()

        extractedMetrics = self.extractionService.getGpioValues()
        self.kafkaService.publishToTopic(self.config["kafka_settings"]["topic_name"], extractedMetrics)