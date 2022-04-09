import serial
import sys
import json
import requests

if len(sys.argv) != 4:
    print("Invalid Number of Command Line Arguments\n")
    print("Usage:\n")
    print("    python EnvironmentSensor.py <BT Device Path> <Sensor ID> <Sensor Server URL>\n")
else:
    print("ENVIRONMENTAL SENSOR PUSH SCRIPT v1.0")
    print("------------------------------------------")
    print("Hardware   : Sensors with RTC")
    print("Device     : " + sys.argv[1])
    print("Sensor ID  : " + sys.argv[2])
    print("Server URL : " + sys.argv[3])
    ser = serial.Serial(sys.argv[1])
    while True:
        try:
            data = ser.readline().decode().replace("\n", "")
            print("Data Received : " + data)
            dataPacket = data.split("|")
            if len(dataPacket) != 3:
                print("Invalid Data Received, will be ignored")
            else:
                dataDict = {
                    "paramName": dataPacket[0],
                    "paramValue": dataPacket[1],
                    "paramTime": dataPacket[2],
                    "sensorId": sys.argv[2]
                }
                jsonPacket = json.dumps(dataDict)
                print("JSON Data: " + jsonPacket)
                response = requests.post(sys.argv[3], json=dataDict)
                if response.status_code != 200:
                    print("Service Error : Return Code is " + str(response.status_code))
                else:
                    print("DATA SENT OK")
        except KeyboardInterrupt:
            print("Closing Down")
            del ser
            sys.exit()
sys.exit()
