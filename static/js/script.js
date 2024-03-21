document.addEventListener('DOMContentLoaded', function () {
    const rows = document.querySelectorAll('#booking-table tbody tr');

    rows.forEach(row => {
        row.addEventListener('click', () => {
            row.querySelector('input[type="radio"]').checked = true;
            document.getElementById('selected-class-id').value = row.dataset.id;
        });
    });

    const bookBtn = document.getElementById('book-button');
    bookBtn.addEventListener('click', () => {
        const selectedRow = document.querySelector('#booking-table tbody tr.selected');
        if (selectedRow) {
            document.getElementById('booking-form').submit();
        } else {
            alert('Please select a class to book.');
        }
    });
});