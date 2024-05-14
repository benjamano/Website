// Get the apply button element
const applybutton = document.getElementById('applytojob')

// Get the application form element
const applyform = document.getElementById('applicationform')

// Get the close button element
const closebutton = document.getElementById('formclosebtn')

// Get the job name element
const jobname = document.getElementById('jobname')

// Get the job requirements element
const jobreq = document.getElementById('jobreq')

// Add event listener to the apply button
applybutton.addEventListener('click', openapplywindow)

// Add event listener to the close button
closebutton.addEventListener('click', closeapplicationform)

// Function to open the apply window
function openapplywindow() {
    // Get all the application form elements
    const jobselected = document.querySelectorAll('.applicationform');

    // Get the name of the job selected
    const name = this.parentNode.querySelector('h2').textContent;

    let requirements = '';

    // Determine the requirements based on the job selected
    switch (name) {
        case 'Front-End Developer':
            requirements = 'GCSE Computing<br>GCSE Mathematics<br>GCSE English<br>A Level Computer Science';
            break;
        case 'Back-End Developer':
            requirements = 'GCSE Computing<br>GCSE Mathematics<br>GCSE English<br>A Level Computer Science';
            break;
        case 'Full Stack Developer':
            requirements = 'GCSE Computing<br>GCSE Mathematics<br>GCSE English<br>A Level Computer Science';
            break;
        case 'UI/UX Designer':
            requirements = 'GCSE Art & Design<br>GCSE Computing<br>GCSE English<br>A Level Design & Technology';
            break;
        case 'Project Manager':
            requirements = 'GCSE Mathematics<br>GCSE English<br>A Level Business Studies<br>GCSE Computing';
            break;
        default:
            requirements = 'Requirements not available.';
            break;
    }

    // Set the text content of jobname element to indicate the job being applied for
    jobname.textContent = ('Applying for ').concat(name);

    // Set the innerHTML of jobreq element to display the job requirements
    jobreq.innerHTML = requirements;

    // Set the opacity of applyform element to make it visible
    applyform.style.opacity = '1';

    // Add the 'open' class to applyform element and remove the 'closed' class
    applyform.classList.add('open');
    applyform.classList.remove('closed');
}


// Function to close the application form
function closeapplicationform(){

    // Add the 'closed' class to applyform element
    applyform.classList.add('closed');

    // Set the opacity of applyform element to make it fade out
    applyform.style.opacity = '1';

    // Delay the opacity change of applyform element
    setTimeout(() => {
        applyform.style.opacity = '0';
    }, 500);

    // Remove the 'open' class from applyform element
    applyform.classList.remove('open');

    // Delay the opacity change of jobDialog element
    setTimeout(() => {
        jobDialog.style.opacity = '0';
    }, 500);

    // Remove the 'open' class from jobDialog element
    jobDialog.classList.remove('open');
}
