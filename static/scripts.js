const form = document.getElementById("form");
const askBtn = document.getElementById("askBtn");
const clearBtn = document.getElementById("clearBtn");
const questionInput = document.getElementById("question");
const responseBox = document.getElementById("response");
const historyBox = document.getElementById("history");

// Fonction pour récupérer et afficher l'historique
async function fetchHistory() {
  try {
    const res = await fetch("/interactions");
    const data = await res.json();
    historyBox.innerHTML = "";

    data.forEach((item, index) => {
      const div = document.createElement("div");
      div.className = "response-item";
      div.style.animationDelay = `${index * 0.1}s`;

      div.innerHTML = `
        <div class="timestamp">${new Date(item.timestamp).toLocaleString()}</div>
        <div class="question">Q: ${item.question}</div>
        <div class="answer">R: ${item.reponse}</div>
      `;

      historyBox.appendChild(div);
    });
  } catch (err) {
    console.error("Erreur en récupérant l'historique :", err);
  }
}

// Soumission du formulaire
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = questionInput.value.trim();
  if (!question) return;

  askBtn.disabled = true;
  askBtn.innerText = "Recherche...";
  responseBox.style.display = "none";
  responseBox.innerText = "";

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();
    if (data.answer) {
      responseBox.innerText = "Réponse : " + data.answer;
      responseBox.style.display = "block";
      await fetchHistory();
    } else {
      responseBox.innerText = "Erreur : " + (data.error || "Réponse non disponible.");
      responseBox.style.display = "block";
    }
  } catch (err) {
    responseBox.innerText = "Erreur réseau.";
    responseBox.style.display = "block";
  } finally {
    askBtn.disabled = false;
    askBtn.innerText = "Poser la question";
    questionInput.value = "";
  }
});

// Effacer l'historique
clearBtn.addEventListener("click", async () => {
  if (!confirm("Effacer tout l’historique ?")) return;

  try {
    const res = await fetch("/clear", { method: "DELETE" });
    if (res.ok) {
      historyBox.innerHTML = "";
    } else {
      alert("Erreur lors de la suppression.");
    }
  } catch (err) {
    alert("Erreur réseau lors de la suppression.");
  }
});

// Chargement initial
window.onload = fetchHistory;
