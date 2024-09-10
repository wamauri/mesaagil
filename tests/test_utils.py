import io
import base64
from unittest import mock

import pytest
from PIL import Image, UnidentifiedImageError
from django.core.files.base import ContentFile

from utils.images import decode_base64_image, compress_image


class TesteUtils:
    def test_decode_valid_image(self):
        # Sample base64 image string (this is a very short example, real data would be longer)
        img_str = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"
        img_file_like, ext = decode_base64_image(img_str)
        
        assert isinstance(img_file_like, ContentFile)
        assert img_file_like.name == "temp.png"
        assert ext == "png"

    def test_decode_invalid_base64(self):
        # Invalid base64 string
        img_str = "data:image/png;base64,invalidbase64"
        
        with pytest.raises(base64.binascii.Error):
            decode_base64_image(img_str)
    
    def test_decode_missing_base64_prefix(self):
        # Missing base64 prefix
        img_str = "data:image/png, iVBORw0KGgoAAAANSUhEUgAAAAUA"
        
        with pytest.raises(ValueError):
            decode_base64_image(img_str)

    @mock.patch('utils.images.decode_base64_image')
    def test_compress_valid_image(self, mock_decode):
        # Mock the return value of decode_base64_image
        mock_image = Image.new('RGB', (500, 500))
        output = io.BytesIO()
        mock_image.save(output, format='PNG')
        output.seek(0)
        mock_decode.return_value = (ContentFile(output.getvalue(), name='test.png'), 'png')
        
        image_str = "data:image/png;base64," + base64.b64encode(output.getvalue()).decode('utf-8')
        
        compressed_file = compress_image(image_str, 'compressed_image')
        
        assert isinstance(compressed_file, ContentFile)
        assert compressed_file.name == 'compressed_image.png'
        assert len(compressed_file.read()) > 0

    @mock.patch('utils.images.decode_base64_image')
    def test_compress_invalid_image(self, mock_decode):
        mock_decode.side_effect = ValueError("Invalid image")
        
        image_str = "data:image/png;base64,invalidbase64string"
        
        with pytest.raises(ValueError):
            compress_image(image_str, 'file_name')

    @mock.patch('utils.images.decode_base64_image')
    @mock.patch('PIL.Image.open')
    def test_compress_invalid_image_format(self, mock_image_open, mock_decode):
        # Mock decode_base64_image to return a valid ContentFile and extension
        mock_image = Image.new('RGB', (500, 500))
        output = io.BytesIO()
        mock_image.save(output, format='PNG')
        output.seek(0)
        mock_decode.return_value = (ContentFile(output.getvalue(), name='test.png'), 'png')
        
        # Mock Image.open to raise an UnidentifiedImageError
        mock_image_open.side_effect = UnidentifiedImageError
        
        image_str = "data:image/png;base64," + base64.b64encode(output.getvalue()).decode('utf-8')
        
        with pytest.raises((TypeError, UnidentifiedImageError)):
            compress_image(image_str)
