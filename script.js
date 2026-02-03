const API_URL = "https://business-ai-app.onrender.com/ai/ask";

// Ask AI (text)
async function askAI() {
  const question = document.getElementById("question").value;
  const responseDiv = document.getElementById("response");
  responseDiv.innerHTML = "⏳ লোড হচ্ছে...";

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    const data = await res.json();
    responseDiv.innerHTML = "🤖 " + data.answer;
    speakText(data.answer);

  } catch (err) {
    responseDiv.innerHTML = "❌ Error: " + err;
  }
}

// Voice input
function startVoice() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = "bn-BD";
  recognition.start();

  recognition.onresult = function(event) {
    const text = event.results[0][0].transcript;
    document.getElementById("question").value = text;
    askAI();
  };
}

// AI voice output
function speakText(text) {
  const speech = new SpeechSynthesisUtterance(text);
  speech.lang = "bn-BD";
  window.speechSynthesis.speak(speech);
}
