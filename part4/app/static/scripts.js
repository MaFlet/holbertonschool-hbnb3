/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

/* ******* 
    Phonx's code snippet for review 

************************************/
function checkAuthentication() {
  const token = getCookie('token');
  if (!token) {
      window.location.href = 'index.html';
  }
  return token;
}

function getCookie(name) {
  // Split the document.cookie string into individual cookies
  const cookies = document.cookie.split(';');
  
  // Loop through the cookies
  for (let i = 0; i < cookies.length; i++) {
      // Trim whitespace and split the cookie into name and value
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
          // Return the value of the cookie
          return cookie.substring(name.length + 1);
      }
  }
  
  // Return null if the cookie is not found
  return null;
}

// old code
//function getPlaceIdFromURL() {
  // Extract the place ID from window.location.search
  // Your code here
  // Get the query string from the URL
//const queryString = window.location.search;

// Parse the query string
//const urlParams = new URLSearchParams(queryString);

// Retrieve the place ID
//const placeId = urlParams.get('place_id');  
//console.log(placeId);
// old code ends here

// ** Egan's code to be reviewed **//
function getPlaceIdFromURL() {
  const queryString = window.location.search; // Extract query string from URL
  const urlParams = new URLSearchParams(queryString); // Parse query string
  const placeId = urlParams.get('place_id'); // Retrieve place_id from query params
  return placeId; // Return place ID
}

async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`/api/places/${placeId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`, // Include JWT token
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch place details');
    }

    const place = await response.json(); // Parse the response JSON
    displayPlaceDetails(place); // Pass the place details to display function
  } catch (error) {
    console.error('Error fetching place details:', error);
    alert('Error fetching place details. Please try again.');
  }
}

function displayPlaceDetails(place) {
  const placeDetailsSection = document.getElementById('place-details');
  placeDetailsSection.innerHTML = ''; // Clear existing content

  // Create and append elements for place details
  const placeName = document.createElement('h1');
  placeName.textContent = place.title;

  const placeHost = document.createElement('p');
  placeHost.innerHTML = `<strong>Host:</strong> ${place.host}`;

  const placePrice = document.createElement('p');
  placePrice.innerHTML = `<strong>Price per night:</strong> $${place.price}`;

  const placeDescription = document.createElement('p');
  placeDescription.innerHTML = `<strong>Description:</strong> ${place.description}`;

  const amenitiesList = document.createElement('ul');
  amenitiesList.id = 'place-amenities';
  place.amenities.forEach(amenity => {
    const amenityItem = document.createElement('li');
    amenityItem.textContent = amenity;
    amenitiesList.appendChild(amenityItem);
  });

  // Append elements to the place details section
  placeDetailsSection.appendChild(placeName);
  placeDetailsSection.appendChild(placeHost);
  placeDetailsSection.appendChild(placePrice);
  placeDetailsSection.appendChild(placeDescription);
  placeDetailsSection.appendChild(amenitiesList);

  // Populate reviews section
  const reviewsSection = document.querySelector('.reviews');
  reviewsSection.innerHTML = '<h2>Reviews</h2>';
  place.reviews.forEach(review => {
    const reviewCard = document.createElement('div');
    reviewCard.className = 'review-card';

    const reviewComment = document.createElement('p');
    reviewComment.className = 'review-comment';
    reviewComment.textContent = `"${review.text}"`;

    const reviewUser = document.createElement('p');
    reviewUser.className = 'review-user';
    reviewUser.textContent = `- ${review.user}`;

    const reviewRating = document.createElement('p');
    reviewRating.className = 'review-rating';
    reviewRating.innerHTML = `<strong>Rating:</strong> ${review.rating}/5`;

    reviewCard.appendChild(reviewComment);
    reviewCard.appendChild(reviewUser);
    reviewCard.appendChild(reviewRating);
    reviewsSection.appendChild(reviewCard);
  });
}

// ** Egan's code end here **//

