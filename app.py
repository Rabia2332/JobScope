from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db

app = Flask(__name__)

@app.route("/")
def hello():
    # Load all jobs from the database
    jobs = load_jobs_from_db()
    # Render the home page with the list of jobs and company name
    return render_template('home.html', jobs=jobs, company_name='JobScope')

@app.route("/api/jobs")
def list_jobs():
    # Load all jobs from the database and return them as a JSON response
    jobs = load_jobs_from_db()
    return jsonify(jobs)

@app.route('/job/<id>')
def show_job(id):
    # Load the job with the given ID from the database
    job = load_job_from_db(id)
    # If the job is not found, return a 404 error
    if not job:
        return 'Not Found', 404
    # Render the job page with the job data
    return render_template('jobpage.html', job=job)

@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
     # Get the form data submitted by the user
     data = request.form
     # Load the job with the given ID from the database
     job = load_job_from_db(id)
     # Add the application data to the database for the given job
     add_application_to_db(id, data)
     # Render the application submitted page with the application data and job data
     return render_template('application_submitted.html', application=data, job=job)

if __name__ == '__main__':
    # Run the Flask app on the local machine with debugging enabled
    app.run(host='0.0.0.0', debug=True)
