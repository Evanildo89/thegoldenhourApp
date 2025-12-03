from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view
from .models import Service, Booking, Professional, Review
from .serializers import ServiceSerializer, BookingSerializer, DisponibilidadeSerializer, ProfessionalSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime, logging
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from urllib.parse import quote
from django.conf import settings
logger = logging.getLogger(__name__)

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

HORARIOS_DISPONIVEIS = ["07:00","09:00","11:00","14:00","16:00","18:00"]

class DisponibilidadeView(APIView):
    def get(self, request, service_id):
        service = Service.objects.get(id=service_id)
        prof_id = request.query_params.get('prof_id')

        # ✅ Se prof_id for válido (numérico e não nulo), filtra por profissional
        if prof_id and prof_id.isdigit():
            bookings = Booking.objects.filter(professional_id=int(prof_id))
        else:
            # ✅ Caso contrário, filtra apenas pelo service_id (fluxo vindo da página "Serviços")
            bookings = Booking.objects.filter(service=service)

        ocupados = {}
        for b in bookings:
            data_str = b.date.strftime("%Y-%m-%d")
            if data_str not in ocupados:
                ocupados[data_str] = []
            ocupados[data_str].append(b.time.strftime("%H:%M"))

        serializer = DisponibilidadeSerializer({
            "horarios_disponiveis": HORARIOS_DISPONIVEIS,
            "ocupados": ocupados
        })
        return Response(serializer.data)

class ProfessionalListAPIView(generics.ListAPIView):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer

