export async function load({ params }) {
    return {
        collectionId: parseInt(params.collection_id)
    }
}