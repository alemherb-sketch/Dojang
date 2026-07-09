document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"][name="image"]');
    if (!fileInput) return;

    // Find the container where the preview should be shown
    let previewImg = null;
    let previewText = null;

    // In Unfold, we might need to find the readonly field container
    const readonlyField = document.querySelector('.field-image_preview .readonly') || document.querySelector('.field-image_preview');
    
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imgHtml = `<img src="${e.target.result}" style="max-height: 250px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);" />`;
                
                if (readonlyField) {
                    readonlyField.innerHTML = imgHtml;
                } else {
                    // Create it if it doesn't exist
                    let livePreview = document.getElementById('live-image-preview');
                    if (!livePreview) {
                        livePreview = document.createElement('div');
                        livePreview.id = 'live-image-preview';
                        livePreview.style.marginTop = '15px';
                        
                        // Append it near the file input
                        const fieldset = fileInput.closest('.form-row') || fileInput.closest('div');
                        if (fieldset) {
                            fieldset.appendChild(livePreview);
                        }
                    }
                    livePreview.innerHTML = imgHtml;
                }
            }
            reader.readAsDataURL(file);
        } else {
            if (readonlyField) {
                readonlyField.innerHTML = 'No hay imagen cargada';
            } else {
                const livePreview = document.getElementById('live-image-preview');
                if (livePreview) livePreview.innerHTML = '';
            }
        }
    });
});
