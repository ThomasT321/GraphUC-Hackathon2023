document.getElementById("myForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the form from submitting in the traditional way

    // Get the data from the form
    const user_request = document.getElementById("textQuery").value;
    const graph_url = document.getElementById("idNumber").value;

    // Define the data to be sent
    const data = {
        user_request: user_request,
        graph_url: graph_url
    };

    // Send the data to the Flask server using the Fetch API
    fetch("http://127.0.0.1:5000/chatapi", {
        method: "POST", // Use POST method to send data
        headers: {
            "Content-Type": "application/json" // Set the content type to JSON
        },
        body: JSON.stringify(data) // Convert data to JSON format
    })
    .then(response => response.json()) // Parse the response as JSON
    .then(responseData => {
        // Handle the response from the server
        document.getElementById("response").textContent = "Response from Flask: " + responseData.message;
    })
    .catch(error => {
        // Handle any errors
        console.error("Error:", error);
        document.getElementById("response").textContent = "Error occurred while sending data to Flask.";
    });
});
