document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login-form');

    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(loginForm);
        const username = formData.get('username');
        const password = formData.get('password');

        // You can perform additional validation here if needed

        // Example: Send login request to the server using fetch API
        fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Login failed');
            }
        })
        .then(data => {
            // Handle successful login response
            console.log(data);
            alert('Login successful!');
            // Redirect to another page if needed
            window.location.href = '/dashboard';
        })
        .catch(error => {
            // Handle login failure
            console.error(error);
            alert('Login failed. Please try again.');
        });
    });
});
