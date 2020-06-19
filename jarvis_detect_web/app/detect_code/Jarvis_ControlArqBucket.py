from .Jarvis_Objects import core_objects


def valida_arquivo_bkt(v_arq_name):
    s3 = core_objects('s3')  # ---s3 = boto3.resource('s3')
    s3Bucket = core_objects('s3Bucket')  # ---s3Bucket = 'filaatmdetections3jarvis'
    v_ret = None
    for file in s3.Bucket(s3Bucket).objects.all():
        if file.key == v_arq_name:
            v_ret = file.key
            break
    return v_ret


#  Exportação para o Buket Comun
def exporta_arquivo_bkt(v_name_arq, v_file, v_bucket):
    s3 = core_objects('s3')  # ---s3 = boto3.resource('s3')
    data = open(v_file, 'rb')
    s3.Bucket(v_bucket).put_object(Key=v_name_arq, Body=data)


#  Exportação para o Buket de Indexação
def exporta_arquivo_index(v_name_arq, v_nomeColaborador, v_funcaoColaborador, v_file, v_bucketIndex):
    s3 = core_objects('s3')  # ---s3 = boto3.resource('s3')
    s3.Bucket(v_bucketIndex).put_object(Key=v_name_arq, Body=v_file,
                                     Metadata={'FullName': v_nomeColaborador, 'Funcao': v_funcaoColaborador})
    print('Acabei de Finalizar o exporta_arquivo_index que esta dentro de Jarvis_ControlArqBucket')

def deleta_arquivo_bkt(v_arq_name):
    s3 = core_objects('s3')  # ---s3 = boto3.resource('s3')
    s3Bucket = core_objects('s3Bucket')  # ---s3Bucket = 'filaatmdetections3jarvis'
    s3.Object(s3Bucket, v_arq_name).delete()
