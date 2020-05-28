from django.db import models
from .detect_code.Jarvis_ListaObjBucket import lista_obj_bkt
from .detect_code.Jarvis_Objects import core_objects


# Create your models here.
class Menu(models.Model):
    MENU_CHOICES = [
        ('1', 'Opção 1 - Detectar Pessoas (Bucket)'),
        ('2', 'Opção 2 - Detectar Faces (Bucket)'),
        ('3', 'Opção 3 - Listar conteudo do Bucket'),
        ('4', 'Opção 4 - Limpar Arquivo do Bucket'),
        ('5', 'Opção 5 - Detectar Pessoas (Local)'),
        ('6', 'Opção 6 - Detectar Faces (Local)'),
        ('7', 'Opção 7 - indexar/Treinar Rekognition'),
    ]
    menu = models.CharField(max_length=1, choices=MENU_CHOICES, null=False, blank=False)


lista_bkt = lista_obj_bkt()
count = 0
for lst in lista_bkt:
    count = count + 1


class DetectPeople(models.Model):
    lst_bucket = core_objects('lst_bucket_dict')
    CERTEZA_CHOICES = [
        (50, 50),
        (80, 80),
        (90, 90),
        (100, 100)
    ]
    certeza = models.IntegerField(max_length=3, choices=CERTEZA_CHOICES, null=False, blank=False)
    ARQ_CHOICES = lst_bucket.items()
    arq = models.CharField(max_length=100, choices=ARQ_CHOICES, null=False, blank=False)


class DetectFaces(models.Model):
    lst_bucket = core_objects('lst_bucket_dict')
    ARQ_CHOICES = lst_bucket.items()
    arq = models.CharField(max_length=100, choices=ARQ_CHOICES, null=False, blank=False)


class DetectPeople_lcl(models.Model):
    CERTEZA_CHOICES = [
        (70, 70),
        (80, 80),
        (90, 90),
        (100, 100)
    ]
    certeza = models.IntegerField(max_length=3, choices=CERTEZA_CHOICES, null=False, blank=False)


class DeleteArquivoBucket(models.Model):
    lst_bucket = core_objects('lst_bucket_dict')
    ARQ_CHOICES = lst_bucket.items()
    arq = models.CharField(max_length=100, choices=ARQ_CHOICES, null=False, blank=False)


class TipoColaborador(models.Model):
    TIPOCOLAB_CHOICES = [
        ('1', 'Colaborador'),
        ('2', 'TecNinja'),
    ]
    tipo_colaborador = models.CharField(max_length=1, choices=TIPOCOLAB_CHOICES, null=False, blank=False)
    nome = models.CharField(max_length=100, null=False)
