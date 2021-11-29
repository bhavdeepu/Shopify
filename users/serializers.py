from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from users.models import EcomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):

   
    class Meta:
        model = EcomUser
        fields = ['id', 'email','first_name', 'is_superuser', 'last_name', 'mobile_no',
                    'user_type','date_joined','about','gender','d_o_b','is_active']


        
class UserRegisterSerializer(serializers.ModelSerializer):
   
    password2 = serializers.CharField()

    class Meta:
        model = EcomUser
        fields = ['email','first_name','last_name','mobile_no','images','gender','password','password2','is_active']


    def save(self):
        user = EcomUser(mobile_no=self.data['mobile_no'])

        if self.data['password'] != self.data['password2']:
            raise serializers.ValidationError({'password':'Password must be same'})

        user.set_password(self.data['password'])
        # if not (self.data['email'] or self.data['mobile_no']):
        #     raise serializers.ValidationError({'Error':'Email or Mobile no both cannot be null'})

        if self.data['email']:
            old_user = EcomUser.objects.filter(email=self.data['email']).first()
            if old_user:
                raise serializers.ValidationError({'Error':'Email already exist'})


        if not self.data['first_name']:
            raise serializers.ValidationError({'first_name':'First name cannot be empty'})
        user.first_name = self.data['first_name']

        if 'last_name' in self.data:
            user.last_name = self.data['last_name']
        if 'mobile_no' in self.data:
            user.mobile_no = self.data['mobile_no']
        if 'images' in self.data:
            user.images = self.data['images']
        if 'gender' in self.data:
            user.gender = self.data['gender']
        if 'ref_through' in self.data:
            ref_user = EcomUser.objects.filter(ref_code=self.data['ref_through']).first()
            if ref_user:
                user.refrence_through = ref_user

        user.save()
        user.ref_code = user.first_name[-4:] + str(user.id)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcomUser
        fields = ['id', 'url', 'email', 'first_name', 'is_superuser', 'last_name', 'mobile_no', 'images',
                    'about', 'gender', 'd_o_b', 'firebase_token', 'full_address' ,'aadhar_no', 'experience_year',
                    'pan_card', 'categories', 'sub_categories','is_active']


