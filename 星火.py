import SparkApi
import json

#以下密钥信息从控制台获取
appid = "41ff96e9"     #填写控制台中获取的 APPID 信息
api_secret = "ZWJmZjc2MWI2YTQxNmJjZDg2NTk0MWZk"   #填写控制台中获取的 APISecret 信息
api_key ="29f4bb960509a99aa6ad4e215bb236e7"    #填写控制台中获取的 APIKey 信息

#用于配置大模型版本，默认“general/generalv2”
domain = "general"   # v1.5版本
# domain = "generalv2"    # v2.0版本
#云端环境的服务地址
Spark_url = "wss://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址

wsParam = SparkApi.Ws_Param(appid, api_key, api_secret, Spark_url)
wsUrl = wsParam.create_url()


import websocket


def on_message(ws, message):
    print("Received: " + message)

def on_error(ws, error):
    print("Error: " + str(error))

def on_close(ws):
    print("Connection closed")

def on_open(ws):
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "random_threshold": 0.5,
                "max_tokens": 2048,
                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": '说出鲁迅的作品？'
            }
        }
    }
    ws.send(json.dumps(data))

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(wsUrl,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

