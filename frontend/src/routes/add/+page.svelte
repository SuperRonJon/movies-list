<script>
    import { TextInput } from "@svelteuidev/core";
    import { searchMovies } from '$lib/index.js';
    import Movie from "../movie.svelte";

    let inputValue = "";
    let movies = [];

    async function handleEnter(keyupEvent) {
        if(keyupEvent.key === "Enter") {
            movies = await searchMovies(inputValue);
        }
    }
</script>

<a class="text-blue-600 dark:text-blue-500 hover:underline pt-2 float-left ml-4" href="/">Back to Collection</a>
<h1 class="text-4xl font-extrabold text-center mb-4">Add To Collection</h1>
<div class="w-1/3 mx-auto mb-10">
    <TextInput on:keyup={( event ) => handleEnter(event)} bind:value={inputValue} placeholder="Enter a film title..." />
</div>

<div class='flex flex-wrap w-10/12 mx-auto'>
{#each movies as movie}
        <Movie {...movie} canAddFilm />
{/each}
</div>