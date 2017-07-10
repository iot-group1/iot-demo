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

data format:

beacon_id

insert_time

value

--------------------------------

989394992934

7/11/2017, 12:51:21 AM

{ "beacon_id" : { "S" : "989394992934" }, "insert_time" : { "S" : "7/11/2017, 12:51:21 AM" }, "value" : { "S" : "15" } }
