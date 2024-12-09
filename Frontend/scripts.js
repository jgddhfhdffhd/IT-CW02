// Global array to store job listings
let jobList = [];

// Fetch job listings from the backend when the page loads
document.addEventListener("DOMContentLoaded", function () {
  fetch('http://127.0.0.1:5000/api/jobs')  // Fetch job data from Flask backend
    .then(response => response.json())
    .then(data => {
      jobList = data;  // Store job data globally
      renderJobs(jobList);  // Initially render all jobs
    })
    .catch(error => console.error('Error fetching jobs:', error));
});

// Function to render job listings
function renderJobs(jobs) {
  const jobListContainer = document.querySelector('.job-list-container');
  jobListContainer.innerHTML = ''; // Clear current job listings

  jobs.forEach(job => {
    const jobCard = document.createElement('div');
    jobCard.classList.add('col-md-4', 'mb-4');
    jobCard.innerHTML = `
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">${job.title}</h5>
          <p class="card-text">Location: ${job.location}</p>
          <p class="card-text">Salary: ${job.salary}</p>
          <p class="card-text">Description: ${job.description}</p>
          <a href="job-details.html?id=${job.id}" class="btn btn-tiffany">View Details</a>
        </div>
      </div>
    `;
    jobListContainer.appendChild(jobCard);
  });
}

// Search functionality
document.querySelector('#search-btn').addEventListener('click', function () {
  const searchTitle = document.querySelector('#search-title').value.toLowerCase();
  const searchLocation = document.querySelector('#search-location').value.toLowerCase();
  const searchSalary = document.querySelector('#search-salary').value.toLowerCase();

  // Filter job list based on the search criteria
  const filteredJobs = jobList.filter(job => {
    return (
      job.title.toLowerCase().includes(searchTitle) &&
      job.location.toLowerCase().includes(searchLocation) &&
      job.salary.toLowerCase().includes(searchSalary)
    );
  });

  // Render filtered jobs
  renderJobs(filteredJobs);
});
