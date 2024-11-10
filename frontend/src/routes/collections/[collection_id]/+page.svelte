<script>
  import Movie from "./movie.svelte";
  import { BASE_URL } from "$lib/index.js";
  import { addTag, addBulkTag } from "$lib/api/tags.js";
  import {
    TextInput,
    Badge,
    CloseButton,
    Switch,
    Button,
  } from "@svelteuidev/core";
  import { invalidate } from "$app/navigation";
  import { Update } from "radix-icons-svelte";

  export let data;
  let filteredMovies = []; // Films that pass the currently selected filters
  let filteredTags = []; // All tags returned for this collection
  let excludeTags = []; // Currently selected tags that are inversed--being filtered OUT
  let currentTags = []; // All currently selected tags
  let selectedFilms = []; // IDs of all films currently selected by their checkboxes
  let selectedFilmNames = []; // Titles of all films currently selected by their checkboxes
  let showInput = false; // Whether or not the input box to add a new tag is shown
  let showUntagged = false; // Flag to have filterMovies() only show movies with no tags
  let canEditTags = false; // Whether or not edit mode is active. Use toggleEditTags() to change
  let inputValue = ""; // String currently typed into the input box
  let filmTagId = ""; // ID of the film most recently selected for adding tags to (not via edit mode)
  let filmTagName = ""; // Title of the film most recently selected for adding tags to (not via edit mode)

  const collectionTagsUrl = `${BASE_URL}/api/collections/${data.collectionId}/tags/`;
  const collectionMoviesUrl = `${BASE_URL}/api/collections/${data.collectionId}/movies/`;

  $: selectedFilmNames = selectedFilms.map(
    (id) => data.movies.filter((movie) => movie.id === id)[0].title
  );
  $: filmTagName = getFilmTagName(filmTagId, data.movies);
  $: inputPlaceholder = determineInputPlaceholder(filmTagName, selectedFilms);
  $: filteredMovies = filterMovies(
    data.movies,
    filteredTags,
    currentTags,
    excludeTags,
    showUntagged,
    selectedFilms
  );
  $: filteredTags = data.tags.sort((a, b) => {
    if (a.name.toLowerCase() < b.name.toLowerCase()) {
      return -1;
    } else {
      return 1;
    }
  });

  function determineInputPlaceholder(filmName, selectedFilms = []) {
    if (selectedFilms.length > 0) {
      return `Enter tag for ${selectedFilmNames.join(", ")}...`;
    }

    return filmName === "" ? "Enter tag..." : `Enter tag for ${filmName}`;
  }

  function getFilmTagName(filmTagId, movies) {
    if (filmTagId === "") {
      return "";
    }
    const film = movies.filter((movie) => movie.id === filmTagId)[0];
    return film.title;
  }

  function getTagsForId(allTags, id) {
    return allTags.filter((tag) => tag.movie == id);
  }

  async function handleEnter(keyupEvent) {
    if (
      keyupEvent.key === "Enter" &&
      inputValue !== "" &&
      selectedFilms.length > 0
    ) {
      await addBulkTag(selectedFilms, inputValue, data.collectionId);
      inputValue = "";
      invalidate(collectionTagsUrl);
      return;
    }
    if (keyupEvent.key === "Enter" && inputValue !== "" && filmTagId !== "") {
      const tagData = {
        movie: filmTagId,
        name: inputValue,
        collection: data.collectionId,
      };
      await addTag(tagData);
      inputValue = "";
      invalidate(collectionTagsUrl);
      return;
    }
  }

  function handleAddTags(event) {
    if (showInput && event.detail.id === filmTagId) {
      showInput = false;
      filmTagId = "";
      return;
    }
    filmTagId = event.detail.id;
    if (!showInput) {
      showInput = true;
    }
  }

  function movieContainsTags(movieId, tags, negativeTags) {
    const movieTags = getTagsForId(filteredTags, movieId).map((tag) =>
      tag.name.toLowerCase()
    );
    for (let i = 0; i < tags.length; i++) {
      const tag = tags[i];
      if (negativeTags.includes(tag) && movieTags.includes(tag)) {
        return false;
      }
      if (!movieTags.includes(tag) && !negativeTags.includes(tag)) {
        return false;
      }
    }
    return true;
  }

  function handleTagClicked(event) {
    const tagName = event.detail.name.toLowerCase();
    if (currentTags.includes(tagName)) {
      removeTagFromFilter(tagName);
      return;
    }
    currentTags = [...currentTags, tagName];
  }

  function removeTagFromFilter(tag) {
    currentTags = currentTags.filter((t) => t !== tag);
    excludeTags = excludeTags.filter((t) => t !== tag);
  }

  function filterMovies(
    movies,
    allTags,
    tagFilters,
    negativeFilters,
    showUntagged,
    currentlySelectedIds
  ) {
    let filtered = movies.filter((movie) => {
      // if movie is currently selected is is always returned regardless
      if (
        currentlySelectedIds.includes(movie.id) ||
        (filmTagId !== "" && filmTagId === movie.id)
      ) {
        return true;
      }
      if (showUntagged) {
        // Only return movies with no tags
        const movieTags = getTagsForId(allTags, movie.id);
        return movieTags.length === 0;
      }
      if (tagFilters.length === 0) {
        // If no currently active filters, returns every movie
        return true;
      }
      // Otherwise return a movie if it fits the currently active filters
      return movieContainsTags(movie.id, tagFilters, negativeFilters);
    });

    filtered.sort((a, b) => {
      if (a.title < b.title) {
        return -1;
      } else {
        return 1;
      }
    });
    return filtered;
  }

  function filmSelected(event) {
    const id = event.detail.id;
    if (selectedFilms.includes(id)) {
      selectedFilms.splice(selectedFilms.indexOf(id), 1);
      selectedFilms = selectedFilms;
    } else {
      selectedFilms = [...selectedFilms, id];
    }

    if (showInput && selectedFilms.length === 0 && filmTagId === "") {
      showInput = false;
    }
    if (!showInput && selectedFilms.length > 0) {
      showInput = true;
    }
  }

  function toggleEditTags() {
    canEditTags = !canEditTags;
    if (!canEditTags) {
      showInput = filmTagId === "" ? false : showInput;
      selectedFilms = [];
    }
  }

  function toggleNegativeTag(tag) {
    if (excludeTags.includes(tag)) {
      excludeTags = excludeTags.filter((t) => t !== tag);
    } else {
      excludeTags = [...excludeTags, tag];
    }
  }
