const detailsContainer = document.getElementById("movie-details");
const movieId = detailsContainer.dataset.movieId;

async function loadMovieDetails(){
    try{
        const response = await fetch(`/movies/${movieId}`);
        const data = await response.json();

        if(!response.ok){
            throw new Error(
                data.message || "Failed to load movie details"
            );
        }

        const movie = Array.isArray(data) ? data[0] : data;

        const genres = movie.genres || []

        const directors = movie.directors || []

        const actors = movie.actors || []

        console.log("movie:", movie);

        const genresHTML = genres.length > 0 
        ? genres.map(genre => `
            <span class="genre-tag">${genre}</span>`).join("")
            : "No genres available";

        const directorsHTML = directors.length > 0 
        ? directors.map(name => `
            <span class="person-tag">${name}</span>`).join("")
            : "No director information available";

        const actorsHTML = actors.length > 0 
        ? actors.map(name => `
            <span class="person-tag">${name}</span>`).join("")
            : "No cast information available";
        // console.log("movie details:", movie);

        // console.log("Generated genre HTML:", genresHTML);
        // console.log("Rendered genre tags:",
        //     detailsContainer.querySelectorAll(".genre-tag").length
        // );
        // console.log("Rendered genre text:",
        //     detailsContainer.querySelector(".genre.list")?.innerText
        // );
        if(!movie){
            throw new Error("Movie not found");
        }
        detailsContainer.innerHTML=`
        <article class="movie-details-card">
        <h2>${movie.title || "Unknown Title"}<h2>
        <p>
        <strong>Type:</strong>
        ${movie.type || "N/A"}
        </p>
        
        <p>
        <strong>Release Year.</strong>
        ${movie.release_year || "N/A"}
        </p>

        <p>
        <strong>Rating</strong>
        ${movie.rating || "N/A"}
        </p>

        <div class="movie-genres">
        <strong>Genres:</strong>
        <div class="genre-list">
        ${genresHTML}
        </div>
        </div>

        <div class="movie-people">
        <strong>Director:</strong>
        <div class="people-list">
        ${directorsHTML}
        </div>
        </div>

        <div class="movie-people">
        <strong>Cast:</strong>
        <div class="people-list">
        ${actorsHTML}
        </div>
        </div>

        <p>
        <strong>Duration</strong>
        ${movie.duration || "N/A"}
        </p>

        <p class="description">
        <strong>Description</strong>
        ${movie.description || "No description available."}
        </p>
        </article>`;
    }catch (error){
        console.error("Movie details error:", error);

        detailsContainer.innerHTML=`
        <p class="error-message">
        Unable to laod movie details.
        Please try again.
        </p>
        `;
    }
}

loadMovieDetails();