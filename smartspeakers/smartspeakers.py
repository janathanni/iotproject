from numpy import true_divide
import requests
from gpiozero import LED
from gpiozero import Button
from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd
import soundfile as sf
import io
import json
from time import sleep
import pyupbit
import paho.mqtt.client as mqtt
from threading import Thread
from food_repository import food_list, food_category
import sys
sys.path.append(r'/home/pi/workspace/phone_lock')               # 각자의 디렉토리를 작성해주세요.
# from ..Dong import controller1
from Dong import controller1 
from firecaution import firealarm
from cctv import ex_scene_adjustment





button = Button(21)
red = LED(16)
green = LED(20)
blue = LED(12)
yellow = LED(19)
seconds = 5
fs = 16000
mqtt_msg = ""
kakao_audio_url =  "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
openweather_api_url = "https://api.openweathermap.org/data/2.5/"
kakao_speech_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize" 
API_KEY = '218c73d60692af6965fa11c043c3bf2d'
rest_api_key = '0cc8a9986f19c2206904038cf941e3c7'
HEADERS = {
    "Content-Type" : "application/xml",
    "Authorization" : "KakaoAK 0cc8a9986f19c2206904038cf941e3c7"
}
headers_speech = {
    "Content-Type": "application/octet-stream",
    "X-DSS-Service": "DICTATION",
    "Authorization": "KakaoAK "+ rest_api_key,
    }


def get_weather(city='Seoul'):
    URL = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}&lang=kr&units=metric'
    weather = {}
    res = requests.get(URL)
    if res.status_code == 200:
        result = res.json()
        weather['main'] = result['weather'][0]['main']
        weather['description'] = result['weather'][0]['description']
        icon = result['weather'][0]['icon']
        weather['icon'] = f'http://openweathermap.org/img/w/{icon}.png'
        weather['etc'] = result['main']
        weather['coord'] = result['coord']
    else:
        print('error', res.status_code)
    return weather

def getNowAirPollution(pos_lat, pos_lon):  
    url_total = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={pos_lat}&lon={pos_lon}&appid={API_KEY}'

    airpollution = {}
    res = requests.get(url_total)

    if res.status_code == 200:
        result = res.json()
        airpollution['airpollution'] = result['list'][0]['main']['aqi']
    else:
        print('error', res.status_code)


    return airpollution
    

    

weather = get_weather('Seoul')
airpollution = getNowAirPollution(weather['coord']['lat'],weather['coord']['lon'])


def question():
    DATA = """
    <speak>
        무엇을 도와드릴까요?
    </speak>
    """
    res = requests.post(kakao_audio_url, headers = HEADERS, data = DATA.encode('utf-8'))
    sound = io.BytesIO(res.content)
    song = AudioSegment.from_mp3(sound)
    play(song)

def recoding():
    seconds = 5
    myrecording = sd.rec(int(seconds * fs), samplerate = fs, channels = 1)
    
    sd.wait()

    sf.write('translate.wav', myrecording, fs)

    with open('translate.wav', 'rb') as fp:
        audio = fp.read()
    res = requests.post(kakao_speech_url, headers=headers_speech, data=audio)
    start = res.text.find('{"type":"finalResult"')
    end = res.text.rindex('}') +1
    if start == -1: 
        start = res.text.find('{"type":"errorCalled"')
    result_json_string = res.text[start:end]
    result = json.loads(result_json_string)
    print(result['value'])

    return result['value']


def translate():
    DATA = """
    <speak>
        <voice name="MAN_DIALOG_BRIGHT">번역 할 문장을 5초동안 말씀해주세요.</voice>
    </speak>
    """
    output_text(DATA)
    translate_url = "https://dapi.kakao.com/v2/translation/translate"
    text = recoding()
    source = 'kr'
    target = 'en'

    params = {'query':text, 'src_lang':source, 'target_lang':target}
    header_translate = {'authorization': f'KakaoAK {rest_api_key}'}
    response = requests.get(url=translate_url, headers=header_translate, params=params)

    if response.status_code == 200:
        decode = response.json()
        translated = decode['translated_text'][0][0]
    else:
        print('error', response.status_code)
    
    return translated


def output_text(DATA):
    res_audio = requests.post(kakao_audio_url, headers = HEADERS, data = DATA.encode('utf-8'))
    sound = io.BytesIO(res_audio.content)
    song = AudioSegment.from_mp3(sound)
    play(song)

