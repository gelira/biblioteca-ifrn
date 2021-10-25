const interpreter = '/home/geraldo/Projetos/biblioteca-ifrn/env/bin/python';

module.exports = {
  apps: [
    {
      name: 'gateway-dev',
      interpreter,
      cwd: '/home/geraldo/Projetos/biblioteca-ifrn/services/gateway',
      script: './manage.py',
      args: 'runserver'
    },
    {
      name: 'autenticacao-dev',
      interpreter,
      cwd: '/home/geraldo/Projetos/biblioteca-ifrn/services/autenticacao',
      script: './manage.py',
      args: 'runserver 8001'
    },
    {
      name: 'catalogo-dev',
      interpreter,
      cwd: '/home/geraldo/Projetos/biblioteca-ifrn/services/catalogo',
      script: './manage.py',
      args: 'runserver 8002'
    },
    {
      name: 'circulacao-dev',
      interpreter,
      cwd: '/home/geraldo/Projetos/biblioteca-ifrn/services/circulacao',
      script: './manage.py',
      args: 'runserver 8003'
    },
    {
      name: 'avaliacao-dev',
      interpreter,
      cwd: '/home/geraldo/Projetos/biblioteca-ifrn/services/avaliacao',
      script: './manage.py',
      args: 'runserver 8004'
    },
    {
      name: 'aquisicao-dev',
      interpreter,
      cwd: '/home/geraldo/Projetos/biblioteca-ifrn/services/aquisicao',
      script: './manage.py',
      args: 'runserver 8005'
    },
    
    {
      name: 'circulacao-worker-dev',
      interpreter: '',
      cwd: '/home/geraldo/Projetos/biblioteca-ifrn/services/circulacao',
      script: '/home/geraldo/Projetos/biblioteca-ifrn/env/bin/python -m ' + 
        'celery -A circulacao worker -l info -n circulacaoworker -Q circulacao -f worker.log'
    },
    {
      name: 'avaliacao-worker-dev',
      interpreter: '',
      cwd: '/home/geraldo/Projetos/biblioteca-ifrn/services/avaliacao',
      script: '/home/geraldo/Projetos/biblioteca-ifrn/env/bin/python -m ' + 
        'celery -A avaliacao worker -l info -n avaliacaoworker -Q avaliacao -f worker.log'
    },
    {
      name: 'notificacao-worker-dev',
      interpreter: '',
      cwd: '/home/geraldo/Projetos/biblioteca-ifrn/services/notificacao',
      script: '/home/geraldo/Projetos/biblioteca-ifrn/env/bin/python -m ' + 
        'celery -A notificacao worker -l info -n notificacaoworker -Q notificacao -f worker.log'
    },
    {
      name: 'catalogo-worker-dev',
      interpreter: '',
      cwd: '/home/geraldo/Projetos/biblioteca-ifrn/services/catalogo',
      script: '/home/geraldo/Projetos/biblioteca-ifrn/env/bin/python -m ' + 
        'celery -A catalogo worker -l info -n catalogoworker -Q catalogo -f worker.log'
    },
    {
      name: 'autenticacao-worker-dev',
      interpreter: '',
      cwd: '/home/geraldo/Projetos/biblioteca-ifrn/services/autenticacao',
      script: '/home/geraldo/Projetos/biblioteca-ifrn/env/bin/python -m ' + 
        'celery -A autenticacao worker -l info -n autenticacaoworker -Q autenticacao -f worker.log'
    },
    {
      name: 'aquisicao-worker-dev',
      interpreter: '',
      cwd: '/home/geraldo/Projetos/biblioteca-ifrn/services/aquisicao',
      script: '/home/geraldo/Projetos/biblioteca-ifrn/env/bin/python -m ' + 
        'celery -A aquisicao worker -l info -n aquisicaoworker -Q aquisicao -f worker.log'
    },

    {
      name: 'circulacao-beat-dev',
      interpreter: '',
      cwd: '/home/geraldo/Projetos/biblioteca-ifrn/services/circulacao',
      script: '/home/geraldo/Projetos/biblioteca-ifrn/env/bin/python -m ' + 
        'celery -A circulacao beat -l info -f beat.log'
    },
  ],
};
