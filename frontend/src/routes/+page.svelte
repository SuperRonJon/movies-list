<script>
  import { TextInput, Button } from "@svelteuidev/core";
  import { addCollection, BASE_URL } from "$lib/index.js";
  import { invalidate } from "$app/navigation";

  export let data;

  let inputValue = "";

  async function handleKeyUp(event) {
    if (event.key === "Enter" && inputValue !== "") {
      const collectionData = {
        name: inputValue,
      };
      await addCollection(collectionData);
      inputValue = "";
      invalidate(`${BASE_URL}/api/collections/`);
      return;
    }
  }
</script>

<h1 class="text-3xl font-bold mb-5 text-center">Collections</h1>

<div class="w-1/3 mx-auto mb-10">
  <TextInput
    on:keyup={(event) => handleKeyUp(event)}
    bind:value={inputValue}
    placeholder="Enter name of new Collection then press Enter..."
  />
</div>

{#each data.collections as collection}
  <div class="text-center">
    <a
      class="text-blue-600 hover:underline text-center"
      href="/collections/{collection.id}">{collection.name}</a
    >
  </div>
{/each}
