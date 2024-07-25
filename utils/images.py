import io, base64
from typing import Tuple

from django.core.files.base import ContentFile
from PIL import Image


def decode_base64_image(img) -> Tuple[ContentFile, str]:
    '''
    Decode the base64-encoded image 
    data into a file-like object.
    '''
    img_format, imgstr = img.split(';base64,')
    ext = img_format.split('/')[-1]
    img_file_like = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    return img_file_like, ext


def compress_image(image):
    image, ext = decode_base64_image(image)

    with Image.open(image) as img:
        img = img.convert('RGB')
        img.thumbnail((250, 250))
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=85)
        compressed_image = output.getvalue()
        return ContentFile(compressed_image, name=f'compressed_image.{ext}')
