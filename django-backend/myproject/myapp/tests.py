from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer

class OrderViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.order1 = Order.objects.create(customer_name='John Doe', total_amount=100.0)
        self.order2 = Order.objects.create(customer_name='Jane Smith', total_amount=200.0)

    def test_list_orders(self):
        response = self.client.get('/orders/')
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_order(self):
        data = {'customer_name': 'Alice', 'total_amount': 300.0}
        response = self.client.post('/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 3)

    def test_retrieve_order(self):
        response = self.client.get(f'/orders/{self.order1.pk}/')
        order = Order.objects.get(pk=self.order1.pk)
        serializer = OrderSerializer(order)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_order(self):
        data = {'customer_name': 'Updated Name', 'total_amount': 150.0}
        response = self.client.put(f'/orders/{self.order1.pk}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.get(pk=self.order1.pk).customer_name, 'Updated Name')

    def test_delete_order(self):
        response = self.client.delete(f'/orders/{self.order1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 1)
