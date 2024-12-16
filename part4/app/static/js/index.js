document.addEventListener('DOMContentLoaded', async () => {
    // Function to load and display places
    async function loadPlaces() {
        const placesList = document.getElementById('places-list');
        if (!placesList) return;

        try {
            const response = await fetch('/api/v1/places');
            const places = await response.json();
            
            placesList.innerHTML = '<h2>Available Places</h2>';
            
            places.forEach(place => {
                const placeCard = document.createElement('div');
                placeCard.className = 'place-card';
                placeCard.innerHTML = `
                    <img src="${place.image_url || 'https://cdn.mos.cms.futurecdn.net/GNMsSAqdJLDicwGiY6Yedd-768-80.jpg.webp'}" 
                         alt="${place.title}" class="place-image">
                    <div class="place-details">
                        <p class="place-name">${place.title}</p>
                        <p class="place-price">$${place.price} per night</p>
                        <button class="details-button" onclick="window.location.href='/place/${place.id}'">View Details</button>
                    </div>
                `;
                placesList.appendChild(placeCard);
            });
        } catch (error) {
            console.error('Error loading places:', error);
            placesList.innerHTML = '<p class="error-message">Error loading places. Please try again later.</p>';
        }
    }

    // Handle price filtering
    function setupPriceFilter() {
        const priceFilter = document.getElementById('price-filter');
        if (!priceFilter) return;

        priceFilter.addEventListener('change', async (e) => {
            const maxPrice = e.target.value;
            try {
                const response = await fetch(`/api/v1/places?max_price=${maxPrice}`);
                const places = await response.json();
                const placesList = document.getElementById('places-list');
                
                placesList.innerHTML = '<h2>Available Places</h2>';
                places.forEach(place => {
                    const placeCard = document.createElement('div');
                    placeCard.className = 'place-card';
                    placeCard.innerHTML = `
                        <img src="${place.image_url || 'https://cdn.mos.cms.futurecdn.net/GNMsSAqdJLDicwGiY6Yedd-768-80.jpg.webp'}" 
                             alt="${place.title}" class="place-image">
                        <div class="place-details">
                            <p class="place-name">${place.title}</p>
                            <p class="place-price">$${place.price} per night</p>
                            <button class="details-button" onclick="window.location.href='/place/${place.id}'">View Details</button>
                        </div>
                    `;
                    placesList.appendChild(placeCard);
                });
            } catch (error) {
                console.error('Error filtering places:', error);
                placesList.innerHTML = '<p class="error-message">Error filtering places. Please try again later.</p>';
            }
        });
    }

    // Initialize the page
    await loadPlaces();
    setupPriceFilter();
});
