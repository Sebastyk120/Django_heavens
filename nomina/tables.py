import django_tables2 as tables
from .models import Jornada


class JornadaTable(tables.Table):
    class Meta:
        model = Jornada
        template_name = "django_tables2/bootstrap5.html"
