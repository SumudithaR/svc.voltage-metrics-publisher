#!/usr/bin/python3
from pykafka import KafkaClient, Topic
import json
import time
# import datetime
from gpiozero import MCP3008  # Installed in GAM 13/09/2019.
from time import sleep       #
#


class RawMetricDto():
    voltage0 = 0
    voltage1 = 0
    voltage2 = 0
    voltage3 = 0
    voltage4 = 0
    voltage5 = 0
    voltage6 = 0
    voltage7 = 0
    deviceTime = None


vref = 3.31
topicName = "raw-voltage-metrics"

try:
    print("[ControlSystemOne]Starting Kafka Service.")
    kafkaClient = KafkaClient(hosts='walpola.tk:9092')

    if kafkaClient is None:
        print("[ControlSystemOne]Failed to instantiate Kafka Client.")

except Exception as ex:
    print("[ControlSystemOne]Failed to connect to Kafka Host.")
    print("[ControlSystemOne]" + ex)

while True:

    adc0 = MCP3008(channel=0)
    adc1 = MCP3008(channel=1)
    adc2 = MCP3008(channel=2)
    adc3 = MCP3008(channel=3)
    adc4 = MCP3008(channel=4)
    adc5 = MCP3008(channel=5)
    adc6 = MCP3008(channel=6)
    adc7 = MCP3008(channel=7)

    voltage0 = vref*4.57*adc0.value  # Battery
    voltage1 = vref*4.57*adc1.value  # Bus
    voltage2 = vref*4.57*adc2.value  # Router
    voltage3 = vref*4.57*adc3.value  # Pi7 Voltage
    voltage4 = vref*adc4.value  # XX3
    voltage5 = vref*adc5.value  # XX4
    voltage6 = vref*adc6.value  # WTL
    voltage7 = vref*adc7.value  # WLL

    localtime = time.asctime(time.localtime(time.time()))

    print("Bat1:", '{:.1f}'.format(voltage0), "V," "Bus:", '{:.1f}'.format(voltage1), "V," "Rou:",
          '{:.1f}'.format(voltage2), "V," "Bat2:", '{:.1f}'.format(voltage3), "V,", localtime)
    fo = open("/Camgam/udin/GampahaLog.txt", "a")
    L1 = ['{:.1f}'.format(voltage0), ",", '{:.1f}'.format(voltage1), ",", '{:.1f}'.format(voltage2), ",", '{:.1f}'.format(voltage3), ",", '{:.1f}'.format(
        voltage4), ",", '{:.1f}'.format(voltage5), ",", '{:.1f}'.format(voltage6), ",", '{:.1f}'.format(voltage7), ",", localtime]
    fo.writelines(L1)
    fo.write('\n')
    fo.close()

    # Metrics Publisher
    try:
        if kafkaClient is not None:
            print("[ControlSystemOne]Starting Voltage Metrics Publish.")

            model = RawMetricDto()

            model.voltage0 = voltage0  # Battery-Main
            model.voltage1 = voltage1  # Bus
            model.voltage2 = voltage2  # Router
            model.voltage3 = voltage3  # Battery-Emg.Lamps
            model.voltage4 = voltage4  # XX3
            model.voltage5 = voltage5  # XX4
            model.voltage6 = voltage6  # WTL
            model.voltage7 = voltage7  # WLL
            model.deviceTime = localtime

            rawVoltageMetricsTopic = kafkaClient.topics[topicName]

            if rawVoltageMetricsTopic is None:
                kafkaClient.topics._create_topic(topicName)
                rawVoltageMetricsTopic = kafkaClient.topics[topicName]

            with rawVoltageMetricsTopic.get_sync_producer() as producer:
                jsonModel = json.dumps(model.__dict__)
                producer.produce(bytes(jsonModel))

    except Exception as ex:
        print("[ControlSystemOne]Failed to publish Volt Metrics.")
        print("[ControlSystemOne]" + ex)

    sleep(30)
