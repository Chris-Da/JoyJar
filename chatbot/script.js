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
"i'm sad": "It's okay to feel sad sometimes. Try expressing your feelings, journaling, or reaching out to someone you trust.",
  // Greetings  
  "hi": "Hi there! 🌟 Welcome to JoyJar—your digital buddy for mental wellness. How can I help you today?",
  "hello": "Hello! 💛 I’m JoyJar, here to support you. What’s on your mind?",
  "hey": "Hey friend! 👋 How are you feeling today?",
  
  // Mental Health Basics  
  "what is mental health": "Mental health includes our emotional, psychological, and social well-being. It shapes how we think, feel, and handle life. Small steps matter! 💪",
  "mental health": "Mental health is just as important as physical health. Let’s nurture it together—want tips or just to talk?",
  
  // Stress & Anxiety  
  "stress": "Stress can feel heavy. Try this: pause, take 3 deep breaths, or step outside for fresh air. You’ve got this. 🌿",  
  "how to reduce stress": "Stress-busters: short walks, laughter, journaling, or humming a calming tune. What works for you?",
  "feeling anxious": "Anxiety is tough but temporary. Try the 5-4-3-2-1 method: Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste. 🌈",  
  "i'm overwhelmed": "Overwhelm is valid. Break tasks into tiny steps, sip water, or scribble your thoughts on paper. One moment at a time. 💧",
  
  // Sadness & Depression  
  "i'm sad": "Your feelings matter. 💔 Would a distraction (like a funny video) help, or do you need to vent? I’m here.",  
  "what is depression": "Depression is more than sadness—it can drain energy and joy. But help exists, and you deserve support. 🌻",  
  "i feel empty": "That sounds really hard. You’re not alone. Even small acts (like a warm shower) can be a start. Be gentle with yourself. 🫂",
  
  // Motivation & Self-Care  
  "how to stay motivated": "Motivation is a flickering flame. Try the 2-minute rule: just start tiny. A walk? One deep breath? Celebrate little wins! 🎉",  
  "how to practice self-care": "Self-care isn’t selfish! Try: a 5-minute stretch, saying no guilt-free, or doodling. What feels nourishing today? 🛁",  
  "i'm tired": "Rest is resistance too. 💤 Can you pause for a 3-minute break? Close your eyes, or listen to calming sounds.",  
  
  // Sleep  
  "can't sleep": "Sleep struggles are real. Try: a warm drink (no caffeine!), dimming lights early, or writing down worries to ‘set them aside’ tonight. 🌙",  
  "insomnia": "Insomnia can feel lonely. Gentle tip: Get up and do something quiet (like reading) if you’re awake >20 mins. Avoid screens! 📚",  
  
  // Mindfulness & Coping  
  "what is mindfulness": "Mindfulness = anchoring to the now. Try noticing your breath or the weight of your feet on the floor. No judgment. 🍃",  
  "panic attack": "Breathe with me: in (4 sec), hold (4), out (6). You’re safe. This will pass. I’m here. 💨",  
  "grounding techniques": "Grounding helps! Name objects around you, press your palms together, or savor a mint. Reconnect to the present. 🌍",  
  
  // Encouragement & Closing  
  "thank you": "You’re so welcome! Remember: progress > perfection. Reach out anytime. 💖",  
  "goodbye": "Goodbye, friend! Be kind to yourself today. JoyJar’s always here if you need me. 🌼",  
  
  // Default fallback  
  "default": "I’m still learning, but I care. Could you rephrase that? Or try: ‘stress’, ‘sadness’, or ‘self-care’. 🌸",  
};
  
    // Match user message to a predefined response
    for (const key in responses) {
      if (message.includes(key)) {
        appendMessage("bot", responses[key]);
        return;
      }
    }
    const apiKey = "Enter you API Key"; // Replace with your OpenAI API key
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
      appendMessage("bot", "Apologies for the hiccup! Could you give it another go.");
    }
  }
});
