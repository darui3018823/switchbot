# SwitchBot API Bot

このプロジェクトは、SwitchBot APIを使用してDiscord向けにSwitchBotデバイスの情報を確認するBotのソースコードです。<br>
Switchbot Appをわざわざ開くのが面倒くさい...なそんなあなたにお勧め！！！（？）<br>

## 機能

- SwitchBotデバイスの情報を取得
  - 現在は以下のデバイスに対応しています：
    - **PlugMini (JP)**
    - **Meter (室温度計)**
  - 私の所持デバイスが増えると、対応デバイスとコマンドも追加されます。

## 必要なもの

- Python (3.12.7を推奨)
- SwitchBotのUser TokenおよびSecret Token
- Discord Bot Token

## 使用方法

1. [こちら](https://github.com/darui3018823/switchbot/releases)よりSource Codeをダウンロードし、解凍してください。<br><br>

2. 解凍したzipファイルにあるvenvをアクティベートします。
    ```bash
    source venv/bin/activate  # Linux/Mac
    .\venv\Scripts\activate  # Windows
    ```
<br>

3. 環境変数の設定<br>
このBotでは3つのTokenが必要です。<br>
- Discord Bot Token
- SwitchBot User Token
- SwitchBot Client Secret Token
<br>
これらのそれぞれの設定方法は以下の通りです。
<br>
<br>

### Discord Bot Token :<br>
[Discord Developer Portal](https://discord.com/developers/applications)にアクセスし、
Botを作っていなければそこで作ってください。<br>
作ったBotからTokenをコピーします。<br>
環境変数を設定します。<br>
変数名は`Switchbot_API_discordbot`にしてください。<br>
すべてOKを押して終了します。<br><br>

### SwitchBot API Token :<br>
以下の公式ページを参考に取得してください。<br>
- [トークンの取得方法 - Switchbotサポート](https://support.switch-bot.com/hc/ja/articles/12822710195351-%E3%83%88%E3%83%BC%E3%82%AF%E3%83%B3%E3%81%AE%E5%8F%96%E5%BE%97%E6%96%B9%E6%B3%95)<br>

取得したTokenを以下のように設定します。<br>
  トークン: 環境変数名`Switchbot_User_Token`<br>
  クライアントシークレット: 環境変数名`Switchbot_Secret_Token`
<br>

4. 実行<br>
ファイル構造は以下のようになっているはずです。
    ```
    root/
    ├── main.py
    ├── imports/
    │   ├── devicelist.py
    │   └── PlugMini.py
    │   └── Room_Temp.py
    └── bat/
    │   └── rerun.bat
    │   └── run.bat
    ```
    `./root/bat/run.bat`を実行してください。
     - 絶対パスになっていますので変更してください<br><br>
    
## 注意事項
- 絶対パスの箇所は適宜変更してください。
- Tokenは漏洩すると悪用の危険がありますので**絶対**に公開しないでください。
- このボットは現在、デバイス情報の取得のみ対応しています。<br>将来的には、デバイスの制御機能などが追加される予定です。<br>私に買ってください（（（
- 特に記載がない場合、すべての効力はreadme.mdの最終更新日から発生します。

## ライセンス
このコード及びその他は[MITライセンス](https://github.com/darui3018823/switchbot/blob/main/LICENSE)の下で公開されています。

## 最終更新日
2024/11/09 23:10
