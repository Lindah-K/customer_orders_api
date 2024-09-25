from django.test import TestCase
from orders.models import Customer, Order
from orders.serializers import CustomerSerializer, OrderSerializer

class CustomerSerializerTest(TestCase):
    def test_customer_serializer(self):
        customer = Customer.objects.create(name="Jane Doe", code="CUST456", phone_number="+254740229525")
        serializer = CustomerSerializer(customer)
        data = serializer.data
        self.assertEqual(data['name'], "Jane Doe")
        self.assertEqual(data['code'], "CUST456")
        self.assertEqual(data['phone_number'],"+254740229525")

class OrderSerializerTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Jane Doe", code="CUST456", phone_number="+254740229525")

    def test_order_serializer(self):
        order = Order.objects.create(item="Smartphone", amount='800.00', customer=self.customer)
        serializer = OrderSerializer(order)
        data = serializer.data
        self.assertEqual(data['item'], "Smartphone")
        self.assertEqual(data['amount'], '800.00')  
        self.assertEqual(data['customer'], self.customer.id)
