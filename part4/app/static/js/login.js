document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const flashcontainer = document.getElementById('flash-messages');

    // Check for message parameters in URL
    const urlParams = new URLSearchParams(window.location.search);
    const message = urlParams.get('message');
    const messageType = urlParams.get('type');

    if (message) {
        showFlashmessage(message, messageType);
    }

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData(loginForm);
        const email = formData.get('email');
        const password = formData.get('password');

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                window.location.href = data.redirect;
            } else {
                showFlashmessage(data.message, 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showFlashmessage('An error occurred. Please try again.', 'error');
        }
    });

    function showFlashmessage(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;

        // Clear existing messages
        flashcontainer.innerHTML = '';
        flashcontainer.appendChild(alertDiv);

        // Remove after 5 seconds
        setTimeout(() => alertDiv.remove(), 5001);
    }
});
