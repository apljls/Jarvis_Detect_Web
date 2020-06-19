import boto3


def core_objects(type_object):
    if type_object == 'client':
        client = boto3.client('rekognition')
        return client

    elif type_object == 's3':
        s3 = boto3.resource('s3')
        return s3

    elif type_object == 'ClientS3':
        cliente = boto3.client('s3')
        return cliente

    elif type_object == 's3Bucket':
        s3Bucket = 'filaatmdetections3jarvis'
        # s3Bucket = 'jarvisdetect'  # -- NOVO BUCKET
        return s3Bucket

    elif type_object == 's3Bucket_index':   # -- BUCKET DE ARQUIVOS PRÉ-INDEXAÇÃO -- #
        # s3Bucket_index = 'filaatmdetections3jarvis-index'
        s3Bucket_index = 'jarvisdetect-index'
        return s3Bucket_index

    elif type_object == 'DynamoDB':
        dynamodb = boto3.client('dynamodb')
        return dynamodb

    elif type_object == 'tbl_dynamoDB':
        tbl_dynamoDB = 't_jarvis_detect'  # --- Tabela antiga: tjarvisfaces
        return tbl_dynamoDB

    # ----- ANTIGA Collection
    elif type_object == 'collectionId':
        collectionId = 'DetectedFacesJarvis'
        return collectionId

    # ----- NOVA Collection
    elif type_object == 'IndexCollectionID':
        collection = 'jarvisDetectCollection'
        return collection

    elif type_object == 'lst_bucket_dict':
        s3 = boto3.resource('s3')
        s3Bucket = core_objects('s3Bucket')
        file = s3.Bucket(s3Bucket).objects.all()
        count = 1
        varDict = {}
        for file in file:
            str_count = str(count)
            varDict[str_count] = file.key
            count = count + 1

        return varDict
