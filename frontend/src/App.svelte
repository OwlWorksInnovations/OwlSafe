<script lang="ts">
    import {
        Initialize,
        GetRows,
        RemoveRows,
        CreateUser,
        AddEntry,
    } from "../wailsjs/go/main/App.js";
    import { onMount } from "svelte";

    onMount(() => {
        Initialize();
        populateList();
    });

    async function addEntry() {
        const username = (
            document.querySelector(".username-input") as HTMLInputElement
        ).value;
        const password = (
            document.querySelector(".password-input") as HTMLInputElement
        ).value;
        const source = (
            document.querySelector(".source-input") as HTMLInputElement
        ).value;

        if (username && password) {
            if (!source) {
                AddEntry(username, password, "");
                populateList();
            } else if (source) {
                AddEntry(username, password, source);
                populateList();
            }
        } else {
            alert("ERROR");
        }
    }

    async function populateList() {
        const entryList = document.querySelector(".vault-items");

        // Clear old list
        const ul = document.querySelector("ul");
        ul.innerHTML = "";

        var entriesList = await GetRows("entries");

        entriesList.forEach((entry) => {
            const entryLI = document.createElement("li");
            entryLI.className = "vault-item";
            entryLI.dataset.id = entry.id;

            const entryLIUsername = document.createElement("p");
            entryLIUsername.innerText = entry.username;
            entryLIUsername.className = "vault-entry-username";
            const entryLIPassword = document.createElement("p");
            entryLIPassword.innerText = entry.password;
            entryLIPassword.className = "vault-entry-password";
            const entryLISource = document.createElement("p");
            entryLISource.innerText = entry.source;
            entryLISource.className = "vault-entry-source";

            entryLI.appendChild(entryLIUsername);
            entryLI.appendChild(entryLIPassword);
            entryLI.appendChild(entryLISource);
            entryList.appendChild(entryLI);
        });

        addSelectEvent();
    }

    // Will add in the future but as of now it isn't a priority
    async function updateList() {}

    let selected: HTMLElement | null = null;
    function addSelectEvent() {
        document.querySelectorAll(".vault-item").forEach((el) => {
            el.addEventListener("click", (e) => {
                selected = e.currentTarget as HTMLElement;
            });
        });
    }

    async function removeEntry() {
        if (!selected) return;
        const id = selected.dataset.id;
        await RemoveRows("entries", "id", id);
        await populateList();
        selected = null;
    }
</script>

<main>
    <div class="header">
        <h1>OwlSafe</h1>
        <h2>Made by Myzerfist</h2>
    </div>
    <div class="vault">
        <ul class="vault-items"></ul>

        <div class="vault-buttons">
            <div class="input-fields">
                <label for="username">Username: </label>
                <input type="text" class="username-input" />
                <label for="password">Password: </label>
                <input type="password" class="password-input" />
                <label for="source">Source: </label>
                <input type="text" class="source-input" />
            </div>
            <button class="add-entry" on:click={addEntry}>Add Entry</button>
            <button class="remove-entry" on:click={removeEntry}
                >Remove Entry</button
            >
        </div>
    </div>
</main>

<style>
    :root {
        --palette-dark: #252422;
        --palette-mid: #403d39;
        --palette-accent: #ccc5b9;
        --palette-accent-glow: rgba(204, 197, 185, 0.3);
        --palette-light: #fffcf2;
        --text-primary: #fffcf2;
        --text-secondary: #ccc5b9;
        --glass-bg: rgba(64, 61, 57, 0.7);
        --glass-border: rgba(255, 252, 242, 0.1);
        --transition-speed: 0.3s;
    }
</style>
