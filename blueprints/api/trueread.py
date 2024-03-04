from flask import jsonify, request,Blueprint, redirect
import boto3

trueread_blueprint = Blueprint("trueread_blueprint", __name__)

def geturl():
    s3 = boto3.client('s3',
    endpoint_url = 'https://s3.wasabisys.com',
    aws_access_key_id = 'UWG7M67XENM4YKS3LZ9H',
    aws_secret_access_key = 'UkzSq2ScwEVQaD1fD7erMkPbncDI7fSemEL5Tfev')
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'trureadlink',
            'Key': 'TrueReadLink.apk'
        }
    )
    return url

@trueread_blueprint.route("/apk/download.php", methods=["GET", "POST"])
def truread_redirect_link():
    url =  geturl()
    return redirect(url)

@trueread_blueprint.route("/apk/download.php/", methods=["GET", "POST"])
def truread_redirect_link2():
    url =  geturl()
    return redirect(url)