const moviesContainer = document.getElementById("movies-container");

async function loadMovies(
    page =1,
    type ="",
    release_year = "",
    sort = "title",
    order = "asc"
){
    try{

        const params = new URLSearchParams({
            page:page,
            limit:20,
            sort:sort,
            order:order
        });

        if(type){
            params.append("type", type);
        }

        if (release_year){
            params.append("release_year", release_year);
        }

        
        const response = await fetch(`/movies?${params.toString()}`);

        const data = await response.json();

        // console.log("API response:", data);
        // console.log("Movies:", data.movies);
        if(!response.ok){
            throw new Error(data.message || "Failed to fetch movies");
        }

        displayMovies(data.movies);
        displayPagination(
            data.pagination,
            type,
            release_year,
            sort,
            order        
        );
    }catch (error) {
        console.error("Error:",error);

        moviesContainer.innerHTML = `
        <p class="error-message">
        Unable to load movies.
        </p>
        `;
    }
}

function displayMovies(movies){
    moviesContainer.innerHTML="";

    if(!movies || movies.length === 0){
        moviesContainer.innerHTML=`
        <p class="no result">
        No movies found.
        </p>
        `;
        return;
    }

    movies.forEach(movie => {
        const card = document.createElement("div");
        card.className = "movie-card";
        card.innerHTML = `
        <h3>${movie.title || "Unknown Title"}<h3>
        <p>
        <strong>Type:</strong>
        ${movie.type || "N/A"}
        </p>
        
        <p>
        <strong>Release Year.</strong>
        ${movie.release_year || "N/A"}
        </p>
        `;

        card.addEventListener("click", () => {
            window.location.href=`/movie/${movie.id}`;
        });
        moviesContainer.appendChild(card);
    });
}

function displayPagination(pagination,
    type="",
    release_year="",
    sort="title",
    order="asc"
) {
    const paginationContainer = document.getElementById("pagination");

    paginationContainer.innerHTML=`
    <button
    id="previous-btn"
    ${pagination.current_page===1 ? "disabled":""}
    >
    Previos
    </button>

    <span>
    Page ${pagination.current_page} of ${pagination.total_page}
    </span>

    <button
    id="next-btn"
    ${pagination.current_page===pagination.total_page ? "disabled":""}
    >
    Next
    </button>
    `;

    document.getElementById("previous-btn").addEventListener("click",() => {
        loadMovies(pagination.current_page - 1,
            type,
            release_year,
            sort,
            order
        );
    });

    document.getElementById("next-btn").addEventListener("click", () => {
        loadMovies(pagination.current_page + 1,
            type,
            release_year,
            sort,
            order
        );
    });
}

loadMovies();


async function searchMovies(searchText){
    try{
        const response = await fetch(
            `/movies/search?title=${encodeURIComponent(searchText)}`
        );

        const data = await response.json();

        // console.log(data);

        if(!response.ok){
            throw new Error(data.message || "Seach failed");
        }

        //Search API returns the movie list
        const movies = Array.isArray(data) ? data: data.movies;

        // console.log("search movies",movies)

        displayMovies(movies);

        //Clear pagination while showing search results

        document.getElementById("pagination").innerHTML="";
    }catch(error){
        console.error("Search error:", error);

        moviesContainer.innerHTML = `
        <p class="error-message">
        Unable to search movies.
        </p>
        `;
    }
}

async function getMovieDetails(movieId){
    try{
        const response = await fetch(`/movies/${movieId}`);

        const data = await response.json();

        console.log("Movie details:", data);

        if (!response.ok){
            throw new Error(data.message || "Failed to fetch movie details");
        }

        const movie = Array.isArray(data) ? data[0] : data;

        const detailsContainer = document.getElementById("movie-details");

        detailsContainer.innerHTML = `
        <div class="movie-details-card>
        <h2>${movie.title || "Unknown Title"}</h2>

        <p>
        <strong>Type:</strong>
        ${movie.type || "N/A"}
        </p>

        <p>
        <strong>Release Year:</strong>
        ${movie.release_year || "N/A"}
        </p>
        </div>
        `;

        console.log("Selected movie:", movie);

    }catch (error){
        console.error("Movie details error:", error);
    }

    const detailsContainer = document.getElementById("movie-details");
    detailsContainer.innerHTML = `
    <p class="error-message">
    Unable to load movie details
    </p>
    `
}



document.getElementById("searchBtn").addEventListener("click", () => {
    const searchText = document.getElementById("searchInput").value.trim();

    if (searchText ===""){
        loadMovies(1);
        return;
    }

    searchMovies(searchText);
});

document.getElementById("applyFilterBtn").addEventListener("click", () => {
    const type = document.getElementById("typeFilter").value;
    const release_year = document.getElementById("yearFilter").value;
    const sort = document.getElementById("sortFilter").value;
    const order = document.getElementById("orderFilter").value;

    loadMovies(1, type, release_year, sort, order);
});