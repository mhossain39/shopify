#!flask/bin/python
from flask import Flask, request, jsonify, redirect, session
import requests, random
app = Flask(__name__)
app.secret_key = str(random.random())

api_key = ''	#Set Partner app api key
api_secret = '' #Set Partner app api secret
scopes = 'read_products,write_products,read_orders,write_orders,read_customers,write_customers,read_inventory,write_inventory,read_fulfillments, write_fulfillments'
redirect_uri = ''  #Set partner app redirect uri

@app.route('/')
def index():
    return '<form method="POST"><table><tr><td><input type="text" name="shop" id="shop" placeholder="something.myshopify.com"></td><td><input type="submit" name="submit" value="Submit"></td></tr></table></form>'

@app.route('/', methods=['POST'])
@app.route('/')
def submit_to_shopify():
    global api_key, api_secret, scopes, redirect_uri
    shop = request.form.get('shop', '')
    nonce = random.random()
    session['nonce_value'] = str(nonce)	 
    url = "https://{}/admin/oauth/authorize?client_id={}&scope={}&redirect_uri={}&state={}&grant_options[]=offline-access".format(shop, api_key,  scopes, redirect_uri, nonce)
    return redirect(url)

@app.route('/return', methods=['GET'])
def get_code():
    global api_key, api_secret, scopes, redirect_uri
    code = request.args.get('code', '')
    shop = request.args.get('shop', '')
    state = request.args.get('state', '')
    if state!=	session['nonce_value']:
      return "Wrong Nonce value "

    url = 'https://{}/admin/oauth/access_token'.format(shop)
    myobj = {'client_id': api_key,'client_secret': api_secret,'code': code}

    x = requests.post(url, data = myobj)
    print (x.json()['access_token'])
    return x.json()['access_token']

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


