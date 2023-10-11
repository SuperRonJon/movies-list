import { getAllMovies, getAllTags } from '$lib/index.js'

export async function load({ fetch }) {
    return {
        movies: await getAllMovies(fetch),
        tags: await getAllTags(fetch),
    }
}