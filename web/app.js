const messages = document.querySelector("#messages");
const question = document.querySelector("#question");
const errorBox = document.querySelector("#error");
const dossierList = document.querySelector("#dossier-list");

function addMessage(text, role) {
  const item = document.createElement("div");
  item.className = `message ${role}`;
  item.innerHTML = `<div class="avatar">${role === "user" ? "V" : "L"}</div><div><span class="message-name">${role === "user" ? "Vous" : "Lisa"}</span><p></p></div>`;
  renderMessage(item.querySelector("p"), text);
  messages.appendChild(item);
  messages.scrollTop = messages.scrollHeight;
}

function renderInline(container, text) {
  const normalized = text.replace(/^\s{0,3}#{1,6}\s+/, "");
  const parts = normalized.split(/(\*\*[^*]+\*\*)/g);
  parts.forEach((part) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      const strong = document.createElement("strong");
      strong.textContent = part.slice(2, -2);
      container.appendChild(strong);
    } else {
      container.appendChild(document.createTextNode(part));
    }
  });
}

function renderMessage(container, text) {
  const lines = String(text || "").replace(/\r\n/g, "\n").split("\n");
  let index = 0;

  while (index < lines.length) {
    if (lines[index].trim().startsWith("|") && lines[index].trim().endsWith("|")) {
      const tableLines = [];
      while (index < lines.length && lines[index].trim().startsWith("|") && lines[index].trim().endsWith("|")) {
        tableLines.push(lines[index].trim());
        index += 1;
      }

      const separatorCells = tableLines.length >= 2
        ? tableLines[1].split("|").slice(1, -1).map((cell) => cell.trim())
        : [];
      if (tableLines.length >= 2 && separatorCells.length > 0 && separatorCells.every((cell) => /^:?-{3,}:?$/.test(cell))) {
        const table = document.createElement("table");
        table.className = "message-table";
        const header = table.insertRow();
        tableLines[0].split("|").slice(1, -1).forEach((cell) => {
          const th = document.createElement("th");
          renderInline(th, cell.trim());
          header.appendChild(th);
        });
        tableLines.slice(2).forEach((line) => {
          const row = table.insertRow();
          line.split("|").slice(1, -1).forEach((cell) => {
            const td = document.createElement("td");
            renderInline(td, cell.trim());
            row.appendChild(td);
          });
        });
        container.appendChild(table);
        continue;
      }
    }

    const line = document.createElement("span");
    renderInline(line, lines[index]);
    container.appendChild(line);
    if (index < lines.length - 1) container.appendChild(document.createElement("br"));
    index += 1;
  }
}

function renderDossiers(dossiers) {
  dossierList.innerHTML = "";
  document.querySelector("#dossier-count").textContent = dossiers.length;
  dossiers.forEach((dossier) => {
    const dgen = dossier.dgen || {};
    const item = document.createElement("div");
    item.className = "dossier";
    item.dataset.search = `${dossier.numero_dossier} ${dossier.client_nom}`.toLowerCase();
    item.innerHTML = `<span class="dossier-status">${dossier.statut}</span><strong></strong><small></small>`;
    item.querySelector("strong").textContent = dossier.numero_dossier;
    item.querySelector("small").textContent = `${dossier.client_nom} · ${Number(dgen.montant_principal || 0).toLocaleString("fr-FR")} EUR`;
    item.addEventListener("click", () => { question.value = `Donne-moi les détails du dossier ${dossier.numero_dossier}`; question.focus(); });
    dossierList.appendChild(item);
  });
}

async function loadDashboard() {
  const response = await fetch("/api/dashboard");
  if (!response.ok) throw new Error("Impossible de charger le tableau de bord.");
  const data = await response.json();
  document.querySelector("#total-dossiers").textContent = data.stats.total_dossiers;
  document.querySelector("#active-dossiers").textContent = data.stats.dossiers_actifs;
  document.querySelector("#total-amount").textContent = Number(data.stats.montant_total_accorde_eur).toLocaleString("fr-FR");
  document.querySelector("#total-events").textContent = data.total_evenements;
  renderDossiers(data.dossiers);
}

async function sendQuestion(value) {
  const text = value.trim();
  if (!text) return;
  addMessage(text, "user");
  question.value = "";
  errorBox.hidden = true;
  const response = await fetch("/api/chat", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({question: text}) });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Erreur pendant la requête.");
  addMessage(data.answer, "assistant");
}

document.querySelector("#chat-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try { await sendQuestion(question.value); } catch (error) { errorBox.textContent = error.message; errorBox.hidden = false; }
});
document.querySelectorAll(".suggestions button").forEach((button) => button.addEventListener("click", () => sendQuestion(button.dataset.question).catch((error) => { errorBox.textContent = error.message; errorBox.hidden = false; })));
document.querySelector("#dossier-search").addEventListener("input", (event) => {
  const search = event.target.value.toLowerCase();
  document.querySelectorAll(".dossier").forEach((item) => { item.hidden = !item.dataset.search.includes(search); });
});
loadDashboard().catch((error) => { errorBox.textContent = error.message; errorBox.hidden = false; });
