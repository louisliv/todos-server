CROSSORIGIN_PORT = '8080'
CROSSORIGIN_LOCALHOST = f'http://localhost:{CROSSORIGIN_PORT}'

CONFIG = {
  'ORIGINS': [
    CROSSORIGIN_LOCALHOST,
    f'http://127.0.0.1:{CROSSORIGIN_PORT}',
  ],
}