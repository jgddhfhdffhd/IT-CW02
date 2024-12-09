// Get the job ID from the URL
const urlParams = new URLSearchParams(window.location.search);
const jobId = parseInt(urlParams.get('id'));

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

      // Set up Apply Now button
      document.getElementById('apply-btn').addEventListener('click', function() {
        const userId = 'user123'; // Simulated user ID (can be dynamic later)

        const applicationData = {
          jobId: job.id,
          userId: userId
        };

        fetch('http://127.0.0.1:5000/api/applications', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(applicationData)
        })
        .then(response => response.json())
        .then(data => {
          alert('Application submitted successfully!');
          console.log('Application data:', data);
        })
        .catch(error => console.error('Error submitting application:', error));
      });
    }
  })
  .catch(error => {
    console.error('Error fetching job details:', error);
    document.getElementById('job-details').innerHTML = `<p>Error loading job details.</p>`;
  });
