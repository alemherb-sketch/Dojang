document.addEventListener('DOMContentLoaded', function() {
    function calculateTotal() {
        let total = 0;
        const qtyInputs = document.querySelectorAll('input[name$="-quantity"]');
        qtyInputs.forEach(qtyInput => {
            if (qtyInput.name.includes('__prefix__')) return; // skip template
            
            const row = qtyInput.closest('tr') || qtyInput.closest('div.border') || qtyInput.closest('div.group') || qtyInput.parentElement.parentElement;
            if (!row) return;

            const priceInput = row.querySelector('input[name$="-price_at_sale"]');
            const deleteInput = row.querySelector('input[name$="-DELETE"]');
            
            if (qtyInput && priceInput && qtyInput.value && priceInput.value) {
                if (deleteInput && deleteInput.checked) return;
                total += (parseFloat(qtyInput.value) * parseFloat(priceInput.value));
            }
        });
        
        const totalInput = document.querySelector('input[name="total"]');
        if (totalInput) {
            totalInput.value = total.toFixed(2);
        } else {
            const totalReadonly = document.querySelector('.field-total .readonly') || document.querySelector('.field-total');
            if (totalReadonly) {
                totalReadonly.textContent = total.toFixed(2);
            }
        }
    }

    document.body.addEventListener('change', function(e) {
        if (e.target.matches('input[name$="-quantity"]') || 
            e.target.matches('input[name$="-price_at_sale"]') || 
            e.target.matches('input[name$="-DELETE"]')) {
            calculateTotal();
        }

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
                            calculateTotal();
                        }
                    });
            } else if (!productId && priceInput) {
                priceInput.value = '';
                calculateTotal();
            }
        }
    });

    // Calculate total on load
    setTimeout(calculateTotal, 500);
});