</script>

<svelte:head>
  {#if data.collectionName}
    <title>{data.collectionName}</title>
  {:else}
    <title>Movie Collection</title>
  {/if}
</svelte:head>

<!-- TOP BAR/MENU -->

<Switch
  class="ml-4 mt-2 float-left"
  on:change={toggleEditTags}
  label="Edit mode"
/>
<Badge
  class="float-left ml-4 mt-2"
  on:click={() => (showUntagged = !showUntagged)}
  variant={showUntagged ? "filled" : "light"}>Untagged</Badge
>
<a
  class="text-blue-600 dark:text-blue-500 hover:underline mt-2 float-right mr-4"
  href={`/collections/${data.collectionId}/add`}>Add Page</a
>
<p class="float-right mt-2 mr-4">Number shown: {filteredMovies.length}</p>
<h1 class="text-3xl font-bold mb-5 text-center">{data.collectionName}</h1>

{#if showInput}
  <div class="w-1/3 mx-auto mb-10">
    <TextInput
      on:keyup={(event) => handleEnter(event)}
      bind:value={inputValue}
      placeholder={inputPlaceholder}
    />
  </div>
{/if}

<!-- FILTER MANAGEMENT -->

<div class="w-11/12 mx-auto pl-7 mb-4 flex">
  {#each currentTags as tag, index}
    <Badge
      class="mr-2"
      size="lg"
      radius="lg"
      variant="filled"
      color={excludeTags.includes(currentTags[index]) ? "red" : "blue"}
    >
      {tag}
      <svelte:fragment slot="leftSection">
        <CloseButton
          on:click={() => removeTagFromFilter(currentTags[index])}
          size="xs"
          iconsize="xs"
          color="white"
          variant="transparent"
        />
      </svelte:fragment>

      <svelte:fragment slot="rightSection">
        <Button
          on:click={() => toggleNegativeTag(currentTags[index])}
          compact
          color={excludeTags.includes(currentTags[index]) ? "red" : "blue"}
        >
          <Update />
        </Button>
      </svelte:fragment>
    </Badge>
  {/each}
</div>

<!-- MOVIES -->

<div class="flex flex-wrap mx-auto w-11/12">
  {#each filteredMovies as movie}
    <div class="basis-1/6">
      <Movie
        {...movie}
        tags={getTagsForId(filteredTags, movie.id)}
        highlightedTags={currentTags}
        canAddTags={canEditTags}
        collectionId={data.collectionId}
        {canEditTags}
        on:add-tags={handleAddTags}
        on:tag-clicked={handleTagClicked}
        on:tag-removed={() => invalidate(collectionTagsUrl)}
        on:movie-removed={() => invalidate(collectionMoviesUrl)}
        on:film-selected={filmSelected}
      />
    </div>
  {/each}
</div>
