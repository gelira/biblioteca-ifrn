from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action

from ..models import Livro
from ..serializers import LivroSerializer

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    permission_classes = []
    lookup_value_regex = '[a-f0-9]{8}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{12}'
    
    def get_object(self):
        return get_object_or_404(self.queryset, _id=self.kwargs['pk'])
