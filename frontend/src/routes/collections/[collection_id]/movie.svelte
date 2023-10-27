<script>
    import { Badge, Image, Tooltip, Group, CloseButton, Checkbox, Menu } from '@svelteuidev/core'
    import { createEventDispatcher } from 'svelte';
    import { IMAGE_BASE, addMovie, removeTag, removeMovie } from '$lib/index.js';
    import { Bookmark, Trash } from 'radix-icons-svelte';

    const dispatch = createEventDispatcher();

    export let title = "";
    export let release_date = "";
    export let poster_path = "";
    export let tags = [];

    export let tmdb_id = "";
    export let id = "";
    export let popularity = "";
    export let overview = "";
    export let collection = "";

    export let canAddFilm = false;
    export let canAddTags = false;
    export let canEditTags = false;
    export let highlightedTags = [];
    export let collectionId = null;

    let posterHovered = false;

    const cursorOverride = {
        cursor: 'pointer'
    };

    const menuOverride = {
        backgroundColor: 'white',
        borderRadius: '10%'
    }

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
            overview: overview,
            collection: collectionId
        }
        await addMovie(filmData);
    }

    function addTagClicked() {
        dispatch('add-tags', {
            id: id,
            tmdb_id: tmdb_id,
            title: title,
        });
    }

    function tagBadgeClicked(event) {
        if(event.target.nodeName === "svg") {
            return;
        }
        const tag = event.target.innerText.toLowerCase();
        dispatch('tag-clicked', {
            name: tag,
        });
    }

    function handleTagDeleteClicked(tagId) {
        removeTag(tagId);
        dispatch('tag-removed');
    }

    function handleMovieDeleteClicked() {
        removeMovie(id);
        dispatch('movie-removed');
    }

    function tagIsHighlighted(tagName) {
        return highlightedTags.includes(tagName.toLowerCase());
    }

    function handleSelected() {
        dispatch('film-selected', {
            id: id,
            tmdb_id: tmdb_id,
            collection: collection,
        });
    }

    function handleMouseOver(toggleValue) {
        posterHovered = toggleValue;
    }
</script>
<div>
    <Group position='center' spacing="xs">
        <Tooltip label={`${title} (${release_year})`}>
            <div role="tooltip" class="image-container mb-4 mr-2"
                on:mouseenter={() => handleMouseOver(true)}
                on:mouseleave={() => handleMouseOver(false)}
            >
                <Image
                    src={IMAGE_BASE + poster_path}
                    width={150}
                    height={225}
                    radius={10}
                    alt='Movie Poster'
                    class="mr-0 pr-0 mb-4"
                />
                {#if canAddTags && !canAddFilm}
                    <div class="overlay-menu">
                        <Menu override={menuOverride}>
                            <Menu.Label>{title}</Menu.Label>
                            <Menu.Item on:click={addTagClicked} icon={Bookmark}>Add Tag</Menu.Item>
                            <Menu.Item on:click={handleMovieDeleteClicked} color="red" icon={Trash}>Remove movie</Menu.Item>
                        </Menu>
                    </div>
                {/if}
                {#if canAddFilm }
                    <button on:click={addMovieClicked} class="overlay-button">+</button>
                {/if}
                {#if canEditTags}
                    <div class="overlay-checkbox">
                        <Checkbox on:click={handleSelected} size="sm" radius="lg" />
                    </div>
                {/if}
            </div>

        </Tooltip>
        <Group class="ml-0 pl-0 mb-2" spacing='xs' direction='column'>
            {#each tags as tag}
                <Badge on:click={tagBadgeClicked} size='sm' radius='sm' variant={tagIsHighlighted(tag.name) ? "filled" : "light"} override={cursorOverride}>
                    {tag.name}
                    <svelte:fragment slot='rightSection'>
                        {#if canEditTags}
                            <CloseButton on:click={() => handleTagDeleteClicked(tag.id)} size='xs' iconSize='xs' color={tagIsHighlighted(tag.name) ? "white" : "blue"} variant='transparent' />
                        {/if}
                    </svelte:fragment>
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

    .overlay-checkbox {
        position: absolute;
        top: 3%;
        left: 5%;
        z-index: 2;
    }

    .overlay-menu {
        position: absolute;
        top: 85%;
        left: 75%;
        z-index: 2;
        padding-left: 5px;
        padding-right: 5px;
    }

</style>