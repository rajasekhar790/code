document.getElementById('userInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    const chatbox = document.getElementById('chatbox');

    chatbox.innerHTML += `<div class="user-message">You: ${userInput}</div>`;

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        chatbox.innerHTML += `<div class="bot-message">Bot: ${data.response}</div>`;
        chatbox.scrollTop = chatbox.scrollHeight;
    });

    document.getElementById('userInput').value = '';
}
