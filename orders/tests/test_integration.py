from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from orders.models import Customer, Order
from unittest.mock import patch

class OrderIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name="John Doe", code="CUST123", phone_number="+254740229525")

    @patch('orders.views.send_sms')
    def test_create_order_triggers_sms(self, mock_send_sms):
        url = "/api/orders/"
        data = {
            "item": "Smartphone",
            "amount": 800,
            "customer": self.customer.id
        }
        response = self.client.post(url, data, format='json')
        
        # Check API response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that order is created in the database
        self.assertEqual(Order.objects.count(), 1)
        
        # Check that SMS was sent
        mock_send_sms.assert_called_once_with(self.customer.phone_number, "New order placed: Smartphone - 800.00")
        
    @patch('orders.views.send_sms')
    def test_create_customer(self, mock_send_sms):
        url = "/api/customers/"
        data = {
            "name": "Jane Smith",
            "code": "CUST456",
            "phone_number": "+254740229525"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(Customer.objects.get(id=response.data['id']).name, "Jane Smith")
        # Ensure SMS was not triggered during customer creation
        mock_send_sms.assert_not_called()

    def test_list_orders(self):
        Order.objects.create(item="Laptop", amount=1200, customer=self.customer)
        url = "/api/orders/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['item'], "Laptop")

    def test_list_customers(self):
        url = "/api/customers/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "John Doe")

    @patch('orders.views.send_sms')  
    def test_create_order_without_phone(self, mock_send_sms):
        # Create a customer with an empty phone number
        customer = Customer.objects.create(name="Test User", code="CUST999", phone_number="")
        response = self.client.post('/api/orders/', {
            'item': 'Tablet',
            'amount': 300,
            'customer': customer.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_send_sms.assert_called_once()  # Check that send_sms was called, but no valid phone
