import boto3
import os
import json

def main(event, context):
  body = json.loads(event['body'])
  print(body)

  # 初回のAPIエンドポイント検証
  if body['type'] == "url_verification":
    response_body = {
        "challenge": body['challenge'],
    }

    return {
      'statusCode': 200,
      'body': json.dumps(response_body),
      'isBase64Encoded': False
    }

  verification_token = os.environ['SLACK_VERIFICATION_TOKEN']
  app_id = os.environ['SLACK_APP_ID']

  # リクエストが正当かチェック
  if body['token'] != verification_token or body['api_app_id'] != app_id:
    return None

  if 'body' in event.keys():
    try:
      client = boto3.client('lambda')
      function_arn = os.environ['MAIN_FUNCTION_ARN']

      body = event['body']
      # payload = body.encode("unicode-escape")
      payload = body.encode()
      print("payload")
      print(payload)
      

      response = client.invoke(
        FunctionName = function_arn,
        InvocationType = 'Event',
        Payload = payload
      )
      print(response)
    except:
      import traceback
      print("[Error]")
      traceback.print_exc()

  return {
    'statusCode': 200,
    'body': "ok",
    'isBase64Encoded': False
  }
