from django.db import models

class Professional(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    photo = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_minutes = models.IntegerField(default=30)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    professionals = models.ManyToManyField(Professional, related_name="services")  # Vários profissionais por serviço

    def __str__(self):
        return self.title

class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="bookings")
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name="bookings")  # Profissional escolhido
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    morada = models.CharField(max_length=300, blank=True)
    date = models.DateField()
    time = models.TimeField()
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.service.title} com {self.professional.name} em {self.date} {self.time}"

class Review(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating} estrelas"