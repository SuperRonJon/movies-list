<script>
    import { Badge, Image, Tooltip, Group } from '@svelteuidev/core'
    import { IMAGE_BASE } from '$lib/index.js'

    export let title = "";
    export let release_date = "";
    export let poster_path = "";
    export let tags = [];

    export let tmdb_id = "";
    export let id = "";
    export let popularity = "";
    export let overview = "";

    $: release_year = release_date.split("-")[0];

    tags.sort((a, b) => {
        if(a.name < b.name) {
            return -1;
        }
        else {
            return 1;
        }
    });
</script>
<div>
    <Group position='apart'>
        <Tooltip label={`${title} (${release_year})`}>
            <Image
                src={IMAGE_BASE + poster_path}
                width={150}
                height={225}
                alt='Movie Poster'
                class='center'
            />
        </Tooltip>
        <Group spacing='xs' direction='column'>
            {#each tags as tag}
                <Badge size='sm' radius='sm'>
                    {tag.name}
                </Badge>
            {/each}
        </Group>
    </Group>
    
</div>