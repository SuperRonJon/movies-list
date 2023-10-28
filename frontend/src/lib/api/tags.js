import { BASE_URL } from "$lib/index.js";

export async function addTag(tagData) {
  const res = await fetch(BASE_URL + "/api/tags/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(tagData),
  });

  if (res.ok) {
    return await res.json();
  } else {
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

  if (res.ok) {
    return;
  } else {
    throw Error("Error removing tag");
  }
}

export async function addBulkTag(filmIds, tagName, collectionId) {
  let postData = [];
  filmIds.forEach((id) => {
    const data = {
      movie: id,
      name: tagName,
      collection: collectionId,
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

  if (res.ok) {
    return await res.json();
  } else {
    throw Error("Error adding tag");
  }
}
