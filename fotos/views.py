# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
#from settings import MEDIA_URL

from photo.models import *

def main(request):
    '''Main listing.'''
    conglomerados = Conglomerado_muestra.objects.all()
    if not request.user.is_authenticated():
        conglomerados = conglomerados.filter(public=True)

    paginator = Paginator(conglomerados, 10)
    # el siguiente try/except cubre el caso donde en el url se solicita una
    # página que no es entero, en este caso te manda a la página 1
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1
    # el siguiente try/except cubre el caso donde en el url se solicita una
    # página que no existe, en este caso te manda a la última página
    try:
        conglomerados_pag = paginator.page(page)
    except (InvalidPage, EmptyPage):
        conglomerados_pag = paginator.page(paginator.num_pages)

    # obtiene las primeras 4 imágenes asociadas a cada conglomerado
    for conglomerado in conglomerados_pag.object_list:
        conglomerado.images = conglomerado.imagen_set.all()[:4]

    return render_to_response("list.html", dict(
        conglomerados_pag = conglomerados_pag, 
        user = request.user, media_url = '/photo/media/'))