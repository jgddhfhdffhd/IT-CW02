from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# MongoDB Atlas connection URI
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.job_portal  # Access the 'job_portal' database

# MongoDB collections
jobs_collection = db.jobs
applications_collection = db.applications

# Sample route
@app.route('/')
def home():
    return "Welcome to DragonMart Job Portal!"

# Get all job listings
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = list(jobs_collection.find({}))
    for job in jobs:
        job['_id'] = str(job['_id'])  # Convert ObjectId to string for JSON serialization
    return jsonify(jobs)

# Get job details by ID
@app.route('/api/jobs/<string:job_id>', methods=['GET'])
def get_job_details(job_id):
    job = jobs_collection.find_one({"_id": job_id})
    if job:
        job['_id'] = str(job['_id'])
        return jsonify(job)
    else:
        return jsonify({"error": "Job not found"}), 404

# Submit job application
@app.route('/api/applications', methods=['POST'])
def apply_for_job():
    application_data = request.get_json()
    job_id = application_data.get('jobId')
    user_id = application_data.get('userId')

    job = jobs_collection.find_one({"_id": job_id})
    if job:
        application = {
            "jobId": job_id,
            "userId": user_id,
            "status": "pending"
        }
        applications_collection.insert_one(application)
        return jsonify(application), 201
    else:
        return jsonify({"error": "Job not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
