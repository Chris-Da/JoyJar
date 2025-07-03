// script.js
document.addEventListener("DOMContentLoaded", function () {
  const chatbotContainer = document.getElementById("chatbot-container");
  const closeBtn = document.getElementById("close-btn");
  const sendBtn = document.getElementById("send-btn");
  const chatbotInput = document.getElementById("chatbot-input");
  const chatbotMessages = document.getElementById("chatbot-messages");

  const chatbotIcon = document.getElementById("chatbot-icon");
  const closeButton = document.getElementById("close-btn");
 // <-- Put your key here

  // Toggle chatbot visibility when clicking the icon
  // Show chatbot when clicking the icon
  chatbotIcon.addEventListener("click", function () {
    chatbotContainer.classList.remove("hidden");
    chatbotIcon.style.display = "none"; // Hide chat icon
  });

  // Also toggle when clicking the close button
  closeButton.addEventListener("click", function () {
    chatbotContainer.classList.add("hidden");
    chatbotIcon.style.display = "flex"; // Show chat icon again
  });

  sendBtn.addEventListener("click", sendMessage);
  chatbotInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

  chatbotInput.addEventListener("input", function () {
    setTimeout(() => {
      chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }, 0);
  });

  // Add welcome message
  appendMessage("bot", "Hello! I'm JoyJar, your mental health companion. How can I help you today?");

  async function sendMessage() {
    const userMessage = chatbotInput.value.trim();
    if (!userMessage) return;

    // Disable input while processing
    chatbotInput.disabled = true;
    sendBtn.disabled = true;

    // Add user message to chat
    appendMessage("user", userMessage);
    chatbotInput.value = "";

    try {
      // Show typing indicator
      // const typingIndicator = appendMessage("bot", "Typing...");
      const typingIndicator = appendMessage("bot", "...");
      
      // Send message to backend
      const response = await fetch("http://127.0.0.1:8000/api/chatterbot-chat/", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage })
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      
      // Remove typing indicator
      typingIndicator.remove();
      
      // Add bot response
      const messageElement = appendMessage("bot", data.reply);
      
      // Add feedback buttons if we have an interaction ID
      if (data.interaction_id) {
        const feedbackContainer = document.createElement('div');
        feedbackContainer.className = 'feedback-container';
        feedbackContainer.innerHTML = `
          <span>Was this helpful?</span>
          <button class="feedback-btn" data-feedback="true">👍</button>
          <button class="feedback-btn" data-feedback="false">👎</button>
        `;
        
        // Add feedback event listeners
        feedbackContainer.querySelectorAll('.feedback-btn').forEach(btn => {
          btn.addEventListener('click', async function() {
            const feedback = this.dataset.feedback === 'true';
            try {
              await fetch('http://localhost:8000/api/chatbot/feedback/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  interaction_id: data.interaction_id,
                  feedback: feedback
                })
              });
              
              // Disable feedback buttons after submission
              feedbackContainer.querySelectorAll('.feedback-btn').forEach(b => b.disabled = true);
              feedbackContainer.querySelector('span').textContent = 'Thank you for your feedback!';
            } catch (error) {
              console.error('Error submitting feedback:', error);
            }
          });
        });
        
        messageElement.appendChild(feedbackContainer);
      }

    } catch (error) {
      console.error('Error:', error);
      appendMessage("bot", "I'm learning and sometimes I make mistakes. Please try again later or contact support.");
    } finally {
      // Re-enable input
      chatbotInput.disabled = false;
      sendBtn.disabled = false;
      chatbotInput.focus();
    }
  }

  async function sendToGeminiViaBackend(userMessage) {
    const res = await fetch("/api/chatterbot-chat/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage })
    });
    const data = await res.json();
    return data.reply || data.error || "No response";
  }

  async function handleUserMessage(userMessage) {
    // Show user message in chat UI...
    const botReply = await sendToGeminiViaBackend(userMessage);
    // Show botReply in chat UI...
  }

  function appendMessage(sender, message) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);
    messageElement.textContent = message;
    chatbotMessages.appendChild(messageElement);

    // Scroll to bottom
    setTimeout(() => {
      chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }, 0);

    return messageElement;
  }
});
