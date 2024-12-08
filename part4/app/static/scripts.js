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
  const visitorForm = document.getElementById('visitor-form');
  const ownerForm = document.getElementById('owner-form');
  const visitorButton = document.getElementById('visitor-button');
  const ownerButton = document.getElementById('owner-button');
  const token = checkAuthentication();
  const placeId = getPlaceIdFromURL();

  const isRegistrationPage = visitorForm && ownerForm && visitorButton && ownerButton;

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
   if (isRegistrationPage) {
    function switchForm(type) {
        if (type === 'visitor') {
            visitorForm.style.display = 'block';
            ownerForm.style.display = 'none';
            visitorButton.classList.add('active');
            ownerButton.classList.remove('active');
        } else {
            visitorForm.style.display = 'none';
            ownerForm.style.display = 'block';
            ownerButton.classList.add('active');
            visitorButton.classList.remove('active');
        }
    }

   switchForm('visitor');

   visitorButton?.addEventListener('click', (e) => {
      e.preventDefault();
      switchForm('visitor');
   });

   ownerButton?.addEventListener('click', (e) => {
      e.preventDefault();
      switchForm('visitor');
   });
   
   function validateForm(formID) {
        const form = document.getElementById(formID);
        if (!form) return false;

        const password = form.querySelector('input[type="password"]')?.value;
        const confirmPassword = form.querySelector('input[name="confirmPassword"]')?.value;

        if (password !== confirmPassword) {
            alert('Passwords do not match');
            return false;
        }
        return true;
  }

  function validateCoordinates() {
      const lat = parseFloat(document.getElementById('latitude')?.value || 0);
      const lng = parseFloat(document.getElementById('longitude')?.value || 0);

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

  visitorForm?.addEventListener('submit', (e) => {
    if (!validateForm('visitor-form')) {
      e.preventDefault();
    }
  });

  ownerForm?.addEventListener('submit', (e) => {
    if (!validateForm('owner-form') || !validateCoordinates()) {
      e.preventDefault();
    }
  });
}

const loginForm = document.getElementById('login-form');
if (loginForm) {
  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(loginForm);
    const data = Object.fromEntries(formData);
    const { email, password } = data;

    if (!email || !password) {
      alert('Please enter both email and password');
      return;
    }
    try {
        const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
          });

          if (!response.ok) {
              throw new Error('Login Unsuccessful');
          }
          window.location.href = 'index.html';
      } catch (error) {
        console.error('Login error:', error);
        alert('Login failed:' + error.message);
      }
  });
  }
  const adminRegister = document.getElementById('admin-register');

  async function adminReg(fname, lname, email, password) {
      const payload = {
                      fname: fname,
                      lname: lname,
                      email: email,
                      password: password
      }
      try {
          const response = await fetch ('http://127.0.0.1:5000/admin', {
              method: 'POST',
              headers: {
                  'content-type': 'application/json'
              },
              body: JSON.stringify( payload )
          });

          if (!response.ok) {
              throw new Error('Failed registration');
          }
      except (error) {
          console.error('Login error:', error)
      }
      }
  }
});
