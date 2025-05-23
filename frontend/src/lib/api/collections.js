import { BASE_URL } from "$lib/index.js";

export async function getMoviesFromCollection(
  collectionId,
  fetchMethod = fetch
) {
  console.log("PUBLIC_BASE_URL", BASE_URL);
  const res = await fetchMethod(
    `${BASE_URL}/api/collections/${collectionId}/movies/`
  );
  if (res.ok) {
    return await res.json();
  } else {
    throw Error("Error getting movies");
  }
}

export async function getTagsFromCollection(collectionId, fetchMethod = fetch) {
  const res = await fetchMethod(
    `${BASE_URL}/api/collections/${collectionId}/tags/`
  );
  if (res.ok) {
    return await res.json();
  } else {
    throw Error("Error getting tags");
  }
}

export async function getAllCollections(fetchMethod = fetch) {
  console.log("PUBLIC_BASE_URL", BASE_URL);
  const res = await fetchMethod(`${BASE_URL}/api/collections/`);
  return await res.json();
}

export async function addCollection(collectionData) {
  const res = await fetch(`${BASE_URL}/api/collections/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(collectionData),
  });

  if (res.ok) {
    return await res.json();
  } else {
    throw Error("Error adding collection");
  }
}
