document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');

    function validatePasswords() {
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        if (password !== confirmPassword) {
            alert('Passwords do not match');
            return false;
        }
        return true;
    }

    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!validatePasswords()) {
            return;
        }

        const formData = new FormData(form);

        try {
            const response = await fetch('http://127.0.0.1:5000/register-visitor', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Registration failed');
            }

            const successMessage = document.createElement('div');
            successMessage.id = 'success-message';
            successMessage.classList.add('success-message');
            successMessage.innerHTML = `
                <h3>Registration Successful!</h3>
                <p>You have successfully registered as a visitor, You can go back to the <a href="index.html">Home Page</a> to book your place.</p>
            `;

            form.insertAdjacentElement('afterend', successMessage);

            form.classList.add('hidden');
            successMessage.classList.remove('hidden');
        } catch (error) {
            console.error('Registration error:', error);
            alert('Registration failed: ' + error.message);
        }
    });
});
