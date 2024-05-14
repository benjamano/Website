// Get the necessary elements from the DOM
const projectDialog = document.getElementById('projectDialog');
const projectTitle = document.getElementById('projectTitle');
const projectDescription = document.getElementById('projectDescription');
const closeDialog = document.getElementById('closeDialog');
const body = document.getElementById('main');

// Function to open the project dialog and populate it with title and description
function openprojectDialog(title, description) {
    projectTitle.textContent = title;
    projectDescription.textContent = description;
    projectDialog.classList.add('open');
    body.style.opacity = '0.5';
    projectDialog.style.opacity = '1';
}

// Function to close the project dialog
function closeprojectDialog() {
    // Delay the opacity change to create a smooth transition
    setTimeout(() => {
        projectDialog.style.opacity = '0';
    }, 500);
    
    body.style.opacity = '1';
    projectDialog.classList.remove('open');
}

// Add event listener to the close button
closeDialog.addEventListener('click', closeprojectDialog);

// Get all project buttons and add event listeners to each
const projectButtons = document.querySelectorAll('.portfolioitem .learnmore');
projectButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Get the project title from the parent node
        const project = this.parentNode.querySelector('h2').textContent;
        console.log("Hello")
        let description = '';
        // Populate the description based on the project title
        switch(project) {
            case 'Google':
                description = "A recently completed project by our web development company in collaboration with Google. The project involved creating a responsive and user-friendly website for Google, implementing cutting-edge technologies and ensuring seamless integration with their existing systems. The website showcases Google's products and services, providing users with an immersive and informative experience. Our team worked closely with Google's design and development teams to deliver a high-quality website that meets their requirements and exceeds user expectations.";
                break;

            case 'Meta':
                description = "A recently completed project by our web development company in collaboration with Meta. The project involved creating an innovative and immersive virtual reality experience for Meta's cutting-edge augmented reality glasses. Our team worked closely with Meta's design and development teams to develop interactive and visually stunning virtual reality applications that showcase the capabilities of their AR glasses. The project required extensive knowledge of 3D modeling, game development, and user experience design. We successfully delivered a captivating virtual reality experience that pushes the boundaries of augmented reality technology.";
                break;

            case 'Firefly':
                description = "A recently completed project by our web development company, Firefly is a comprehensive resource page designed specifically for schools to track homework and upload resources. Our team worked closely with educators and administrators to create a user-friendly platform that streamlines the homework tracking process and enhances communication between teachers, students, and parents. The website features a secure login system, intuitive interface, and robust file management capabilities. With Firefly, schools can easily manage and organize homework assignments, share important resources, and facilitate seamless collaboration within the school community.";
                break;

            case 'Microsoft':
                description = "A recently completed project by our web development company in collaboration with Microsoft. The project involved creating a robust and scalable web application using Microsoft technologies such as .NET and Azure. Our team worked closely with Microsoft's engineers to ensure seamless integration with their cloud services and to leverage their cutting-edge tools and frameworks. The web application provides users with a highly secure and efficient platform for managing their data and performing complex tasks. With our expertise in Microsoft technologies, we delivered a high-quality solution that meets the client's requirements and exceeds industry standards.";
                break;

            default:
                description = 'Description not available.';
        }
        // Open the project dialog with the title and description
        openprojectDialog(project, description);
    });
});