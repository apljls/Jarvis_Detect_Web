import boto3

def lista_obj_bkt():
    s3 = boto3.resource('s3')
    s3Bucket = 'filaatmdetections3jarvis'
    file = s3.Bucket(s3Bucket).objects.all()

    return file

