from django.db import models
from tenant_schemas.models import TenantMixin


# This TenantMixin only has two fields (domain_url and schema_name) and both are required


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until =  models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True



# tenant = Client(domain_url='tenant.my-domain.com', # don't add your port or www here!
#                 schema_name='tenant1',
#                 name='Fonzy Tenant',
#                 paid_until='2014-12-05',
#                 on_trial=True)


# tenant = Client(domain_url='merashehar.localhost', schema_name='localhost', name='Bhavdeep Upadhyay',paid_until='2920-12-05', on_trial=False)