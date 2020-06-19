from .Jarvis_Objects import core_objects

def lista_obj_bkt():
    # s3 = boto3.resource('s3')
    s3 = core_objects('s3')
    # s3Bucket = 'filaatmdetections3jarvis'
    s3Bucket = core_objects('s3Bucket')
    file = s3.Bucket(s3Bucket).objects.all()

    return file

