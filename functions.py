import shopify
import requests

api_key = ''
access_token = ''
api_version = '2019-10'
shop_url = 'something.myshopify.com'

def creat_a_product(**kwargs):
    session = shopify.Session(shop_url,api_version, access_token)
    shopify.ShopifyResource.activate_session(session)
    
    variants = []
    images = []
    new_product = shopify.Product()

    for key, value in kwargs.items():
      if key=='variants':
        for item in value:
          variant = shopify.Variant(item)
          variants.append(variant)
        value = variants
      elif key=='images':
        for item in value:
          image = shopify.Image()
          with open(item, "rb") as f:
            filename = item.split("/")[-1:][0]
            encoded = f.read()
            image.attach_image(encoded, filename=filename)
            images.append(image)
        value = images
	
      setattr(new_product,  key, value)
    new_product.save()
    print(new_product.id)	
    print (new_product.to_dict())

#creat_a_product(title="test title X", body_html="body of the page <br/><br/> test <br/> test", variants=[{'price': 1.00, 'requires_shipping': False,'sku':'000007'}], images=['/home/improsys/superman.png','/home/improsys/giphy_s.png'])


def edit_a_product(product_id, **kwargs):
    session = shopify.Session(shop_url,api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    variants = []
    images = []
    product = shopify.Product.find(product_id)  

    for key, value in kwargs.items():
      if key=='variants':
        for item in value:
          variant = shopify.Variant(item)
          variants.append(variant)
        value = variants
      elif key=='images':
        for item in value:
          image = shopify.Image()
          with open(item, "rb") as f:
            filename = item.split("/")[-1:][0]
            encoded = f.read()
            image.attach_image(encoded, filename=filename)
            images.append(image)
        value = images
	
      setattr(product,  key, value)

    result = product.save()
    print (result)

#edit_a_product(4353678704743, title="test title Y", body_html="body of the page <br/><br/> test <br/> test", variants=[{'price': 1.00, 'requires_shipping': False,'sku':'000007'}], images=['/home/improsys/superman.png','/home/improsys/giphy_s.png','/home/improsys/b.png'])

def delete_a_product(product_id):
    session = shopify.Session(shop_url,api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    product = shopify.Product.find(product_id)  
    product.destroy()


def create_a_customer(**kwargs):
    session = shopify.Session(shop_url,api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    new_customer=shopify.Customer()

    for key, value in kwargs.items():
      setattr(new_customer,  key, value)

    new_customer.save()
    print(new_customer.to_dict())

#create_a_customer(first_name='John', last_name='Travolta', email='travolta@travolta.com')

def edit_a_customer(customer_id, **kwargs):
    session = shopify.Session(shop_url,api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    customer=shopify.Customer().find(customer_id)

    for key, value in kwargs.items():
      setattr(customer,  key, value)

    result = customer.save()
    print (result)

#edit_a_customer(2716826796135, first_name='John', last_name='Travolta', email='travolta@tt.com')

def delete_a_customer(customer_id):
    session = shopify.Session(shop_url,api_version, access_token)
    shopify.ShopifyResource.activate_session(session)
    try:
      customer=shopify.Customer().find(customer_id)
      customer.destroy()
    except:
      print ("Failed to delete")

def create_an_order(**kwargs):
    session = shopify.Session(shop_url,api_version, access_token)
    shopify.ShopifyResource.activate_session(session)
    variants = []
    new_order=shopify.Order()
    for key, value in kwargs.items():       
      setattr(new_order,  key, value)
    result = new_order.save()
    print (result)
    print (new_order.id)
    print(new_order.to_dict())


#create_an_order(line_items=[{"title": "A product","price": 74.99,"grams": "1300","quantity": 3,"tax_lines": [{ "price": 13.5,    "rate": 0.06,    "title": "State tax"  }]}, {"title": "Another product","price": 24.99,"quantity": 9}], email='foo@foo.com', shipping_address={"first_name": "John","last_name": "Smith","address1": "123 Fake Street","phone": "555-555-5555","city": "Fakecity","province": "Ontario","country": "Canada","zip": "K2P 1L4"}, billing_address={"first_name": "John","last_name": "Smith","address1": "123 Fake Street","phone": "555-555-5555","city": "Fakecity","province": "Ontario","country": "Canada","zip": "K2P 1L4"}) 

def edit_an_order(order_id, **kwargs):
    session = shopify.Session(shop_url,api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    order=shopify.Order.find(order_id)
    for key, value in kwargs.items():       
      setattr(order,  key, value)

    result = order.save()
    print (result)

#edit_an_order(1870932901991, line_items=[{"title": "A product","price": 74.99,"grams": "1300","quantity": 3,"tax_lines": [{ "price": 13.5,    "rate": 0.06,    "title": "State tax"  }]}, {"title": "Another product","price": 24.99,"quantity": 9}], email='foo@foo.com', shipping_address={"first_name": "John","last_name": "Smith","address1": "123 Fake Street","phone": "555-555-5555","city": "Fakecity","province": "Ontario","country": "Canada","zip": "K2P 1L4"}, billing_address={"first_name": "John","last_name": "Smith","address1": "123 Fake Street","phone": "555-555-5555","city": "Fakecity","province": "Ontario","country": "Canada","zip": "K2P 1L4"}) 

def delete_an_order(order_id):
    session = shopify.Session(shop_url,api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    try:	
      order=shopify.Order.find(order_id)
      order.destroy()
    except:
      print ("Failed to delete") 


def create_a_fulfillment(order_id, **kwargs):
    session = shopify.Session(shop_url,api_version, access_token)
    shopify.ShopifyResource.activate_session(session)
    locations = dict()
    for location in shopify.Location.find():
      locations[location.city] = location.id
    city = 'Dhaka' 	# Change it to appropriate city
    order=shopify.Order.find(order_id)
   
    fulfillment = shopify.Fulfillment({'order_id':order.id,'line_items':order.line_items,'location_id':locations[city]})

    for key, value in kwargs.items():       
      setattr(fulfillment,  key, value)

    result = fulfillment.save()
    print (fulfillment.id)
    print (result)

#create_a_fulfillment(1870967701607, tracking_company='DHL', tracking_number = '12343', tracking_url = 'some-tracking-url.com/12343', notify_customer = True)

def modify_fulfillment(order_id, fulfillment_id, payload):
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    url = "https://{}:{}@{}/admin/api/{}/orders/{}/fulfillments/{}.json".format(api_key, access_token, shop_url, api_version, order_id,fulfillment_id)
    r = requests.put(url, json=payload,  headers=headers)
    print(r.json())

#modify_fulfillment(1870967701607, 1765464342631, {"fulfillment": {"tracking_url": "some-tracking-url.com/12343"}})

def cancel_fulfillment(order_id,fulfillment_id):
    payload = {}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    url = "https://{}:{}@{}/admin/api/{}/orders/{}/fulfillments/{}/cancel.json".format(api_key, access_token, shop_url, api_version, order_id, fulfillment_id)
    r = requests.post(url, json=payload,  headers=headers)
    print(r.json())

#cancel_fulfillment(1870967701607, 1765464342631)


def get_all_products():
    url = "https://{}:{}@{}/admin/api/{}/products.json".format(api_key, access_token, shop_url, api_version)
    r = requests.get(url)
    print(r.json())

#get_all_products()


def get_all_customers():
    url = "https://{}:{}@{}/admin/api/{}/customers.json".format(api_key, access_token, shop_url, api_version)
    r = requests.get(url)
    print(r.json())

get_all_products()


def get_all_orders():
    url = "https://{}:{}@{}/admin/api/{}/orders.json".format(api_key, access_token, shop_url, api_version)
    r = requests.get(url)
    print(r.json())

get_all_orders()