def print_current_coin(coin):
    
    coin_value1 = pyupbit.get_current_price(coin)
    KRW_coin = ""
    msg = f"coin,{coin_value1}"
    coin_value2 = int(coin_value1)
    client.publish("Mqtt_pb", msg)
    print(coin_value2)
    coin_value = str(coin_value2)
    nstring=['','십','백','천','만','십','백','천','억']
    nd={'1':'','2':'이','3':'삼','4':'사','5':'오','6':'육',
        '7':'칠','8':'팔','9':'구','0':''}
        
    nlist=list(coin_value)
    nlen=len(coin_value)
    nlen = nlen-1
    for  i in nlist :
        if i == '0'  :
            nlen -= 1
            continue
        else : 
            KRW_coin = KRW_coin + nd[i] + nstring[nlen]
            nlen -= 1
    KRW_coin = KRW_coin + "원"
    if coin == "KRW-BTC":
        coin_name = "비트"

    if coin == "KRW-ETH":
        coin_name = "이더리움"

    if coin == "KRW-SAND":
        coin_name = "샌드박스" 

    if coin == "KRW-LTC":
        coin_name = "라이트"

    if coin == "KRW-XRP":
        coin_name = "리플"

    DATA = f"""
    <speak>
       현재  {coin_name} 코인의 시세는 {KRW_coin} 입니다.
    </speak>
    """
    output_text(DATA)
    
client = mqtt.Client()
def mqtt():
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        client.subscribe("Mqtt")

    def on_message(client, userdata, msg):
        global mqtt_msg
        # mqtt_msg = str(msg.payload)
        mqtt_msg = msg.payload.decode("UTF-8")
    
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.0.3",1883,60)
    client.loop_forever()


t = Thread(target = mqtt)
t.start()

def rasp_trans(text):
    translate_url = "https://dapi.kakao.com/v2/translation/translate"
    trans_text = text
    source = 'kr'
    target = 'en'

    params = {'query':trans_text, 'src_lang':source, 'target_lang':target}
    header_translate = {'authorization': f'KakaoAK {rest_api_key}'}
    response = requests.get(url=translate_url, headers=header_translate, params=params)

    if response.status_code == 200:
        decode = response.json()
        translated = decode['translated_text'][0][0]
    else:
        print('error', response.status_code)
    
    msg = f"trans,{translated}"
    client.publish("Mqtt_pb", msg)
    return translated

# 한식 중식, 일식, 양식, 간편식, 무관
# 매움 안매움 무관
# 면류 비면류 무관
def select_category(kind, spicy, noodle):
    kind_selected_list = []
    spicy_selected_list = []
    noodle_selected_list = []
    # 1kind 한식 2spicy 매움 3noodle 비면류
    for food in food_list:
        if(kind=='한식' and food[1]=='한식'):
            kind_selected_list.append(food)
        elif(kind=='중식'and food[1]=='중식'):
            kind_selected_list.append(food)
        elif(kind=='일식'and food[1]=='일식'):
            kind_selected_list.append(food)
        elif(kind=='양식'and food[1]=='양식'):
            kind_selected_list.append(food)
        elif(kind=='무관'):
            kind_selected_list = food_list
            break
        else:
            pass
    
    for food in kind_selected_list:
        if((spicy=='매움' or spicy=='매운') and food[2]=='매움'):
            spicy_selected_list.append(food)
        elif((spicy=='안 매움' or spicy=='안매움') and food[2]=='안매움'):
            spicy_selected_list.append(food)
        elif(spicy=='무관'):
            spicy_selected_list = kind_selected_list
            break
        else:
            pass
    
    for food in spicy_selected_list:
        if(noodle=='누들' and food[3]=='누들'):
            noodle_selected_list.append(food)
        elif(noodle=='비누들' and food[3]=='비누들'):
            noodle_selected_list.append(food)
        elif(noodle=='무관'):
            noodle_selected_list = spicy_selected_list
            break
        else:
            pass
    final_list = []
    for temp in noodle_selected_list:
        final_list.append(temp[0])
    return final_list





#####################################################################################################################################################################
#####################################################################################################################################################################
#####################################################################################################################################################################
#####################################################################################################################################################################
#####################################################################################################################################################################

