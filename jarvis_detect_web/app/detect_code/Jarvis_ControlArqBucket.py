from .Jarvis_Objects import core_objects

#fileUp = 'C:\Estudos\TecNinjas\PycharmProjects\Fotos\Fila_Bank_Chipre.jpg'
#dfileUp = 'C:\Estudos\TecNinjas\PycharmProjects\Fotos\Fila_Bank_Melbourne.jpg'
#arq_name = 'img_teste_upload.jpg'
#arq_name = '16318113.jpeg'


def valida_arquivo_bkt(v_arq_name):
    s3 = core_objects('s3')  # ---s3 = boto3.resource('s3')
    s3Bucket = core_objects('s3Bucket')  # ---s3Bucket = 'filaatmdetections3jarvis'
    v_ret = None
    for file in s3.Bucket(s3Bucket).objects.all():
        if file.key == v_arq_name:
            v_ret = file.key
            break
    return v_ret


def exporta_arquivo_bkt(v_arq_name, v_fileUp, v_bkt_index):
    s3 = core_objects('s3')  # ---s3 = boto3.resource('s3')
    # s3Bucket = core_objects('s3Bucket')  # ---s3Bucket = 'filaatmdetections3jarvis'
    # Upload a new file
    # v_arq_name -- Espera-se o nome que o arquivo ficará no bucket
    # v_fileUp   -- Espera-se o caminho completo do arquivo + nome do arquivo
    data = open(v_fileUp, 'rb')
    s3.Bucket(v_bkt_index).put_object(Key=v_arq_name, Body=data)


def exporta_arquivo_index(v_arq_name, v_fileUp, v_index):
    # images = [(r'C:\Estudos\TecNinjas\Estudo_Reconhecimento Face\Fotos\Anderson_03.jpeg', 'Anderson Lima', 'TecNinja')

    # v_arq_name = ('img_' + data_atual + '.jpg')
    # v_fileUp = caminho do arquivo
    # v_index = 'jarvisdetect-index'

    count = 1
    for image in images:
        s3.Bucket('jarvisdetect-index').put_object(Key=key, Body=file,
                                                       Metadata={'FullName': image[1], 'Funcao': image[2]})
        count = count + 1
        ControlaIndex('jarvisdetect-index', key)

def deleta_arquivo_bkt(v_arq_name):
    s3 = core_objects('s3')  # ---s3 = boto3.resource('s3')
    s3Bucket = core_objects('s3Bucket')  # ---s3Bucket = 'filaatmdetections3jarvis'
    s3.Object(s3Bucket, v_arq_name).delete()


