const API = "/items/";

async function loadItems() {
  const res = await fetch(API);
  const items = await res.json();
  const list = document.getElementById("item-list");
  list.innerHTML = "";
  if (items.length === 0) { list.innerHTML = "<p>No items yet.</p>"; return; }
  items.forEach(item => {
    const card = document.createElement("div");
    card.className = "item-card";
    card.innerHTML = `
      <p><strong>#${item.id} — ${item.name}</strong></p>
      <p>${item.description || "(no description)"}</p>
      <button onclick="deleteItem(${item.id})">Delete</button>
    `;
    list.appendChild(card);
  });
}

async function createItem() {
  document.getElementById("create-error").textContent = "";
  const name = document.getElementById("name").value.trim();
  const description = document.getElementById("description").value.trim() || null;
  if (!name) { document.getElementById("create-error").textContent = "Name is required."; return; }
  const res = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, description })
  });
  if (!res.ok) {
    const err = await res.json();
    document.getElementById("create-error").textContent = err.detail || "Error creating item.";
  } else {
    document.getElementById("name").value = "";
    document.getElementById("description").value = "";
    loadItems();
  }
}

async function updateItem() {
  document.getElementById("update-error").textContent = "";
  const id = document.getElementById("update-id").value;
  const name = document.getElementById("update-name").value.trim();
  const description = document.getElementById("update-description").value.trim() || null;
  if (!id || !name) { document.getElementById("update-error").textContent = "ID and Name are required."; return; }
  const res = await fetch(`${API}${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, description })
  });
  if (!res.ok) {
    const err = await res.json();
    document.getElementById("update-error").textContent = err.detail || "Error updating item.";
  } else {
    document.getElementById("update-id").value = "";
    document.getElementById("update-name").value = "";
    document.getElementById("update-description").value = "";
    loadItems();
  }
}

async function deleteItem(id) {
  const res = await fetch(`${API}${id}`, { method: "DELETE" });
  if (res.ok) loadItems();
}

loadItems();
