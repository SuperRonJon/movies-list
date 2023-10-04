<script>
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

<h1>Movies</h1>

{#each data.movies as movie}
<h4>{movie.title} ({getYear(movie.release_date)})</h4>
<ul>
    {#each getTagsForId(movie.tmdb_id) as tag}
        <li>{tag.name}</li>
    {/each}
</ul>
{/each}

