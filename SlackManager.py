import requests

class SlackManager:
	def __init__(self, token, oauth_token, channel):
		self.token = token
		self.oauth_token = oauth_token
		self.channel = channel

	def post_message_slack(self, message):
		method_url = "https://slack.com/api/chat.postMessage"

		payload = {
			"channel": self.channel,
			"token": self.token,
			"text": message,
			"unfurl_links": True,
			"unfurl_media": True
		}

		response = requests.post(method_url, payload)
		return response

	def post_block_message(self, channel_name, message, user_icon_url):
		method_url = "https://slack.com/api/chat.postMessage"

		block = """[
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

		payload = {
			"channel": self.channel,
			"token": self.token,
			"text": message,
			"unfurl_links": "true",
			"unfurl_media": "true",
			"blocks": block
		}

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