<script>
    import { Badge, Image, Tooltip, Group } from '@svelteuidev/core'
    import { IMAGE_BASE } from '$lib/index.js'

    export let title = "";
    export let tmdb_id = "";
    export let release_date = "";
    export let poster_path = "";
    export let tags = [];

    $: release_year = release_date.split("-")[0];
    console.log(`${title} tags`, tags);
</script>
<div>
    <Group position='apart'>
        <Tooltip label={title}>
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
<!--
<h4 class="mb-0">{title} ({release_year})</h4>

<ul class="mt-0">
    {#each tags as tag}
        <li>{tag.name}</li>
    {/each}
</ul>
-->

<style>
    .mb-0 {
        margin-bottom: 0;
    }

    .mt-0 {
        margin-top: 0;
    }

    .center {
        margin: 0 auto;
    }
</style>