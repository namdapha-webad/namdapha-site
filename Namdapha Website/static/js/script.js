function validateForm() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    // Basic validation (you can improve this based on your logic)
    if (username === "" || password === "") {
        errorMessage.textContent = "Both fields are required!";
        console.log("Validation failed: Empty fields detected.");
        return false;
    }

    // Assuming validation passes, log the form values for debugging (remove in production)
    console.log("Username:", username);
    console.log("Password:", password);

    
    window.location.href = "/home"; 

    return false; // Prevent default form submission
}
document.body.style.backgroundImage = "url('/static/images/homepic.jpg')";