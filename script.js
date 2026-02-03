const API_URL = "https://business-ai-app.onrender.com/ai/ask";

function askAI() {
  const q = document.getElementById("question").value;
  document.getElementById("answer").innerText = "লোড হচ্ছে...";

  fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ question: q })
  })
  .then(res => res.json())
  .then(data => {
    const ans = data.answer || data.message || data.result || JSON.stringify(data);
    document.getElementById("answer").innerText = ans;
    speak(ans);
  })
  .catch(err => {
    document.getElementById("answer").innerText = "Error: " + err;
  });
}

// Voice input
function startVoice() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = "bn-BD";
  recognition.start();

  recognition.onresult = function(event) {
    const text = event.results[0][0].transcript;
    document.getElementById("question").value = text;
  };
}

// Voice output
function speak(text) {
  const msg = new SpeechSynthesisUtterance(text);
  msg.lang = "bn-BD";
  speechSynthesis.speak(msg);
}
