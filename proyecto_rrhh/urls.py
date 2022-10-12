"""proyecto_rrhh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
""" El "include" y el "path(include)" me ayudarán a que mi código detecte los 
templates, y así peuda eliminar la página de inicio del cohete que viene por defecto en 
Django (fuente: https://youtu.be/pRNhdI9PVmg .)

Necesito unas bibliotecas de 'static' para poder subir imagenes a mi proyecto de django usando
MEDIA ROOT y MEDIA URL (fuente: https://www.youtube.com/watch?v=ygzGr51dbsY).

Luego, en el 'urlpatterns', voy a tener que agregar una línea rara de código que empieza por
'+ static', la cual me dejará usar el MEDIA ROOT y el MEDIA URL.
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_rrhh.urls'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
