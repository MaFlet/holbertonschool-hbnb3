document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const preview = document.getElementById('preview');
    let files = [];

    // Adding drag and drop funcitonality
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drop-zone--over');
    });

    ['dragleave', 'dragend'].forEach(type => {
        dropZone.addEventListener(type, (e) => {
            dropZone.classList.remove('drop-zone--over');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drop-zone--over');

        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            updateThumbnail(e.dataTransfer.files);
        }
    });

    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', () => {
        updateThumbnail(fileInput.files);
    });

    function updateThumbnail(fileList) {
        files = [...fileList];
        preview.innerHTML = '';

        files.forEach((file, index) => {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();

                reader.onload = () => {
                    const div = document.createElement('div');
                    div.className = 'preview-item';
                    div.innerHTML = `
                        <img src="${reader.result}" alt="Preview>
                        <span class="remove-image" data-index="${index}">*</span>
                    `;
                    preview.appendChild(div);
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Removing image functionality
    preview.addEventListener('click', (e) => {
        if (e.target.classList.contains('remove-image')) {
            const index = parseInt(e.target.dataset.index);
            files.splice(index, 1);
            updateThumbnail(files);
        }
    });

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
            const response = await fetch('/register-owner', {
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
