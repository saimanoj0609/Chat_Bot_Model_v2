const chatToggle = document.getElementById('chatToggle');
const chatBox = document.querySelector('.chatbot-container');
const closeBtn = document.getElementById('closeBtn');
const sendBtn = document.getElementById('sendBtn');
const userInput = document.getElementById('userInput');
const chatBody = document.getElementById('chatBody');

// Toggle chat visibility
chatToggle.onclick = () => {
  chatBox.style.display = 'flex';
  chatToggle.style.display = 'none';
};

closeBtn.onclick = () => {
  chatBox.style.display = 'none';
  chatToggle.style.display = 'block';
};

// Send message
sendBtn.onclick = () => {
  const message = userInput.value.trim();
  if (message === '') return;

  addMessage('user', message);
  userInput.value = '';

  if (message.toLowerCase() === 'exit') {
    setTimeout(() => {
      addMessage('bot', "👋 Chat closed. Have a nice day!");
      setTimeout(() => {
        clearChat();
        closeChat();
      }, 1000);
    }, 500);
    return;
  }
  const greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "thanks"];
  if (greetings.includes(message.toLowerCase())) {
    addMessage('bot', "👋 Hello! How can I help you today?");
    return;
  }


  setTimeout(() => {
    generateBotReply(message);
  }, 600);
};

function addMessage(type, text) {
  const msg = document.createElement('div');
  msg.classList.add('message', type);
  msg.innerHTML = text;
  chatBody.appendChild(msg);
  chatBody.scrollTop = chatBody.scrollHeight;
}

userInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendBtn.click();
  }
});

function generateBotReply(userMsg) {
  const loadingWrapper = document.createElement('div');
  loadingWrapper.classList.add('loader-wrapper');

  const loadingMsg = document.createElement('div');
  loadingMsg.classList.add('loader');

  loadingWrapper.appendChild(loadingMsg);
  chatBody.appendChild(loadingWrapper);
  chatBody.scrollTop = chatBody.scrollHeight;

  fetch('/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: userMsg })
  })
    .then(response => response.json())
    .then(data => {
      chatBody.removeChild(loadingWrapper);
      let reply = data.reply;

      if (typeof reply === 'object') {
        reply = `<b>Description:</b> ${reply.description}<br>
        <b>Input:</b> ${reply.input}<br>
        <b>Syntax:</b> ${reply.syntax}`;
      } else {
        try {
          const parsedReply = JSON.parse(reply);
          if (typeof parsedReply === 'object') {
            reply = `<b>Description:</b> ${parsedReply.description}<br>
            <b>Input:</b> ${parsedReply.input}<br>
            <b>Syntax:</b> ${parsedReply.syntax}`;
          }
        } catch (e) {
          // Not JSON
        }
      }

      addMessage('bot', reply);
    })
    .catch(error => {
      chatBody.removeChild(loadingWrapper);
      console.error('Error:', error);
      addMessage('bot', "Sorry, I couldn't reach the server.");
    });
}

// Clear all messages
function clearChat() {
  chatBody.innerHTML = '';
}

// Close chat
function closeChat() {
  chatBox.style.display = 'none';
  chatToggle.style.display = 'block';
}
