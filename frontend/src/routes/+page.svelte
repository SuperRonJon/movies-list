<script>
    import Movie from "./movie.svelte";
    import { addTag, addBulkTag } from '$lib/index.js';
    import { TextInput, Badge, CloseButton, Switch } from "@svelteuidev/core";
    import { invalidateAll } from '$app/navigation';

    export let data;
    let filteredMovies = [];
    let inputValue = "";
    let showInput = false;
    let filmTagId = "";
    let filmTagName = "";
    let currentTags = [];
    let canEditTags = false;
    let selectedFilms = [];
    let showUntagged = false;

    $: inputPlaceholder = determineInputPlaceholder(filmTagName, selectedFilms);
    $: filteredMovies = filterMovies(data.movies, currentTags, showUntagged);
    $: filteredTags = data.tags.sort((a, b) => {
        if(a.name < b.name) {
            return -1;
        }
        else {
            return 1;
        }
    });

    function determineInputPlaceholder(filmName, selected) {
        if(selected.length > 0) {
            return "Enter tag for selections...";
        }

        return filmName === "" ? "Enter tag..." : `Enter tag for ${filmName}`;
    }

    function getTagsForId(id){
        return filteredTags.filter((tag) => tag.movie == id)
    }

    async function handleEnter(keyupEvent) {
        if(keyupEvent.key === "Enter" && inputValue !== "" && selectedFilms.length > 0) {
            await addBulkTag(selectedFilms, inputValue);
            inputValue = "";
            invalidateAll();
            return;
        }
        if(keyupEvent.key === "Enter" && inputValue !== "" && filmTagId !== "") {
            const tagData = {
                movie: filmTagId,
                name: inputValue
            }
            await addTag(tagData);
            inputValue = "";
            invalidateAll();
           return;
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
            removeTagFromFilter(tagName);
            return;
        }
        currentTags = [...currentTags, tagName];
    }

    function removeTagFromFilter(tag) {
        currentTags = currentTags.filter(t => t !== tag);
    }

    function resetTagFilter() {
        currentTags = [];
    }

    function filterMovies(movies, tags, showUntagged) {
        let filtered = movies.filter((movie) => {
            if(showUntagged) {
                const movieTags = getTagsForId(movie.tmdb_id);
                return movieTags.length === 0;
            }
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

    function filmSelected(event) {
        const id = event.detail.tmdb_id;
        if(selectedFilms.includes(id)) {
            selectedFilms.splice(selectedFilms.indexOf(id), 1);
            selectedFilms = selectedFilms;
        }
        else {
            selectedFilms = [...selectedFilms, id];
        }

        if(showInput && selectedFilms.length === 0) {
            showInput = false;
        }
        if(!showInput && selectedFilms.length > 0) {
            showInput = true;
        }
        
    }

    function toggleEditTags() {
        canEditTags = !canEditTags;
        if(!canEditTags) {
            selectedFilms = [];
        }
    }
</script>

<Switch class="ml-4 mt-2 float-left" on:change={toggleEditTags} label="Edit tags" />
<Badge class="float-left ml-4 mt-2" on:click={() => showUntagged = !showUntagged} variant={showUntagged ? 'filled' : 'light'}>Untagged</Badge>
<a class="text-blue-600 dark:text-blue-500 hover:underline mt-2 float-right mr-4" href="/add">Add Page</a>
<h1 class='text-3xl font-bold mb-5 text-center'>Movies</h1>

{#if showInput}
    <div class="w-1/3 mx-auto mb-10">
        <TextInput on:keyup={( event ) => handleEnter(event)} bind:value={inputValue} placeholder={inputPlaceholder} />
    </div>
{/if}

{#if currentTags.length > 0}
    <div class="ml-12 mb-4 flex">
        {#each currentTags as tag, index}
            <Badge class='mr-2' size='lg' radius='lg' variant='filled' >
                {tag}
                <svelte:fragment slot='leftSection'>
                    <CloseButton on:click={() => removeTagFromFilter(currentTags[index])} size='xs' iconsize='xs' color='white' variant='transparent' />
                </svelte:fragment>
            </Badge>
        {/each}
    </div>
{/if}

<div class='flex flex-wrap w-10/12 mx-auto'>
{#each filteredMovies as movie}
    <div class="basis-1/6">
        <Movie
            {...movie} 
            tags={getTagsForId(movie.tmdb_id)} 
            highlightedTags={currentTags} 
            canAddTags
            {canEditTags}
            on:add-tags={handleAddTags} 
            on:tag-clicked={handleTagClicked} 
            on:tag-removed={invalidateAll}
            on:film-selected={filmSelected}
        />
    </div>
{/each}
</div>

