// Get the job dialog element
const jobDialog = document.getElementById('jobDialog');

// Get the job title, description, and requirements elements
const jobTitle = document.getElementById('jobTitle');
const jobDescription = document.getElementById('jobDescription');
const jobRequirements = document.getElementById('jobRequirements');

// Get the close dialog element
const closeDialog = document.getElementById('closeDialog');

// Function to open the job dialog and populate it with the given title, description, and requirements
function openJobDialog(title, description, requirements) {
    jobTitle.textContent = title;
    jobDescription.textContent = description;
    jobRequirements.textContent = requirements;
    jobDialog.style.opacity = '1';
    jobDialog.classList.add('open');
}

// Function to close the job dialog
function closeJobDialog() {
    // Set the opacity of the job dialog to 0 after a delay of 500 milliseconds
    setTimeout(() => {
        jobDialog.style.opacity = '0';
    }, 500);

    // Remove the 'open' class from the job dialog
    jobDialog.classList.remove('open');
}

// Add event listener to the close dialog button
closeDialog.addEventListener('click', closeJobDialog);

// Get all job buttons and add event listeners to them
const jobButtons = document.querySelectorAll('.job button');
jobButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Get the job title from the parent node of the button
        const job = this.parentNode.querySelector('h2').textContent;
        let description = '';
        let requirements = '';

        // Populate the description and requirements based on the selected job
        switch(job) {
            case 'Front-End Developer':
                description = 'As a Front-End Developer, you will be responsible for creating and implementing user-facing features, ensuring the technical feasibility of UI/UX designs, and optimizing applications for maximum speed and scalability. You should have a strong understanding of web development technologies such as HTML, CSS, and JavaScript, as well as experience with front-end frameworks like React or Angular.';
                requirements = 'Requirements:\n- Proficiency in HTML, CSS, and JavaScript\n- Experience with front-end frameworks (e.g., React, Angular)\n- Knowledge of responsive design principles\n- Familiarity with version control systems (e.g., Git)\n- Strong problem-solving and communication skills';
                break;
            case 'Back-End Developer':
                description = 'As a Back-End Developer, you will be responsible for designing, developing, and maintaining the server-side logic of web applications. You will work closely with front-end developers to ensure seamless integration between the front-end and back-end components. You should have a strong understanding of server-side programming languages (e.g., Node.js, Python, Ruby) and databases (e.g., MySQL, MongoDB).';
                requirements = 'Requirements:\n- Proficiency in server-side programming languages (e.g., Node.js, Python, Ruby)\n- Experience with databases (e.g., MySQL, MongoDB)\n- Knowledge of RESTful API design and development\n- Familiarity with version control systems (e.g., Git)\n- Strong problem-solving and collaboration skills';
                break;
            case 'Full Stack Developer':
                description = 'As a Full Stack Developer, you will be responsible for developing both the front-end and back-end components of web applications. You should have a strong understanding of both client-side and server-side technologies, as well as experience with databases and version control systems. You will work on implementing features, optimizing performance, and ensuring the overall functionality of the application.';
                requirements = 'Requirements:\n- Proficiency in front-end technologies (e.g., HTML, CSS, JavaScript)\n- Proficiency in server-side programming languages (e.g., Node.js, Python, Ruby)\n- Experience with databases (e.g., MySQL, MongoDB)\n- Knowledge of RESTful API design and development\n- Familiarity with version control systems (e.g., Git)\n- Strong problem-solving and collaboration skills';
                break;
            case 'UI/UX Designer':
                description = 'As a UI/UX Designer, you will be responsible for creating intuitive and visually appealing user interfaces for web and mobile applications. You will work closely with developers and stakeholders to understand user requirements and translate them into design concepts. You should have a strong understanding of user-centered design principles, as well as proficiency in design tools such as Sketch or Adobe XD.';
                requirements = 'Requirements:\n- Proficiency in design tools (e.g., Sketch, Adobe XD)\n- Knowledge of user-centered design principles\n- Experience with wireframing and prototyping\n- Familiarity with front-end technologies (e.g., HTML, CSS, JavaScript)\n- Strong attention to detail and creativity';
                break;
            case 'Project Manager':
                description = 'As a Project Manager, you will be responsible for overseeing the planning, execution, and delivery of projects within the organization. You will work closely with cross-functional teams to ensure project goals are met on time and within budget. You should have strong leadership and communication skills, as well as experience in project management methodologies.';
                requirements = 'Requirements:\n- Proven experience in project management\n- Strong leadership and communication skills\n- Knowledge of project management methodologies (e.g., Agile, Scrum)\n- Ability to manage multiple projects simultaneously\n- Strong problem-solving and decision-making abilities';
                break;
            default:
                description = 'Description not available.';
                requirements = 'Requirements';
        }

        // Open the job dialog with the selected job's title, description, and requirements
        openJobDialog(job, description, requirements);
    });
});