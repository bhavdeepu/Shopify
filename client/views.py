from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.db import connection
from datetime import date
from dateutil.relativedelta import relativedelta
from rest_framework_simplejwt.tokens import RefreshToken

from client.serializers import ClientTenantSerializer
from client.models import Client
from users.models import EcomUser

class ClientTenan(viewsets.ModelViewSet):

    serializer_class = ClientTenantSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return Client.objects.all()

    @action(methods=['post'], detail=False,
        url_path='client', url_name='client')
    def client(self, request):
        connection.set_schema("public")
        name = request.data['name']
        email = request.data['email']
        password = request.data['password']
        store = request.data['store']
        

        store_schema = store.replace(' ', '-').lower()
        store_schema = ''.join(e for e in store if e.isalnum() or e == '-')

        
        paid_until = date.today() + relativedelta(months=+6)

        tenant = Client(domain_url=store_schema+'.localhost',
                        schema_name=store_schema,
                        name=store ,
                        paid_until=paid_until,
                        on_trial=True)
        tenant.save()
        connection.set_schema(tenant.schema_name)
        user = EcomUser(first_name = name.split()[0],
                last_name =  name[len(name.split()[0])+1:],
                email = email,
                is_active = True,
                user_type = 'ADM',
                date_joined = date.today(),
                tenant_admin = True)

        user.save()
        
        refresh = RefreshToken.for_user(user)

        return Response({'refresh': str(refresh),'access': str(refresh.access_token)}, status=status.HTTP_200_OK)