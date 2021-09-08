import uuid
from django.db import transaction

from ..models import Contato

class ContatoService:
    @classmethod
    def salvar_contato(cls, usuario_id, data):
        try:
            uuid.UUID(usuario_id)
        except:
            raise Exception({
                'error': {
                    'detail': 'id de usuário inválido',
                },
                'status': 400
            })

        with transaction.atomic():
            nome = data.get('nome')
            matricula = data.get('matricula')
            email_institucional = data.get('email_institucional')
            email_pessoal = data.get('email_pessoal')

            ct = Contato.objects.filter(usuario_id=usuario_id).first()

            if not ct:
                if not nome or not matricula or not email_institucional:
                    raise Exception({
                        'error': {
                            'detail': 'Informações pendentes para salvar contato',
                        },
                        'status': 422
                    })

                ct = Contato()
                ct.usuario_id = usuario_id

            if nome is not None:
                ct.nome = nome
            
            if matricula is not None:
                ct.matricula = matricula

            if email_institucional is not None:
                ct.email_institucional = email_institucional

            if email_pessoal is not None:
                ct.email_pessoal = email_pessoal
            
            ct.save()
