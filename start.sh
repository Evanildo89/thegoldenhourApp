#!/bin/bash

# Navega para o diretório do Django
cd landing_app

# Ativa o venv se necessário (ou confia no Railway)
# pip install dependências
pip install -r requirements.txt

# Aplica migrações
python manage.py migrate

# Coleta arquivos estáticos
python manage.py collectstatic --noinput

# Inicia o Gunicorn na porta do Railway
gunicorn landing_app.wsgi:application --bind 0.0.0.0:$PORT