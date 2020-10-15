import configparser
from .core.exc import VoltageMetricsPublisherError
from .controllers.voltageMetrics import VoltageMetrics
import click

class VoltageMetricsPublisher():
    """Voltage Metrics Publisher primary application."""

    def __enter__(self):
        config = configparser.ConfigParser()
        config.read('../config/voltagemetricspublisher.ini')
        self.debug = config["app"]["debug"]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return
    
    def run(self):
        VoltageMetrics().start()
        return self

@click.command()
def main():
    with VoltageMetricsPublisher() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except VoltageMetricsPublisherError as e:
            print('VoltageMetricsPublisherError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()


# if __name__ == '__main__':
#     main()
