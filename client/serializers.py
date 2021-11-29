from rest_framework import serializers
from django.db import connection

from client.models import Client

      
class ClientTenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name','domain_url','schema_name','paid_until','on_trial']
    
    def create(self, validated_data):
        connection.set_schema("public")
        obj = Client(**validated_data)
        obj.save()
        return obj