@csrf_exempt
def enviar_confirmacao_email(request):
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:3000')
    print("BASE_URL usada no e-mail:", BASE_URL)
    if request.method == 'POST':
        data = json.loads(request.body)
        nome = data.get('nome')
        email = data.get('email')
        morada = data.get('morada', '--')
        data_reserva = data.get('data')
        hora_reserva = data.get('hora')
        duracao = data.get('duracao')
        servico = data.get('servico')
        profissional_json = data.get('profissional')
        total = data.get('total')
        lembrete = data.get('lembrete', False)  # True ou False

        try:
            prof_obj = json.loads(profissional_json)
            prof_nome = prof_obj.get('name', '')
            prof_bio = prof_obj.get('bio', '')
        except:
            prof_nome = ''
            prof_bio = ''

        assunto = "Confirmação da sua reserva - The Golden Light Photography"

        dias_semana = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        ano, mes, dia = map(int, data_reserva.split("-"))
        date_obj = datetime.date(ano, mes, dia)
        dia_semana = dias_semana[date_obj.weekday()]
        data_formatada = f"{dia_semana}. {dia} {meses[mes-1]}, {ano}"

        html_mensagem = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 10px;
                }}
                .container {{
                    display: flex;
                    max-width: 700px;
                    margin: auto;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                    flex-wrap: wrap;
                }}
                .box-esquerda, .box-direita {{
                    box-sizing: border-box;
                }}
                .box-esquerda {{
                    background-color: #ffffff;
                    padding: 20px;
                    width: 60%;
                    min-width: 250px;
                }}
                .box-esquerda h1 {{
                    font-size: 22px;
                    font-weight: bold;
                    color: #000000;
                    margin-bottom: 10px;
                }}
                .box-esquerda p, .box-esquerda .info {{
                    font-size: 14px;
                    color: #333;
                    margin: 4px 0;
                }}
                .divider {{
                    border-top: 1px solid #ccc;
                    margin: 15px 0;
                }}
                .fornecedor {{
                    margin-top: 8px;
                    font-size: 14px;
                }}
                .box-direita {{
                    background-color: #e0e0e0;
                    width: 40%;
                    min-width: 200px;
                    padding: 20px;
                    text-align: center;
                }}
                .profissional-nome {{
                    font-weight: bold;
                    font-size: 16px;
                    margin-bottom: 15px;
                }}
                .botao {{
                     display: block;
                        width: 100%;
                        margin: 8px 0;
                        padding: 8px;
                        font-size: 13px;
                        color: #007bff; /* texto azul */
                        background-color: #ffffff; /* fundo branco */
                        border:1px solid #007bff; /* borda azul */
                        text-decoration: none;
                        border-radius: 5px;
                        box-sizing: border-box;
                }}
                @media only screen and (max-width: 480px) {{
                    .container {{
                        flex-direction: column;
                    }}
                    .box-esquerda, .box-direita {{
                        width: 100% !important;
                        padding: 15px;
                    }}
                    .box-esquerda h1 {{
                        font-size: 20px;
                    }}
                    .box-esquerda p, .box-esquerda .info {{
                        font-size: 13px;
                    }}
                    .profissional-nome {{
                        font-size: 14px;
                    }}
                    .botao {{
                        font-size: 14px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="box-esquerda">
                    <h1>Obrigado!</h1>
                    <p>Olá {nome},</p>
                    <p>O seu compromisso foi agendado com sucesso!</p>

                    <div class="divider"></div>

                    <div class="info"><strong>Quando:</strong> {data_formatada} às {hora_reserva}</div>
                    <div class="info"><strong>Serviço:</strong> {servico}</div>
                    <div class="fornecedor"><strong>Fornecedor:</strong> {prof_nome} - {prof_bio}</div>
                    <div class="info"><strong>Valor:</strong> €{total}</div>

                    <div class="divider"></div>

                    <div class="assinatura">Thanks,<br>{prof_nome}</div>
                </div>

                <div class="box-direita">
                    <div class="profissional-nome">{prof_nome}</div>
                    <a href="{BASE_URL}/detalhes-reserva.html?nome={quote(nome)}&email={quote(email)}&servico={quote(servico)}&morada={quote(morada)}&data={quote(data_formatada)}&hora={quote(hora_reserva)}&valor={quote(total)}&fornecedor={quote(prof_nome)}&prof={quote(prof_nome)}&duracao={quote(duracao)}&bio={quote(prof_bio)}" class="botao">Reagendar</a>
<a href="{BASE_URL}/detalhes-reserva.html?nome={quote(nome)}&email={quote(email)}&servico={quote(servico)}&morada={quote(morada)}&data={quote(data_formatada)}&hora={quote(hora_reserva)}&valor={quote(total)}&fornecedor={quote(prof_nome)}&prof={quote(prof_nome)}&duracao={quote(duracao)}&bio={quote(prof_bio)}" class="botao">Cancelar compromisso</a>
<a href="{BASE_URL}/nova-consulta" class="botao">Marcar nova consulta</a>
                </div>
            </div>
        </body>
        </html>
        """

        if lembrete and email:
            try:
                email_msg = EmailMultiAlternatives(
                    subject=assunto,
                    body="Confirmação da sua reserva",
                    from_email=settings.DEFAULT_FROM_EMAIL,  # Use DEFAULT_FROM_EMAIL
                    to=[email]
                )
                email_msg.attach_alternative(html_mensagem, "text/html")
                email_msg.send(fail_silently=False)
            except Exception as e:
                logger.exception(f"Erro ao enviar e-mail para o cliente {email}: {e}")

        try:
            email_responsavel = settings.DEFAULT_FROM_EMAIL   # trocar pelo e-mail real
            html_mensagem_responsavel = f"""
                    <html>
                    <body>
                        <p>Olá,</p>
                        <p>O cliente <strong>{nome}</strong> agendou uma nova marcação.</p>
                        <p><strong>Serviço:</strong> {servico}</p>
                        <p><strong>Data e hora:</strong> {data_formatada} às {hora_reserva}</p>
                        <p><strong>Profissional:</strong> {prof_nome}- {prof_bio}</p>
                        <p><strong>Valor:</strong> €{total}</p>
                        <p><strong>Duração:</strong> {duracao} min</p>
                        <p>Por favor, atualize a agenda interna conforme necessário.</p>
                    </body>
                    </html>
                    """
            email_msg_responsavel = EmailMultiAlternatives(
                subject=f"Nova reserva: {nome} - {servico}",
                body=f"O cliente {nome} agendou uma marcação para {data_formatada} às {hora_reserva}.",
                from_email=f"The Golden Light Photography <{settings.DEFAULT_FROM_EMAIL}>",
                to=[email_responsavel],
                reply_to=[email],
            )
            email_msg_responsavel.attach_alternative(html_mensagem_responsavel, "text/html")
            email_msg_responsavel.send(fail_silently=False)
        except Exception as e:
            logger.exception(f"Erro ao enviar e-mail interno para responsável: {e}")

        return JsonResponse({'success': True, 'message': 'E-mail enviado com sucesso!'})

    return JsonResponse({'success': False, 'message': 'Método inválido.'})

@csrf_exempt
def enviar_cancelamento_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nome = data.get('nome')
        email = data.get('email')
        servico = data.get('servico')
        data_reserva = data.get('data')
        duracao = data.get('duracao', '--')
        hora_reserva = data.get('hora')
        prof = data.get('profissional')
        total = data.get('total', '--')

        assunto = "Cancelamento da sua reserva - The Golden Light Photography"

        # --- E-mail para o cliente ---
        html_mensagem = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 10px;
                }}
                .container {{
                    max-width: 700px;
                    margin: auto;
                    background-color: #fff;
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #000;
                    font-size: 22px;
                }}
                p {{
                    color: #333;
                    font-size: 15px;
                }}
                .detalhes {{
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #f9f9f9;
                    border-radius: 8px;
                    font-size: 14px;
                }}
                .rodape {{
                    margin-top: 25px;
                    font-size: 13px;
                    color: #555;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>A sua marcação foi cancelada</h1>
                <p>Olá {nome},</p>
                <p>Lamentamos que não possa comparecer, mas a sua marcação foi cancelada com sucesso.</p>

                <div class="detalhes">
                    <strong>Serviço:</strong> {servico}<br>
                    <strong>Data:</strong> {data_reserva}<br>
                    <strong>Hora:</strong> {hora_reserva}<br>
                    <strong>Profissional:</strong> {prof}<br>
                    <strong>Valor:</strong> €{total}
                </div>

                <div class="rodape">
                    <p>Esperamos vê-lo em breve.<br>
                    The Golden Light Photography</p>
                </div>
            </div>
        </body>
        </html>
        """

        # --- Envia e-mail ao cliente ---
        email_cliente = EmailMultiAlternatives(
            subject=assunto,
            body="A sua marcação foi cancelada.",
            from_email=f"The Golden Light Photography <{settings.DEFAULT_FROM_EMAIL}>",
            to=[email],
            reply_to=[email]  # ✅ respostas vão para o cliente
        )
        email_cliente.attach_alternative(html_mensagem, "text/html")
        email_cliente.send(fail_silently=False)

        # --- E-mail interno ---
        try:
            email_responsavel = ["reservas@thedgoldenlight.pt", "evanildovrodrigues@gmail.com"]
            html_mensagem_responsavel = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f8f9fa; padding: 20px;">
                <div style="background-color: #ffffff; border-radius: 10px; padding: 20px; max-width: 600px; margin:auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #c0392b;">❌ Cancelamento de Reserva</h2>
                    <p>O cliente <strong>{nome}</strong> cancelou uma marcação.</p>
                    <hr style="border:none; border-top:1px solid #ddd; margin: 15px 0;">
                    <p><strong>Serviço:</strong> {servico}</p>
                    <p><strong>Data:</strong> {data_reserva}</p>
                    <p><strong>Hora:</strong> {hora_reserva}</p>
                    <p><strong>Profissional:</strong> {prof}</p>
                    <p><strong>Duração:</strong> {duracao} min</p>
                    <p><strong>Valor:</strong> €{total}</p>
                    <p><strong>Email do cliente:</strong> {email}</p>
                    <hr style="border:none; border-top:1px solid #ddd; margin: 15px 0;">
                    <p style="color:#555;">A reserva foi automaticamente removida do sistema.</p>
                    <p style="font-size:13px; color:#999;">The Golden Light Photography — Sistema de reservas</p>
                </div>
            </body>
            </html>
            """

            email_msg_responsavel = EmailMultiAlternatives(
                subject=f"Cancelamento de reserva: {nome} - {servico}",
                body=f"O cliente {nome} cancelou a reserva de {servico} marcada para {data_reserva} às {hora_reserva}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=email_responsavel,
                reply_to=[email]
            )
            email_msg_responsavel.attach_alternative(html_mensagem_responsavel, "text/html")
            email_msg_responsavel.send(fail_silently=False)
        except Exception as e:
            print(f"⚠️ Erro ao enviar e-mail interno: {e}")

        # --- Remover reserva do banco de dados ---
        try:
            from .models import Booking, Service, Professional

            service = Service.objects.filter(title__iexact=servico.strip()).first()
            professional = Professional.objects.filter(name__iexact=prof.strip()).first()

            if not service or not professional:
                print("❌ Serviço ou profissional não encontrado.")
            else:
                # Converter data da string diretamente para date
                try:
                    data_obj = datetime.datetime.strptime(data_reserva.strip(), "%Y-%m-%d").date()
                except ValueError:
                    print(f"❌ Formato de data inválido: {data_reserva}")
                    data_obj = None

                if data_obj:
                    # Converter hora para time
                    try:
                        hora_obj = datetime.datetime.strptime(hora_reserva.strip(), "%H:%M").time()
                    except ValueError:
                        print(f"❌ Formato de hora inválido: {hora_reserva}")
                        hora_obj = None

                    if hora_obj:
                        # Criar intervalo de 5 minutos para ignorar segundos
                        hora_min = hora_obj
                        hora_max = (datetime.datetime.combine(datetime.date.today(), hora_obj) + datetime.timedelta(
                            minutes=5)).time()

                        print("Buscando reserva com:")
                        print(f"email={email.strip().lower()}")
                        print(f"service={service}")
                        print(f"professional={professional}")
                        print(f"data_obj={data_obj}")
                        print(f"hora_min={hora_min}")
                        print(f"hora_max={hora_max}")

                        reserva = Booking.objects.filter(
                            email__iexact=email.strip(),
                            service=service,
                            professional=professional,
                            date=data_obj,
                            time__gte=hora_min,
                            time__lt=hora_max
                        ).first()

                        if reserva:
                            reserva_id = reserva.id
                            reserva.delete()
                            print(f"✅ Reserva {reserva_id} apagada com sucesso ({email} - {data_obj} {hora_obj}).")
                        else:
                            print("❌ Nenhuma reserva correspondente encontrada.")

        except Exception as e:
            print(f"💥 Erro ao tentar apagar a reserva: {e}")

        return JsonResponse({'success': True, 'message': 'Cancelamento concluído e reserva apagada.'})

    return JsonResponse({'success': False, 'message': 'Método inválido.'})


@csrf_exempt
def enviar_reagendamento_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nome = data.get('nome')
        email = data.get('email')
        servico_titulo = data.get('servico')
        morada = data.get('morada', '--')
        data_reserva = data.get('data')
        hora_reserva = data.get('hora')
        duracao = data.get('duracao', '-- min')
        total = data.get('total', '--')

        prof_obj = data.get('profissional', {})
        prof_nome = prof_obj.get('name', '')
        prof_bio = prof_obj.get('bio', '')

        logger.info(f"📩 Reagendamento recebido para {nome} ({email}) - Serviço: {servico_titulo}, Profissional: {prof_nome}")
        logger.debug(f"Dados recebidos: data={data_reserva}, hora={hora_reserva}, total={total}, duracao={duracao}")

        assunto = "Reagendamento da sua reserva - The Golden Light Photography"

        # --- Formatar data (para o e-mail) ---
        dias_semana = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        try:
            ano, mes, dia = map(int, data_reserva.split("-"))
            date_obj = datetime.date(ano, mes, dia)
            dia_semana = dias_semana[date_obj.weekday()]
            data_formatada = f"{dia_semana}. {dia} {meses[mes-1]}, {ano}"
        except Exception as e:
            data_formatada = data_reserva
            logger.warning(f"⚠️ Falha ao formatar data '{data_reserva}': {e}")

        # --- Atualizar no banco de dados ---
        try:
            service = Service.objects.get(title=servico_titulo)
            professional = Professional.objects.get(name=prof_nome)
            logger.debug(f"Serviço '{service.title}' e profissional '{professional.name}' encontrados.")

            booking = Booking.objects.filter(
                email=email,
                service=service,
                professional=professional
            ).latest('created_at')

            logger.info(f"🔄 Atualizando reserva ID {booking.id} de {booking.date} {booking.time} para {data_reserva} {hora_reserva}.")

            booking.date = datetime.datetime.strptime(data_reserva, "%Y-%m-%d").date()
            booking.time = datetime.datetime.strptime(hora_reserva, "%H:%M").time()
            booking.save()

            logger.info("✅ Reserva atualizada com sucesso no banco de dados.")

        except Service.DoesNotExist:
            logger.error(f"❌ Serviço '{servico_titulo}' não encontrado.")
            return JsonResponse({'success': False, 'message': 'Serviço não encontrado.'})
        except Professional.DoesNotExist:
            logger.error(f"❌ Profissional '{prof_nome}' não encontrado.")
            return JsonResponse({'success': False, 'message': 'Profissional não encontrado.'})
        except Booking.DoesNotExist:
            logger.error(f"❌ Nenhuma reserva encontrada para {email}, serviço '{servico_titulo}', profissional '{prof_nome}'.")
            return JsonResponse({'success': False, 'message': 'Reserva não encontrada para reagendamento.'})
        except Exception as e:
            logger.exception(f"💥 Erro ao atualizar reserva: {e}")
            return JsonResponse({'success': False, 'message': f'Erro ao atualizar reserva: {str(e)}'})

        # --- Enviar o e-mail ---
        try:
            html_mensagem = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f5f5f5;
                        margin: 0;
                        padding: 10px;
                    }}
                    .container {{
                        display: flex;
                        max-width: 700px;
                        margin: auto;
                        border-radius: 10px;
                        overflow: hidden;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                        flex-wrap: wrap;
                    }}
                    .box-esquerda, .box-direita {{
                        box-sizing: border-box;
                    }}
                    .box-esquerda {{
                        background-color: #ffffff;
                        padding: 20px;
                        width: 60%;
                        min-width: 250px;
                    }}
                    .box-esquerda h1 {{
                        font-size: 22px;
                        font-weight: bold;
                        color: #000000;
                        margin-bottom: 10px;
                    }}
                    .box-esquerda p, .box-esquerda .info {{
                        font-size: 14px;
                        color: #333;
                        margin: 4px 0;
                    }}
                    .divider {{
                        border-top: 1px solid #ccc;
                        margin: 15px 0;
                    }}
                    .fornecedor {{
                        margin-top: 8px;
                        font-size: 14px;
                    }}
                    .box-direita {{
                        background-color: #e0e0e0;
                        width: 40%;
                        min-width: 200px;
                        padding: 20px;
                        text-align: center;
                    }}
                    .profissional-nome {{
                        font-weight: bold;
                        font-size: 16px;
                        margin-bottom: 15px;
                    }}
                    .botao {{
                        display: block;
                        width: 100%;
                        margin: 8px 0;
                        padding: 8px;
                        font-size: 13px;
                        color: #007bff;
                        background-color: #ffffff;
                        border:1px solid #007bff;
                        text-decoration: none;
                        border-radius: 5px;
                        box-sizing: border-box;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="box-esquerda">
                        <h1>Reagendamento concluído!</h1>
                        <p>Olá {nome},</p>
                        <p>A sua marcação foi reagendada com sucesso.</p>

                        <div class="divider"></div>

                        <div class="info"><strong>Quando:</strong> {data_formatada} às {hora_reserva}</div>
                        <div class="info"><strong>Serviço:</strong> {servico_titulo}</div>
                        <div class="fornecedor"><strong>Fornecedor:</strong> {prof_nome} - {prof_bio}</div>
                        <div class="info"><strong>Valor:</strong> €{total}</div>
                        <div class="info"><strong>Duração:</strong> {duracao}</div>
                    </div>

                    <div class="box-direita">
                        <div class="profissional-nome">{prof_nome}</div>
                        <a href="https://untranscendentally-atelectatic-eugena.ngrok-free.dev/detalhes-reserva.html?nome={quote(nome)}&email={quote(email)}&servico={quote(servico_titulo)}&morada={quote(morada)}&data={quote(data_formatada)}&hora={quote(hora_reserva)}&valor={quote(total)}&fornecedor={quote(prof_nome)}&duracao={quote(duracao)}&bio={quote(prof_bio)}" class="botao">Reagendar</a>
                        <a href="https://untranscendentally-atelectatic-eugena.ngrok-free.dev/detalhes-reserva.html?nome={quote(nome)}&email={quote(email)}&servico={quote(servico_titulo)}&morada={quote(morada)}&data={quote(data_formatada)}&hora={quote(hora_reserva)}&valor={quote(total)}&fornecedor={quote(prof_nome)}&duracao={quote(duracao)}&bio={quote(prof_bio)}" class="botao">Cancelar compromisso</a>
                        <a href="https://untranscendentally-atelectatic-eugena.ngrok-free.dev/nova-consulta" class="botao">Marcar nova consulta</a>
                    </div>
                </div>
            </body>
            </html>
            """

            email_cliente = EmailMultiAlternatives(
                subject=assunto,
                body="Reagendamento da sua reserva",
                from_email=f"{nome} via The Golden Light Photography <{settings.DEFAULT_FROM_EMAIL}>",
                to=[email],  # e-mail do cliente
                reply_to=[email]  # resposta volta para o cliente
            )
            email_cliente.attach_alternative(html_mensagem, "text/html")
            email_cliente.send(fail_silently=False)

            logger.info(f"📧 E-mail de reagendamento enviado para o cliente {email} com sucesso.")

            # --- E-mail interno de notificação ---
            assunto_interno = f"Reagendamento efetuado: {nome} - {servico_titulo}"
            mensagem_interna = f"""
            O cliente {nome} ({email}) reagendou a reserva.

             Nova data: {data_formatada} às {hora_reserva}
             Serviço: {servico_titulo}
             Profissional: {prof_nome}
             Valor: €{total}
             Duração: {duracao}min
            

            Verifique a atualização no sistema.
            """

            email_interno = EmailMultiAlternatives(
                subject=assunto_interno,
                body=mensagem_interna,
                from_email=settings.DEFAULT_FROM_EMAIL,  # e-mail da empresa
                to=[settings.DEFAULT_FROM_EMAIL]  # notificação interna
            )
            email_interno.send(fail_silently=False)

            logger.info("📨 E-mail interno de notificação de reagendamento enviado com sucesso.")

        except Exception as e:
            logger.exception(f"💥 Erro ao enviar e-mail: {e}")
            return JsonResponse({'success': False, 'message': f'Erro ao enviar e-mail: {str(e)}'})

        return JsonResponse({
            'success': True,
            'message': 'Reserva atualizada e e-mail enviado com sucesso!',
            'updated_booking': {
                'id': booking.id,
                'date': booking.date.strftime('%Y-%m-%d'),
                'time': booking.time.strftime('%H:%M'),
            }
        })

    return JsonResponse({'success': False, 'message': 'Método inválido.'})

@csrf_exempt
def criar_reserva(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Dados recebidos:", data)

            nome = data.get("nome")
            email = data.get("email")
            telefone = data.get("telefone")
            morada = data.get("morada", "--")
            comentario = data.get("comentario", "")
            servico_nome = data.get("servico")
            data_reserva = data.get("data")
            hora_reserva = data.get("hora")
            prof_json = data.get("profissional")

            # Converte a string JSON do profissional
            prof_data = json.loads(prof_json)
            professional = Professional.objects.filter(name=prof_data["name"]).first()

            if not professional:
                return JsonResponse({"success": False, "error": "Profissional não encontrado."})

            # Busca o serviço
            service = Service.objects.filter(title=servico_nome).first()
            if not service:
                return JsonResponse({"success": False, "error": "Serviço não encontrado."})

            # Converte data/hora
            data_obj = datetime.datetime.strptime(data_reserva, "%Y-%m-%d").date()
            hora_obj = datetime.datetime.strptime(hora_reserva, "%H:%M").time()

            # Cria a reserva
            reserva = Booking.objects.create(
                name=nome,
                email=email,
                phone=telefone,
                morada=morada,
                date=data_obj,
                time=hora_obj,
                notes=comentario,
                service=service,
                professional=professional
            )

            duracao = getattr(service, "duration_minutes", "-- min")  # substitua "duration" pelo campo correto
            duracao_texto = f"{duracao} min"

            print("Reserva criada com sucesso:", reserva.id, "Duração:", duracao)

            print("Reserva criada com sucesso:", reserva.id)

            return JsonResponse({"success": True, "reserva_id": reserva.id, "duracao": duracao_texto})

        except Exception as e:
            print("Erro ao criar reserva:", e)
            return JsonResponse({"success": False, "error": str(e)})

@csrf_exempt
def booking_detail(request):
    nome = request.GET.get('nome')
    email = request.GET.get('email')
    logger.info(f"🔎 Booking detail solicitado para nome={nome}, email={email}")

    if nome and email:
        reservas = Booking.objects.filter(name=nome, email=email).order_by('-updated_at')
        if reservas.exists():
            reserva = reservas.first()
            data = {
                'service': reserva.service.title,
                'date': reserva.date.strftime('%Y-%m-%d'),
                'time': reserva.time.strftime('%H:%M'),
                'prof': reserva.professional.name,
                'morada': reserva.morada or "--",
                'valor': str(reserva.total or reserva.service.price or 0.00),
                'duracao': f"{reserva.service.duration_minutes} "
            }
            logger.info(f"✅ Reserva encontrada: {data}")
            return JsonResponse(data)
        else:
            logger.warning(f"❌ Nenhuma reserva encontrada para {nome}, {email}")
    else:
        logger.warning("❌ Nome ou email não fornecido na requisição")
    return JsonResponse({}, status=404)

@api_view(['POST'])
def submit_review(request):
    data = request.data
    name = data.get('name')
    email = data.get('email')
    rating = data.get('rating')
    comment = data.get('comment')

    if not all([name, email, rating, comment]):
        return Response({"error": "Todos os campos são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

    # Salvar no banco
    review = Review.objects.create(
        name=name,
        email=email,
        rating=rating,
        comment=comment
    )

    # Enviar email para a empresa
    send_mail(
        subject=f"Nova Avaliação de {name}",
        message=f"Nome: {name}\nEmail: {email}\nRating: {rating}\nComentário: {comment}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],  # Coloque aqui o email da empresa
        fail_silently=False,
    )

    return Response({"message": "Avaliação enviada com sucesso!"}, status=status.HTTP_201_CREATED)

def index(request):
    return render(request, 'index.html')

# def atualizar_photos(request):
#     Professional.objects.all().update(photo='/images/vansophie.jpg')
#     return HttpResponse("Photos atualizadas!")