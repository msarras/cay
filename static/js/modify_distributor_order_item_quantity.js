document.addEventListener('DOMContentLoaded', function() {
    const incrementButtons = document.querySelectorAll('.increment-btn');
    const decrementButtons = document.querySelectorAll('.decrement-btn');

    incrementButtons.forEach(button => {
        button.addEventListener('click', function() {
            handleQuantityChange(this, 1);
        });
    });

    decrementButtons.forEach(button => {
        button.addEventListener('click', function() {
            handleQuantityChange(this, -1);
        });
    });

    function handleQuantityChange(button, change) {
        const itemId = button.dataset.id;
        console.log(button.dataset);
        const quantityInput = document.getElementById('quantity-input-' + itemId);
        let currentQuantity = parseInt(quantityInput.value) || 0;

        // Retrieve the CSRF token
        const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        // Update quantity based on button clicked
        currentQuantity += change;
        if (currentQuantity < 0) currentQuantity = 0; // Prevent negative quantities

        // Update the input field
        quantityInput.value = currentQuantity;

        const url = modifyDistributorOrderBasketUrl;
        fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'item_id': itemId,
                'quantity': currentQuantity
            })
        })
        .then(response => response.json())
        .then(data => {
            // Update the UI based on the response
            if (data.status === 'success') {
                // Update the relevant fields in the UI
                const quantityPriceCell = quantityInput.closest('tr').querySelector('.quantity-price-' + itemId);
                const unitsPerBasketCell = quantityInput.closest('tr').querySelector('.units-per-basket-' + itemId);
                const costPerBasketCell = quantityInput.closest('tr').querySelector('.cost-per-basket-' + itemId);

                // Update the displayed values
                quantityPriceCell.textContent = (data.quantity_price).toFixed(2);
                unitsPerBasketCell.textContent = (data.units_per_basket).toFixed(1);
                costPerBasketCell.textContent = (data.cost_per_item_per_basket).toFixed(2);

                // update the subtotal line per section
                basketId = data.basket_id
                console.log('basket id: ', basketId);
                const sectionCostPerBasket = document.querySelector('.cost-per-basket-' + basketId);
                const sectionSubtotal = document.querySelector('.subtotal-' + basketId);

                sectionCostPerBasket.textContent = '$' + (data.cost_per_basket).toFixed(2);
                sectionSubtotal.textContent = '$' + (data.basket_cost).toFixed(2);

                // update the total costs in the footer
                const totalCostElement = document.querySelector('.total-cost'); // Adjust the selector as needed

                totalCostElement.textContent = '$' + (data.total_purchase_cost).toFixed(2);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
