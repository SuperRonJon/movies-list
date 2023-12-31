import {
  getMoviesFromCollection,
  getTagsFromCollection,
  getAllCollections,
} from "$lib/api/collections.js";

async function getCollectionName(id, fetchMethod = fetch) {
  const collections = await getAllCollections(fetchMethod);
  const filteredCollections = collections.filter(
    (collection) => collection.id === id
  );
  if (filteredCollections.length === 0) {
    return null;
  }
  return collections.filter((collection) => collection.id === id)[0].name;
}

export async function load({ fetch, params }) {
  let collectionId = parseInt(params.collection_id);
  return {
    movies: await getMoviesFromCollection(collectionId, fetch),
    tags: await getTagsFromCollection(collectionId, fetch),
    collectionId: collectionId,
    collectionName: await getCollectionName(collectionId, fetch),
  };
}
