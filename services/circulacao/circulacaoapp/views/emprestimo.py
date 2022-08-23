from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from ..services import EmprestimoService
from ..models import Emprestimo
from ..serializers import (
    EmprestimoRetrieveSerializer,
    EmprestimoCreateSerializer,
    DevolucaoEmprestimosSerializer,
    RenovacaoEmprestimosSerializer
)
from ..permissions import (
    AutenticadoPermissao,
    FazerEmprestimoPermissao,
    AvaliacaoServicePermissao
)

class EmprestimoViewSet(ModelViewSet):
    lookup_value_regex = '[a-f0-9]{8}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{12}'
    queryset = Emprestimo.objects.all()
    permission_classes = [
        AutenticadoPermissao,
        FazerEmprestimoPermissao
    ]
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(usuario_id=self.request.user['_id']).order_by('-created').all()

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), 
            _id=self.kwargs['pk']
        )

    def get_serializer_class(self):
        if self.action == 'devolucoes':
            return DevolucaoEmprestimosSerializer
        
        if self.action == 'renovacoes':
            return RenovacaoEmprestimosSerializer
        
        if self.action in ['retrieve', 'list']:
            return EmprestimoRetrieveSerializer
        
        return EmprestimoCreateSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [
                AutenticadoPermissao()
            ]

        if self.action == 'emprestimo_avaliado':
            return [
                AutenticadoPermissao(),
                AvaliacaoServicePermissao()
            ]

        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='devolucoes')
    def devolucoes(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='renovacoes', permission_classes=[AutenticadoPermissao])
    def renovacoes(self, request):
        request.data['faz_emprestimo'] = FazerEmprestimoPermissao().has_permission(request, self)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True, url_path='avaliado', authentication_classes=[], permission_classes=[])
    def emprestimo_avaliado(self, request, pk):
        EmprestimoService.emprestimo_avaliado(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
