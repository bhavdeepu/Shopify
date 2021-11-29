from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from datetime import date, timedelta

from users.models import EcomUser
from users.serializers import UserSerializer, UserRegisterSerializer


class UserViewSet(viewsets.ModelViewSet):

    # authentication_classes = (TokenAuthentication,)
    
    permission_classes = (AllowAny, )
    queryset = EcomUser.objects.all()

    # def get_permissions(self):
    #     if self.request.method in ['GET','PATCH','PUT']:
    #         return [IsAuthenticated(),]
    #     else:
    #         return [AllowAny(),]

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserRegisterSerializer
        if self.action in ['update']:
            return UserUpdateSerializer
        else:
            return UserSerializer

    # def get_queryset(self):
    #     queryset = EcomUser.objects.all()

    #     return queryset

    def perform_update(self, serializer):
        super(UserViewSet, self).perform_update(serializer)
        instance = self.get_object()
        key = self.request.data        
        if 'categories' in key:
            all_categories = Categories.objects.filter(id__in=key['categories']).exclude(
                                    id__in=instance.categories.values_list('id'))
            categories = EcomUser.categories.through
            relations = []
            for cat in all_categories:
                relations.extend([categories(
                                    appuser_id=instance.id,
                                    categories_id=cat.id
                                )])
            if relations:
                categories.objects.bulk_create(relations)

        if 'ref_through' in key:
            ref_user = EcomUser.objects.filter(ref_code=key['ref_through']).first()
            if ref_user:
                instance.refrence_through = ref_user
                instance.save()

        return instance

    @action(methods=['get'], detail=False,
            url_path='currentuser', url_name='currentuser')
    def currentuser(self, request):
        users_data = self.get_serializer(request._user,context={'request': request}).data
        return Response(users_data, status=status.HTTP_200_OK)




class ObtainAuthToken(ObtainAuthToken):
    def post(self, request):

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if 'firebase' in request.data:
            user.firebase_token = request.data['firebase']
            user.save()

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'first_name': user.first_name
        })

        return Response(content)

