document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('change', function(e) {
        if (e.target.matches('select[name$="-product"]')) {
            const productId = e.target.value;
            const row = e.target.closest('tr') || e.target.closest('.inline-related') || e.target.closest('div');
            if (!row) return;
            const priceInput = row.querySelector('input[name$="-price_at_sale"]');
            
            if (productId && priceInput) {
                fetch(`/api/product-price/${productId}/`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.price !== undefined && data.price !== '') {
                            priceInput.value = data.price;
                        }
                    });
            } else if (!productId && priceInput) {
                priceInput.value = '';
            }
        }
    });
});
