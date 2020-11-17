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
      script: '/home/geraldo/Projetos/Biblioteca\\ IFRN/env/bin/python -m celery -A circulacao worker -l info'
    }
  ],
};
