from .Jarvis_Objects import core_objects
from _datetime import datetime

s3 = core_objects('s3')  # ---s3 = boto3.resource('s3')
cliente = core_objects('ClientS3')  # ---boto3.client('s3')
rekognition = core_objects('client')  # ---boto3.client('rekognition')
dynamodb = core_objects('DynamoDB')  # --- boto3.client('dynamodb')
collectionID = core_objects('IndexCollectionID') #collectionId --- ANTIGA Collection

def index_faces(bucket, key):
    response = rekognition.index_faces(
        Image={'S3Object':
                   {'Bucket': bucket,
                    'Name': key}},
        CollectionId=collectionID)  # --- "jarvisDetectCollection")
    return response


def update_index(faceId, fullName, funcao, tableName):
    dynamodb.put_item(
        TableName=tableName,
        Item={
            'RekognitionId': {'S': faceId},
            'FullName': {'S': fullName},
            'Funcao': {'S': funcao}
        }
    )


def ControlaIndex(bucket, key):
    try:
        response = index_faces(bucket, key)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']

            ret = cliente.head_object(Bucket=bucket, Key=key)
            personFullName = ret['Metadata']['fullname']
            personfuncao = ret['Metadata']['funcao']

            print(f'faceId: {faceId} === Per_FullName: {personFullName} === Funcao: {personfuncao}')

            update_index(faceId, personFullName, personfuncao, 't_jarvis_detect')
            return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket))
        raise e


def ControlaArquivos():
    # Get list of objects for indexing
    images = [(r'C:\Estudos\TecNinjas\Estudo_Reconhecimento Face\Fotos\Anderson_03.jpeg', 'Anderson Lima', 'TecNinja')
              ]

    # Iterate through list to upload objects to S3
    count = 1
    for image in images:
        file = open(image[0], 'rb')
        data_atual = datetime.now().strftime('%Y%m%d_%H%M%S')

        #full_name = image[1]
        #s3.Bucket('rekognitions3g6tyr31hj').put_object(Key=key, Body=file,
        # Preciso do nome da tabela (DynamoDB)
        # Key = nome do arquivo -- key = '0' + str(count) + '_' + image[1] + '_' + str(data_atual) + '.jpeg'
        # file = a imagem -- file = open(image[0], 'rb')
        s3.Bucket('jarvisdetect-index').put_object(Key=key, Body=file,
                                                       Metadata={'FullName': image[1], 'Funcao': image[2]})
        count = count + 1
        ControlaIndex('jarvisdetect-index', key)

    return ('Executado')


Processo = ControlaArquivos()

print(Processo)
