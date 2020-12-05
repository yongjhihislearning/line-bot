# 用python要架設伺服器或寫網站常用: 
# flask(沒畫面，小規模的), django(網頁，有畫面的，大規模的)

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('6cafa0z+flaefXMab+ewmIxPHQUviCm5LYyK12ek4Ir3D7m5ILWxFuEghTZ2L0qUHzPkHWSK283ZmhIHULXXOY7m97geWnWbnthd7U/zsdQwGAobHsQXYK7VJ+XWpOW7BzqCkQneQkRncPca/O3vUQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0629e0035df70ee54f53a71748c127d7')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉，你說什麼'

    if msg in ['hi', 'Hi']:
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位，是嗎?'

    line_bot_api.reply_message(
        event.reply_token,
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
    ))


if __name__ == "__main__":
    app.run()