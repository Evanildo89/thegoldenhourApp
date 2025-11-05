from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, BookingViewSet, DisponibilidadeView, ProfessionalListAPIView, criar_reserva, index, booking_detail, enviar_confirmacao_email, enviar_cancelamento_email, enviar_reagendamento_email, submit_review

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('index/', index),  # ou '' se quiser que seja só o domínio principal
    path('api/', include(router.urls)),
    path('disponibilidade/<int:service_id>/', DisponibilidadeView.as_view(), name='disponibilidade'),
    path('professionals/', ProfessionalListAPIView.as_view(), name='professional-list'),
    path('criar_reserva/', criar_reserva, name='criar_reserva'),
    path('booking_detail/', booking_detail, name='booking_detail'),
    path('enviar_confirmacao/', enviar_confirmacao_email, name='enviar_confirmacao_email'),
    path('enviar_cancelamento_email/', enviar_cancelamento_email, name='enviar_cancelamento_email'),
    path('enviar_reagendamento_email/', enviar_reagendamento_email, name='enviar_reagendamento_email'),
    path('reviews/', submit_review, name='submit_review'),
]