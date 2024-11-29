const chatBody = document.getElementById('chat-body');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Envia a mensagem
function sendMessage() {
    const userMessage = userInput.value.trim();

    if (userMessage === '') return;

    addMessage('user-message', userMessage);

    getBotResponse(userMessage);

    userInput.value = '';
}

function addMessage(className, message) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add(className);
    messageDiv.innerText = message;
    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
}

function getBotResponse(message) {
    fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: message }),
    })
        .then((response) => response.json())
        .then((data) => addMessage('bot-message', data.answer))
        .catch((err) =>
            addMessage('bot-message', 'Desculpe, houve um erro ao processar sua mensagem.')
        );
}
