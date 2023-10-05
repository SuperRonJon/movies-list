// place files you want to import through the `$lib` alias in this folder.
const BASE_URL = "http://127.0.0.1:8000"
export const IMAGE_BASE = "http://image.tmdb.org/t/p/w300"

export async function getAllMovies() {
    const res = await fetch(BASE_URL + "/api/movies/");
    const data = await res.json()
    return data;
}

export async function getAllTags() {
    const res = await fetch(BASE_URL + "/api/tags/")
    if(res.ok) {
        return await res.json();
    }
    else {
        throw Error("Error getting tags");
    }
}