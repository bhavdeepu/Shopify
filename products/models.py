from django.db import models
from django.conf import settings


def get_image_filename(instance, filename):
    name=instance.name
    if instance.__class__.__name__ == 'Categories':
        return 'categories/%s/'%(filename)

    if instance.__class__.__name__ == 'Product':
        return 'product/%s/'%(filename)


class Categories(models.Model):

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cat_created_by')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                    related_name='cat_modified_by', null=True, blank=True)
    is_trashed = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)

    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(default='default.png',blank=True, null=True,upload_to=get_image_filename)
    parent = models.ForeignKey('Categories', on_delete=models.CASCADE, null=True, blank=True)


class Product(models.Model):

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pro_created_by')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                    related_name='pro_modified_by', null=True, blank=True)
    is_trashed = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    category = models.ForeignKey(Categories, on_delete=models.CASCADE, 
            related_name='pro_category')
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    image = models.ImageField(default='default.png',blank=True, null=True,upload_to=get_image_filename)


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(default='default.png', blank=True, upload_to=get_image_filename)


class Cart(models.Model):

    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_created_by')
    product = models.ManyToManyField(Product, related_name='cart_product')


