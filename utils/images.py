import io, base64
from typing import Tuple

from django.core.files.base import ContentFile
from PIL import Image, ImageOps
from slugify import slugify

from apps.restaurants.models import FoodImage


def product_image_name(product) -> str:
    file_name = slugify(text=product.name, separator='_')
    return f'{file_name}_{str(product.code)[-7:]}'


def decode_base64_image(img) -> Tuple[ContentFile, str]:
    '''
    Decode the base64-encoded image 
    data into a file-like object.
    '''
    img_format, imgstr = img.split(';base64,')
    ext = img_format.split('/')[-1]
    img_file_like = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    return img_file_like, ext


def compress_image(image, file_name):
    image, ext = decode_base64_image(image)

    with Image.open(image) as img:
        img = img.convert('RGB')
        img.thumbnail((370, 200))
        output = io.BytesIO()
        img.save(output, format='PNG', quality=100)
        compressed_image = output.getvalue()
        return ContentFile(compressed_image, name=f'{file_name}.{ext}')


def resize_image(image):
    with Image.open(image) as img:
        thumbnail_size = (80, 80)
        scale = max(thumbnail_size[0] / img.width, thumbnail_size[1] / img.height)
        new_size = (int(img.width * scale), int(img.height * scale))
        resized_image = img.resize(new_size, Image.LANCZOS)
        return ImageOps.fit(
            image=resized_image, 
            size=thumbnail_size, 
            method=Image.LANCZOS, 
            centering=(0.5, 0.5)
        )


def image_to_thumbnail(img, file_name):
    final_image = resize_image(img)
    thumb_io = io.BytesIO()
    final_image.save(thumb_io, format='PNG')
    return ContentFile(thumb_io.getvalue(), f'{file_name}_thumb.png')


def prepare_images(image, file_name):
    food_image = FoodImage()
    compressed_image = compress_image(image, file_name)
    thumbnail = image_to_thumbnail(compressed_image, file_name)
    food_image.image.save(compressed_image.name, compressed_image)
    food_image.save()
    food_image.thumbnail.save(thumbnail.name, thumbnail)
    return food_image
