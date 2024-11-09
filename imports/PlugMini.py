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

async def fetch_plugmini_data(device_id):
    # 現在の13桁のタイムスタンプを取得
    t = int(round(time.time() * 1000))
    nonce = uuid.uuid4()
    
    # トークン、タイムスタンプ、nonceを使って署名を生成
    string_to_sign = '{}{}{}'.format(token, t, nonce)
    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret_bytes = bytes(secret, 'utf-8')
    sign = base64.b64encode(hmac.new(secret_bytes, msg=string_to_sign, digestmod=hashlib.sha256).digest()).decode()

    # APIリクエストのURL設定
    url = f'https://api.switch-bot.com/v1.1/devices/{device_id}/status'
    
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
        
        # deviceNameが存在するかチェックして取得
        device_name = body.get('deviceId', '不明なデバイス名')  # deviceNameは存在しないのでこのままにしています
        device_type = body.get('deviceType', '不明なタイプ')
        hub_device_id = body.get('hubDeviceId', '不明な親ハブID')

        # 電源状態と消費電力を取得
        power_status = body.get('power', '不明')
        voltage = body.get('voltage', '不明')  # 電圧のデータ
        weight = body.get('weight', '不明')  # 電力のデータ
        electricity_of_day = body.get('electricityOfDay', '不明')  # 当日の消費電力量
        electric_current = body.get('electricCurrent', '不明')  # 電流
        version = body.get('version', '不明')  # バージョン情報
        status_message = data.get('message', 'No status message available')
        
        embed_1 = [
            f"- デバイスID: {device_id}",
            f"- デバイスタイプ: {device_type}",
            f"- Plug Miniの状態: {power_status}",
            f"- デバイスバージョン: {version}"
        ]
        
        embed_2 = [
            f"- 当日の消費電力: {weight}W",
            f"- 現在の電圧: {voltage}V",
            f"- 現在の電流値: {electric_current}A",
            f"- 当日の使用時間: {electricity_of_day}(Min)",
        ]

        # Embedメッセージを作成
        embed = discord.Embed(
            title=f"Plug Mini {device_name}",
            description="現在のPlug Miniの情報です。",
            color=0x00fff00
        )

        # 各情報をEmbedに追加
        embed.add_field(name="デバイス詳細", value="\n".join(embed_1), inline=False)
        embed.add_field(name="電力詳細", value="\n".join(embed_2), inline=False)

        # フッターにステータスメッセージを追加
        embed.set_footer(text=f"Message: {status_message}")

        return embed
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
