# Netflix Explorer

A full-stack web application for exploring Netflix titles using Python, Flask, MySQL, and JavaScript.

Netflix Explorer lets users browse and search titles, filter and sort results, navigate through paginated listings, and explore detailed information about individual titles, including genres, directors, and cast.

## Features

- **Movie and TV Show Browsing** — Explore Netflix titles from a structured MySQL database.
- **Search** — Find titles by name.
- **Filtering** — Filter titles by type and release year.
- **Sorting** — Sort results by title or release year in ascending or descending order.
- **Pagination** — Browse results in manageable pages.
- **Detailed Title View** — View title information, rating, duration, description, genres, directors, and cast.
- **REST API** — Retrieve title information through Flask endpoints.
- **Relational Data Model** — Store titles, actors, directors, and genres using relational tables and junction tables.
- **ETL Pipeline** — Process source CSV data and load it into MySQL.
- **Responsive Interface** — Browse the application across different screen sizes.

## Tech Stack

| Area | Technologies |
|---|---|
| Backend | Python, Flask |
| Database | MySQL |
| Data Processing | Pandas |
| Frontend | HTML, CSS, JavaScript |
| API | REST |
| Version Control | Git, GitHub |

## Architecture

The application follows a simple data-processing and web-application workflow:

```text
Netflix Titles CSV
        |
        v
Python ETL Pipeline
        |
        v
MySQL Database
        |
        v
Flask REST APIs
        |
        v
HTML, CSS and JavaScript
        |
        v
Netflix Explorer UI
```

The ETL pipeline prepares the source data for relational storage. Flask provides API endpoints for retrieving and managing title records, while the frontend uses these endpoints to display searchable listings and title details.

## Project Structure

```text
netflix-explorer/
├── app.py
├── etl_pipeline.py
├── sql_connection.py
├── requirements.txt
├── .env.example
├── .gitignore
├── netflix_titles_nov_2019.csv
├── static/
│   ├── script.js
│   ├── movie_details.js
│   └── style.css
└── templates/
    ├── index.html
    └── movie_details.html
```

## Getting Started

### Prerequisites

- Python 3
- MySQL Server
- Git

### 1. Clone the repository

```bash
git clone https://github.com/naveen-0908/netflix-explorer.git
cd netflix-explorer
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file using `.env.example` as a reference.

Configure your MySQL host, username, password, and database name. Never commit your `.env` file or actual credentials.

### 5. Prepare the database

Create the `netflix_explorer` database in MySQL and set up the required tables and relationships expected by the ETL pipeline.

Review `etl_pipeline.py` to understand the expected source file, transformations, and database-loading process before running it.

### 6. Run the ETL pipeline

```bash
python etl_pipeline.py
```

Run this after the required database schema is ready. If the pipeline assumes pre-existing tables, create those tables first.

### 7. Start the application

```bash
python app.py
```

Open the local URL shown in your terminal, typically:

`http://127.0.0.1:5000/`

## 🔌 API Overview

The application provides endpoints for common title operations, including:

| Endpoint | Purpose |
|---|---|
| `GET /movies` | Retrieve paginated titles with supported filters and sorting |
| `GET /movies/search?title=...` | Search titles by name |
| `GET /movies/genres` | Retrieve available genres |
| `GET /movies/genre/<genre_name>` | Find titles by genre |
| `GET /movies/actor/<actor_name>` | Find titles by actor |
| `GET /movies/year/<year>` | Find titles by release year |
| `GET /movies/<id>` | Retrieve detailed title information |
| `POST /movies/add` | Add a title |
| `PATCH /movies/update/<id>` | Update supported title fields |
| `DELETE /movies/delete/<id>` | Delete a title |

The exact request parameters and response formats can be inspected in `app.py`.

## Key Learning Outcomes

This project provided hands-on practice with:

- Designing relational database tables and many-to-many relationships.
- Building an ETL pipeline for CSV data.
- Integrating Python applications with MySQL.
- Developing REST APIs with Flask.
- Writing SQL queries involving joins and filtering.
- Implementing search, sorting, and pagination.
- Connecting frontend JavaScript to backend APIs.
- Managing configuration through environment variables.
- Using Git and GitHub for version control.

## Potential Improvements

- Add automated unit and integration tests.
- Improve API validation and error handling.
- Add further data-quality checks to the ETL pipeline.
- Deploy the application to a hosting platform.

## Dataset and Disclaimer

This project is an independent learning project and is not affiliated with or endorsed by Netflix.

The included dataset is a historical snapshot of Netflix titles. Its completeness and accuracy may vary. Please verify the dataset's original source and redistribution terms before sharing it publicly or using it for other purposes.

## Author

**Naveen Babu Ethakota**

[GitHub Profile](https://github.com/naveen-0908)