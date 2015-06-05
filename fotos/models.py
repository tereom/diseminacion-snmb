# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

import os
from diseminacion.settings import MEDIA_ROOT

# Para thumbnail2 necesitamos los siguientes

from PIL import Image as PImage
from django.core.files import File
from os.path import join as pjoin
from tempfile import *

# Los nombres de las clases se mapean del esquema de la base de datos

class Conglomerado_muestra(models.Model):
    '''public: si es abierto o requiere contraseña
    se incluirán los otros campos del conglomerado para búsqueda
    incluiremos otras clases adentro de conglomerado muestra'''

    nombre = models.CharField(max_length=60)
    publico = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nombre

    def imagenes(self):
        # self.imagen_set.all() es tipo queryset que significa que hay que 
        # extraer las Imagenes y a este el nombre del archivo
        # obtenemos así lst de tipo lista
        lst = [x.archivo.name for x in self.imagen_set.all()]
        # el segundo lst crea una lista con los urls completos a las imágenes
        lst = ["<a href='/photo/media/%s'>%s</a><br/>" % (x, x.split('/')[-1]) for x in lst]
        urls_imagenes = ''.join(lst)
        return urls_imagenes
    # para que no escape las etiquetas de html
    imagenes.allow_tags = True

class Tag(models.Model):
    tag = models.CharField(max_length=50)
    def __unicode__(self):
        return self.tag

class Imagen(models.Model):
    '''tipo_nombre: huella/excreta, especie invasora, cámara, ...'''

    tipo_nombre = models.CharField(max_length=60, blank=True, null=True)
    archivo = models.FileField(upload_to="imagenes/")
    tags = models.ManyToManyField(Tag, blank=True)
    conglomerado_muestra_id = models.ForeignKey(Conglomerado_muestra, blank=True)
    # created = models.DateTimeField(auto_now_add=True)
    # rating = models.IntegerField(default=50)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    # user = models.ForeignKey(User, null=True, blank=True)

    thumbnail1 = models.FileField(upload_to="imagenes/",blank=True,null=True)
    thumbnail2 = models.FileField(upload_to="imagenes/",blank=True,null=True)


    def size(self):
        """Image size."""
        return "%s x %s" % (self.width, self.height)

    def save(self, *args, **kwargs):
        '''Este método se define en el modelo porque es para guardar imágenes
        a partir del admin, si se quieren guardar desde otra parte se debería
        incluir en un controlador usual'''
        super(Imagen, self).save(*args, **kwargs)
        im = PImage.open(pjoin(MEDIA_ROOT, self.archivo.name))

        # convertir imagen a RGB si no 
        if im.mode != "RGB":
            im = im.convert("RGB")

        self.width, self.height = im.size

        # large thumbnail
        fn, ext = os.path.splitext(self.archivo.name)
        im.thumbnail((128,128), PImage.ANTIALIAS)
        thumb_fn = fn + "-thumb2" + ext
        tf2 = NamedTemporaryFile()
        im.save(tf2.name, "JPEG")
        self.thumbnail1.save(thumb_fn, File(open(tf2.name)), save=False)
        tf2.close()

        # small thumbnail
        im.thumbnail((40,40), PImage.ANTIALIAS)
        thumb_fn = fn + "-thumb" + ext
        tf = NamedTemporaryFile()
        im.save(tf.name, "JPEG")
        self.thumbnail2.save(thumb_fn, File(open(tf.name)), save=False)
        tf.close()

        # este save guarda la ruta a la imagen
        super(Imagen, self).save(*args, ** kwargs)

    def __unicode__(self):
        return self.archivo.name

    def tags_(self):
        lst = [x[1] for x in self.tags.values_list()]
        print type(lst)
        return ', '.join(lst)

    def conglomerado_muestra_id_(self):
        return (self.conglomerado_muestra_id.nombre)

    def thumbnail(self):
        return """<a href="/photo/media/%s"><img border="0" alt="" src="/photo/media/%s" height="40" /></a>""" % ((self.archivo.name, self.archivo.name))
    thumbnail.allow_tags = True


    ######################

    def __unicode__(self):
        return self.archivo.name




