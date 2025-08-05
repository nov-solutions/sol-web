from rest_framework import serializers

from .models import ConnectedAccount, Customer, Invoice, Subscription


class ConnectedAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedAccount
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    connected_account = ConnectedAccountSerializer()

    class Meta:
        model = Subscription
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    connected_account = ConnectedAccountSerializer()
    subscription = SubscriptionSerializer()

    class Meta:
        model = Invoice
        fields = "__all__"
