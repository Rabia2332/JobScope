from sqlalchemy import create_engine, text
import os

# Set up database connection string from environment variable
db_connection_string = os.environ["DB_CONNECTION_STRING"]

# Create a database engine object to connect to the database
engine = create_engine(
    db_connection_string,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"  # Configure SSL/TLS connection
        }
    })

# Load all jobs from the database and return them as a list of dictionaries
def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))
        column_names = result.keys()  # Fetch the column names

        jobs = []
        for row in result:
            # Zip column names and row values and convert the result into a dictionary
            result_dict = dict(zip(column_names, row))
            jobs.append(result_dict)
        return jobs

# Load a specific job with a given ID from the database and return it as a dictionary, or None if it doesn't exist
def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs WHERE id = "+id))

        rows = result.fetchall()
        if len(rows) == 0:
            return None
        else:
            jobs = []
            column_names = result.keys()  # Fetch the column names
            for row in rows:
                # Zip column names and row values and convert the result into a dictionary
                result_dict = dict(zip(column_names, row))
                jobs.append(result_dict)
            return jobs

# Add a new job application to the database
def add_application_to_db(job_id, data):
    with engine.connect() as conn:
        # Construct the SQL query to insert the job application data into the database
        query = text('INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES(:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)')

        # Execute the SQL query with the job application data as parameters
        conn.execute(query, {
            'job_id': job_id,
            'full_name': data['full_name'],
            'email': data['email'],
            'linkedin_url': data['linkedin_url'],
            'education': data['education'],
            'work_experience': data['work_experience'],
            'resume_url': data['resume_url']
        })
