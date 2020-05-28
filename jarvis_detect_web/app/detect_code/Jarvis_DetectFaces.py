import json
import boto3
import io
from PIL import Image, ImageDraw, ImageFont, ExifTags, ImageColor
from .Jarvis_Objects import core_objects


def detecta_faces(collectionid, attributes, extimageid, bucket, image):
    client = core_objects('client')  # boto3.client('rekognition')
    faces_detectadas = client.index_faces(
        CollectionId=collectionid,
        DetectionAttributes=[attributes],  # DEFAULT | ALL
        ExternalImageId=extimageid,
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': image,
            },
        },
    )
    # print(json.dumps(faces_detectadas, indent=4))
    # print("Usando client.index_faces()")
    # print()
    countfaces = 0
    countfacesUndet = 0
    for label in faces_detectadas['FaceRecords']:
        if label['Face']:
            countfaces = countfaces + 1
            # print("Face #", countfaces)
            # print("  Bounding box")
            # print("    Top: " + str(label['FaceDetail']['BoundingBox']['Top']))
            # print("    Left: " + str(label['FaceDetail']['BoundingBox']['Left']))
            # print("    Width: " + str(label['FaceDetail']['BoundingBox']['Width']))
            # print("    Height: " + str(label['FaceDetail']['BoundingBox']['Height']))
            # print("  Confidence: " + str(label['FaceDetail']['Confidence']))
        # print("--------")

    for label in faces_detectadas['UnindexedFaces']:
        countfacesUndet = countfacesUndet + 1
        # print("Face Unindexed#", countfacesUndet)
        # print("  Bounding box")
        # print("    Top: " + str(label['FaceDetail']['BoundingBox']['Top']))
        # print("    Left: " + str(label['FaceDetail']['BoundingBox']['Left']))
        # print("    Width: " + str(label['FaceDetail']['BoundingBox']['Width']))
        # print("    Height: " + str(label['FaceDetail']['BoundingBox']['Height']))
        # print("  Confidence: " + str(label['FaceDetail']['Confidence']))
        # print()
    # print("--------")
    # print()
    countfacesUndet = len(faces_detectadas['UnindexedFaces'])
    # print("Faces Identificadas:", countfaces)
    # print("Faces Não Identificadas", countfacesUndet)
    # print()


def abre_foto(s3, s3Bucket, arq_name):
    # Abrindo Imagem do Bucket
    s3_object = s3.Object(s3Bucket, arq_name)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image = Image.open(stream)
    image.show()


def reorient_image(im):
    try:
        image_exif = im._getexif()
        image_orientation = image_exif[274]
        if image_orientation in (2, '2'):
            return im.transpose(Image.FLIP_LEFT_RIGHT)
        elif image_orientation in (3, '3'):
            return im.transpose(Image.ROTATE_180)
        elif image_orientation in (4, '4'):
            return im.transpose(Image.FLIP_TOP_BOTTOM)
        elif image_orientation in (5, '5'):
            return im.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM)
        elif image_orientation in (6, '6'):
            return im.transpose(Image.ROTATE_270)
        elif image_orientation in (7, '7'):
            return im.transpose(Image.ROTATE_270).transpose(Image.FLIP_TOP_BOTTOM)
        elif image_orientation in (8, '8'):
            return im.transpose(Image.ROTATE_90)
        else:
            return im
    except (KeyError, AttributeError, TypeError, IndexError):
        return im


def exibe_imagem_boundingbox(arq_name):
    #Objetos
    s3 = core_objects('s3')  # boto3.resource('s3')
    bucket = core_objects('s3Bucket')  # s3Bucket
    client = core_objects('client')  # boto3.client('rekognition')
    dynamodb = core_objects('DynamoDB')
    tbl_dynamoDB = core_objects('tbl_dynamoDB')
    CollectionId = 'family_collection'
    # CollectionId = core_objects('IndexCollectionID')

    # Load image from S3 bucket
    s3_connection = s3
    s3_object = s3_connection.Object(bucket, arq_name)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image = Image.open(stream)

    image = reorient_image(image)

    # Call DetectFaces
    response = client.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': arq_name}},
                                   Attributes=['ALL'])

    # Get image diameters
    imgWidth = image.size[0]
    imgHeight = image.size[1]

    draw = ImageDraw.Draw(image)
    draw.text((1, 1), 'IMAGEM ANALISADA ATRAVÉS DA APLICAÇÃO JARVIS DETECT')
    count = 0
    # calculate and display bounding boxes for each detected face
    #print('Detected faces for ' + arq_name)

    for faceDetail in response['FaceDetails']:
        count += 1

        box = faceDetail['BoundingBox']
        left = imgWidth * box['Left']
        x1 = int(box['Left'] * imgWidth) * 0.99
        top = imgHeight * box['Top']
        y1 = int(box['Top'] * imgHeight) * 0.99
        width = imgWidth * box['Width']
        x2 = int(box['Left'] * imgWidth + box['Width'] * imgWidth) * 1.010
        height = imgHeight * box['Height']
        y2 = int(box['Top'] * imgHeight + box['Height'] * imgHeight) * 1.010
        image_crop = image.crop((x1, y1, x2, y2))

        stream = io.BytesIO()
        image_crop.save(stream, format="JPEG")
        #image_crop.show() #Exibe cada Face encontrada dentro da Foto analisada
        image_crop_binary = stream.getvalue()

        person = 'Não identificado'

        try:
            # Submit individually cropped image to Amazon Rekognition
            response = client.search_faces_by_image(
                CollectionId=CollectionId,
                Image={'Bytes': image_crop_binary},
                MaxFaces=1
            )

            if len(response['FaceMatches']) > 0:
                # Return results
                for match in response['FaceMatches']:
                    face = dynamodb.get_item(
                        TableName=tbl_dynamoDB,
                        Key={'RekognitionId': {'S': match['Face']['FaceId']}}
                    )
                    if 'Item' in face:
                        person = face['Item']['FullName']['S']
                    else:
                        person = 'no match found'
                # print(match['Face']['FaceId'], match['Face']['Confidence'], person)
        except:
            person = 'Nao Identificado'
        points = (
            (left, top),
            (left + width, top),
            (left + width, top + height),
            (left, top + height),
            (left, top)
        )
        draw.line(points, fill='#00d400', width=2)
        # draw.text((left, top), 'Face #{}'.format(str(count)))
        draw.text((left, top), f'Face: {person}')

    image.show()
    return count
