from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import MenuForm, DetectPeopleForm, DetectFacesForm, DetectPeopleForm_lcl, DeleteArquivosForm, TipoColaboradorForm
from tkinter import filedialog, Tk
from .detect_code.Jarvis_ListaObjBucket import lista_obj_bkt
from .detect_code.Jarvis_DetectPeople import exibe_label_boundingbox
from .detect_code.Jarvis_DetectFaces import exibe_imagem_boundingbox
from .detect_code.Jarvis_Objects import core_objects
from .detect_code.Jarvis_ControlArqBucket import exporta_arquivo_bkt, deleta_arquivo_bkt
from .detect_code.Jarvis_Index_Imagens import index_imagem
from _datetime import datetime


# from .views import *

def home_page(request):
    return render(request, 'home/index.html')


def menu(request):
    if request.method == 'POST':
        form_menu = MenuForm(request.POST)
        if form_menu.is_valid():
            opc = form_menu.cleaned_data['menu']
            if opc == '1':  # ------------Detectar Pessoas
                return redirect('opc01')
            elif opc == '2':  # ------------Detectar Faces
                return redirect('opc02')
            elif opc == '3':  # ------------Listar conteudo do Bucket
                return redirect('opc03')
            elif opc == '4':  # ------------Limpa arquivos vazios no bucket
                return redirect('opc04')
            elif opc == '5':  # ------------Detectar Pessoas (Local)
                return redirect('opc05')
            elif opc == '6':  # ------------Detectar Faces (Local)
                return redirect('opc06')
            elif opc == '7':  # ------------Indexar Fotos
                return redirect('opc07')
    else:
        form_menu = MenuForm()
    return render(request, 'menu/menu.html', {'form_menu': form_menu})


# --- Detecta Pessoas
def opc_01(request):
    count = None
    if request.method == 'POST':
        form_detect_people = DetectPeopleForm(request.POST)
        if form_detect_people.is_valid():
            var_certeza = form_detect_people.cleaned_data['certeza']
            var_arq = form_detect_people.cleaned_data['arq']
            lst_bucket = core_objects('lst_bucket_dict')
            arq_select = lst_bucket[var_arq]
            count = exibe_label_boundingbox(arq_select, var_certeza)
            return render(request, 'menu/result.html', {'result_count': count})
    else:
        form_detect_people = DetectPeopleForm()
    return render(request, 'menu/detecta_pessoas.html', {'form_detect_people': form_detect_people})


# --- Detecta Faces
def opc_02(request):
    count = None
    if request.method == 'POST':
        form_detect_face = DetectFacesForm(request.POST)
        if form_detect_face.is_valid():
            var_arq = form_detect_face.cleaned_data['arq']
            lst_bucket = core_objects('lst_bucket_dict')
            arq_select = lst_bucket[var_arq]
            count = exibe_imagem_boundingbox(arq_select)
            return render(request, 'menu/result.html', {'result_count': count})
    else:
        form_detect_face = DetectFacesForm()
    return render(request, 'menu/detecta_faces.html', {'form_detect_face': form_detect_face})


# --- Lista Objetos do Bucket
def opc_03(request):
    lst_bkt = lista_obj_bkt()
    return render(request, 'menu/lista_bucket.html', {'lista_bucket': lst_bkt})


# --- Limpa Objetos do Bucket
def opc_04(request):
    if request.method == 'POST':
        form_delete_arq = DeleteArquivosForm(request.POST)
        if form_delete_arq.is_valid():
            var_arq = form_delete_arq.cleaned_data['arq']
            lst_bucket = core_objects('lst_bucket_dict')
            arq_select = lst_bucket[var_arq]
            deleta_arquivo_bkt(arq_select)
            msg = f'Arquivo: {arq_select}, Deletado do Bucket !!!'
            return render(request, 'menu/result.html', {'result_count': msg})
    else:
        form_delete_arq = DeleteArquivosForm()
    return render(request, 'menu/limpa_bucket.html', {'form_delete_arq': form_delete_arq})


# --- Detectar Pessoas (Local)
def opc_05(request):
    if request.method == 'POST':
        form_detect_people = DetectPeopleForm_lcl(request.POST)
        if form_detect_people.is_valid():
            var_certeza = form_detect_people.cleaned_data['certeza']

            root = Tk()
            root.fileName = filedialog.askopenfilename(filetypes=(("Image Files", "*.jpg"), ("All files", "*.*")))

            data_atual = datetime.now().strftime('%Y%m%d_%H%M%S')
            name_arq = ('img_' + data_atual + '.jpg')

            bucket = core_objects('s3Bucket')
            exporta_arquivo_bkt(name_arq, root.fileName, bucket)

            count = exibe_label_boundingbox(name_arq, var_certeza)
            root.destroy()
            return render(request, 'menu/result.html', {'result_count': count})

            # message = f'Foi encontrado o arquivo {root.fileName} e será salvo no bucket com o nome de: {name_arq}'
    else:
        form_detect_people = DetectPeopleForm_lcl()
    return render(request, 'menu/detecta_pessoas_local.html', {'form_detect_people': form_detect_people})


# --- Detectar Faces (Local)
def opc_06(request):
    count = None
    if request.method == 'POST':
        root = Tk()
        root.fileName = filedialog.askopenfilename(filetypes=(("Image Files", "*.jpg"), ("All files", "*.*")))

        data_atual = datetime.now().strftime('%Y%m%d_%H%M%S')
        name_arq = ('img_' + data_atual + '.jpg')


        bucket = core_objects('s3Bucket')
        exporta_arquivo_bkt(name_arq, root.fileName, bucket)

        count = exibe_imagem_boundingbox(name_arq)
        root.destroy()
        return render(request, 'menu/result.html', {'result_count': count})
    return render(request, 'menu/detecta_faces_local.html')


# --- Indexar Fotos no DynamoDB
def opc_07(request):
    if request.method == 'POST':

        form = TipoColaboradorForm(request.POST)
        if form.is_valid():
            tpColab = form.cleaned_data['tipo_colaborador']  # 1-Colaborador // 2-TecNinja
            nome = form.cleaned_data['nome']

            if tpColab == 1:
                tipoColaborador = 'Colaborador'
            elif tpColab == 2:
                tipoColaborador = 'TecNinja'

            root = Tk()
            root.fileName = filedialog.askopenfilename(filetypes=(("Image Files", "*.jpg"), ("All files", "*.*")))

            data_atual = datetime.now().strftime('%Y%m%d_%H%M%S')
            name_arq = ('img_' + data_atual + '.jpg')
            root_filename = root.fileName

            print('Iniciando o Fluxo do Jarvis_Index_Imagens')

            #  ------------- Isso está em   Jarvis_Index_Imagens.py
            index_imagem(name_arq, root_filename, nome, tipoColaborador)

            print(f'Nome do arquivo: {name_arq}, o tipo de colaborador: {tipoColaborador}, Nome da Pessoa: {nome}')
            root.destroy()

            count = 0
            return render(request, 'menu/result.html', {'result_count': count})
    else:
        form = TipoColaboradorForm()
    return render(request, 'menu/indexFaces.html', {'form': form})


def result(request):
    count = None
    return render(request, 'menu/result.html', {'count_people': count})


def menu_acesso(request):
    return render(request, 'menu/menu_acesso.html')
