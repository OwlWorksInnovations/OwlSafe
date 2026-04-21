<script lang="ts">
    import {
        Initialize,
        CreateUser,
        AddEntry,
    } from "../wailsjs/go/main/App.js";
    import { onMount } from "svelte";

    onMount(() => {
        Initialize();
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
            } else if (source) {
                AddEntry(username, password, source);
            }
        } else {
            alert("ERROR");
        }
    }
</script>

<main>
    <div class="header">
        <h1>OwlSafe</h1>
        <h2>Made by Myzerfist</h2>
    </div>
    <div class="vault">
        <ul class="vault-items">
            <li class="vault-item">Item one example</li>
        </ul>

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
            <button class="remove-entry">Remove Entry</button>
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
