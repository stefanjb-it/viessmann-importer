import sys
import logging
import time

from PyViCare.PyViCareGazBoiler import GazBoiler
from influxdb import InfluxDBClient
from PyViCare.PyViCare import PyViCare

# creds
client_id = ""
email = ""
password = ""

client = InfluxDBClient(host='swarm_node_2', port='8086')
client.switch_database('heating')
sys.path.insert(0, 'PyViCare')

vicare = PyViCare()
vicare.initWithCredentials(email,password,client_id,"token.save")
device = vicare.devices[0]
print(device.getModel())
print("Online" if device.isOnline() else "Offline")

t = device.asAutoDetectDevice()
print(t.getDomesticHotWaterConfiguredTemperature())
print(t.getDomesticHotWaterStorageTemperature())
print(t.getOutsideTemperature())
print(t.getBoilerTemperature())

circuit = t.circuits[1]

print(circuit.getSupplyTemperature())
print(circuit.getHeatingCurveShift())
print(circuit.getHeatingCurveSlope())

burner = t.burners[0]
print(burner.getActive())


while True:
    t = GazBoiler("", "")
    HotWaterStorageTemperature = t.getDomesticHotWaterStorageTemperature()
    BoilerTemperature = float(t.getBoilerTemperature())
    BurnerHours = float(t.getBurnerHours())
    BurnerStarts = t.getBurnerStarts()
    BurnerActive = t.getBurnerActive()
    BurnerModulation = t.getBurnerModulation()
    OutsideTemperature = float(t.getOutsideTemperature())
    print(str(HotWaterStorageTemperature) + "," + str(BoilerTemperature) + "," + str(BurnerHours) + "," +
          str(BurnerStarts) + "," + str(BurnerActive) + "," + str(BurnerModulation) + "," +
          str(OutsideTemperature))

    if (HotWaterStorageTemperature == "error") | (isinstance(HotWaterStorageTemperature, str)):
        HotWaterStorageTemperature = 0.0
    else:
        HotWaterStorageTemperature = float(HotWaterStorageTemperature)
    if (BoilerTemperature == "error") | (isinstance(BoilerTemperature, str)):
        BoilerTemperature = 0.0
    else:
        BoilerTemperature = float(BoilerTemperature)
    if (BurnerHours == "error") | (isinstance(BurnerHours, str)):
        BurnerHours = 0
    else:
        BurnerHours = float(BurnerHours)
    if (BurnerStarts == "error") | (isinstance(BurnerStarts, str)):
        BurnerStarts = 0
    else:
        BurnerStarts = int(BurnerStarts)
    if (BurnerModulation == "error") | (isinstance(BurnerModulation, str)):
        BurnerModulation = 0
    else:
        BurnerModulation = int(BurnerModulation)
    if (OutsideTemperature == "error") | (isinstance(OutsideTemperature, str)):
        OutsideTemperature = 0.0
    else:
        OutsideTemperature = float(OutsideTemperature)
    db_data = [
        {
            "measurement": "WaterStorageTemperature",
            "tags": {
                "location": "Home",
                "unit": "°C"
            },
            "fields": {
                "temperature": HotWaterStorageTemperature
            }
        },
        {
            "measurement": "BoilerTemperature",
            "tags": {
                "location": "Home",
                "unit": "°C"
            },
            "fields": {
                "temperature": BoilerTemperature
            }
        },
        {
            "measurement": "BurnerHours",
            "tags": {
                "location": "Home",
                "unit": "h"
            },
            "fields": {
                "BurnerHours": BurnerHours
            }
        },
        {
            "measurement": "BurnerStarts",
            "tags": {
                "location": "Home",
                "unit": ""
            },
            "fields": {
                "BurnerStarts": BurnerStarts
            }
        },
        {
            "measurement": "BurnerActive",
            "tags": {
                "location": "Home",
                "unit": "boolean"
            },
            "fields": {
                "BurnerActive": str(BurnerActive)
            }
        },
        {
            "measurement": "BurnerModulation",
            "tags": {
                "location": "Home",
                "unit": "%"
            },
            "fields": {
                "BurnerModulation": BurnerModulation
            }
        },
        {
            "measurement": "OutsideTemperature",
            "tags": {
                "location": "Home",
                "unit": "°C"
            },
            "fields": {
                "temperature": OutsideTemperature
            }
        }
    ]
    client.write_points(db_data)
    time.sleep(600)

