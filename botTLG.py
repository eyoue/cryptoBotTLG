# ---------------
# Simply chat-bot
# ---------------
from flask import Flask, request, jsonify
import requests, json, re
from flask_sslify import SSLify

app = Flask(__name__) # innit Flask application
sslify = SSLify(app) # include SSL in application

URL = token # Acces token Example: 'https://api.telegram.org/bot123456789:JCLEpOr3fAA4SSdD2wGZZdX4kEEdiTiSuVw/'

# Write data in fromat json
def write_json(data, filename='answer.json'):
	with open(filename, 'w') as f:
		json.dump(data, f, indent=2, ensure_ascii=False)

# Updates data
def get_updates():
	url = URL + 'getupdates'
	r = requests.get(url)
	return r.json()

# Send message active clients
def send_message(chat_id, text='Hello'):
	url = URL + 'sendMessage'
	answer = {'chat_id': chat_id,
	          'text': text}
	r = requests.post(url, json=answer)
	return r.json()

# Parse client request
def parse_text(text):
	pattern = r'/\w+\-+\w+'
	crpt = re.search(pattern, text).group()
	return crpt[1:]

# Get course by API
def get_price(crpt):
	url = 'https://api.cryptonator.com/api/ticker/{}'.format(crpt)
	response = requests.get(url).json()
	price = response['ticker']['price']
	return price


@app.route('/', methods=['POST', 'GET']) # innit rout GET/POST

# Communication with client.
# Reaction on the command.
def index():
	if request.method == 'POST':
		r = request.get_json()
		chat_id = r['message']['chat']['id']
		message = r['message']['text']

		if message == '/start':
			send_message(chat_id, '''Вижу ты здесь, чтобы узнать курс крипты?!
						 Команда /help тебе в помощь''')
		if message == '/help':
			send_message(chat_id, '''Пример запроса: /btc-usd
						Список поддерживаемых криптовалют:
						Bitcoin BTC
						Bitcoin Cash BCH
						Blackcoin BLK
						Bytecoin BCN
						Dash DASH
						Dogecoin DOGE
						Emercoin EMC
						Ethereum ETH
						Ethereum Classic ETC (coming soon)
						Litecoin LTC
						Monero XMR
						Peercoin PPC
						Primecoin XPM
						Reddcoin RDD
						Ripple XRP
						Zcash ZEC

						Список конвертируемых фиатных валют:
						US Dollar USD
						Euro EUR
						Russian Ruble RUR
						Ukrainian Hryvnia UAH
						''')
		pattern = r'/\w+\-+\w+'

		if re.search(pattern, message):
			price = get_price(parse_text(message))
			send_message(chat_id, text=price)
		return jsonify(r)
	return '<p>Hello men</p>'

def main():
	pass

if __name__ == '__main__':
	app.run() # Run application