def main():
    controller1.Controller().start()
    Thread(target = firealarm.main).start()
    Thread(target = ex_scene_adjustment.main).start()

    mqtt_msg = ""
    air_condition = ""
    if (airpollution['airpollution'] == 2 or airpollution['airpollution'] == 3 or airpollution['airpollution'] == 4 or airpollution['airpollution'] == 5):
        air_condition = "미세먼지가 심하니 마스크를 껴주시기 바랍니다."
    else:
        air_condition = "오늘 공기는 맑으니 마스크는 안끼셔도 되겠습니다."
    umbrella = ""
    if ((weather['main']).find("Rain") == 0):
        umbrella = "밖에 비가 오니 우산을 챙기셔야 합니다."

    if ((weather['main']).find("Snow") == 0):
        umbrella = "밖에 눈이 오니 우산을 챙기셔야 합니다."


    while(True):
        if(weather['main'] == 'Clouds'):
            green.on()
        if(weather['main'] == 'Clear'):
            red.on()
        if(weather['main'] == 'Rain' or weather['main'] == 'Snow'):
            blue.on()
        if(airpollution['airpollution'] == 2 or airpollution['airpollution'] == 3 or airpollution['airpollution'] == 4 or airpollution['airpollution'] == 5):
            yellow.on()
        #####################################################
        if button.is_pressed:
            mqtt_msg = ""
            question()
            answer = recoding()
            if(answer == "날씨 알려줘"):
                DATA = f"""
                <speak>
                오늘의 날씨는 {weather['description']} 입니다.
                {umbrella}
                그리고 온도는 {(weather['etc']['temp'])} 도이고 
                습도는  {weather['etc']['humidity']} 퍼센트입니다.
                미세먼지 심각 레벨은 {airpollution['airpollution']} 레벨 입니다. 
                {air_condition}
                </speak>
                """
                output_text(DATA)

            # 이름
            # 한식 중식, 일식, 양식, 간편식, 무관
            # 매움 안매움 무관
            # 면류 비면류 무관


            if(answer == "뭐먹지" or answer == '뭐 먹지'):
                DATA = f"""
                <speak>
                한식, 중식, 일식, 양식, 간편식, 무관 중 선택해주세요.
                </speak>
                """
                output_text(DATA)
                answer1 = recoding()
                if(answer1 in food_category[0]):
                    output_text(f"""
                    <speak>
                    매움, 안매움, 무관 중 선택해주세요.
                    </speak>
                    """)
                    answer2 = recoding()
                    if(answer2 in food_category[1]):
                        output_text(f"""
                        <speak>
                        누들, 비누들, 무관 중 선택해주세요.
                        </speak>
                        """)
                        answer3 = recoding()
                        if(answer3 in food_category[2]):
                            output_text(f"""
                            <speak>
                            음식을 나열하겠습니다. 
                            </speak>
                            """)

                if(answer1 in food_category[0] and answer2 in food_category[1] and answer3 in food_category[2]):
                    for food in select_category(answer1, answer2, answer3):
                        output_text(f"""
                        <speak>
                        {food}
                        </speak>
                        """)





            if(answer == "번역기 틀어줘"):
                translated_text = translate()
                print(translated_text)
                DATA = f"""
                <speak>
                <voice name="MAN_DIALOG_BRIGHT">{translated_text}</voice>
                </speak>
                """
                output_text(DATA)

            if(answer == "비트코인 시세 알려줘"):
                print_current_coin("KRW-BTC")
            if(answer == "이더리움 시세 알려줘"):
                print_current_coin("KRW-ETH")
            if(answer == "sandbox 시세 알려줘"):
                print_current_coin("KRW-SAND")
            if(answer == "라이트 코인 시세 알려줘"):
                print_current_coin("KRW-LTC")
            if(answer == "리플 시세 알려줘"):
                print_current_coin("KRW-XRP")

        if(answer == 'food'):
                DATA = f"""
                <speak>
                한식, 중식, 일식, 양식, 간편식, 무관 중 선택해주세요.
                </speak>
                """
                output_text(DATA)
                answer1 = recoding()
                if(answer1 in food_category[0]):
                    output_text(f"""
                    <speak>
                    매움, 안매움, 무관 중 선택해주세요.
                    </speak>
                    """)
                    answer2 = recoding()
                    if(answer2 in food_category[1]):
                        output_text(f"""
                        <speak>
                        누들, 비누들, 무관 중 선택해주세요.
                        </speak>
                        """)
                        answer3 = recoding()
                        if(answer3 in food_category[2]):
                            output_text(f"""
                            <speak>
                            음식을 나열하겠습니다. 
                            </speak>
                            """)

                if(answer1 in food_category[0] and answer2 in food_category[1] and answer3 in food_category[2]):
                    for food in select_category(answer1, answer2, answer3):
                        output_text(f"""
                        <speak>
                        {food}
                        </speak>
                        """)

        if(mqtt_msg == "weather"):
            mqtt_msg = ""
            DATA = f"""
                <speak>
                오늘의 날씨는 {weather['description']} 입니다.
                {umbrella}
                그리고 온도는 {(weather['etc']['temp'])} 도이고 
                습도는  {weather['etc']['humidity']} 퍼센트입니다.
                미세먼지 심각 레벨은 {airpollution['airpollution']} 레벨 입니다. 
                {air_condition}
                </speak>
                """
            output_text(DATA)

        if "trans" in mqtt_msg:
            msg = mqtt_msg[5:]
            mqtt_msg = ""
            print(msg)
            translated_text = rasp_trans(msg)
            print(translated_text)
            DATA = f"""
            <speak>
            <voice name="MAN_DIALOG_BRIGHT">{translated_text}</voice>
            </speak>
            """
            output_text(DATA)
        
        if(mqtt_msg == "btc"):
            mqtt_msg = ""
            print_current_coin("KRW-BTC")
        if(mqtt_msg == "eth"):
            mqtt_msg = ""
            print_current_coin("KRW-ETH")
        if(mqtt_msg == "sand"):
            mqtt_msg = ""
            print_current_coin("KRW-SAND")
        if(mqtt_msg == "ltc"):
            mqtt_msg = ""
            print_current_coin("KRW-LTC")
        if(mqtt_msg == "xrp"):
            mqtt_msg = ""
            print_current_coin("KRW-XRP")


main()