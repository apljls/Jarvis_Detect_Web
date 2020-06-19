from .Jarvis_ControlArqBucket import exporta_arquivo_index
from .Jarvis_Objects import core_objects
from _datetime import datetime


def index_faces(bucket, key):
    rekognition = core_objects('client')
    collectionID = core_objects('IndexCollectionID')  # --- "jarvisDetectCollection" Nova Collection
    response = rekognition.index_faces(
        Image={'S3Object':
                   {'Bucket': bucket,
                    'Name': key}},
        CollectionId=collectionID)
    return response


def update_index(faceId, fullName, funcao, tableName):
    dynamodb = core_objects('DynamoDB')
    dynamodb.put_item(
        TableName=tableName,
        Item={
            'RekognitionId': {'S': faceId},
            'FullName': {'S': fullName},
            'Funcao': {'S': funcao}
        }
    )


def index_imagem(name_arq, root_filename, nomeColaborador, funcaoColaborador):  # ControlaArquivos():
    cliente = core_objects('ClientS3')
    tbl_dynamo = core_objects('tbl_dynamoDB')
    bucket = core_objects('s3Bucket_index')
    file = open(root_filename, 'rb')

    # Importando arquivo para dentro do bucket com dados da pessoa
    exporta_arquivo_index(name_arq, nomeColaborador, funcaoColaborador, file, bucket)

    try:
        response = index_faces(bucket, name_arq)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']

            ret = cliente.head_object(Bucket=bucket, Key=name_arq)
            personFullName = ret['Metadata']['fullname']
            personfuncao = ret['Metadata']['funcao']
            # print(f'faceId: {faceId} === Per_FullName: {personFullName} === Funcao: {personfuncao}')

            update_index(faceId, personFullName, personfuncao, tbl_dynamo)
            return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(name_arq, bucket))
        raise e
