from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServiceViewSet,
    BookingViewSet,
    DisponibilidadeView,
    ProfessionalListAPIView,
    criar_reserva,
    booking_detail,
    enviar_confirmacao_email,
    enviar_cancelamento_email,
    enviar_reagendamento_email,
    submit_review,
    atualizar_photos
)

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),  # gera /services/ e /bookings/
    path('professionals/', ProfessionalListAPIView.as_view(), name='professional-list'),
    path('disponibilidade/<int:service_id>/', DisponibilidadeView.as_view(), name='disponibilidade'),
    path('criar_reserva/', criar_reserva, name='criar_reserva'),
    path('booking_detail/', booking_detail, name='booking_detail'),
    path('enviar_confirmacao/', enviar_confirmacao_email, name='enviar_confirmacao_email'),
    path('enviar_cancelamento_email/', enviar_cancelamento_email, name='enviar_cancelamento_email'),
    path('enviar_reagendamento_email/', enviar_reagendamento_email, name='enviar_reagendamento_email'),
    path('reviews/', submit_review, name='submit_review'),
    # path('atualizar-photos/', atualizar_photos, name='atualizar_photos')
]