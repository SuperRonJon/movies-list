<script>
    import { TextInput, Button } from "@svelteuidev/core";
    import { searchMovies } from '$lib/index.js';
    import Movie from "../movie.svelte";

    let inputValue = "";
    let movies = [];

    async function handleEnter(keyupEvent) {
        if(keyupEvent.key === "Enter") {
            console.log("searching", inputValue);
            movies = await searchMovies(inputValue);
            console.log("found movies", movies);
        }
    }
</script>

<a class="text-blue-600 dark:text-blue-500 hover:underline pt-2 float-left ml-4" href="/">Back to Collection</a>
<h1 class="text-4xl font-extrabold text-center mb-4">Add Page</h1>
<div class="w-1/3 mx-auto mb-10">
    <TextInput on:keyup={( event ) => handleEnter(event)} bind:value={inputValue} placeholder="Enter a film title..." />
</div>

<div class='results-container'>
{#each movies as movie}
    <Movie {...movie} canAdd={true} />
{/each}
</div>

<style>
    .results-container {
        display: flex;
        justify-content: space-evenly;
        flex-wrap: wrap;
    }
</style>