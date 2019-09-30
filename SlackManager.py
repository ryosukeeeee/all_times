import requests

class SlackManager:
	def __init__(self, token, oauth_token, channel):
		self.token = token
		self.oauth_token = oauth_token
		self.channel = channel

	def post_message_slack(self, message, thread_ts=None):
		method_url = "https://slack.com/api/chat.postMessage"

		payload = {
			"channel": self.channel,
			"token": self.token,
			"text": message,
			"unfurl_links": True,
			"unfurl_media": True
		}

		if thread_ts:
			payload['thread_ts'] = thread_ts

		response = requests.post(method_url, payload)
		return response

	def post_block_message(self, channel_name, message, user_icon_url, thread_ts=None):
		method_url = "https://slack.com/api/chat.postMessage"

		# thread_tsがあったらsectionはなし
		block = ""
		if not thread_ts:
			block = block + """[
							{
									"type": "section",
									"text": {
											"type": "mrkdwn","""
			block = block + '"text": "*#{0}*"'.format(channel_name)
			block = block + """
									}
							},
							{
									"type": "divider"
							},
							{
									"type": "context",
									"elements": [
											{
											"type": "image","""
			block = block + '"image_url": "{0}",'.format(user_icon_url)
			block = block + """"alt_text": "images"
									}
							]
					}
			]"""

		else:
			block = block + """[
							{
									"type": "divider"
							},
							{
									"type": "context",
									"elements": [
											{
											"type": "image","""
			block = block + '"image_url": "{0}",'.format(user_icon_url)
			block = block + """"alt_text": "images"
									}
							]
					}
			]"""

		payload = {
			"channel": self.channel,
			"token": self.token,
			"text": "",
			"unfurl_links": "true",
			"unfurl_media": "true",
			"blocks": block
		}

		if thread_ts:
			payload['thread_ts'] = thread_ts

		response = requests.post(method_url, payload)
		return response

	def get_channel_info(self, channel):
		method_url = "https://slack.com/api/channels.info"

		payload = {
			"token": self.token,
			"channel": channel
		}

		response = requests.get(method_url, payload)
		return response

	def get_user_info(self, user_id):
		method_url = "https://slack.com/api/users.info"

		payload = {
			"token": self.token,
			"user": user_id
		}

		response = requests.get(method_url, payload)
		return response

	def get_channel_history(self, channel_id, oldest_ut=''):
		method_url = "https://slack.com/api/channels.history"

		payload = {
			"token": self.oauth_token,
			"channel": channel_id,
			"count": 100
		}

		if oldest_ut != '':
			payload['oldest'] = oldest_ut

		response = requests.get(method_url, payload)
		return response

	def is_valid_response(self, event_api_request: dict):

		return True

	def is_posted_channel(self, channel_history: dict, channel_name: str):
		ts = ""

		if channel_history["ok"] == True:
					channel_event_list = channel_history["messages"]

					block_list = []

					for event in channel_event_list:
							if 'blocks' in event.keys():
									for block in event['blocks']:
											if block['type'] == "section":
													block_list.append((block, event))
					
					print(block_list)

					for tup_block_event in block_list:
							print(tup_block_event[0]['text']['text'])
							if channel_name in tup_block_event[0]['text']['text']:
								ts = tup_block_event[1]['ts']

		return ts