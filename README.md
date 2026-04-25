# InJob – Job Recommendation Platform

A Django-based web application that recommends jobs to users based on their skills and provides insights into job market trends.

## Features

- **Job Recommendations** – Enter your skills (comma-separated) and get the top matching job listings from the dataset.
- **Market Insights** – Explore analytics including top in-demand skills, top hiring companies, average salaries by job title, and jobs by location.
- **Responsive UI** – Clean, Bootstrap-powered interface accessible on all screen sizes.

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| Web Framework | Django 6.0 |
| Data Processing | Pandas |
| Frontend | Bootstrap 5, Django Templates |
| Database | SQLite3 |

## Project Structure

```
job-recommendation-platform/
├── analyzer/               # Django app – views, URLs, app templates
│   ├── views.py            # Home, Recommend, and Insights view handlers
│   ├── urls.py             # App-level URL routing
│   └── templates/          # Per-view HTML templates
├── data_analyzer/          # Django project – settings and root URL config
├── datasets/
│   └── job_market.csv      # 249-row job market dataset
├── ml_engine/
│   └── recommender.py      # Skill-matching recommendation logic
├── templates/
│   └── base.html           # Shared base template with navigation
└── manage.py
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/28harivijay/job-recommendation-platform.git
cd job-recommendation-platform

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install django pandas

# 4. Apply database migrations
python manage.py migrate

# 5. Start the development server
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Usage

| Route | Description |
|---|---|
| `/` | Landing page |
| `/recommend` | Enter your skills and receive job matches |
| `/insights` | Browse job market analytics |

### How Recommendations Work

The recommender in `ml_engine/recommender.py` uses a **skill-set intersection** approach:

1. The user provides a comma-separated list of skills.
2. Each job's required skills are parsed from the dataset.
3. A match score is calculated as the number of overlapping skills.
4. The top 5 highest-scoring jobs are returned.

## Dataset

`datasets/job_market.csv` contains 249 job listings with the following columns:

`job_title`, `company`, `location`, `skills`, `salary_min`, `salary_max`, and more.

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "Add your feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a pull request.

## License

This project is open source. See the repository for details.
