document.addEventListener('DOMContentLoaded', () => {
    const visitorForm = document.getElementById('visitor-form');
    const ownerForm = document.getElementById('owner-form');
    const visitorButton = document.getElementById('visitor-button');
    const ownerButton = document.getElementById('owner-button');

    function handleFocusTrap(formElement) {
        const focusableElements = formElement.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"]'
        );
        const firstFocusable = focusableElements[0];
        const lastFocusable = focusableElements[focusableElements.length -1];

        formElement.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                if (e.shiftkey && document.activeElement === firstFocusable) {
                    e.preventDefault();
                    lastFocusable.focus();
                } else if (!e.shiftkey && document.activeElement === lastFocusable) {
                    e.preventDefault();
                    firstFocusable.focus();
                }
            }
        });
    }

    function releaseFocus() {
        document.querySelectorAll('[tabindex]').forEach(element => {
            if (element.getAttribute('tabindex') === '-1') {
                element.removeAttribute('tabindex');
            }
        });

        document.querySelectorAll('[aria-hidden="true"]').forEach(element => {
            element.removeAttribute('aria-hidden');
        });

        document.body.style.overflow = '';
        document.body.style.paddingRight = '';
        document.querySelectorAll('.model-backdrop').forEach(el => el.remove());

        document.body.setAttribute('tabindex', '-1');
        document.body.focus();
        document.body.removeAttribute('tabindex');
    }

    function switchForm(type) {
        releaseFocus();
        console.log('Switching to:', type);

        if (type === 'visitor') {
            visitorForm.style.display = 'block';
            ownerForm.style.display = 'none';
            visitorButton.classList.add('active');
            ownerButton.classList.remove('active');
            handleFocusTrap(visitorForm);
            document.getElementById('visitor-first-name')?.focus();
            visitorForm.removeAttribute('aria-hidden');
            ownerForm.setAttribute('aria-hidden', 'true');
        } else if (type === 'owner') {
            visitorForm.style.display = 'none';
            ownerForm.style.display = 'block';
            ownerButton.classList.add('active');
            visitorButton.classList.remove('active');
            handleFocusTrap(ownerForm);
            document.getElementById('owner-first-name')?.focus();
            ownerForm.removeAttribute('aria-hidden');
            visitorForm.setAttribute('aria-hidden', 'true');
        }
    }

    switchForm('visitor');

    visitorButton?.addEventListener('click', (e) => {
        e.preventDefault();
        console.log('Visitor button clicked');
        switchForm('visitor');
    });

    ownerButton?.addEventListener('click', (e) => {
        e.preventDefault();
        console.log('Owner button clicked');
        switchForm('owner');
    });

    function validatePasswords(formId) {
        const form = document.getElementById(formId);
        const password = form.querySelector('input[name="password"]')?.value;
        const confirmPassword = form.querySelector('input[name="comfirmPassword"]')?.value;

        if (password !== confirmPassword) {
            alert('Password do not match');
            return false;
        }
        return true;
    }

    function validateCoordinates() {
        const lat = parseFloat(document.getElementById('latitude')?.value || 0);
        const lng = parseFloat(document.getElementById('longitude')?.value || 0);

        if (isNaN(lat) || isNaN(lng)) {
            alert('Please enter valid coordinates');
            return false;
        }

        if (lat < -90 || lat > 90) {
            alert('Latitude must be between -90 and 90 degrees');
            return false;
        }
        if (lng < -180 || lng > 180) {
            alert('Longitude must be between -180 and 180 degrees')
            return false
        }
        return true;
    }

    visitorForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!validatePasswords('visitor-form')) {
            document.querySelector('#visitor-form input[name="password"]')?.focus();
            return;
        } 
    
        const formData = new FormData(visitorFrom);
        try {
            const response = await fetch('http://127.0.0.1:5000/register-visitor', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Registration failed');
            }

            releaseFocus();
            alert('Registration successful! Please login.');
            window.location.href = '/login';
        } catch (error) {
            console.error('Registration error:', error);
            alert('Registration failed: ' + error.message);
            document.getElementById('visitor-first-name')?.focus();
        }
    });

    ownerForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!validatePasswords('owner-form')) {
            document.querySelector('#owner-form input[name="password"]')?.focus();
            return;
        }
        if (!validateCoordinates()) {
            document.getElementById('latitude')?.focus();
            return;
        }

        const formData = new FormData(ownerForm);
        try {
            const response = await fetch('http://127.0.0.1:5000/register-owner', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Registration failed');
            }

            releaseFocus();
            alert('Registration successful! Please login.');
            window.location.href = '/login';
        } catch (error) {
            console.error('Registration error:', error);
            alert('Registration failed: ' + error.message);
            document.getElementById('owner-first-name')?.focus();
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            releaseFocus();
        }
    });

    window.addEventListener('beforeunload', () => {
        releaseFocus();
    });
});
