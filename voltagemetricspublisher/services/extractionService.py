from time import sleep
from gpiozero import MCP3008  # Installed in GAM 13/09/2019.
import time
import gpiozero
from ..models.rawMetricDto import RawMetricDto

class ExtractionService():
    def __init__(self):
        self.vref = 3.3  
        
    def getGpioValues(self) -> RawMetricDto:
        adc0 = MCP3008(channel=0)
        adc1 = MCP3008(channel=1)
        adc2 = MCP3008(channel=2)
        adc3 = MCP3008(channel=3)
        adc4 = MCP3008(channel=4)
        adc5 = MCP3008(channel=5)
        adc6 = MCP3008(channel=6)
        adc7 = MCP3008(channel=7)

        model = RawMetricDto()

        model.voltage0 = self.vref*4.57*adc0.value  # Battery-Main
        model.voltage1 = self.vref*4.57*adc1.value  # Bus
        model.voltage2 = self.vref*4.57*adc2.value  # Router
        model.voltage3 = self.vref*4.57*adc3.value  # Battery-Emg.Lamps
        model.voltage4 = self.vref*adc4.value  # XX3
        model.voltage5 = self.vref*adc5.value  # XX4
        model.voltage6 = self.vref*adc6.value  # WTL
        model.voltage7 = self.vref*adc7.value  # WLL

        model.deviceTime = time.asctime(time.localtime(time.time()))

        return model