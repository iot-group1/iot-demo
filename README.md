# Beacon

Main entry: app.js


Prerequisite:

Os: raspbian

nodejs(npm) 6.11.0

install modules: bluetooth,bluez,libbluetooth-dev,libudev-dev

sudo apt-get install bluetooth bluez libbluetooth-dev libudev-dev

install blean(iBean module)

npm install bleacon

# AWS-IoT

topic: iot-demo

rule:   DynamoDB

SELECT * FROM 'iot_demo'

talbe name : beacon_rfid

Partition Key: beacon_id, type: STRING, value:${beacon_ID}

Sort Key: insert_time, type:STRING, value${insert_time}

role: awsiot_admin