// Async function to submit review
async function submitReview(token, placeId, reviewText) {
  const reviewData = {
      placeId: placeId,
      review: reviewText,
  };

  // Make a POST request to submit review data
  const response = await fetch('/api/reviews', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`, // Include the token in the Authorization header
      },
      body: JSON.stringify(reviewData), // Send placeId and reviewText in the request body
  });

  return response; // Return the response for further handling
}

// Function to handle the response from the API
function handleResponse(response) {
  if (response.ok) {
      alert('Review submitted successfully!');
      // Clear the form
      document.getElementById('review-form').reset(); // Clear the form after submission
  } else {
      alert('Failed to submit review');
  }
}
  /* ******* 
    Phonx's code snippet for review ends here

************************************/

document.addEventListener('DOMContentLoaded', () => {
  //review form submission script
/* ******* 
    Phonx's code snippet for review 

************************************/

  const reviewForm = document.getElementById('review-form');
  const token = checkAuthentication();
  const placeId = getPlaceIdFromURL();

  if (reviewForm) {
      reviewForm.addEventListener('submit', async (event) => {
          event.preventDefault();

          // Get review text from form
          const reviewText = reviewForm.querySelector('textarea[name="review"]').value;

          try {
              // Call the submitReview function
              const response = await submitReview(token, placeId, reviewText);
              
                // Handle the response
                handleResponse(response);
            } catch (error) {
                console.error('Network error:', error);
                alert('There was a network error while submitting your review.');
            }

      });
  }





  /* ******* 
    Phonx's code snippet for review ends here

************************************/
 /* ******* 
    Mary's code
    ********/
    async function loginUser(email, password) {
      const response = await fetch('http://127.0.0.1:5000/login', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
      });
      if (!response.ok) {
        throw new Error('Login Unsuccessful')
      }
      const data = await response.json();
      return data;
    //   if (response.ok) {
    //     const data = await response.json();
    //     document.cookie = `token=${data.access_token}; path=/`;
    //     window.location.href = 'index.html';
    // } else {
    //     alert('Login failed: ' + response.statusText);
    // }
  }

      if (loginForm) {
          loginForm.addEventListener('submit', async (event) => {
              event.preventDefault();
          const formData = new FormData(loginForm);
          const data = Object.fromEntries(formData);
          const { email, password } = data;
          if (!email || !password) {
            window.location.href="login.html";
          return;
          }
          try {
            const result = await loginUser(email, password);
            // Handle successful login
            console.log('Login successful:', result);
        } catch (error) {
            console.error('Login error:', error);
        }
          });
        }
        function switchform(type) {
          const visitorForm = document.getElementById('visitor-form');
          const ownerForm = document.getElementById('owner-form');
          const visitorButton = document.getElementById('visitor-button');
          const ownerbutton = document.getElementById('owner-button');

          if (type === 'visitor') {
            visitorForm.style.display = 'block';
            ownerForm.style.display = 'none';
            visitorButton.classList.add('active');
            ownerbutton.classList.remove('active');
          } else {
            visitorForm.style.display = 'none';
            ownerForm.style.display = 'block';
            visitorButton.classList.remove('active');
            ownerbutton.classList.add('active');
          }
        }

        function validateForm(formID) {
          const form = document.getElementById(formID);
          const password = form.querySelector('input[type="password"]').value;
          const confirmPassword = form.querySelector('input[name="confirmPassword"]').value;

          if (password !== confirmPassword) {
            alert('Passwords do not match');
            return false;
          }
          return true;
        }
        document.getElementById('visitor-form').onsubmit = function(e) {
          if (!validateForm('visitor-form')) {
            e.preventDefault();
          }
        };
        document.getElementById('owner-form').onsubmit = function(e) {
          if (!validateForm('owner-form')) {
            e.preventDefault();
          }
        }

        function validateCoordinates() {
          const lat = parseFloat(document.getElementById('latitude')).value;
          const lng = parseFloat(document.getElementById('longitude')).value;

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
        document.getElementById('owner-form').onsubmit = function(e) {
          if (!validateForm('owner-form') || !validateCoordinates()) {
            e.preventDefault();
          }
        }
});
