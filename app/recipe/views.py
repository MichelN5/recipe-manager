from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipe import serializers
from core.models import Tag, Ingredient

# Create your views here.

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    authentication_classes= (TokenAuthentication, )
    permission_classes= (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class= serializers.TagSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    def perforsm_create(self, serializer):
        serializer.save(user= self.request.user)



    

