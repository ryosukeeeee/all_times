import json
import os
import pprint
import datetime as dt
from SlackManager import *

def main(event, context):
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
        # pprint.pprint(body)
        print(body)

        # イベントの発生したチャンネルのID
        event_channel_id = body['event']['channel']
        event_user_id = body['event']['user']
        if body['event']['type'] == 'message':
            event_message = body['event']['text']
        else:
            event_message = "null"
        print("event_message: ", event_message)
            
        # チャンネル名を取得
        channel_info = slack_manager.get_channel_info(event_channel_id)
        channel_info_dict = json.loads(channel_info.text)
        channel_name = channel_info_dict['channel']['name']

        # ユーザー情報を取得
        user_info = slack_manager.get_user_info(event_user_id)
        user_info_dict = json.loads(user_info.text)
        # pprint.pprint(user_info_dict)
        user_name = user_info_dict['user']['name']
        profile_real_name = user_info_dict['user']['profile']['real_name'] # displaynameがないときはこっちを使う
        profile_display_name = user_info_dict['user']['profile']['display_name'] #これがよさそう
        user_icon_url = user_info_dict['user']['profile']['image_192']

        print("username: {0}\nrealname: {1}\ndisplayname: {2}".format(user_name, profile_real_name, profile_display_name))
        print("this event happend by {0} in #{1}".format(user_name, channel_name))

        res = slack_manager.post_block_message(channel_name, event_message, user_icon_url)
        print(res.text)
        res = slack_manager.post_message_slack(event_message)
        print(res.text)
        # event_info = slack_manager.post_message_slack(body)

        res = slack_manager.get_channel_history(channel_id)
        print(res.text)

        return {
            'statusCode': 200,
            'body': "ok",
            'isBase64Encoded': False
        }
    except Exception as e:
        print(e)

        return {
            'statusCode': 200,
            'body': "ok",
            'isBase64Encoded': False
        }

# #times_nakagawaに投稿があったとき
# #times_allで今日の投稿のなかに#times_nakagawaがあるか確認
# なければ新たに作る
# もしあれば、tsを検索し、thread_tsを設定してスレッドにする


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