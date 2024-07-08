document.addEventListener("DOMContentLoaded", function() {
    // Show the initial step on page load
    document.querySelector(".personal-info").classList.add("show");

    let currentStep = 0;
    const steps = [
        "personal-info",
        "school-info",
        "pg-info",
        "sibling-info",
        "scholarship-application"
    ];

    function showStep(step) {
        steps.forEach((stepId, index) => {
            const element = document.getElementById(stepId);
            if (index === step) {
                element.classList.add("show");
            } else {
                element.classList.remove("show");
            }
        });
    }

    document.querySelectorAll(".back-btn").forEach(button => {
        button.addEventListener("click", function(e) {
            e.preventDefault();
            if (currentStep > 0) {
                currentStep--;
                showStep(currentStep);
            }
        });
    });

    document.querySelectorAll(".next-btn").forEach(button => {
        button.addEventListener("click", function(e) {
            e.preventDefault();
            if (currentStep < steps.length - 1) {
                currentStep++;
                showStep(currentStep);
            }
        });
    });

    function showPopup(popupId) {
        document.getElementById(popupId).classList.add("show");
    }

    function hidePopup(popupId) {
        document.getElementById(popupId).classList.remove("show");
    }

    document.querySelectorAll("#cancel-btn").forEach(button => {
        button.addEventListener("click", function(e) {
            e.preventDefault();
            showPopup("cancel-popup");
        });
    });

    document.querySelectorAll("#continue-btn").forEach(button => {
        button.addEventListener("click", function(e) {
            e.preventDefault();
            hidePopup("cancel-popup");
        });
    });

    document.querySelectorAll("#submit").forEach(button => {
        button.addEventListener("click", function(e) {
            e.preventDefault();
            showPopup("thankyou-popup");
        });
    });

    let parentCount = 0;

    function addParentSection() {
        const container = document.getElementById('parent-guardian-container');
        const template = document.getElementById('parent-template');
        const clone = template.content.cloneNode(true);
        
        const elements = clone.querySelectorAll('[id], [for], [name]');
        elements.forEach(el => {
            if (el.id) el.id = el.id.replace('{index}', parentCount);
            if (el.htmlFor) el.htmlFor = el.htmlFor.replace('{index}', parentCount);
            if (el.name) el.name = el.name.replace('{index}', parentCount);
        });

        container.appendChild(clone);
        parentCount++;
    }

    addParentSection();
    document.getElementById('add-parent-btn').addEventListener('click', addParentSection);

    let siblingNLSCount = 0;
    let siblingSiblingCount = 0;

    function addSibling(type) {
        const container = document.getElementById(`sibling-${type}-container`);
        const template = document.getElementById(`sibling-${type}-template`).content.cloneNode(true);
        const elements = template.querySelectorAll('[id], [for], [name]');
        const count = type === 'nls' ? siblingNLSCount : siblingSiblingCount;

        elements.forEach((element) => {
            if (element.id) {
                element.id = element.id.replace('{index}', count);
            }
            if (element.htmlFor) {
                element.htmlFor = element.htmlFor.replace('{index}', count);
            }
            if (element.name) {
                element.name = element.name.replace('{index}', `[${count}]`);
            }
        });

        container.appendChild(template);
        if (type === 'nls') {
            siblingNLSCount++;
        } else {
            siblingSiblingCount++;
        }
    }

    document.getElementById('add-sibling-nls-btn').addEventListener('click', function() {
        addSibling('nls');
    });

    document.getElementById('add-sibling-ss-btn').addEventListener('click', function() {
        addSibling('ss');
    });
    
    document.getElementById('submit-btn').addEventListener('click', function(e) {
        e.preventDefault();
        document.getElementById('scholarship-form').submit();
    });

});