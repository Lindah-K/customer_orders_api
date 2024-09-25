from django.test import TestCase
from orders.models import Customer, Order

class CustomerModelTest(TestCase):
    def test_customer_creation(self):
        customer = Customer.objects.create(name="John Doe", code="CUST123", phone_number="+254740229525")
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(customer.code, "CUST123")
        self.assertEqual(customer.phone_number, "+254740229525")


class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="John Doe", code="CUST123", phone_number="+254740229525")

    def test_order_creation(self):
        order = Order.objects.create(item="Laptop", amount=1200, customer=self.customer)
        self.assertEqual(order.item, "Laptop")
        self.assertEqual(order.amount, 1200)
        self.assertEqual(order.customer, self.customer)
