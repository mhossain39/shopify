# Project Files

app.py : A very simple few line Flask code demonstration partner app authentication with any shop using oAuth

README.md: All details of all crud operation and oauth

functions.py: Contains functions with example for making crud operations with Products, Customers, Orders and Fulfillments. These functions are ready to use in any python 3 environment. Tested with Python 3.5 and 3.6. These functions handles every property of Products, Customer, Orders and Fullfilments but properties needs to be supplied correctly following API documentation

# Authentication for Partner App

Partner app gets control over a shop data, when shop admin add partner app through oauth authentication in their shop.

To let shop admin add our partner app in their shop, we need to ask shop admin their shop address. Shopify shop addresses are https://{shop}.shopify.com. After collecting shop address we need to send user/visitor to following address:
```
https://{shop}.myshopify.com/admin/oauth/authorize?client_id={api_key}&scope={scopes}&redirect_uri={redirect_uri}&state={nonce}&grant_options[]={access_mode}

{shop}: The name of the user's shop.
{api_key}: The app's API Key.
{scopes}: A comma-separated list of scopes. For example, to write orders and read customers, use scope=write_orders,read_customers. Any permission to write a resource includes the permission to read it.
{redirect_uri}: The URL to which a user is redirected after authorizing the client. The complete URL specified here must be added to your app as a whitelisted redirection URL, as defined in the Partner Dashboard.
```
Before sending user to above url we need to save {nonce} in SESSION variable so that we can match this value to verify user, when user return after oauth authentication.

After authentication user will come with following parameter.

https://partner_app/redirect/uri?code={authorization_code}&hmac=da9d83c171400a41f8db91a950508985&timestamp=1409617544&state={nonce}&shop={hostname} 

First we would verify nonce to verify user session then we would use above code to retrieve access token. We need this access token to make all CRUD operations. Here is the python code for retrieving access token.

import requests
```
api_key = ''
api_secret = ''

code = request.args.get('code', '')
shop = request.args.get('shop', '')
url = ('https://{}/admin/oauth/access_token'.format(shop))
myobj = {'client_id': api_key,'client_secret': api_secret,'code': code}
x = requests.post(url, data = myobj)
access_token = x.json()['access_token']
```
Now we have access_token, we can proceed with CRUD operations.

We will use shopify Python official API(http://shopify.github.io/shopify_python_api/) which can be installed/upgrade using:

pip install --upgrade ShopifyAPI

and it can be used using:

import shopify

First we need to create a API session and activate it using following two lines of code for doing any operation:
```
session = shopify.Session(shop,api_version, access_token)
shopify.ShopifyResource.activate_session(session)
```
# Product CRUD
https://help.shopify.com/en/api/reference/products

#To add a product

```
new_product = shopify.Product()
new_product.title = "Audi pictures test "
new_product.body_html = "body of the page <br/><br/> test <br/> test"
variant = shopify.Variant({'price': 1.00, 'requires_shipping': False,'sku':'000007'})
new_product.variants = [variant]	#details available at https://help.shopify.com/en/api/reference/products/product-variant
path = "/path/to/product/image/audi.jpg"
image = shopify.Image()
with open(path, "rb") as f:
    filename = path.split("/")[-1:][0]
    encoded = f.read()
    image.attach_image(encoded, filename=filename)
new_product.images = [image]
new_product.save()
new_product.id # To get the id of added product
```
#To edit a product

```
product = shopify.Product.find(4350181081191)  # 4350181081191 is product id
product.title = "Audi pictures  "
product.body_html = "body of the page <br/><br/> final <br/> test"
variant = shopify.Variant({'price': 2.00, 'requires_shipping': False,'sku':'000007'})
product.variants = [variant]
product.save()
```

#To delete a product

```
product = shopify.Product.find(4350181081191)
product.destroy()
```

# Customer CRUD
https://help.shopify.com/en/api/reference/customers

#To add a Customer

```
new_customer=shopify.Customer()
new_customer.first_name='John'
new_customer.last_name='Travolta'
new_customer.email='travolta@travolta.com'
new_customer.save()
new_customer.id #To get id of added customer
```

#To Edit a Customer
```
customer=shopify.Customer().find(2712154734695)
customer.first_name='John'
customer.last_name='Travolta'
customer.email='travolta@travolta.com'
customer.save()
```

#To Delete a Customer

```
customer=shopify.Customer().find(2712154734695)
customer.save()
```

# Orders CRUD
https://help.shopify.com/en/api/reference/orders

#To add an Order

```
new_order=shopify.Order()
variant = shopify.Variant({"title": "A product","price": 74.99,"grams": "1300","quantity": 3,"tax_lines": [{ "price": 13.5,    "rate": 0.06,    "title": "State tax"  }]})
variant1 = shopify.Variant({"title": "Another product","price": 24.99,"quantity": 9})
new_order.line_items=[variant, variant1] # A for variant for each ordered product 
new_order.email='foo@foo.com'
new_order.fulfillment_status='fulfilled'
new_order.billing_address=shopify.Address({"first_name": "John","last_name": "Smith","address1": "123 Fake Street","phone": "555-555-5555","city": "Fakecity","province": "Ontario","country": "Canada","zip": "K2P 1L4"})
new_order.shipping_address=shopify.Address({"first_name": "John","last_name": "Smith","address1": "123 Fake Street","phone": "555-555-5555","city": "Fakecity","province": "Ontario","country": "Canada","zip": "K2P 1L4"})
new_order.save()
new_order.id # To get the id of added Order
```

#To edit an Order

```
order=shopify.Order.find(1867846549607)
order.email='foo@foo.com'
order.save()
```

#To delete an Order

```
order=shopify.Order.find(1867846549607)
order.destroy()
```

# Fulfillment CRUD
https://help.shopify.com/en/api/reference/shipping-and-fulfillment/

#To add a fulfilment

```
locations = dict()
for location in shopify.Location.find():
    locations[location.city] = location.id
city = YOUR_LOCATION #str
order=shopify.Order.find(1869518569575)
fulfillment = shopify.Fulfillment({'order_id':order.id,'line_items':order.line_items,'location_id':locations[city], 'tracking_number':''})
fulfillment.tracking_company = 'DHL'
fulfillment.tracking_number = '12343'
fulfillment.tracking_url = 'some-tracking-url.com/12343'
fulfillment.notify_customer = True
fulfillment.save()
```

#To edit a fulfilment

Fulfilment Edits does not work using shopify Python API. Thats why I did it using direct call.
```
def modify_fulfillment(order_id, fulfillment_id, payload):
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    url = "https://{}:{}@{}/admin/api/{}/orders/{}/fulfillments/{}.json".format(api_key, access_token, shop_url, api_version, order_id,fulfillment_id)
    r = requests.put(url, json=payload,  headers=headers)
    print(r.json())
```

#To cancel a fulfilment

Fulfilment Cancelation does not work using shopify Python API. Thats why I did it using direct call.
```
def cancel_fulfillment(order_id,fulfillment_id):
    payload = {}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    url = "https://{}:{}@{}/admin/api/{}/orders/{}/fulfillments/{}/cancel.json".format(api_key, access_token, shop_url, api_version, order_id, fulfillment_id)
    r = requests.post(url, json=payload,  headers=headers)
    print(r.json())
```


Check function for each crud operation in functions.py. Funtions support all properties of products, orders and fulfilments. Properties should be according to shopify documentation


