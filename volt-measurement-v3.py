#!/usr/bin/python3
from kafka import KafkaProducer
#import socket
import json
#import time
# import datetime
from gpiozero import MCP3008  # Installed in GAM 13/09/2019.
from time import sleep       #
#import threading
#import sched
import time
#


class RawMetricDto():
    voltage0 = 0.0
    voltage1 = 0.0
    voltage2 = 0.0
    voltage3 = 0.0
    voltage4 = 0.0
    voltage5 = 0.0
    voltage6 = 0.0
    voltage7 = 0.0
    deviceTime = ""


debug = False
vref = 3.31
topicName = "raw-voltage-metrics"
kafkaProducer = None
#fileLock = threading.Lock()
#mcpLock = threading.Lock()
schedulerInterval = 30

try:
    if(debug):
        print("[ControlSystemOne] Starting Kafka Service.")

    kafkaProducer = KafkaProducer(
        bootstrap_servers='walpola.tk:9094', batch_size=0)

except Exception as ex:
    if(debug):
        print("[ControlSystemOne] Failed to connect to Kafka Host.")
        print(ex)


# def on_send_success(record_metadata):
#     if(debug):
#         print(record_metadata.topic)
#         print(record_metadata.partition)
#         print(record_metadata.offset)


# def on_send_error(excp):
#     if(debug):
#         #log.error('I am an errback', exc_info=excp)
#         # # handle exception
#         print(excp)
def getDigitalValue(channel):
    try:
        adc = MCP3008(channel=channel)
        adcValue = adc.value
        adc.close()
        return adcValue
    except Exception as ex:
        print(ex)


while True:

    adc0 = getDigitalValue(0)
    adc1 = getDigitalValue(1)
    adc2 = getDigitalValue(2)
    adc3 = getDigitalValue(3)
    adc4 = getDigitalValue(4)
    adc5 = getDigitalValue(5)
    adc6 = getDigitalValue(6)
    adc7 = getDigitalValue(7)

    voltage0 = vref*4.57*adc0  # Battery
    voltage1 = vref*4.57*adc1  # Bus
    voltage2 = vref*4.57*adc2  # Router
    voltage3 = vref*4.57*adc3  # Pi7 Voltage
    voltage4 = vref*adc4  # XX3
    voltage5 = vref*adc5  # XX4
    voltage6 = vref*adc6  # WTL
    voltage7 = vref*adc7  # WLL

    localtime = time.asctime(time.localtime(time.time()))

    print("Bat1:", '{:.1f}'.format(voltage0), "V," "Bus:", '{:.1f}'.format(voltage1), "V," "Rou:",
          '{:.1f}'.format(voltage2), "V," "Bat2:", '{:.1f}'.format(voltage3), "V,", localtime)
    fo = open("/Camgam/udin/GampahaLog.txt", "a")
    L1 = ['{:.1f}'.format(voltage0), ",", '{:.1f}'.format(voltage1), ",", '{:.1f}'.format(voltage2), ",", '{:.1f}'.format(voltage3), ",", '{:.1f}'.format(
        voltage4), ",", '{:.1f}'.format(voltage5), ",", '{:.1f}'.format(voltage6), ",", '{:.1f}'.format(voltage7), ",", localtime]
    fo.writelines(L1)
    fo.write('\n')
    fo.close()

    try:
        if kafkaProducer is not None:
            if(debug):
                print("[ControlSystemOne] Starting Voltage Metrics Publish.")

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

            jsonModel = json.dumps(model.__dict__)
            jsonBytes = bytes(jsonModel, 'utf-8')
            # .add_callback(on_send_success).add_errback(on_send_error)
            kafkaProducer.send(topic=topicName, value=jsonBytes)

            if(debug):
                print("[ControlSystemOne] Metrics Publish Complete.")

    except Exception as ex:
        if(debug):
            print("[ControlSystemOne] Failed to publish Volt Metrics.")
            print(ex)

    sleep(30)


# def getVoltages():
#     extractionScheduler.enter(schedulerInterval, 0, getVoltages)

    # if(adc0 is None or adc1 is None or adc2 is None or adc3 is None or adc4 is None or adc5 is None or adc6 is None or adc7 is None):
    #     return


# extractionScheduler = sched.scheduler(time.time, time.sleep)
# extractionScheduler.enter(schedulerInterval, 0, getVoltages)
# extractionScheduler.run()
