from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings



import requests

from .models import Element, Category

class PayPalPayment:
    def __init__(self):
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.secret = settings.PAYPAL_SECRET
        self.base_url = settings.PAYPAL_BASE_URL

    def get_access_token(self):

        if settings.DEMO:
            return "DEMO_TOKEN"

        url = f"{self.base_url}/v1/oauth2/token"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"	
        }

        data = {
            "grant_type": "client_credentials"	
        }

        response = requests.post(url, auth=(self.client_id, self.secret), headers=headers, data=data)

        if response.status_code == 200:
            return response.json()['access_token']
        return None
    
    def capture_order(self, order_id) -> dict:



        url = f"{self.base_url}/v2/checkout/orders/{order_id}/capture"

        access_token = self.get_access_token()

        if not access_token:
            return {'error': "No se pudo generar el token"}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"	
        }

        data = {
            "application_context":{
                "return_url": "http://localhost:8000/elements",
                "cancel_url": "http://localhost:8000/elements"
            }
        }

        response = requests.post(url, json=data, headers=headers)

        # print(response.json())
        # print(response.json()['id'])
        # print(response.json()['status'])
        # print(response.json()['purchase_units'][0]['payments']['captures'][0]['amount']['value'])
        # print(response.status_code)

        if response.status_code == 201:
            return response.json()
        return None
   


# Create your views here.

def index(request):
    
    search = request.GET.get('search') if request.GET.get('search') else ''

    category_id = request.GET.get('category_id')
    category_id = int(category_id) if category_id else ''

    elements = Element.objects
    
    if search:
        elements = elements.filter(title__contains=search)
        
    if category_id:
        elements = elements.filter(category_id=category_id)

    elements = elements.filter(type=2).all()

    categories = Category.objects.all()

    paginator = Paginator(elements,10)
    page_number = request.GET.get('page')

    return render(request,'elements/index.html', 
                  {'elements': paginator.get_page(page_number), 
                        'search' : search, 
                        'category_id': category_id,
                        'categories': categories
                        })

# def detail(request, pk):
def detail(request, slug):

    element = Element.objects.get(slug=slug)
    return render(request,'elements/detail.html',
                  {'element': element, 'paypal_client_id': 
                   settings.PAYPAL_CLIENT_ID})

def capture_payment(request, order_id):

    paypal = PayPalPayment()
    res = paypal.capture_order(order_id)

    if res:
        return render(request,'elements/capture_payment.html', {'res': res, 
                                                                'id': res['id'], 
                                                                'status': res['status'], 
                                                                'price': res['purchase_units'][0]['payments']['captures'][0]['amount']['value']})	

    return render(request,'elements/error.html')	