# Article Scoring System

This is a Django-based API project for managing articles and allowing users to score them. The project is designed with performance and scalability in mind, ensuring proper handling of high traffic and preventing biased scoring activities.

---

## Features

### 1. Article Management
- **View all articles**: Users can view the list of articles, including the number of scores and the average score for each article.
- **Create an article**: Authenticated users can create new articles.

### 2. Article Scoring
- **Score an article**: Authenticated users can assign a score between 0 and 5 to an article.
- **Update a score**: Users can update their previous scores after a cooldown period of 5 minutes.
- **Prevent bias**: Suspicious scoring activity is detected and flagged to ensure unbiased scores.

### 3. Authentication
- **User registration**: Users can create accounts through the API.
- **Login**: Users can log in to obtain an authentication token to interact with the API.

### 4. Performance Enhancements
- **Caching**: Redis is used to cache article statistics (e.g., number of scores and average score).
- **Cooldown mechanism**: User scoring is throttled to prevent rapid score updates.
- **Anomaly detection**: Abnormal scoring activities are identified and flagged.

---
## Anomaly Detection Techniques

To ensure fair scoring and prevent manipulation, the following techniques are implemented:
1. **Rate Limiting and Heuristic Detection**:
   - Abnormal activity is flagged by monitoring the number of scores for an article in a short period (e.g., 10 minutes). If the count exceeds a predefined threshold, the activity is marked as suspicious.

2. **Time-Based Weighted Average Calculation**:
   - A weighted average is calculated for scores, reducing the impact of recent manipulative scores by assigning them lower weights.

---

## Installation

### Prerequisites
- Python 3.9+
- Django 4.x
- Redis

### Setup

1. **Clone the repository**:
   ```bash
   git clone git@github.com:iliya-hajjar/FairRate.git
   cd FairRate
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the server**:
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints

### Authentication
- **Register**:
  ```http
  POST /api/v1/auth/register/
  {
      "username": "example",
      "password": "password123",
      "email": "testuser@example.com"
  }
  ```
- **Login**:
  ```http
  POST /api/v1/auth/login/
  {
      "username": "example",
      "password": "password123"
  }
  ```

### Articles
- **List articles**:
  ```http
  GET /api/v1/articles/
  ```
  Response:
  ```json
  [
      {
          "title": "Article 1",
          "num_scores": 10,
          "average_score": 4.5
      }
  ]
  ```
- **Create an article**:
  ```http
  POST /api/v1/articles/
  {
      "title": "New Article",
      "content": "Article content goes here."
  }
  ```

### Scoring
- **Score an article**:
  ```http
  POST /api/v1/articles/<article_id>/score/
  {
      "score": 5
  }
  ```

---

## Running Tests

The project uses `pytest` for testing.

1. **Install test dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run tests**:
   ```bash
   pytest
   ```
