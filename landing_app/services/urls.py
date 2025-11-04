from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ServiceViewSet, BookingViewSet, DisponibilidadeView, ProfessionalListAPIView, criar_reserva

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('disponibilidade/<int:service_id>/', DisponibilidadeView.as_view(), name='disponibilidade'),
    path('professionals/', ProfessionalListAPIView.as_view(), name='professional-list'),
    path('criar_reserva/', criar_reserva, name='criar_reserva'),
    path('booking_detail/', views.booking_detail, name='booking_detail'),
    path('enviar_confirmacao/', views.enviar_confirmacao_email, name='enviar_confirmacao_email'),
    path('enviar_cancelamento_email/', views.enviar_cancelamento_email, name='enviar_cancelamento_email'),
    path('enviar_reagendamento_email/', views.enviar_reagendamento_email, name='enviar_reagendamento_email'),

]
