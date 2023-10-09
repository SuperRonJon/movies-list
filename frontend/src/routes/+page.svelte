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
    let currentTags = [];

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

    function movieContainsTags(movieId, tags) {
        const movieTags = getTagsForId(movieId).map((tag) => tag.name.toLowerCase());
        for(let i = 0; i < tags.length; i++) {
            if(!movieTags.includes(tags[i])) {
                return false;
            }
        }
        
        return true;
    }

    function handleTagClicked(event) {
        const tagName = event.detail.name.toLowerCase();
        if(currentTags.includes(tagName)) {
            const index = currentTags.indexOf(tagName);
            if(index > -1) {
                currentTags.splice(index, 1);
                currentTags = currentTags;
            }
            return;
        }
        currentTags = [...currentTags, tagName];
    }

    function resetTagFilter() {
        currentTags = [];
    }

    function filterMovies(movies, tags) {
        let filtered = movies.filter((movie) => {
            if(tags.length === 0) {
                return true;
            }
            return movieContainsTags(movie.tmdb_id, tags);
        });

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

    $: filteredMovies = filterMovies(data.movies, currentTags)
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
{#if currentTags.length !== 0}
<button on:click={resetTagFilter} class="float-left mt-2 text-blue-600 dark:text-blue-500 hover:underline ml-4">Reset filter</button>
{/if}
<h1 class='text-3xl font-bold mb-5 text-center'>Movies</h1>

{#if showInput}
<div class="w-1/3 mx-auto mb-10">
    <TextInput on:keyup={( event ) => handleEnter(event)} bind:value={inputValue} placeholder={inputPlaceholder} />
</div>
{/if}

<div class='flex flex-wrap justify-around ml-2'>
{#each filteredMovies as movie}
    <div class="basis-1/6">
        <Movie on:add-tags={handleAddTags} on:tag-clicked={handleTagClicked} {...movie} tags={getTagsForId(movie.tmdb_id)} highlightedTags={currentTags} canAddTags />
    </div>
{/each}
</div>

