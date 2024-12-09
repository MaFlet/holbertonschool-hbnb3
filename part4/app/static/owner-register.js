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

    function validateCoordinates() {
        const lat = parseFloat(document.getElementById('latitude').value || 0);
        const lng = parseFloat(document.getElementById('longitude').value || 0);

        if (isNaN(lat) || isNaN(lng)) {
            alert('Please enter valid coordinates');
            return false;
        }

        if (lat < -90 || lat > 90) {
            alert('Latitude must be between -90 and 90 degrees');
            return false;
        }
        if (lng < -180 || lng > 180) {
            alert('Longitude must be between -180 and 180 degrees');
            return false;
        }
        return true;
    }

    form?.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!validatePasswords()) {
            return;
        }

        if (!validateCoordinates()) {
            return;
        }

        const formData = new FormData(form);

        try {
            const response = await fetch('http://127.0.0.1:5000/register-owner', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Registration failed');
            }

            alert('Registration successful! Please login.');
            window.location.href = '/login';
        } catch (error) {
            console.error('Registration error:', error);
            alert('Registration failed: ' + error.message);
        }
    });
});
