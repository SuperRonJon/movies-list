<script>
    import Movie from "./movie.svelte";

    export let data;
    console.log("movies", data.movies);
    console.log("tags", data.tags);

    function getYear(date) {
        return date.split("-")[0];
    }

    function getTagsForId(id){
        return data.tags.filter((tag) => tag.movie == id)
    }
</script>

<h1 class='center'>Movies</h1>

<div class='results-container'>
{#each data.movies as movie}
<Movie {...movie} tags={getTagsForId(movie.tmdb_id)} />
{/each}
</div>

<!--
{#each data.movies as movie}
<h4>{movie.title} ({getYear(movie.release_date)})</h4>
<ul>
    {#each getTagsForId(movie.tmdb_id) as tag}
        <li>{tag.name}</li>
    {/each}
</ul>
{/each}
-->

<style>
    .results-container {
        display: flex;
        justify-content: space-evenly;
        flex-wrap: wrap;
    }

    .center {
        text-align: center;
    }
</style>