document.addEventListener('DOMContentLoaded', function() {
    // When concept select2 changes
    const amountField = document.querySelector('#id_amount');
    
    // We bind to both standard change and jQuery select2 change
    if (typeof django !== 'undefined' && django.jQuery) {
        django.jQuery('#id_concept').on('change', function() {
            const conceptId = this.value;
            if (conceptId) {
                fetch('/api/concept-price/' + conceptId + '/')
                    .then(response => response.json())
                    .then(data => {
                        if (data.price) {
                            amountField.value = data.price;
                        }
                    });
            }
        });
    } else {
        // Fallback for native select
        const conceptField = document.querySelector('#id_concept');
        if (conceptField) {
            conceptField.addEventListener('change', function() {
                const conceptId = this.value;
                if (conceptId) {
                    fetch('/api/concept-price/' + conceptId + '/')
                        .then(response => response.json())
                        .then(data => {
                            if (data.price) {
                                amountField.value = data.price;
                            }
                        });
                }
            });
        }
    }
});
