document.addEventListener('DOMContentLoaded', function() {
    const allCategories = ['Accounting_Finance', 'Engineering', 'Healthcare_Nursing', 'Sales'];

    const populateDropdown = () => {
        const dropdown = document.getElementById("category");
        dropdown.innerHTML = "";
        allCategories.forEach((category) => {
            let option = document.createElement("option");
            option.value = option.text = category;
            dropdown.add(option);
        });
    };

    populateDropdown();

    document.getElementById("predict-button").addEventListener("click", function() {
        document.getElementById("loading").style.display = "block";
        
        const title = document.getElementById("title").value;
        const description = document.getElementById("description").value;
        
        fetch('/predict-category', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `title=${title}&description=${description}`
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("loading").style.display = "none";
            document.getElementById("category").value = data.predicted_category;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});