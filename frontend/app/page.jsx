import Image from 'next/image'

export default async function Home() {
  const baseImage = "http://image.tmdb.org/t/p/w300";
  const baseAPI = "http://127.0.0.1:8000/api";

  async function getMovies() {
    const moviesUrl = `${baseAPI}/movies`;
    const res = await fetch(moviesUrl);
    return res.json();
  }

  async function getTags() {
    const tagsUrl = `${baseAPI}/tags`;
    const res = await fetch(tagsUrl);
    return res.json();
  }

  function getYear(date) {
    return date.split("-")[0];
  }

  function sortTags(movies, tags) {
    movies.forEach(movie => {
      movie.tags = [];
      movie.tags.push(...tags.filter(tag => tag.movie === movie.tmdb_id))
    });
  }

  function getTagItemsForMovie(movie) {
    return movie.tags.map(tag => (
      <li key={tag.id}>
        {tag.name}
      </li>
    ))
  }

  
  const movies = await getMovies();
  const tags = await getTags();
  sortTags(movies, tags);

  const movieItems = movies.map(movie => (
    <li key={movie.tmdb_id}>
      {movie.title} ({getYear(movie.release_date)})
      <ul>
        {getTagItemsForMovie(movie)}
      </ul>
    </li>
  ));
  

  return (
    <div>
      <h1>Hello world</h1>
      <ul>
        {movieItems}
      </ul>
    </div>
    
  )
}
