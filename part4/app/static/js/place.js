document.addEventListener('DOMContentLoaded', function() {
    // Get place ID from URL
    // const urlParams = new URLSearchParams(window.location.search);
    // const placeId = urlParams.get('id');
    const placeId = window.location.pathname.split('/').pop();

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
            if (!response.ok) {
                throw new Error(`HTTP error! Response status: ${response.status} ${response.statusText}`)
            }
            const place = await response.json();

            // Updating place details
            document.getElementById('place-title').textContent = place.title;
            document.getElementById('host-name').textContent = `${place.owner.first_name} ${place.owner.last_name}`;
            document.getElementById('place-price').textContent = place.price;
            document.getElementById('place-description').textContent = place.description;

            //   // Update images if they exist
            //   if (place.image_paths && place.image_paths.length > 0) {
            //     const imageGallery = document.querySelector('.image-gallery');
            //     imageGallery.innerHTML = ''; // Clear existing images
            //     place.image_paths.forEach(imagePath => {
            //         const img = document.createElement('img');
            //         img.src = imagePath;
            //         img.alt = 'Place Image';
            //         imageGallery.appendChild(img);
            //     });
            // }

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
            if (!response.ok) {
                throw new Error(`HTTP error! Response status: ${response.status} ${response.statusText}`)
            }
            const reviews = await response.json();
            
            const reviewsContainer = document.getElementById('reviews-container');
            reviewsContainer.innerHTML = ''; // Clearing exisiting reviews
            
            reviews.forEach(review => {
                const reviewCard = document.createElement('div');
                reviewCard.className = 'review-card';
                reviewCard.innerHTML = `
                    <p class="review-text">${review.text}</p>
                    <div class="review-meta">
                        <p class="review-rating">Rating: ${review.rating}/5</p>
                        <p class="review-button">By: ${review.user.first_name} ${review.user.last_name}</p>
                    </div>
                `;
                reviewsContainer.appendChild(reviewCard);
            });
        } catch (error) {
            console.error('Error loading reviews:', error);
            document.getElementById('review-container').innerHTML =
            '<p class="error"> Error loading reviews. Please try again later.</p>';
        }
    }

    // Initial load
    loadPlaceDetails();
    loadReviews();
});
