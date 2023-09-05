// Function to upload a machine
document.getElementById('upload-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var formData = new FormData(this);
    fetch('http://127.0.0.1:5000/upload_machine', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => alert(data))
    .catch(error => alert('Error uploading machine: ' + error));
});


// Function to view all machines
document.getElementById('view-machines-btn').addEventListener('click', function () {
    fetch('http://127.0.0.1:5000/view_machines', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        var machinesList = document.getElementById('machines-list');
        machinesList.innerHTML = '';
        data.forEach(machine => {
            machinesList.innerHTML += `
                <div>
                    <h3>${machine.machine_name} - ${machine.description}</h3>
                    <img class="machine-image" src="${machine.photo_url}" alt="Machine Photo">
                    <p>Status: ${machine.status}</p>
                    <p>Last Service Date: ${machine.last_service_date}</p>
                    <p>Next Service Date: ${machine.next_service_date}</p>
                    <p>Service Notes: ${machine.notes}</p>  <!-- Include notes -->
                </div>`;
        });
    })
    .catch(error => alert('Error fetching machines: ' + error));
});



function showSection(sectionId) {
    // Hide all sections
    document.getElementById('upload-section').style.display = 'none';
    document.getElementById('machines-section').style.display = 'none';
    document.getElementById('service-section').style.display = 'none';

    // Show the selected section
    document.getElementById(sectionId).style.display = 'block';
}


function loadMachineList() {
    fetch('http://127.0.0.1:5000/get_machine_list', {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(`Server returned ${response.status}: ${text}`);
            });
        }
        return response.json();
    })
    .then(data => {
        var dropdown = document.getElementById('machine-dropdown');
        data.forEach(machine => {
            var option = document.createElement('option');
            option.value = machine.machine_id;
            option.text = machine.description;
            dropdown.appendChild(option);
        });
    })
    .catch(error => alert('Error fetching machine list: ' + error));
}
// todo the list is extending indefinitely

// Call the function to populate the dropdown when the page loads


document.getElementById('service-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var formData = new FormData(this);
    fetch('http://127.0.0.1:5000/service_machine', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => alert(data))
    .catch(error => alert('Error logging service details: ' + error));
});
