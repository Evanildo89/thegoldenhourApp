# Usa imagem oficial do Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia tudo para dentro do container
COPY . /app

# Atualiza pip e instala dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn dj-database-url psycopg2-binary

# Aplica migrações e coleta estáticos
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Exponha a porta que o Railway vai usar
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:$PORT"]