// Get the job ID from the URL
const urlParams = new URLSearchParams(window.location.search);
const jobId = urlParams.get('id');  // Ensure it's a string, not parsed to an integer

// Check if jobId is a valid MongoDB ObjectId format (24 characters, hexadecimal)
if (!/^[0-9a-fA-F]{24}$/.test(jobId)) {
  document.getElementById('job-details').innerHTML = `<p>Invalid job ID format.</p>`;
} else {
  // Fetch job details from the backend
  fetch(`http://127.0.0.1:5000/api/jobs/${jobId}`)
    .then(response => response.json())
    .then(job => {
      if (job.error) {
        // Handle job not found
        document.getElementById('job-details').innerHTML = `<p>${job.error}</p>`;
      } else {
        // Populate the job details
        document.getElementById('job-title').textContent = job.title;
        document.getElementById('job-location').textContent = "Location: " + job.location;
        document.getElementById('job-salary').textContent = "Salary: " + job.salary;
        document.getElementById('job-description').textContent = "Description: " + job.description;

        // Dynamically create the Apply Now button link
        const applyBtn = document.getElementById('apply-btn');
        applyBtn.href = `job-application.html?id=${job._id}`;  // Pass the jobId as a query parameter
      }
    })
    .catch(error => {
      console.error('Error fetching job details:', error);
      document.getElementById('job-details').innerHTML = `<p>Error loading job details.</p>`;
    });
}
