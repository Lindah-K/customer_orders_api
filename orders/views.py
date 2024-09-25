from django.conf import settings
from rest_framework import viewsets
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated 
from django.http import JsonResponse
import africastalking
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required



africastalking.initialize("sandbox", settings.SMS_API_KEY)
sms = africastalking.SMS

def send_sms(customer_phone, message):
    if not customer_phone:
        print("Error: Customer phone number is empty.")
        return
    print(f"Sending SMS to: {customer_phone}")
    if not customer_phone.startswith('+'):
        print(f"Error: Invalid phone number format: {customer_phone}")
        raise ValueError("Invalid phone number: " + customer_phone)
    sms.send(message, [customer_phone])

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling order-related operations.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.save() #save the customer
        customer = order.customer
        print(f"Order created for customer: {customer}")  
        print(f"Customer phone number: {customer.phone_number}") 
        if customer: #ensure the customer exists
            send_sms(customer.phone_number, f"Dear {customer.name}, your order has been received: {order.item} - {order.amount}")

class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling customer-related operations.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]


def login(request):
    return redirect('/home/')

@login_required
def home(request):
    return redirect('/api/')

