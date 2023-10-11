// place files you want to import through the `$lib` alias in this folder.
export const BASE_URL = "http://127.0.0.1:8000"
export const IMAGE_BASE = "http://image.tmdb.org/t/p/w300"

export async function getAllMovies(fetchMethod=fetch) {
    const res = await fetchMethod(BASE_URL + "/api/movies/");
    const data = await res.json()
    return data;
}

export async function getAllTags(fetchMethod=fetch) {
    const res = await fetchMethod(BASE_URL + "/api/tags/")
    if(res.ok) {
        return await res.json();
    }
    else {
        throw Error("Error getting tags");
    }
}

export async function searchMovies(query) {
    const res = await fetch(BASE_URL + "/api/search/?q=" + query)
    if(res.ok) {
        return await res.json();
    }
    else {
        throw Error("Error searching with query: " + query);
    }
}

export async function addMovie(filmData) {
    const res = await fetch(BASE_URL + "/api/movies/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(filmData),
    });

    if(res.ok) {
        return await res.json();
    }
    else {
        throw Error("Error adding film");
    }
}

export async function addTag(tagData) {
    const res = await fetch(BASE_URL + "/api/tags/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(tagData),
    });

    if(res.ok) {
        return await res.json();
    }
    else {
        throw Error("Error adding tag");
    }
}

export async function removeTag(tagId) {
    const res = await fetch(`${BASE_URL}/api/tags/${tagId}/`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
    });

    if(res.ok) {
        return;
    }
    else {
        throw Error("Error removing tag");
    }
}

export async function addBulkTag(filmIds, tagName) {
    let postData = [];
    filmIds.forEach(id => {
        const data = {
            movie: id,
            name: tagName
        };
        postData.push(data);
    });

    const res = await fetch(BASE_URL + "/api/tags/bulk/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(postData),
    });

    if(res.ok) {
        return await res.json();
    }
    else {
        throw Error("Error adding tag");
    }
}