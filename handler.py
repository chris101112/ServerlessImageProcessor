
import json

from lambda_util.util import get_logger
import boto3
import base64
from PIL import Image
import io
from image_processor import *

log = get_logger()


def handler(event, context):

    try:
        log.debug(sns_event=event)
        image_name = event.get('pathParameters').get('image_name')
        image_width = event.get('queryStringParameters').get('width')
        image_height = event.get('queryStringParameters').get('height')
        key = "cover/" + image_name
        if image_width == "":
            image_width = None
        elif image_width != "":
            image_width = int(image_width)
        if image_height == "":
            image_height = None
        elif image_height != "":
            image_height = int(image_height)
        image_data = process_image2(key, image_width, image_height)
        body = {
            'event': image_data,
        }

        response = {
            'statusCode': 200,
            'headers': {"Content-Type": 'image/jpeg'},
            'isBase64Encoded': True,
            'body': image_data,
        }
        log.info(response=response)

        return response

    except Exception as e:
        log.exception(e)
        response = {
            'statusCode': 500,
            'body': json.dumps('%s: %s' % (type(e), str(e))),
        }
        log.info(response=response)
        return response


def handler2(event, context):
    try:
        with open('website.html', 'r') as f:
            website = f.read()
        response = {
            'statusCode': 200,
            'headers': {"Content-Type": 'text/html'},
            'body': website,
        }
        return response
    
    except Exception as e:
        log.exception(e)
        response = {
            'statusCode': 500,
            'body': json.dumps('%s: %s' % (type(e), str(e))),
        }
        log.info(response=response)
        return response
    
