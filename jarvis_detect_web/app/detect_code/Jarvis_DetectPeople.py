import json
import io
from PIL import Image, ImageDraw, ImageFont, ExifTags, ImageColor
from .Jarvis_Objects import core_objects


def abre_foto(s3, s3Bucket, arq_name):
    # Abrindo Imagem do Bucket
    s3_object = s3.Object(s3Bucket, arq_name)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image = Image.open(stream)
    image.show()


def exibe_label_boundingbox(photo, confidence):
    bucket = core_objects('s3Bucket')  #---s3Bucket = 'filaatmdetections3jarvis'
    s3 = core_objects('s3')  #---s3 = boto3.resource('s3')
    client = core_objects('client')  #---boto3.client('rekognition')
    source = 'S3'
    local = ''
    image = None

    if source == "S3":
        # Load image from S3 bucket
        s3_object = s3.Object(bucket, photo)
        s3_response = s3_object.get()

        stream = io.BytesIO(s3_response['Body'].read())
        image = Image.open(stream)
        # Call DetectFaces
        response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})

    elif source == 'local':
        # Load local image
        imageFile = local + photo
        with open(imageFile, 'rb') as image:
            response = client.detect_labels(Image={'Bytes': image.read()})
        stream = open(imageFile, 'rb')
        image = Image.open(stream)
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)
    draw.text((1, 1), 'IMAGEM ANALISADA COM BOTO3 DETECT_LABELS')
    count = 0
    # calculate and display bounding boxes for each detected face
    # print('Detected faces for ' + photo)
    for label in response['Labels']:
        if label['Name'] == "Person":
            for instance in label['Instances']:
                if instance['Confidence'] >= confidence:
                    count += 1
                    box = ['BoundingBox']
                    left = imgWidth * instance['BoundingBox']['Left']
                    top = imgHeight * instance['BoundingBox']['Top']
                    width = imgWidth * instance['BoundingBox']['Width']
                    height = imgHeight * instance['BoundingBox']['Height']
                    # print()
                    # print('Person #{}'.format(str(count)))
                    # print('Left: ' + '{0:.0f}'.format(left))
                    # print('Top: ' + '{0:.0f}'.format(top))
                    # print('Face Width: ' + "{0:.0f}".format(width))
                    # print('Face Height: ' + "{0:.0f}".format(height))

                    points = (
                        (left, top),
                        (left + width, top),
                        (left + width, top + height),
                        (left, top + height),
                        (left, top)

                    )
                    draw.line(points, fill='#00d400', width=2)
                    draw.text((left, top), 'Person #{}'.format(str(count)))
        # Alternatively can draw rectangle. However you can't set line width
        # draw.rectangle([left,top, left + width, top + height], outline='#00d400')

    # print(f'Foram identificadas {count} pessoas na Foto !!!')
    image.show()
    return count

# abre_foto(s3,s3Bucket,arq_name)
# exibe_label_boundingbox('local', s3Bucket, arq_name, certeza, 'S3')
