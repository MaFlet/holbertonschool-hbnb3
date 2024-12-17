document.addEventListener('DOMContentLoaded', function() {
    const placeId = window.location.pathname.split('/').pop();
    const form = document.getElementById('review-form');
    const backLink = document.getElementById('back-to-place');
    
    // Update back link
    backLink.href = `/place/${placeId}`;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
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
                    rating: parseInt(rating)
                })
            });
            if (response.ok) {
                alert('Review submitted successfully!');
                window.location.href = `/place/${placeId}`;
            } else {
                throw new Error('Failed to submit review');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error submitting review');
        }
    });
});
