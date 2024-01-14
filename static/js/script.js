
      let modalBtns = [...document.querySelectorAll(".button, [data-modal='modalLogin']")];
      modalBtns.forEach(function (btn) {
        btn.onclick = function () {
          let modal = btn.getAttribute("data-modal");
          document.getElementById(modal).style.display = "block";
        };
      });
      let closeBtns = [...document.querySelectorAll(".close")];
      closeBtns.forEach(function (btn) {
        btn.onclick = function () {
          let modal = btn.closest(".modal");
          modal.style.display = "none";
        };
      });
      window.onclick = function (event) {
        if (event.target.className === "modal") {
          event.target.style.display = "none";
        }
      };

      document.addEventListener('DOMContentLoaded', function () {
        var loginForm = document.getElementById('login-form');
        var loginError = document.getElementById('login-error');

        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();

            var formData = new FormData(loginForm);

            fetch(loginForm.action, {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Successful login, you can redirect or perform any other action
                    window.location.href = '/';
                } else {
                    // Display the error in the modal
                    loginError.innerHTML = data.error;
                    $('#modalLogin').modal('show');
                }
            })
            .catch(error => {
                console.error('An error occurred during the fetch request.', error);
            });
        });
    });
    document.addEventListener('DOMContentLoaded', function () {
        var signupForm = document.getElementById('signup-form');
        var signupError = document.getElementById('signup-error');

        signupForm.addEventListener('submit', function (e) {
            e.preventDefault();

            var formData = new FormData(signupForm);

            fetch(signupForm.action, {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Successful signup, you can redirect or perform any other action
                    window.location.href = '/';
                } else {
                    // Display the error in the modal
                    signupError.innerHTML = data.error;
                    $('#modalSignup').modal('show');
                }
            })
            .catch(error => {
                console.error('An error occurred during the fetch request.', error);
            });
        });
    });




document.addEventListener('DOMContentLoaded', function() {
    // Check if the user is authenticated
    var authenticated = false; // Default to not authenticated

    // Assume your server provides an API endpoint for checking authentication
    fetch('/api/check_auth/')  // Update with your actual API endpoint
        .then(response => response.json())
        .then(data => {
            authenticated = data.authenticated;
            if (!authenticated) {
                // User is not authenticated, show the login modal
                var modalLogin = new bootstrap.Modal(document.getElementById('modalLogin'));
                modalLogin.show();
            }
        })
        .catch(error => console.error('Error:', error));

    // Handle form submission (assuming you have a form with the id 'login-form')
    var loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission

        if (loginForm.getAttribute('method').toUpperCase() === 'POST') {
            // Assume your server provides an API endpoint for handling form submission
            fetch('/api/signin/', {  // Update with your actual API endpoint
                method: 'POST',
                body: new FormData(loginForm),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Login successful, close the modal or redirect
                        var modalLogin = new bootstrap.Modal(document.getElementById('modalLogin'));
                        modalLogin.hide();
                    } else {
                        // Display login error
                        document.getElementById('login-error').innerText = data.error;
                        document.getElementById('login-error').style.display = 'block';
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    });
});

function get_html_code(){
    var x = CKEDITOR.instances['id_body'].getData();
    var y=document.getElementById('htmldata');
    y.innerHTML=x;
}


    document.querySelectorAll('.like-comment-button').forEach(button => {
        button.addEventListener('click', () => {
            const commentId = button.dataset.commentId;

            // Log comment ID to verify it's being extracted correctly
            console.log('Comment ID:', commentId);

            // Send AJAX request
            fetch(`/like/comment/${commentId}/`, {
                method: 'POST',  // You can use 'GET' or 'POST' depending on your view
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                // Log response data for debugging
                console.log('Response Data:', data);

                // Update the UI with the new like count for the comment
                const likesCountElement = button.nextElementSibling;
                likesCountElement.textContent = `${data.likes} likes`;

                // Toggle like button text based on the 'liked' property
                button.textContent = data.liked ? 'Unlike' : 'Like';
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });



    