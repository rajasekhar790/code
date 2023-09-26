function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    if (userInput.trim() === "") return;  // Prevent empty messages

    // Display user's message
    const chatbox = document.getElementById("chatbox");
    const userMessageDiv = document.createElement("div");
    userMessageDiv.className = "user-message";
    userMessageDiv.textContent = userInput;
    chatbox.appendChild(userMessageDiv);

    // Fetch response from Flask server
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const botMessageDiv = document.createElement("div");
        botMessageDiv.className = "bot-message";
        botMessageDiv.textContent = data.response;
        chatbox.appendChild(botMessageDiv);
    });

    // Clear the input field
    document.getElementById("userInput").value = "";
}
