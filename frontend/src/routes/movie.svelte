<script>
    import { Badge, Image, Tooltip, Group, Button } from '@svelteuidev/core'
    import { IMAGE_BASE, addMovie } from '$lib/index.js'

    export let title = "";
    export let release_date = "";
    export let poster_path = "";
    export let tags = [];

    export let tmdb_id = "";
    export let id = "";
    export let popularity = "";
    export let overview = "";

    export let canAdd = false;

    $: release_year = release_date.split("-")[0];

    tags.sort((a, b) => {
        if(a.name < b.name) {
            return -1;
        }
        else {
            return 1;
        }
    });

    async function addClicked() {
        const filmData = {
            title: title,
            release_date: release_date,
            poster_path: poster_path,
            tmdb_id: tmdb_id,
            popularity: popularity,
            overview: overview

        }
        console.log("Add film", filmData);
        await addMovie(filmData);
    }
</script>
<div>
    <Group position='center' spacing="xs">
        <Tooltip label={`${title} (${release_year})`}>
            <Image
                src={IMAGE_BASE + poster_path}
                width={150}
                height={225}
                radius={10}
                alt='Movie Poster'
                class="mr-0 pr-0 mb-4"
            />
        </Tooltip>
        <Group class="ml-0 pl-0" spacing='xs' direction='column'>
            {#each tags as tag}
                <Badge size='sm' radius='sm'>
                    {tag.name}
                </Badge>
            {/each}
            {#if canAdd }
                <Button on:click={addClicked}>Add</Button>
            {/if}
        </Group>
    </Group>
    
</div>