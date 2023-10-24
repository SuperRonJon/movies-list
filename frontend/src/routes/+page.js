import { getAllCollections } from "../lib";

export async function load({ fetch }) {
    return {
        collections: await getAllCollections(fetch)
    }
}