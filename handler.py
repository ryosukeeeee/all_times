import json
import os
import pprint
import datetime as dt
from SlackManager import *
import Common

def main(event, context):
    # tokenのチェックをする

    token = os.environ['SLACK_TOKEN']
    oauth_token = os.environ['SLACK_OAUTH_TOKEN']
    channel_id = os.environ['SLACK_CHANNEL_ID']

    slack_manager = SlackManager(
        token, 
        oauth_token,
        channel_id
    )

    try: 
        body = json.loads(event['body'])
        print("event")
        print(body)

        # イベントの発生したチャンネルのID
        event_channel_id = body['event']['channel']

        # イベントを起こしたユーザーのID
        event_user_id = body['event']['user']

        # イベントのタイプがmessageならメッセージテキストを取得
        if body['event']['type'] == 'message':
            event_message = body['event']['text']
        else:
            event_message = "null"
        print("event_message: ", event_message)
            
        # チャンネル名を取得
        channel_info = slack_manager.get_channel_info(event_channel_id)
        channel_name = json.loads(channel_info.text)['channel']['name']

        # ユーザー情報を取得
        user_info = slack_manager.get_user_info(event_user_id)
        user_info_dict = json.loads(user_info.text)
        user_name = user_info_dict['user']['name']
        profile_real_name = user_info_dict['user']['profile']['real_name'] # displaynameがないときはこっちを使う
        profile_display_name = user_info_dict['user']['profile']['display_name'] #これがよさそう

        # ユーザーのアイコンのurl
        user_icon_url = user_info_dict['user']['profile']['image_192']

        print("username: {0}\nrealname: {1}\ndisplayname: {2}".format(user_name, profile_real_name, profile_display_name))
        print("this event happend by {0} in #{1}".format(user_name, channel_name))

        # アプリが投稿する先のチャンネルで、受け取ったイベントの起こった日の午前2時以降に投稿したイベントを取得
        now = Common.ts_to_date_object(float(body['event_time']))
        if now.hour > 2:
            oldest_ts = Common.get_timestamp(now.year, now.month, now.day, 2)
        else:
            oldest_ts = Common.get_timestamp(now.year, now.month, now.day - 1, 2)
        res = slack_manager.get_channel_history(channel_id, str(oldest_ts.timestamp()))

        print('channel_history')
        print(res.text)

        # 受け取ったイベントが発生したチャンネルの投稿をすでにしているかチェック
        ts = slack_manager.is_posted_channel(json.loads(res.text), channel_name)

        # もし初めてのイベントなら#{チャンネル名}を最初に投稿する
        if ts != "":
            res = slack_manager.post_block_message(channel_name, event_message, user_icon_url, ts)
            print(res.text)
            res = slack_manager.post_message_slack(event_message,ts)
            print(res.text)
        # 初めてではなければ、リプライにする
        else:
            res = slack_manager.post_block_message(channel_name, event_message, user_icon_url)
            print(res.text)
            res_dict = json.loads(res.text)
            res = slack_manager.post_message_slack(event_message, res_dict["ts"])
            print(res.text)

        return {
            'statusCode': 200,
            'body': "ok",
            'isBase64Encoded': False
        }

    except Exception as e:
        print("Error")
        print(e)

        return {
            'statusCode': 200,
            'body': "ok",
            'isBase64Encoded': False
        }

# url登録時のバリデーション用
def validation(event):

    request_body = json.loadcs(event['body'])
    # challenge = body["challenge"]
    # print(challenge)

    body = {
        "challenge": request_body['challenge'],
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response