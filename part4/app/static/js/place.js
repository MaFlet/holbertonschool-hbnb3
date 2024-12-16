document.addEventListener('DOMContentLoaded', function() {
    // Get place ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    // Show/hide review form based on login status
    const isLoggedIn = !!localStorage.getItem('user_id');
    const addReviewSection = document.getElementById('add-review');
    addReviewSection.style.display = isLoggedIn ? 'block' : 'none';

    // Handle review form submission
    const reviewForm = document.getElementById('review-form');
    reviewForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        if (!isLoggedIn) {
            window.location.href = '/login';
            return;
        }

        const reviewText = document.getElementById('review-text').value;
        const rating = document.getElementById('review-rating').value;

        try {
            const response = await fetch(`/api/v1/places/${placeId}/reviews`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: reviewText,
                    rating: rating
                })
            });

            if (response.ok) {
                loadReviews(); // Reload reviews after submission
                reviewForm.reset();
            } else {
                throw new Error('Failed to submit review');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error submitting review');
        }
    });

    // Load place details
    async function loadPlaceDetails() {
        try {
            const response = await fetch(`/api/v1/places/${placeId}`);
            const place = await response.json();
            
            document.getElementById('place-title').textContent = place.title;
            document.getElementById('host-name').textContent = `${place.owner.first_name} ${place.owner.last_name}`;
            document.getElementById('place-price').textContent = place.price;
            document.getElementById('place-description').textContent = place.description;

            // Load amenities
            const amenitiesList = document.getElementById('place-amenities');
            amenitiesList.innerHTML = '';
            place.amenities.forEach(amenity => {
                const li = document.createElement('li');
                li.textContent = amenity.name;
                amenitiesList.appendChild(li);
            });
        } catch (error) {
            console.error('Error:', error);
        }
    }

    // Load reviews
    async function loadReviews() {
        try {
            const response = await fetch(`/api/v1/places/${placeId}/reviews`);
            const reviews = await response.json();
            
            const reviewsContainer = document.getElementById('reviews-container');
            reviewsContainer.innerHTML = '';
            
            reviews.forEach(review => {
                const reviewCard = document.createElement('div');
                reviewCard.className = 'review-card';
                reviewCard.innerHTML = `
                    <p>${review.text}</p>
                    <p>Rating: ${review.rating}/5</p>
                    <p>By: ${review.user.first_name}</p>
                `;
                reviewsContainer.appendChild(reviewCard);
            });
        } catch (error) {
            console.error('Error:', error);
        }
    }

    // Initial load
    loadPlaceDetails();
    loadReviews();
});
