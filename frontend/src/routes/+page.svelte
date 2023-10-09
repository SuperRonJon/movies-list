<script>
    import Movie from "./movie.svelte";
    import { addTag } from '$lib/index.js';
    import { TextInput } from "@svelteuidev/core";
    import { invalidateAll } from '$app/navigation';

    export let data;
    let filteredMovies = [];
    let inputValue = "";
    let showInput = false;
    let filmTagId = "";
    let filmTagName = "";
    let currentTag = null;

    $: inputPlaceholder = filmTagName === "" ? "Enter tag..." : "Enter tag for " + filmTagName;

    function getYear(date) {
        return parseInt(date.split("-")[0])
    }

    function getTagsForId(id){
        return filteredTags.filter((tag) => tag.movie == id)
    }

    function sortDataAlphabet() {
        data.movies.sort((a, b) => {
            if(a.title < b.title) {
                return -1;
            }
            else {
                return 1;
            }
        })
    }

    function sortDataYear() {
        data.movies.sort((a, b) => {
            if(getYear(a.release_date) > getYear(b.release_date)) {
                return -1;
            }
            else if(getYear(a.release_date) === getYear(b.release_date)) {
                if(a.title < b.title) {
                    return -1;
                }
                else {
                    return 1;
                }
            }
            else {
                return 1;
            }
        });
    }

    async function handleEnter(keyupEvent) {
        if(keyupEvent.key === "Enter" && inputValue !== "" && filmTagId !== "") {
            const tagData = {
                movie: filmTagId,
                name: inputValue
            }
            await addTag(tagData);
            inputValue = "";
            invalidateAll();
        }
    }

    function handleAddTags(event) {
        if(showInput && event.detail.tmdb_id === filmTagId) {
            showInput = false;
            filmTagId = "";
            filmTagName = "";
            return;
        }
        filmTagId = event.detail.tmdb_id;
        filmTagName = event.detail.title;
        if(!showInput) {
            showInput = true;
        }
        
    }

    function movieContainsTag(movieId, tag) {
        const tags = getTagsForId(movieId).map((tag) => tag.name.toLowerCase());
        const contains = tags.includes(tag.toLowerCase())
        return tags.includes(tag.toLowerCase())
    }

    function handleTagClicked(event) {
        const tagName = event.detail.name;
        currentTag = tagName;
    }

    function resetTagFilter() {
        currentTag = null;
    }

    function filterMovies(movies, currentTag) {
        let filtered = movies.filter((movie) => {
            if(currentTag === null) {
                return true;
            }
            return movieContainsTag(movie.tmdb_id, currentTag);
        });

        console.log("filtered", filtered);

        filtered.sort((a, b) => {
            if(a.title < b.title) {
                return -1;
            }
            else {
                return 1;
            }
        });
        return filtered;
    }

    $: filteredMovies = filterMovies(data.movies, currentTag)
    $: filteredTags = data.tags.sort((a, b) => {
        if(a.name < b.name) {
            return -1;
        }
        else {
            return 1;
        }
    });
</script>

<a class="text-blue-600 dark:text-blue-500 hover:underline pt-2 float-right mr-4" href="/add">Add Page</a>
{#if currentTag !== null}
<button on:click={resetTagFilter} class="float-left mt-2 text-blue-600 dark:text-blue-500 hover:underline ml-4">Reset filter</button>
{/if}
<h1 class='text-3xl font-bold mb-5 text-center'>Movies</h1>

{#if showInput}
<div class="w-1/3 mx-auto mb-10">
    <TextInput on:keyup={( event ) => handleEnter(event)} bind:value={inputValue} placeholder={inputPlaceholder} />
</div>
{/if}

<div class='results-container'>
{#each filteredMovies as movie}
    <div class="basis-1/6">
        <Movie on:add-tags={handleAddTags} on:tag-clicked={handleTagClicked} {...movie} tags={getTagsForId(movie.tmdb_id)} canAddTags />
    </div>
{/each}
</div>

<style>
    .results-container {
        display: flex;
        justify-content: space-evenly;
        flex-wrap: wrap;
    }

</style>