import { getAllMovies, getAllTags } from '$lib/index.js'

export async function load({ params }) {
    return {
        movies: await getAllMovies(),
        tags: await getAllTags(),
    }
}