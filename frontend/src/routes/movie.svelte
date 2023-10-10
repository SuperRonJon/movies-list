<script>
    import { Badge, Image, Tooltip, Group, Button } from '@svelteuidev/core'
    import { createEventDispatcher } from 'svelte';
    import { IMAGE_BASE, addMovie } from '$lib/index.js'

    const dispatch = createEventDispatcher();

    export let title = "";
    export let release_date = "";
    export let poster_path = "";
    export let tags = [];

    export let tmdb_id = "";
    export let id = "";
    export let popularity = "";
    export let overview = "";

    export let canAddFilm = false;
    export let canAddTags = false;
    export let highlightedTags = [];

    const cursorOverride = {
        cursor: 'pointer'
    };

    $: release_year = release_date.split("-")[0];

    tags.sort((a, b) => {
        if(a.name < b.name) {
            return -1;
        }
        else {
            return 1;
        }
    });

    async function addMovieClicked() {
        const filmData = {
            title: title,
            release_date: release_date,
            poster_path: poster_path,
            tmdb_id: tmdb_id,
            popularity: popularity,
            overview: overview

        }
        await addMovie(filmData);
    }

    function addTagClicked() {
        dispatch('add-tags', {
            tmdb_id: tmdb_id,
            title: title,
        });
    }

    function tagBadgeClicked(event) {
        const tag = event.target.innerText.toLowerCase();
        dispatch('tag-clicked', {
            name: tag,
        });
    }
</script>
<div>
    <Group position='center' spacing="xs">
        <Tooltip label={`${title} (${release_year})`}>
            <div class="image-container mb-4 mr-2">
                <Image
                    src={IMAGE_BASE + poster_path}
                    width={150}
                    height={225}
                    radius={10}
                    alt='Movie Poster'
                    class="mr-0 pr-0 mb-4"
                />
                {#if canAddTags}
                    <button on:click={addTagClicked} class="overlay-button">...</button>
                {/if}
                {#if canAddFilm }
                    <button on:click={addMovieClicked} class="overlay-button">+</button>
                {/if}
            </div>
            
        </Tooltip>
        <Group class="ml-0 pl-0" spacing='xs' direction='column'>
            {#each tags as tag}
                <Badge on:click={tagBadgeClicked} size='sm' radius='sm' variant={highlightedTags.includes(tag.name.toLowerCase()) ? "filled" : "light"} override={cursorOverride}>
                    {tag.name}
                </Badge>
            {/each}
        </Group>
    </Group>
    
</div>

<style>
    .image-container {
        position: relative;
        width: 150px;
        height: 225px;
    }

    .overlay-button {
        position: absolute;
        top: 85%;
        left: 80%;
        z-index: 2;
        color: white;
        background-color: rgba(100, 100, 100, 0.603);
        padding-left: 5px;
        padding-right: 5px;
    }

</style>