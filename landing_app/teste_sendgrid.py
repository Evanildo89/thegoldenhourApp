import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, MailSettings, SandBoxMode
from dotenv import load_dotenv

# Carrega o .env do projeto
load_dotenv(dotenv_path="../.env")  # ajuste o caminho se necessário

print("SENDGRID_API_KEY:", os.environ.get("SENDGRID_API_KEY"))

# E-mail de destino (cliente externo)
destinatario = "vany_casal@hotmail.com"

# E-mail de envio (deve estar verificado no SendGrid)
remetente = "evanildovrodrigues@gmail.com"

# Conteúdo do e-mail
mensagem = Mail(
    from_email=remetente,
    to_emails=destinatario,
    subject="Teste de envio SendGrid",
    html_content="<strong>Olá! Este é um teste de envio para o cliente.</strong>"
)

# Configurações de e-mail (sandbox desativado)
mensagem.mail_settings = MailSettings(sandbox_mode=SandBoxMode(enable=False))

try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(mensagem)
    print(f"Status Code: {response.status_code}")
    print(f"Body: {response.body}")
    print(f"Headers: {response.headers}")
except Exception as e:
    print(f"Erro ao enviar e-mail: {e}")