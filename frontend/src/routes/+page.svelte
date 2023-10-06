<script>
    import Movie from "./movie.svelte";

    export let data;

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