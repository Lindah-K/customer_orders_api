from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from orders.models import Customer, Order

class CustomerOrderAcceptanceTest(TestCase):
    def setUp(self):
        # URL names that you will use in your project
        self.create_customer_url = reverse('customer-list')  # Assuming your CustomerViewSet uses 'customer-list' name
        self.create_order_url = reverse('order-list')  # Assuming your OrderViewSet uses 'order-list' name

        # Create a sample customer
        self.customer_data = {
            "name": "Jane Doe",
            "code": "CUST456",
            "phone_number":"+2547402229525"
        }
        self.customer = Customer.objects.create(**self.customer_data)
    
    def test_create_customer(self):
        """
        Test the API to create a customer and verify response status and data
        """
        # Sample data to create a customer
        new_customer_data = {
            "name": "John Doe",
            "code": "CUST789",
            "phone_number":"+254102369051"
        }
        
        # Make POST request to create a new customer
        response = self.client.post(self.create_customer_url, data=new_customer_data, content_type='application/json')
        
        # Assert the customer was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], new_customer_data['name'])
        self.assertEqual(response.data['code'], new_customer_data['code'])
    
    def test_create_order(self):
        """
        Test the API to create an order and verify response status and data
        """
        # Sample data for creating an order
        new_order_data = {
            "item": "Smartphone",
            "amount": "800.00",
            "customer": self.customer.id  
        }
        
        # Make POST request to create a new order
        response = self.client.post(self.create_order_url, data=new_order_data, content_type='application/json')

        # Assert that the order was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['item'], new_order_data['item'])
        self.assertEqual(response.data['amount'], new_order_data['amount'])
        self.assertEqual(response.data['customer'], self.customer.id)
    
    def test_create_order_invalid_customer(self):
        """
        Test that creating an order with an invalid customer returns an error
        """
        # Sample data for creating an order with an invalid customer
        new_order_data = {
            "item": "Laptop",
            "amount": "1200.00",
            "customer": 9999  # Invalid customer ID
        }
        
        # Make POST request to create a new order with invalid customer
        response = self.client.post(self.create_order_url, data=new_order_data, content_type='application/json')
        
        # Assert that the request fails with a 400 status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_customers(self):
        """
        Test the API to list customers
        """
        # Make GET request to fetch the list of customers
        response = self.client.get(self.create_customer_url)
        
        # Assert that the response status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert that the customer created in setup is listed
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.customer_data['name'])

    def test_list_orders(self):
        """
        Test the API to list orders
        """
        # Create a sample order for the customer
        Order.objects.create(item="Smartphone", amount="800.00", customer=self.customer)
        
        # Make GET request to fetch the list of orders
        response = self.client.get(self.create_order_url)
        
        # Assert that the response status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert that the order created is listed
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['item'], "Smartphone")
        self.assertEqual(response.data[0]['amount'], "800.00")
        self.assertEqual(response.data[0]['customer'], self.customer.id)
    
    def test_order_creation_without_customer(self):
        response = self.client.post('/api/orders/', {
            'item': 'Tablet',
            'amount': 300,
            # No customer provided
        })
        self.assertEqual(response.status_code, 400)
