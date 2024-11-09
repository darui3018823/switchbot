import datetime
from pydoc import text
import re
import subprocess
import time
import discord
from discord.ext import commands
from discord import Embed, Interaction, app_commands
import pytz
from imports.PlugMini import fetch_plugmini_data
from imports.Room_Temp import fetch_room_temp_data
from imports.devicelist import get_device_list  # 作成した非同期関数をインポート
import os

# DiscordのBotトークンを取得
discord_token = os.getenv('Switchbot_API_discordbot')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
auth_user = ['973782871963762698', '1100809098460668004', '1152214038781104250', '1258342490990182473']
daruks = 973782871963762698

@bot.event
async def on_ready():    
    print("Bot is Ready.")
    print("Used Switchbot API v1.1")
    
    await bot.change_presence(activity=discord.CustomActivity("Checking Switchbot API..."))
    
    # スラッシュコマンドを同期
    try:
        synced = await bot.tree.sync()  
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
        
@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000  # bot.latencyは秒単位なので、ミリ秒に変換
    await ctx.send(f'Pong! Latency: {latency:.2f} ms')

@bot.tree.command()
async def stop(interaction: Interaction):
    OMG = interaction
    print(OMG.user)
    print(OMG.user.id)

    if interaction.user.id != daruks:  # daruks に管理者ユーザーIDを設定していると仮定
        await interaction.response.send_message('You do not have permission to use this command!')
        return
    
    await interaction.response.send_message('Bot is stopping...')

    # Botを閉じる
    await bot.close()

    print("Bot has been stopped.")

@bot.tree.command()
async def restart(interaction: Interaction):
    OMG = interaction
    print(OMG.user)
    print(OMG.user.id)

    if interaction.user.id != daruks:  # daruks に管理者ユーザーIDを設定していると仮定
        await interaction.response.send_message('You do not have permission to use this command!')
        return
    
    await interaction.response.send_message('Bot is Restarting...')
    
    # Botを閉じる
    await bot.close()

    # バッチファイルのパスを指定
    script_path = r'C:\Users\user\vsc\Switchbot\bat\rerun.bat'

    # バッチファイルを実行
    os.system(f'"{script_path}"')


@bot.tree.command(name="devicelist", description="daruのTokenから取得できるデバイスリストを送信します。")
async def devicelist(interaction: discord.Interaction):
    embed = discord.Embed(title="Device List", description="Sending request to Switchbot API...\nPlease wait a Moment.", color=0x1e90ff)
    await interaction.response.send_message(embed=embed)
    try:
        # device_info.pyの非同期関数を呼び出して、デバイス情報を取得
        Deviceid = await get_device_list()

        # Embedの作成
        embed = discord.Embed(
            title="Device List", 
            description="daru's House Switchbot devices", 
            color=0x00ff00 # 色はお好みで変更できます
        )

        # デバイスごとにデバイスタイプをリスト化し、デバイスごとにフィールドを追加
        device_types = {}
        
        # デバイスリストをループしてタイプ別に情報を収集
        for device_id, device_info in Deviceid.items():
            device_name = device_info['name']
            device_type = device_info['type']
            
            if device_type not in device_types:
                device_types[device_type] = []

            device_types[device_type].append({
                'device_id': device_id,
                'device_name': device_name
            })
        
        # デバイスタイプごとにデバイス情報をEmbedに追加
        for device_type, devices in device_types.items():
            embed.add_field(
                name=f"{device_type} (総数: {len(devices)})", 
                value="\n".join([
                    f"デバイス名: {device['device_name']}\nデバイスタイプ: {device_type}" 
                    for device in devices
                ]),
                inline=False
            )
        
        # メッセージを送信
        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)}")
        
@bot.tree.command(name="room_temp", description="室温湿度計の情報を取得します")
async def room_temp(interaction: discord.Interaction):
    embed = discord.Embed(title="Room Temp", description="Sending request to Switchbot API...\nPlease wait a Moment.", color=0x1e90ff)
    await interaction.response.send_message(embed=embed)
    
    # Room_Temp.pyから取得した非同期関数でEmbedメッセージを生成
    embed = await fetch_room_temp_data()

    if embed:
        # インタラクションを返してEmbedメッセージを送信
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("APIの呼び出しに失敗しました。")
        
@bot.tree.command(name="plugmini", description="Plug Miniデバイスの情報を取得します")
@app_commands.describe(device="Device Last 2txt. e.g, 6A, B6, 6E")
async def plugmini(interaction: discord.Interaction, device: str):
    embed = discord.Embed(title="Plug Mini", description="Sending request to Switchbot API...\nPlease wait a Moment.", color=0x1e90ff)
    await interaction.response.send_message(embed=embed)
    # deviceパラメータでデバイスIDを指定
    device_mapping = {
        '6A': 'DCDA0CDC436A',
        'B6': 'DCDA0CDC4DB6',
        '6E': 'DCDA0CDA956E'
    }

    # 入力されたデバイスIDがマッピングに存在するかチェック
    if device in device_mapping:
        device_id = device_mapping[device]
        embed = await fetch_plugmini_data(device_id)

        if embed:
            # インタラクションを返してEmbedメッセージを送信
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("APIの呼び出しに失敗しました。")
    else:
        await interaction.followup.send("無効なデバイスIDが指定されました。")

bot.run(discord_token)
