def fetch_data():
    #!/usr/bin/python3
    User = "tdoa-project@ttn"
    Password = "NNSXS.YIFDZX6FK2DFB4X4SYBWXEUF5KBUOHLIGZAQICY.V6CKYR4KIHCDRY6WMUXFLXRL57KUGKOAGQTPL3NHBCLRHAT2456A"
    theRegion = "EU1"		# The region you are using

    VER  = "2021-05-24 v1.2"
    import os, sys, logging, time
    print(os.path.basename(__file__) + " " + VER)

    print("Imports:")
    import paho.mqtt.client as mqtt
    import json

    print("Functions:")

    # Write uplink to tab file
    def getInfos(msg):
        if("uplink_message" in msg):	
            # Metadata of lora packets
            uplink_message = msg["uplink_message"]
            rx_metadata = uplink_message["rx_metadata"]

            gateways_data = []
    
            for gateway_metadata in rx_metadata:
                gateway = dict()
                gateway["gateway_id"] = gateway_metadata["gateway_ids"]["gateway_id"]
                gateway["received_rssi"] = gateway_metadata["rssi"]
                gateways_data.append(gateway)
            
            # This will contain all the needed data for the device that sent the data to locate it
            device = dict()
            # ID of end device sending the uplink
            end_device_ids = msg["end_device_ids"]
            device_id = end_device_ids["device_id"]
    
            # True GPS coordinates of device
            alt = uplink_message["decoded_payload"]["altitude"]
            lat = uplink_message["decoded_payload"]["latitude"]
            lng = uplink_message["decoded_payload"]["longitude"]
    
            device["device_id"] = device_id
            device["location"] = {"latitude": lat, "longitude":lng, "altitude": alt}
            device["gateways"] = gateways_data
            
            # Save relevant data into a json ffile
            filename = "Geolocation/Data/chemin8A/" + str(int(time.time())) # Change the directory path here according to where you want to save your data
            with open(filename + ".json", "a") as file: # Create a JSON file for each uplink message and store it. They will be used for the tests
                json.dump(device, file, indent=4)
            return "Data saved successfully in JSON file"
        else:
            # Do nothing is the message is not in desired format
            return "Nothing to do here"

    # MQTT event functions
    def on_connect(mqttc, obj, flags, rc):
        print("\nConnect: rc = " + str(rc))

    def on_message(mqttc, obj, msg):
        print("\nMessage: " + msg.topic + " " + str(msg.qos)) # + " " + str(msg.payload))
        parsedJSON = json.loads(msg.payload)
        print(json.dumps(parsedJSON, indent=4))	# Uncomment this to fill your terminal screen with JSON
        getInfos(parsedJSON)
        
    def on_subscribe(mqttc, obj, mid, granted_qos):
        print("\nSubscribe: " + str(mid) + " " + str(granted_qos))

    print("Body of program:")

    print("Init mqtt client")
    mqttc = mqtt.Client()

    print("Assign callbacks")
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe
    mqttc.on_message = on_message

    print("Connect")
    # Setup authentication from settings above
    mqttc.username_pw_set(User, Password)

    mqttc.tls_set()	

    mqttc.connect(theRegion.lower() + ".cloud.thethings.network", 8883, 60)

    print("Subscribe")
    mqttc.subscribe("#", 0)	# all device uplinks

    print("And run forever")

    try:    
        run = True
        while run:
            mqttc.loop(10) 	# seconds timeout / blocking time
            print(".", end="", flush=True)	# feedback to the user that something is actually happening
            
    except KeyboardInterrupt:
        print("Exit")
        sys.exit(0)