from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AreaAdministrativa(models.Model):
	class Meta:
		verbose_name_plural = u'Areas Administrativas'

	nombre = models.CharField(max_length=40, null=False, help_text = 'Nombre del area administrativa')
	usuario = models.ManyToManyField(User)