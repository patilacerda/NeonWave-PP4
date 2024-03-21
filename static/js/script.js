//Waits for the HTML document to be completely loaded 
document.addEventListener('DOMContentLoaded', function () {
    const rows = document.querySelectorAll('#booking-table tbody tr');
    //Iterates over each row of the booking table
    rows.forEach(row => {
        row.addEventListener('click', () => {
            row.querySelector('input[type="radio"]').checked = true;
            document.getElementById('selected-class-id').value = row.dataset.id;
        });
    });

    const bookBtn = document.getElementById('book-button');
    //Book button
    bookBtn.addEventListener('click', () => {
        const selectedRow = document.querySelector('#booking-table tbody tr.selected');
        if (selectedRow) {
            document.getElementById('booking-form').submit();
        } else {
            alert('Please select a class to book.');
        }
    });

    const cancelButtons = document.querySelectorAll('.cancel-booking');
    //Cancel button
    cancelButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const bookingId = this.getAttribute('data-booking-id');
            if (confirm('Are you sure you want to cancel this booking?')) {
                // Send a POST request to cancel the booking
                fetch(`/cancel-booking/${bookingId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': '{{ csrf_token }}'
                    }
                }).then(response => {
                    if (response.ok) {
                        // Booking canceled successfully, reload the page
                        window.location.reload();
                    } else {
                        // Display error message on the page
                        const errorMessage = document.createElement('p');
                        errorMessage.textContent = 'Failed to cancel booking. Please try again later.';
                        document.body.appendChild(errorMessage);
                        // Reload the page after displaying the error message
                        setTimeout(() => {
                            window.location.reload();
                        }, 3000);
                    }
                }).catch(error => {
                    // Display error message on the page
                    const errorMessage = document.createElement('p');
                    errorMessage.textContent = 'An error occurred while canceling the booking. Please try again later.';
                    document.body.appendChild(errorMessage);
                    // Reload the page after displaying the error message
                    setTimeout(() => {
                        window.location.reload();
                    }, 3000);
                });
            }
        });
    });
});