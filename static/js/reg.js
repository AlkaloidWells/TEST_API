document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registration-form');
    const message = document.getElementById('message');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch('/api/auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(Object.fromEntries(formData))
        })
        .then(response => {
            if (response.ok) {
                message.textContent = 'User registered successfully!';
                form.reset();
            } else {
                message.textContent = 'Error registering user.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            message.textContent = 'An error occurred.';
        });
    });
});
