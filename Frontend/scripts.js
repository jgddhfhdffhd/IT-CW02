// Global array to store job listings
let jobList = [];

// Fetch job listings from the backend when the page loads
document.addEventListener("DOMContentLoaded", function () {
  fetch('https://backend-8b6i.onrender.com/api/jobs')
  .then(response => response.json())
  .then(data => {
    console.log(data);
  })
  .catch(error => {
    console.error('Error fetching jobs:', error);
  });
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
          <a href="job-details.html?id=${job._id}" class="btn btn-tiffany">View Details</a>
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
      (searchLocation === "" || job.location.toLowerCase().includes(searchLocation)) &&
      (searchSalary === "" || job.salary.toLowerCase().includes(searchSalary))
    );
  });

  // Render filtered jobs
  renderJobs(filteredJobs);
});
