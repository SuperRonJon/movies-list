import { BASE_URL } from "$lib/index.js";

export async function getAllMovies(fetchMethod = fetch) {
  const res = await fetchMethod(BASE_URL + "/api/movies/");
  const data = await res.json();
  return data;
}

export async function searchMovies(query) {
  const res = await fetch(BASE_URL + "/api/search/?q=" + query);
  if (res.ok) {
    return await res.json();
  } else {
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

  if (res.ok) {
    return await res.json();
  } else {
    throw Error("Error adding film");
  }
}

export async function updateMovie(filmData) {
  const res = await fetch(`${BASE_URL}/api/movies/${filmData.id}/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(filmData),
  });

  if (res.ok) {
    return await res.json();
  } else {
    throw Error("Error updating film");
  }
}

export async function getTmdbInfo(tmdbId) {
  const res = await fetch(`${BASE_URL}/api/info/${tmdbId}/`);
  if (res.ok) {
    return await res.json();
  } else {
    throw Error("Error getting tmdb info");
  }
}

export async function removeMovie(movieId) {
  const res = await fetch(`${BASE_URL}/api/movies/${movieId}/`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (res.ok) {
    return;
  } else {
    throw Error("Error removing movie");
  }
}
