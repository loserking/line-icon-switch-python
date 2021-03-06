import os
from flask import request
from flask_restful import Resource
import json
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TextSendMessage,
    Sender)

LINE_FRIEND = dict(
    BROWN="https://stickershop.line-scdn.net/stickershop/v1/sticker/52002734/iPhone/sticker_key@2x.png",
    CONY="https://stickershop.line-scdn.net/stickershop/v1/sticker/52002735/iPhone/sticker_key@2x.png",
    SALLY="https://stickershop.line-scdn.net/stickershop/v1/sticker/52002736/iPhone/sticker_key@2x.png"
)


class LineIconSwitchController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        payload = request.get_json(force=True)

        line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
        handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
        token = payload['events'][0]['replyToken']
        msg = payload['events'][0]['message']['text'].upper()

        if msg in LINE_FRIEND:
            name = msg
            icon = LINE_FRIEND[msg]
            text = TextSendMessage(
                text=msg,
                sender=Sender(
                    name=name,
                    icon_url=icon))
        else:
            text = TextSendMessage(text=msg)
        line_bot_api.reply_message(token, text)

        response = {
            "statusCode": 200,
            "body": json.dumps({"message": 'ok'})
        }

        return response
