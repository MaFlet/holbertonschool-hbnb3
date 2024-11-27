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

function getPlaceIdFromURL() {
  // Extract the place ID from window.location.search
  // Your code here
  // Get the query string from the URL
const queryString = window.location.search;

// Parse the query string
const urlParams = new URLSearchParams(queryString);

// Retrieve the place ID
const placeId = urlParams.get('place_id');  
//console.log(placeId);
}

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
});
