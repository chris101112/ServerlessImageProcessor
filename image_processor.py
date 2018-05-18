import base64
import boto3
from PIL import Image
import io
from lambda_util.util import get_logger
log = get_logger()

def process_image(image_data):
    image_jpg = to_jpeg(image_data)
    string_image = encode_image(image_jpg)
    return(string_image)


def decode_image(image_string, output_file='test_output.jpg'):
    binary_image = base64.decodestring(image_string)
    image_result = open(output_file, 'wb')
    image_result.write(binary_image)


def process_image2(image_name, width = None, height = None):
    """
        Fetch and base64 encode image
    """
    if width == None and height == None:
        return(encode_image(to_jpeg(get_s3_image(image_name))))
    else:
        return(encode_image(resize_image(to_jpeg(get_s3_image(image_name)), width, height)))


def encode_image(image_data):
    """
        Given binary image data, base64 encode and return results
    """
    image_bytes = base64.b64encode(image_data)
    image_str = image_bytes.decode('ascii')
    return(image_str)


def get_local_image(file_name):
    with open(file_name, 'rb') as f:
        image_data = f.read()
    return(image_data)


def get_s3_image(key, bucket='images.findawayworld.com'):
    """
        Given a key, fetch the image data into memory and return image data
    """
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key)
    image_data = obj.get()['Body'].read()
    return(image_data)


def to_jpeg(image_data):
    img = Image.open(io.BytesIO(image_data))
    img_jpeg = img.convert('RGB')
    img_byte = io.BytesIO()
    img_jpeg.save(img_byte, format='jpeg')
    return(img_byte.getvalue())


def resize_image(image_data, width, height):
    img = Image.open(io.BytesIO(image_data))
    img_size = img.size
    if width == None:
        img_ratio = img_size[0] / img_size[1]
        width = int(height * img_ratio)
    elif height == None:
        img_ratio = img_size[1] / img_size[0]
        height = int(width * img_ratio)
    log.debug("resize to " + str(width) + " by " + str(height))
    img_resize = img.resize((width, height))
    img_byte = io.BytesIO()
    img_resize.save(img_byte, format='jpeg')
    return(img_byte.getvalue())