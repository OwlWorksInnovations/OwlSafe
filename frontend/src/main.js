import './style.css';
import './app.css';

import { InitialSetup, CreateEntry, ImportVault } from '../wailsjs/go/main/App';

function chooseView() {
    const viewLogin = document.querySelector(".view-login");
    const viewVault = document.querySelector(".view-vault");
    const viewSignup = document.querySelector(".view-signup");

    // TODO: handle logic for view
    InitialSetup();
    viewVault.style.display = "block";
}

const createEntryBtn = document.querySelector("#create-entry");
createEntryBtn.addEventListener("click", async () => {
    await CreateEntry();
})

const importVaultBtn = document.querySelector("#import-vault");
importVaultBtn.addEventListener("click", async () => {
    await ImportVault();
})

document.addEventListener("DOMContentLoaded", chooseView);
