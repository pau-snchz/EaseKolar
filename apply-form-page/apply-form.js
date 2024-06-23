document.addEventListener("DOMContentLoaded", function() {
    // FOR: Next, Back, Cancel (Buttons)
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

    function showPopup(popupId) {
        document.getElementById(popupId).classList.add("show");
    }

    function hidePopup(popupId) {
        document.getElementById(popupId).classList.remove("show");
    }

    document.querySelectorAll(".next-btn").forEach(button => {
        button.addEventListener("click", function(e) {
            e.preventDefault();
            if (currentStep < steps.length - 1) {
                currentStep++;
                showStep(currentStep);
            } else {
                showPopup("thankyou-popup");
            }
        });
    });

    document.querySelectorAll("#back-btn").forEach(button => {
        button.addEventListener("click", function(e) {
            e.preventDefault();
            if (currentStep > 0) {
                currentStep--;
                showStep(currentStep);
            }
        });
    });

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
});