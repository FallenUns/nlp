Project Title: Job Seeker Website

Description:
This project is a simple Job Seeker Website built using Python Flask. It allows users to browse job listings by category, search for jobs, and post new job listings.

Features:
- Browse jobs by categories
- Search functionality
- Post a new job listing
- Predict job category based on the job description and title

Requirements:
- Python 3.9.5 or higher
- Flask
- Jinja2
- NumPy
- scikit-learn
- pandas
- Gensim

How to Run Locally:
1. Install all required packages:
   pip install -r requirements.txt

2. Set Environment Variables
   Set the directory file in the environment if needed.

3. Run the Flask app:
   flask run

** Note that the flask run command will run for about 2 minutes depending on the machine it run because it needs to load a large file for the ML algorithm**

4. Open the web browser and go to `http://127.0.0.1:5000/`

Files Included:
- app.py: The main Python file that runs the Flask app
- /templates: Contains HTML files
- /static: Contains static files like CSS and JavaScript
- /data : Contains the data for ML and existing job data.
- `requirements.txt`: Lists all the required packages.
- README.txt: This file

Files Missing:
- a2-milestone2/data/crawl-300d-2M-subword.bin the file size is 6.73 can be obtained in https://fasttext.cc/docs/en/english-vectors.html
