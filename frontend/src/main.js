import './style.css';
import './app.css';

import { InitialSetup, CreateEntry, ImportVault, GetEntries } from '../wailsjs/go/main/App';
import { EventsOn } from '../wailsjs/runtime/runtime';

const vaultItems = document.querySelector(".vault-items");

function renderEntries(entries) {
    vaultItems.innerHTML = "";

    entries.forEach((entry) => {
        const item = document.createElement("li");
        item.textContent = `${entry.Username} (${entry.Email})`;
        vaultItems.appendChild(item);
    });
}

async function loadEntries() {
    const entries = await GetEntries();
    renderEntries(entries);
}

async function chooseView() {
    const viewLogin = document.querySelector(".view-login");
    const viewVault = document.querySelector(".view-vault");
    const viewSignup = document.querySelector(".view-signup");

    // TODO: handle logic for view
    await InitialSetup();
    viewVault.style.display = "block";
    await loadEntries();

    EventsOn("vault:changed", async () => {
        await loadEntries();
    });
}

const createEntryBtn = document.querySelector("#create-entry");
createEntryBtn.addEventListener("click", async () => {
    await CreateEntry();
    await loadEntries();
});

const importVaultBtn = document.querySelector("#import-vault");
importVaultBtn.addEventListener("click", async () => {
    await ImportVault();
    await loadEntries();
});

document.addEventListener("DOMContentLoaded", chooseView);
