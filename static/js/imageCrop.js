export function initImageCropScript() {
  var cropper;
  var $imageInput = $('#id_image');
  var $imagePreview = $('#image-preview');
  var $croppedImage = $('#cropped-image');
  var $imageData = $('#image-data');
  var cropperModal = new bootstrap.Modal(document.getElementById('cropperModal'));
  var $cropImageButton = $('#crop-image-button');
  var $imageForm = $('#uploadProductsImageForm');

  $imageInput.off('change').on('change', function (event) {
    var files = event.target.files;
    if (files && files.length > 0) {
      var file = files[0];
      var reader = new FileReader();
      reader.onload = function (e) {
        $imagePreview.attr('src', e.target.result).show();
        if (cropper) {
          cropper.destroy();
          cropper = null;
        }
        cropper = new Cropper($imagePreview[0], {
          aspectRatio: 370 / 200,
          viewMode: 3,
          autoCropArea: 1,
          movable: false,
          rotatable: false,
          scalable: false,
          ready: function () {
            // Set fixed crop box size to 370x200 pixels
            cropper.setCropBoxData({
              width: 370,
              height: 200,
            });
          }
        });
        cropperModal.show();
      };
      reader.readAsDataURL(file);
    }
  });

  $cropImageButton.off('click').on('click', function () {
    if (cropper) {
      var canvas = cropper.getCroppedCanvas({
        width: 370,
        height: 200,
      });
      canvas.toBlob(function (blob) {
        var reader = new FileReader();
        reader.onloadend = function () {
          $imageData.val(reader.result);
          $croppedImage.attr('src', reader.result).show();
          cropperModal.hide();
        };
        reader.readAsDataURL(blob);
      });
    }
  });

  $imageForm.off('submit').on('submit', function (event) {
    if (!$imageData.val()) {
      event.preventDefault();
      alert('Please select and crop an image before submitting.');
    } else {
      // Form is valid, allow submission, then reset the fields
      setTimeout(function() {
        // Reset image input and preview elements after form submission
        $imageInput.val('');
        $imagePreview.attr('src', '').hide();
        $croppedImage.attr('src', '').hide();
        $imageData.val('');
        
        // Destroy the cropper instance
        if (cropper) {
          cropper.destroy();
          cropper = null;
        }
      }, 100); // Delay to allow form submission
    }
  });
}