document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.toggle-basket-item');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const inBasket = this.getAttribute('data-in-basket') === 'true';
            const basketId = this.getAttribute('data-basket-id');

            // Retrieve the CSRF token
            const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            // Construct the URL using the variable and the basketId
            const url = manageWeeklyBasketItemsUrl.replace('0', basketId);

            // Prepare the AJAX request
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrftoken
                },
                body: new URLSearchParams({
                    'product_id': productId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update the button text and classes based on the action
                    if (data.action === 'added') {
                        this.textContent = 'Remove';
                        this.classList.remove('bg-primary-700', 'hover:bg-primary-800');
                        this.classList.add('bg-red-600', 'hover:bg-red-700');
                        this.setAttribute('data-in-basket', 'true');
                    } else if (data.action === 'removed') {
                        this.textContent = 'Add';
                        this.classList.remove('bg-red-600', 'hover:bg-red-700');
                        this.classList.add('bg-primary-700', 'hover:bg-primary-800');
                        this.setAttribute('data-in-basket', 'false');
                    }
                } else {
                    console.error('Error:', data);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
