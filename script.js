// Function to upload a machine
document.getElementById('upload-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var formData = new FormData(this);
    fetch('/upload_machine', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => alert(data))
    .catch(error => alert('Error uploading machine: ' + error));
});

// Function to set default servicing frequency
document.getElementById('frequency-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var machineId = this.elements.machine_id.value;
    var frequency = this.elements.frequency.value;
    fetch('/set_frequency', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ machine_id: machineId, frequency: frequency })
    })
    .then(response => response.text())
    .then(data => alert(data))
    .catch(error => alert('Error setting frequency: ' + error));
});

// Function to view all machines
document.getElementById('view-machines-btn').addEventListener('click', function () {
    fetch('/get_machines', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        var machinesList = document.getElementById('machines-list');
        machinesList.innerHTML = '';
        data.forEach(machine => {
            machinesList.innerHTML += `
                <div>
                    <h3>${machine.description}</h3>
                    <img src="${machine.photo_url}" alt="Machine Photo">
                    <p>Frequency: ${machine.default_frequency} days</p>
                    <p>Service By: ${machine.service_by_date}</p>
                    <p>Notes: ${machine.notes}</p>
                </div>`;
        });
    })
    .catch(error => alert('Error fetching machines: ' + error));
});

function showSection(sectionId) {
    // Hide all sections
    document.getElementById('upload-section').style.display = 'none';
    document.getElementById('frequency-section').style.display = 'none';
    document.getElementById('machines-section').style.display = 'none';

    // Show the selected section
    document.getElementById(sectionId).style.display = 'block';
}