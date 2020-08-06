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
    }
  ],
};
