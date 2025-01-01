from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId
import os
from flask_cors import CORS
from bson import ObjectId

# Helper function to convert ObjectId to string
def json_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)  # Convert ObjectId to string
    if isinstance(obj, dict):
        return {key: json_serializer(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [json_serializer(item) for item in obj]
    return obj


app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# MongoDB Atlas connection URI
MONGO_URI = 'mongodb://admin:admin@35.197.233.18:27017/admin'
client = MongoClient(MONGO_URI)
db = client.job_portal  # Access the 'job_portal' database

# MongoDB collections
jobs_collection = db.jobs
applications_collection = db.applications

# Sample route
@app.route('/')
def home():
    return "Welcome to DragonMart Job Portal!"

# Get job details by ID
@app.route('/api/jobs/<string:job_id>', methods=['GET'])
def get_job_details(job_id):
    try:
        # Convert job_id from string to ObjectId
        if len(job_id) != 24 or not all(c in '0123456789abcdefABCDEF' for c in job_id):
            raise ValueError("Invalid ObjectId format")

        job = jobs_collection.find_one({"_id": ObjectId(job_id)})
        if job:
            job['_id'] = str(job['_id'])  # Convert ObjectId to string for JSON serialization
            return jsonify(job)
        else:
            return jsonify({"error": "Job not found"}), 404
    except Exception as e:
        return jsonify({"error": "Invalid job ID format"}), 400




@app.route('/api/applications', methods=['POST'])
def apply_for_job():
    application_data = request.get_json()
    job_id = application_data.get('jobId')
    user_id = application_data.get('userId')
    name = application_data.get('name')
    email = application_data.get('email')
    phone = application_data.get('phone')
    resume = application_data.get('resume')  # Here you can handle file upload if needed

    job = jobs_collection.find_one({"_id": ObjectId(job_id)})
    if job:
        application = {
            "jobId": job_id,
            "userId": user_id,
            "name": name,
            "email": email,
            "phone": phone,
            "resume": resume,
            "status": "pending"
        }
        applications_collection.insert_one(application)

        # Use json_serializer to convert ObjectId and return the response
        return jsonify(json_serializer(application)), 201
    else:
        return jsonify({"error": "Job not found"}), 404

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        jobs = list(jobs_collection.find({}))
        for job in jobs:
            job['_id'] = str(job['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify(jobs)
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/jobs/<string:job_id>', methods=['DELETE'])
def delete_job(job_id):
    result = jobs_collection.delete_one({"_id": ObjectId(job_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Job deleted successfully"}), 200
    else:
        return jsonify({"error": "Job not found"}), 404

@app.route('/api/jobs/<string:job_id>', methods=['PUT'])
def update_job(job_id):
    updated_job_data = request.get_json()

    # Ensure the necessary fields are present
    if not updated_job_data.get('title') or not updated_job_data.get('location') or not updated_job_data.get('salary'):
        return jsonify({"error": "Missing required fields"}), 400

    # Convert job_id from string to ObjectId for MongoDB query
    try:
        job_id_object = ObjectId(job_id)
    except Exception as e:
        return jsonify({"error": "Invalid job ID format"}), 400

    # Update the job in the database
    result = jobs_collection.update_one(
        {"_id": job_id_object},
        {"$set": {
            "title": updated_job_data.get('title'),
            "location": updated_job_data.get('location'),
            "salary": updated_job_data.get('salary'),
            "description": updated_job_data.get('description')
        }}
    )

    if result.modified_count > 0:
        return jsonify({"message": "Job updated successfully!"}), 200
    else:
        return jsonify({"error": "Job not found or no changes made"}), 404

@app.route('/api/jobs', methods=['POST'])
def add_job():
    # Get job data from the request body
    new_job_data = request.get_json()

    # Validate the required fields
    if not new_job_data.get('title') or not new_job_data.get('location') or not new_job_data.get('salary'):
        return jsonify({"error": "Missing required fields"}), 400

    # Insert the new job into the database
    job = {
        "title": new_job_data.get('title'),
        "location": new_job_data.get('location'),
        "salary": new_job_data.get('salary'),
        "description": new_job_data.get('description')
    }

    result = jobs_collection.insert_one(job)

    # Return the added job with its unique ID
    job['_id'] = str(result.inserted_id)  # Convert ObjectId to string for JSON serialization
    return jsonify(job), 201


@app.route('/api/job_analytics', methods=['GET'])
def get_job_analytics():
    # Fetch job data
    jobs = list(jobs_collection.find({}))

    job_analytics = []

    for job in jobs:
        # Get the number of applications for each job
        job_id = job['_id']
        num_applicants = applications_collection.count_documents({"jobId": job_id})

        # Determine the job status (Active if there are applicants, otherwise Closed)
        status = "Active" if num_applicants > 0 else "Closed"

        job_analytics.append({
            "title": job['title'],
            "num_applicants": num_applicants,
            "status": status
        })

    return jsonify(job_analytics)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
