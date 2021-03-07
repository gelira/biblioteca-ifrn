const interpreter = '/home/geraldo/Projetos/Biblioteca IFRN/env/bin/python';

module.exports = {
  apps: [
    {
      name: 'gateway-dev',
      interpreter,
      cwd: '/home/geraldo/Projetos/Biblioteca IFRN/services/gateway',
      script: './manage.py',
      args: 'runserver'
    },
    {
      name: 'autenticacao-dev',
      interpreter,
      cwd: '/home/geraldo/Projetos/Biblioteca IFRN/services/autenticacao',
      script: './manage.py',
      args: 'runserver 8001'
    },
    {
      name: 'catalogo-dev',
      interpreter,
      cwd: '/home/geraldo/Projetos/Biblioteca IFRN/services/catalogo',
      script: './manage.py',
      args: 'runserver 8002'
    },
    {
      name: 'circulacao-dev',
      interpreter,
      cwd: '/home/geraldo/Projetos/Biblioteca IFRN/services/circulacao',
      script: './manage.py',
      args: 'runserver 8003'
    },
    {
      name: 'avaliacao-dev',
      interpreter,
      cwd: '/home/geraldo/Projetos/Biblioteca IFRN/services/avaliacao',
      script: './manage.py',
      args: 'runserver 8004'
    },
    
    {
      name: 'circulacao-worker-dev',
      interpreter: '',
      cwd: '/home/geraldo/Projetos/Biblioteca IFRN/services/circulacao',
      script: '/home/geraldo/Projetos/Biblioteca\\ IFRN/env/bin/python -m ' + 
        'celery -A circulacao worker -l info -n circulacaoworker -Q circulacao -f worker.log'
    },
    {
      name: 'avaliacao-worker-dev',
      interpreter: '',
      cwd: '/home/geraldo/Projetos/Biblioteca IFRN/services/avaliacao',
      script: '/home/geraldo/Projetos/Biblioteca\\ IFRN/env/bin/python -m ' + 
        'celery -A avaliacao worker -l info -n avaliacaoworker -Q avaliacao -f worker.log'
    },
    {
      name: 'notificacao-worker-dev',
      interpreter: '',
      cwd: '/home/geraldo/Projetos/Biblioteca IFRN/services/notificacao',
      script: '/home/geraldo/Projetos/Biblioteca\\ IFRN/env/bin/python -m ' + 
        'celery -A notificacao worker -l info -n notificacaoworker -Q notificacao -f worker.log'
    }
  ],
};
