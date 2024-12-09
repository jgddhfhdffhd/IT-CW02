from pymongo import MongoClient
from faker import Faker
import random
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()  # Load environment variables from .env file

# MongoDB Atlas connection URI
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.job_portal  # Access the 'job_portal' database

# Access the 'jobs' and 'applications' collections
jobs_collection = db.jobs
applications_collection = db.applications

# Initialize Faker instance
fake = Faker()


# Generate 20 job listings
def generate_jobs():
    job_data = []
    for _ in range(20):
        job = {
            "title": fake.job(),
            "location": fake.city(),
            "salary": f"£{random.randint(30, 100)}k-£{random.randint(50, 150)}k",  # Random salary range
            "description": fake.text(max_nb_chars=200)  # Random job description
        }
        job_data.append(job)
    return job_data


# Insert generated job data into MongoDB
def insert_jobs():
    job_data = generate_jobs()
    jobs_collection.insert_many(job_data)
    print("Inserted 20 job listings.")


# Generate 20 job applications
def generate_applications():
    application_data = []
    job_ids = [job["_id"] for job in jobs_collection.find({})]  # Get all job IDs from MongoDB
    if not job_ids:
        print("No jobs found in the database.")
        return

    for _ in range(20):
        application = {
            "jobId": random.choice(job_ids),  # Randomly assign a job ID from existing jobs
            "userId": fake.uuid4(),  # Random user ID
            "status": "pending"  # Default status
        }
        application_data.append(application)
    return application_data


# Insert generated application data into MongoDB
def insert_applications():
    application_data = generate_applications()
    if application_data:
        applications_collection.insert_many(application_data)
        print("Inserted 20 job applications.")


# Run the script
if __name__ == '__main__':
    # Insert job listings and applications
    insert_jobs()
    insert_applications()
