import discord
import requests
import os
import time
import hmac
import hashlib
import base64
import uuid

# TokenとSecretは環境変数から取得します
token = os.getenv('Switchbot_User_Token')
secret = os.getenv('Switchbot_Secret_Token')

async def fetch_room_temp_data():
    # 現在の13桁のタイムスタンプを取得
    t = int(round(time.time() * 1000))
    nonce = uuid.uuid4()
    
    # トークン、タイムスタンプ、nonceを使って署名を生成
    string_to_sign = '{}{}{}'.format(token, t, nonce)
    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret_bytes = bytes(secret, 'utf-8')
    sign = base64.b64encode(hmac.new(secret_bytes, msg=string_to_sign, digestmod=hashlib.sha256).digest()).decode()

    # APIリクエストのURL設定
    url = f'https://api.switch-bot.com/v1.1/devices/D03234356C31/status'
    
    # APIリクエストのヘッダー設定
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'charset': 'utf8',
        't': str(t),
        'sign': sign,
        'nonce': str(nonce)
    }

    # APIからのレスポンスを取得
    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)

    # レスポンスにbodyが含まれているか確認
    if response.status_code == 200 and 'body' in data:
        body = data['body']
        
        # 必要な情報を変数に格納
        device_id = body.get('deviceId', '不明なデバイス名')
        device_type = body.get('deviceType', '不明なタイプ')
        hub_device_id = body.get('hubDeviceId', '不明な親ハブID')
        battery = body.get('battery', '不明')
        temp = body.get('temperature', '不明')
        humi = body.get('humidity', '不明')
        electric_current = body.get('electricCurrent', '不明')
        version = body.get('version', '不明')
        status_message = data.get('message', 'No status message available')
        
        # Embed内容をまとめる
        embed_1 = (
            f"- デバイスID: {device_id}\n"
            f"- デバイスタイプ: {device_type}\n"
            f"- ハブID: {hub_device_id}\n"
            f"- バッテリー残量: {battery}\n"
            f"- デバイスバージョン: {version}"
        )
        
        embed_2 = (
            f"- 室温: {temp}℃\n"
            f"- 湿度: {humi}%\n"
        )
        
        # Embedメッセージを作成
        embed = discord.Embed(
            title=f"室温度計情報",
            description="現在の室温度計の情報です。",
            color=0x00fff00
        )

        # 各情報をEmbedに追加
        embed.add_field(name="室温・湿度の詳細", value=embed_2, inline=False)
        embed.add_field(name="デバイス詳細", value=embed_1, inline=False)

        # フッターにステータスメッセージを追加
        embed.set_footer(text=f"Message: {status_message}")

        return embed
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
