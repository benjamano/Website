document.addEventListener('DOMContentLoaded', function() {
  // Selecting elements
  const carousel = document.querySelector('.carousel');
  const traineecarousel = document.querySelector('.traineecarousel');
  const jobs = document.querySelectorAll('.job');
  const trainees = document.querySelectorAll('.trainee');
  const prevBtn = document.querySelector('.prev');
  const nextBtn = document.querySelector('.next');
  const traineeprevBtn = document.querySelector('.traineeprev');
  const traineenextBtn = document.querySelector('.traineenext');

  // Initializing variables
  let currentIndex = 2;
  let traineecurrentIndex = 2;

  // Function to show job at a given index
  function showJob(index) {
    const containerWidth = carousel.offsetWidth;
    const jobWidth = jobs[0].offsetWidth;
    const jobMargin = parseFloat(window.getComputedStyle(jobs[0]).marginRight);
    const totalJobWidth = jobWidth + jobMargin;
    const offset = -((index * totalJobWidth) + (totalJobWidth / 2) - (containerWidth / 2));
    carousel.style.transform = `translateX(${offset}px)`;

    // Updating button states
    if (index == jobs.length - 1){
      console.log('At end, disabling next button')
      nextBtn.classList.add('disabled')
    } else if (index == 0) {
      console.log('At start, disabling prev button')
      prevBtn.classList.add('disabled')
    } else{
      prevBtn.classList.remove('disabled')
      nextBtn.classList.remove('disabled')
    }
  
    // Adding 'active' class to the selected job
    jobs.forEach((job, i) => {
      if (i === index) {
        job.classList.add('active');
      } else {
        job.classList.remove('active');
      }
    });
  }

  // Function to show trainee at a given index
  function showTrainee(index){
    const traineecontainerWidth = traineecarousel.offsetWidth;
    const traineewidth = trainees[0].offsetWidth;
    const traineemargin = parseFloat(window.getComputedStyle(trainees[0]).marginRight);
    const totaltraineewidth = traineewidth + traineemargin;
    const offset = -((index * totaltraineewidth) + (totaltraineewidth / 2) - (traineecontainerWidth / 2));
    traineecarousel.style.transform = `translateX(${offset}px)`;

    // Updating button states
    if (index == trainees.length - 1){
      console.log('At end, disabling next button')
      traineenextBtn.classList.add('disabled')
    } else if (index == 0) {
      console.log('At start, disabling prev button')
      traineeprevBtn.classList.add('disabled')
    } else{
      traineeprevBtn.classList.remove('disabled')
      traineenextBtn.classList.remove('disabled')
    }

    // Adding 'active' class to the selected trainee
    trainees.forEach((trainee, i) => {
      if (i==index) {
        trainee.classList.add('active');
      } else{
        trainee.classList.remove('active');
      }
    });
  }

  // Function to handle next job button click
  function nextJob() {
    currentIndex = (currentIndex + 1) % jobs.length;
    console.log('Next button pressed',currentIndex, jobs.length)
    showJob(currentIndex);
  }

  // Function to handle previous job button click
  function prevJob() {
    currentIndex = (currentIndex - 1 + jobs.length) % jobs.length;
    console.log('Prev button pressed',currentIndex, jobs.length)
    showJob(currentIndex);
  }

  // Function to handle next trainee button click
  function nexttrainee(){
    traineecurrentIndex = (traineecurrentIndex + 1) % trainees.length;
    console.log('Next button pressed',traineecurrentIndex, trainees.length)
    showTrainee(traineecurrentIndex)
  }

  // Function to handle previous trainee button click
  function prevtrainee(){
    traineecurrentIndex = (traineecurrentIndex - 1 + trainees.length) % trainees.length;
    console.log('Prev button pressed',traineecurrentIndex, trainees.length)
    showTrainee(traineecurrentIndex)
  }

  // Adding event listeners to buttons
  prevBtn.addEventListener('click', prevJob);
  nextBtn.addEventListener('click', nextJob);
  traineeprevBtn.addEventListener('click', prevtrainee);
  traineenextBtn.addEventListener('click', nexttrainee);

  // Initial setup
  showJob(2);
  showTrainee(2);

  console.log('Carousel.js init\nJob index:',currentIndex+'\nTrainee index:',traineecurrentIndex);
});
