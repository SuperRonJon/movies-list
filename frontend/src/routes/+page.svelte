<script>
    import Movie from "./movie.svelte";

    export let data;

    function getYear(date) {
        return parseInt(date.split("-")[0])
    }

    function getTagsForId(id){
        return data.tags.filter((tag) => tag.movie == id)
    }

    function sortDataAlphabet() {
        data.movies.sort((a, b) => {
            if(a.title < b.title) {
                return -1;
            }
            else {
                return 1;
            }
        })
    }

    function sortDataYear() {
        data.movies.sort((a, b) => {
            if(getYear(a.release_date) > getYear(b.release_date)) {
                return -1;
            }
            else if(getYear(a.release_date) === getYear(b.release_date)) {
                if(a.title < b.title) {
                    return -1;
                }
                else {
                    return 1;
                }
            }
            else {
                return 1;
            }
        });
    }
    sortDataAlphabet();
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