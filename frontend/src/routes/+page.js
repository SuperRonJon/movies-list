import { getAllCollections } from "$lib/api/collections";

export async function load({ fetch }) {
  return {
    collections: await getAllCollections(fetch),
  };
}
