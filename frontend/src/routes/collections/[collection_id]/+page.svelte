<script>
    import Movie from "./movie.svelte";
    import { addTag, addBulkTag, BASE_URL } from '$lib/index.js';
    import { TextInput, Badge, CloseButton, Switch, Button } from "@svelteuidev/core";
    import { invalidate } from '$app/navigation';
    import { Update } from 'radix-icons-svelte';

    export let data;
    let filteredMovies = [];
    let filteredTags = [];
    let excludeTags = [];
    let currentTags = [];
    let selectedFilms = [];
    let showInput = false;
    let showUntagged = false;
    let canEditTags = false;
    let inputValue = "";
    let filmTagId = "";
    let filmTagName = "";

    $: selectedFilmNames = selectedFilms.map(id => data.movies.filter(movie => movie.id === id)[0].title);
    $: inputPlaceholder = determineInputPlaceholder(filmTagName, selectedFilms);
    $: filteredMovies = filterMovies(data.movies, filteredTags, currentTags, excludeTags, showUntagged);
    $: filteredTags = data.tags.sort((a, b) => {
        if(a.name.toLowerCase() < b.name.toLowerCase()) {
            return -1;
        }
        else {
            return 1;
        }
    });


    function determineInputPlaceholder(filmName, selectedFilms=[]) {
        if(selectedFilms.length > 0) {
            return `Enter tag for ${selectedFilmNames.join(", ")}...`;
        }

        return filmName === "" ? "Enter tag..." : `Enter tag for ${filmName}`;
    }

    function getTagsForId(allTags, id){
        return allTags.filter((tag) => tag.movie == id);
    }

    async function handleEnter(keyupEvent) {
        if(keyupEvent.key === "Enter" && inputValue !== "" && selectedFilms.length > 0) {
            await addBulkTag(selectedFilms, inputValue, data.collectionId);
            inputValue = "";
            invalidate(`${BASE_URL}/api/collections/${data.collectionId}/tags/`);
            return;
        }
        if(keyupEvent.key === "Enter" && inputValue !== "" && filmTagId !== "") {
            const tagData = {
                movie: filmTagId,
                name: inputValue,
                collection: data.collectionId
            }
            await addTag(tagData);
            inputValue = "";
            invalidate(`${BASE_URL}/api/collections/${data.collectionId}/tags/`);
           return;
        }
    }

    function handleAddTags(event) {
        if(showInput && event.detail.id === filmTagId) {
            showInput = false;
            filmTagId = "";
            filmTagName = "";
            return;
        }
        filmTagId = event.detail.id;
        filmTagName = event.detail.title;
        if(!showInput) {
            showInput = true;
        }
        
    }

    function movieContainsTags(movieId, tags, negativeTags) {
        const movieTags = getTagsForId(filteredTags, movieId).map((tag) => tag.name.toLowerCase());
        for(let i = 0; i < tags.length; i++) {
            const tag = tags[i];
            if(negativeTags.includes(tag) && movieTags.includes(tag)) {
                return false;
            }
            if(!movieTags.includes(tag) && !negativeTags.includes(tag)) {
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
        excludeTags = excludeTags.filter(t => t !== tag);
    }

    function resetTagFilter() {
        currentTags = [];
    }

    function filterMovies(movies, allTags, tagFilters, negativeFilters, showUntagged) {
        let filtered = movies.filter((movie) => {
            if(showUntagged) {
                const movieTags = getTagsForId(allTags, movie.id);
                return movieTags.length === 0;
            }
            if(tagFilters.length === 0) {
                return true;
            }
            return movieContainsTags(movie.id, tagFilters, negativeFilters);
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
        const id = event.detail.id;
        if(selectedFilms.includes(id)) {
            selectedFilms.splice(selectedFilms.indexOf(id), 1);
            selectedFilms = selectedFilms;
        }
        else {
            selectedFilms = [...selectedFilms, id];
        }

        if(showInput && selectedFilms.length === 0 && filmTagId === "") {
            showInput = false;
        }
        if(!showInput && selectedFilms.length > 0) {
            showInput = true;
        }
        
    }

    function toggleEditTags() {
        canEditTags = !canEditTags;
        if(!canEditTags) {
            showInput = filmTagId === "" ? false : showInput;
            selectedFilms = [];
        }
    }

    function toggleNegativeTag(tag) {
        if(excludeTags.includes(tag)) {
            excludeTags = excludeTags.filter(t => t !== tag);
        }
        else {
            excludeTags = [...excludeTags, tag];
        }
    }
</script>

<Switch class="ml-4 mt-2 float-left" on:change={toggleEditTags} label="Edit mode" />
<Badge class="float-left ml-4 mt-2" on:click={() => showUntagged = !showUntagged} variant={showUntagged ? 'filled' : 'light'}>Untagged</Badge>
<a class="text-blue-600 dark:text-blue-500 hover:underline mt-2 float-right mr-4" href={`/collections/${data.collectionId}/add`}>Add Page</a>
<p class="float-right mt-2 mr-4">Number shown: {filteredMovies.length}</p>
<h1 class='text-3xl font-bold mb-5 text-center'>{data.collectionName}</h1>

{#if showInput}
    <div class="w-1/3 mx-auto mb-10">
        <TextInput on:keyup={( event ) => handleEnter(event)} bind:value={inputValue} placeholder={inputPlaceholder} />
    </div>
{/if}

<div class="w-11/12 mx-auto pl-7 mb-4 flex">
    {#each currentTags as tag, index}
        <Badge class='mr-2' size='lg' radius='lg' variant='filled' color={excludeTags.includes(currentTags[index]) ? 'red' : 'blue'} >
            {tag}
            <svelte:fragment slot='leftSection'>
                <CloseButton on:click={() => removeTagFromFilter(currentTags[index])} size='xs' iconsize='xs' color='white' variant='transparent' />
            </svelte:fragment>
            
            <svelte:fragment slot='rightSection'>
                <Button on:click={() => toggleNegativeTag(currentTags[index])} compact color={excludeTags.includes(currentTags[index]) ? 'red' : 'blue'}>
                    <Update />
                </Button>
            </svelte:fragment>
        </Badge>
    {/each}
</div>

<div class='flex flex-wrap mx-auto w-11/12'>
{#each filteredMovies as movie}
    <div class="basis-1/6">
        <Movie
            {...movie} 
            tags={getTagsForId(filteredTags, movie.id)} 
            highlightedTags={currentTags} 
            canAddTags={canEditTags}
            collectionId={data.collectionId}
            {canEditTags}
            on:add-tags={handleAddTags} 
            on:tag-clicked={handleTagClicked} 
            on:tag-removed={() => invalidate(`${BASE_URL}/api/collections/${data.collectionId}/tags/`)}
            on:movie-removed={() => invalidate(`${BASE_URL}/api/collections/${data.collectionId}/movies/`)}
            on:film-selected={filmSelected}
        />
    </div>
{/each}
</div>

