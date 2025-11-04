#!/bin/bash

# Navega para o diretório do Django
cd landing_app

# Instala dependências
pip install -r requirements.txt

# Aplica migrações
python manage.py migrate

# Coleta arquivos estáticos
python manage.py collectstatic --noinput

# Inicia o servidor
gunicorn landing_app.wsgi --bind 0.0.0.0:$PORT