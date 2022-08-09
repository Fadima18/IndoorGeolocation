VER  = "2021-05-24 v1.2"
import os, sys, logging, time
import paho.mqtt.client as mqtt
import json
import threading
import pickle

from .models import Position

# room_coordinates = {
#         'Tidiane': [14.795032593150454, -16.965048462152478], 
#         'Aziz': [14.795003742888513, -16.96504008024931], 
#         'Fasou': [14.795038103874212, -16.965012587606907],
#         'Assane': [14.794998880484428, -16.96500051766634], 
#         'Fallou': [14.795044587078454, -16.964992471039295],
#         'Ass': [14.795006984491168, -16.9649800658226],
#         'Mor': [14.795058850127111, -16.964958608150482], 
#         'Youssou': [14.795032268990242, -16.964949555695057],
#         'Empty_room': [14.795066954131599, -16.964938156306744],
#         'Bachir': [14.795037455553775, -16.96492776274681],
#         'Mounir': [14.795072140694318, -16.964903622865677],
#         'Moustapha': [14.795034213951578, -16.964890882372856],
#         'Khadre': [14.795007956971958, -16.965119540691376],
#         'Moussa': [14.794975540943344, -16.965108141303062],
#         'Naby': [14.795059174287298, -16.965147703886032],
#         'Dieme': [14.79495673964453, -16.96513496339321],
#         'Cheikh': [14.794988507355377, -16.965169161558148],
#         'Saliou': [14.794948311475569, -16.96515642106533],
#         'Elimane': [14.794948959796272, -16.96518927812576],
#         'Balla': [14.794981375828854, -16.965199336409565],
#         'Malick': [14.79497618926396, -16.965220794081688],
#         'Massamba': [14.794943773230601, -16.96521006524563],
#         'Kaba': [14.79492367528749, -16.965242251753807],
#         'Ameth': [14.794961926209883, -16.965256333351135],
#         'Chemin10_A': [14.795071492373983, -16.964921057224274],
#         'Chemin10_B': [14.795034862272027, -16.964908987283707],
#         'Door10': [14.795092562783811, -16.96492675691843],
#         'Chemin9_A': [14.79505560852522, -16.964977383613586],
#         'Chemin9_B': [14.795018330100092, -16.964964978396893],
#         'Door9': [14.795075058135794, -16.96498341858387],
#         'Chemin8_A': [14.795001797926897, -16.96501828730106],
#         'Chemin8_B': [14.795001797926897, -16.96501828730106],
#         'Door8': [14.795059174287298, -16.96503572165966],
#         'Chemin7_A': [14.795005039529578, -16.965134628117085],
#         'Chemin7_B': [14.79497035437831, -16.96512322872877],
#         'Door7': [14.79502610994587, -16.965140663087368],
#         'Chemin6_A': [14.7949875348745, -16.965184584259987],
#         'Chemin6_B': [14.794952201399754, -16.965173855423927],
#         'Door6': [14.795010550254036, -16.96519162505865],
#         'Chemin5_A': [14.794972299340218, -16.965236216783524],
#         'Chemin5_B': [14.79493631754225, -16.965225487947464],
#         'Door5': [14.794994018080255, -16.965243257582188],
#         'Chemin5_B': [14.79493631754225, -16.965225487947464],
#         'Door5': [14.794994018080255, -16.965243257582188]
# }

room_coordinates = {
    'Chambre5': [14.795050746122305, -16.964914351701736],
    'Chambre6': [14.795036483073138, -16.964970007538795],
    'Chambre7': [14.795019626741068, -16.96502298116684],
    'Chambre8': [14.79498461743184, -16.96512758731842],
    'Chambre9': [14.794969706057682, -16.965179219841954],
    'Chambre10': [14.794952849720433, -16.965229511260983]
}

model = pickle.load(open('indoorGeolocation/chamodel.pkl', 'rb'))
file = 1

class TTNRequest:
    
    rssi_data = dict()
    position = list()
        
    User = "tdoa-project@ttn"
    Password = "NNSXS.YIFDZX6FK2DFB4X4SYBWXEUF5KBUOHLIGZAQICY.V6CKYR4KIHCDRY6WMUXFLXRL57KUGKOAGQTPL3NHBCLRHAT2456A"
    theRegion = "EU1"		# The region you are using

    # Write uplink to tab file
    @staticmethod
    def getRssiData(msg):
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
                
            if(len(gateway_metadata) == 3):
                gateway1 = (list(filter(lambda gateway: gateway["gateway_id"] == "last-gateway" or gateway["gateway_id"] == "final-gateway", gateway_metadata)))[0]
                gateway2 = (list(filter(lambda gateway: gateway["gateway_id"] == "gateway5projettrans", gateway_metadata)))[0]
                gateway3 = (list(filter(lambda gateway: gateway["gateway_id"] == "gatewayfourprojettrans", gateway_metadata)))[0]
            
                TTNRequest.rssi_data["rssi1"] = gateway1["received_rssi"]
                TTNRequest.rssi_data["rssi2"] = gateway2["received_rssi"]
                TTNRequest.rssi_data["rssi3"] = gateway3["received_rssi"]
                
                global file
                filename = "indoorGeolocation/Data/test/" + str(file) 
            else:
                print("Less than 3 gateways received the packet")
        else:
            pass

    # MQTT event functions
    @staticmethod
    def on_connect(mqttc, obj, flags, rc):
        print("\nConnect: rc = " + str(rc))

    @staticmethod
    def on_message(mqttc, obj, msg):
        print("\nMessage: " + msg.topic + " " + str(msg.qos)) # + " " + str(msg.payload))
        parsedJSON = json.loads(msg.payload)
        TTNRequest.getRssiData(parsedJSON)
        position = model.predict(TTNRequest.rssi_data)
        new_position = Position(x=position[0], y=position[1], device_id=1)
        new_position.save()
    
    @staticmethod
    def on_subscribe(mqttc, obj, mid, granted_qos):
        print("\nSubscribe: " + str(mid) + " " + str(granted_qos))

    @staticmethod
    def fetch_data():
        mqttc = mqtt.Client()
        mqttc.on_connect = TTNRequest.on_connect
        mqttc.on_subscribe = TTNRequest.on_subscribe
        mqttc.on_message = TTNRequest.on_message

        # Setup authentication from settings above
        mqttc.username_pw_set(TTNRequest.User, TTNRequest.Password)
        mqttc.tls_set()	
        mqttc.connect(TTNRequest.theRegion.lower() + ".cloud.thethings.network", 8883, 60)
        mqttc.subscribe("#", 0)	# all device uplinks
        print("All is done, now run forever")

        try:    
            run = True
            while run:
                mqttc.loop(10) 	# seconds timeout / blocking time
                print(".", end="", flush=True)	# feedback to the user that something is actually happening
                
        except KeyboardInterrupt:
            print("Exit")
            sys.exit(0)

if __name__=="__main__":
    th = threading.Thread(target=TTNRequest.fetch_data)
    th.start()