// script.js
document.addEventListener("DOMContentLoaded", function () {
  const chatbotContainer = document.getElementById("chatbot-container");
  const closeBtn = document.getElementById("close-btn");
  const sendBtn = document.getElementById("send-btn");
  const chatbotInput = document.getElementById("chatbot-input");
  const chatbotMessages = document.getElementById("chatbot-messages");

  const chatbotIcon = document.getElementById("chatbot-icon");
  const closeButton = document.getElementById("close-btn");

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
    chatbotMessages.scrollTo({
      top: chatbotMessages.scrollHeight,
      behavior: "smooth",
    });
  });

  function sendMessage() {
    const userMessage = chatbotInput.value.trim();
    if (userMessage) {
      appendMessage("user", userMessage);
      chatbotInput.value = "";
      getBotResponse(userMessage);
    }
  }

  function appendMessage(sender, message) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);
    messageElement.textContent = message;
    chatbotMessages.appendChild(messageElement);

    setTimeout(() => {
    chatbotMessages.scrollTo({
      top: chatbotMessages.scrollHeight,
      behavior: "smooth",
    });
  }, 100);
  }

  async function getBotResponse(userMessage) {

    const message = userMessage.toLowerCase();

    // Predefined responses
    const responses = {
      "hi":"Hi there!, Welcome to JoyJar - Your digital buddy.",
      "what is mental health": "Mental health includes our emotional, psychological, and social well-being. It affects how we think, feel, and act.",
      "how to reduce stress": "Try deep breathing, physical activity, connecting with friends, or mindfulness exercises to help reduce stress.",
      "feeling anxious": "It's okay to feel anxious. Try grounding techniques, breathing exercises, or talking to someone you trust.",
      "can't sleep": "Poor sleep can be caused by stress. Try a relaxing bedtime routine, limit screens before bed, and avoid caffeine late in the day.",
      "what is mindfulness": "Mindfulness is being fully present and aware of the moment. It helps reduce stress and improve focus.",
      "how to stay motivated": "Break tasks into small steps, set achievable goals, and reward yourself along the way. Progress matters more than perfection!",
      "what is depression": "Depression is a mood disorder with persistent sadness or loss of interest. You're not alone—support and treatment are available.",
      "how to practice self-care": "Self-care includes resting, eating well, staying active, and doing activities that bring you joy and relaxation.",
      "how to improve mental health": "Start small: talk to someone, stay active, sleep well, and be kind to yourself.",
      "hello": "Hi there! How can I support your mental wellness today?",
    "mental health": "Mental health is about emotional, psychological, and social well-being.",
    "stress": "Take a deep breath. Try a quick walk, journaling, or talking to someone you trust.",
    "depression": "You’re not alone. It's okay to reach out. Want some self-care tips?",
"i'm sad": "It's okay to feel sad sometimes. Try expressing your feelings, journaling, or reaching out to someone you trust."
    };
  
    // Match user message to a predefined response
    for (const key in responses) {
      if (message.includes(key)) {
        appendMessage("bot", responses[key]);
        return;
      }
    }
    const apiKey = "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"; // Replace with your OpenAI API key
    const apiUrl = "https://api.openai.com/v1/chat/completions";

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model: "gpt-3.5-turbo",
          messages: [{ role: "user", content: userMessage }],
          max_tokens: 150,
        }),
      });

      const data = await response.json();
      const botMessage = data.choices[0].message.content;
      appendMessage("bot", botMessage);
    } catch (error) {
      console.error("Error fetching bot response:", error);
      appendMessage("bot", "Sorry, something went wrong. Please try again.");
    }
  }
});
