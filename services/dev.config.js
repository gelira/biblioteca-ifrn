const interpreter = '/home/geraldo/Projetos/Biblioteca IFRN/env/bin/python';

module.exports = {
  apps : [
    {
      name: 'gateway-dev',
      interpreter,
      cwd: '/home/geraldo/Projetos/Biblioteca IFRN/services/gateway',
      script: './manage.py',
      args: 'runserver',
      env: {
        DEBUG: '1',
        SECRET_KEY: '0avvuHjyx5nWCFvVpg3SZuiGCTIIk6eeILNlBfgy2gDSIwOAFxhSbLlv8g5bB0oDheKHbi',
        REDIS_HOST: '172.25.0.11',
        AUTENTICACAO_SERVICE_URL: 'http://127.0.0.1:8001'
      }
    },
    {
      name: 'autenticacao-dev',
      interpreter,
      cwd: '/home/geraldo/Projetos/Biblioteca IFRN/services/autenticacao',
      script: './manage.py',
      args: 'runserver 8001',
      env: {
        DEBUG: '1',
        SECRET_KEY: 'sCM8UOw4T7i1cjYTtpGRDzhZGYbQ02xZApcNWtxt9duvuUPyr9jImSwjp1MjQ6ZuyMDEtG',
        DB_NAME: 'autenticacao_integrador',
        DB_USER: 'postgres',
        DB_PASSWORD: 'abc@123',
        DB_HOST: '127.0.0.1',
        DB_PORT: '5432'
      }
    }
  ],
};
