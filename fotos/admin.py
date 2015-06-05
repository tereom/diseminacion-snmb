# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Conglomerado_muestra, Imagen, Tag



class Conglomerado_muestra_admin(admin.ModelAdmin):
    search_fields = ["nombre"]
    list_display = ["nombre", "imagenes"]

class Tag_admin(admin.ModelAdmin):
    list_display = ["tag"]

class Imagen_admin(admin.ModelAdmin):
    '''list_display muestra los atributos/ resultados de los métodos de la clase
    imagen'''

    search_fields = ["tipo_nombre"]
    list_display = ["__unicode__", "tipo_nombre", "conglomerado_muestra_id_", "thumbnail", "tags_"]
    list_filter = ["tags", "conglomerado_muestra_id"]

    ### El siguiente método puede resultar innecesario
    def save_model(self, request, obj, form, change):
        '''función pública que ve el usuario y que llama a la privada.'''
    #     obj.user = request.user
        obj.save()

admin.site.register(Conglomerado_muestra, Conglomerado_muestra_admin)
admin.site.register(Tag, Tag_admin)
admin.site.register(Imagen, Imagen_admin)
