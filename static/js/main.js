// static/js/main.js

document.addEventListener('DOMContentLoaded', () => {
    // Determine which page is loaded and initialize accordingly
    if (document.getElementById('addRoomForm')) {
        initializeManagePage();
    }
    if (document.getElementById('generateBtn')) {
        initializeDashboard();
    }
});

// ======================================================================
// --- MANAGE PAGE LOGIC (CRUD for Rooms, Batches, Subjects, Faculty) ---
// ======================================================================

function initializeManagePage() {
    // --- Room Elements ---
    const addRoomForm = document.getElementById('addRoomForm');
    const roomNameInput = document.getElementById('roomName');
    const roomList = document.getElementById('roomList');

    // --- Batch Elements ---
    const addBatchForm = document.getElementById('addBatchForm');
    const batchNameInput = document.getElementById('batchName');
    const batchList = document.getElementById('batchList');

    // --- Subject Elements ---
    const addSubjectForm = document.getElementById('addSubjectForm');
    const subjectNameInput = document.getElementById('subjectName');
    const subjectCodeInput = document.getElementById('subjectCode');
    const subjectHoursInput = document.getElementById('subjectHours');
    const subjectList = document.getElementById('subjectList');

    // --- Faculty Elements ---
    const addFacultyForm = document.getElementById('addFacultyForm');
    const facultyNameInput = document.getElementById('facultyName');
    const facultyList = document.getElementById('facultyList');
    const assignSubjectForm = document.getElementById('assignSubjectForm');
    const assignFacultySelect = document.getElementById('assignFacultySelect');
    const assignSubjectSelect = document.getElementById('assignSubjectSelect');


    // --- Generic Fetch Helper ---
    async function fetchData(url, method = 'GET', data = null) {
        const options = {
            method: method,
            headers: { 'Content-Type': 'application/json' },
        };
        if (data) {
            options.body = JSON.stringify(data);
        }
        try {
            const response = await fetch(url, options);
            if (response.status === 401) {
                alert('Session expired or Unauthorized. Please log in again.');
                window.location.href = '/'; // Redirect to login
                return null;
            }
            return response.json();
        } catch (error) {
            console.error('Fetch error:', error);
            return null;
        }
    }

    // --- Rooms CRUD ---
    const loadRooms = async () => {
        const rooms = await fetchData('/api/rooms');
        if (!rooms) return;
        roomList.innerHTML = '';
        if (rooms.length === 0) {
            roomList.innerHTML = '<li class="list-group-item text-muted">No rooms added yet.</li>';
        } else {
            rooms.forEach(room => {
                const li = document.createElement('li');
                li.className = 'list-group-item d-flex justify-content-between align-items-center';
                li.textContent = room.name;
                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'btn btn-danger btn-sm';
                deleteBtn.textContent = 'Delete';
                deleteBtn.onclick = async () => {
                    if (confirm(`Are you sure you want to delete room "${room.name}"?`)) {
                        await fetchData(`/api/rooms/${room.id}`, 'DELETE');
                        loadRooms();
                    }
                };
                li.appendChild(deleteBtn);
                roomList.appendChild(li);
            });
        }
    };

    addRoomForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = roomNameInput.value.trim();
        if (!name) return;
        await fetchData('/api/rooms', 'POST', { name });
        roomNameInput.value = '';
        loadRooms();
    });

    // --- Batches CRUD ---
    const loadBatches = async () => {
        const batches = await fetchData('/api/batches');
        if (!batches) return;
        batchList.innerHTML = '';
        if (batches.length === 0) {
            batchList.innerHTML = '<li class="list-group-item text-muted">No batches added yet.</li>';
        } else {
            batches.forEach(batch => {
                const li = document.createElement('li');
                li.className = 'list-group-item d-flex justify-content-between align-items-center';
                li.textContent = batch.name;
                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'btn btn-danger btn-sm';
                deleteBtn.textContent = 'Delete';
                deleteBtn.onclick = async () => {
                    if (confirm(`Are you sure you want to delete batch "${batch.name}"?`)) {
                        await fetchData(`/api/batches/${batch.id}`, 'DELETE');
                        loadBatches();
                    }
                };
                li.appendChild(deleteBtn);
                batchList.appendChild(li);
            });
        }
    };

    addBatchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = batchNameInput.value.trim();
        if (!name) return;
        await fetchData('/api/batches', 'POST', { name });
        batchNameInput.value = '';
        loadBatches();
    });

    // --- Subjects CRUD ---
    const loadSubjects = async () => {
        const subjects = await fetchData('/api/subjects');
        if (!subjects) return;
        subjectList.innerHTML = '';
        assignSubjectSelect.innerHTML = '<option value="">Select Subject</option>'; // Reset for dropdown
        if (subjects.length === 0) {
            subjectList.innerHTML = '<li class="list-group-item text-muted">No subjects added yet.</li>';
        } else {
            subjects.forEach(subject => {
                const li = document.createElement('li');
                li.className = 'list-group-item d-flex justify-content-between align-items-center';
                li.innerHTML = `<span><b>${subject.name}</b> (${subject.code}) - ${subject.hours_per_week} hrs/week</span>`;
                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'btn btn-danger btn-sm';
                deleteBtn.textContent = 'Delete';
                deleteBtn.onclick = async () => {
                    if (confirm(`Are you sure you want to delete subject "${subject.name}"?`)) {
                        await fetchData(`/api/subjects/${subject.id}`, 'DELETE');
                        loadSubjects();
                        loadFaculties(); // Reload faculties as subject associations might change
                    }
                };
                li.appendChild(deleteBtn);
                subjectList.appendChild(li);

                // Populate assign subject dropdown
                const option = document.createElement('option');
                option.value = subject.id;
                option.textContent = `${subject.name} (${subject.code})`;
                assignSubjectSelect.appendChild(option);
            });
        }
    };

    addSubjectForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = subjectNameInput.value.trim();
        const code = subjectCodeInput.value.trim();
        const hours_per_week = parseInt(subjectHoursInput.value);
        if (!name || !code || isNaN(hours_per_week) || hours_per_week <= 0) {
            alert('Please fill all subject fields correctly.');
            return;
        }
        await fetchData('/api/subjects', 'POST', { name, code, hours_per_week });
        subjectNameInput.value = '';
        subjectCodeInput.value = '';
        subjectHoursInput.value = '';
        loadSubjects();
        loadFaculties(); // Reload faculties as new subjects can be assigned
    });

    // --- Faculty CRUD and Subject Assignment ---
    const loadFaculties = async () => {
        const faculties = await fetchData('/api/faculties');
        if (!faculties) return;
        facultyList.innerHTML = '';
        assignFacultySelect.innerHTML = '<option value="">Select Faculty</option>'; // Reset for dropdown
        if (faculties.length === 0) {
            facultyList.innerHTML = '<li class="list-group-item text-muted">No faculty added yet.</li>';
        } else {
            faculties.forEach(faculty => {
                const li = document.createElement('li');
                li.className = 'list-group-item d-flex justify-content-between align-items-center flex-wrap';
                
                const facultyInfo = document.createElement('span');
                facultyInfo.innerHTML = `<b>${faculty.name}</b><br><small class="text-muted">Can teach: ${faculty.subjects.map(s => s.code).join(', ') || 'None'}</small>`;
                li.appendChild(facultyInfo);

                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'btn btn-danger btn-sm ms-auto';
                deleteBtn.textContent = 'Delete';
                deleteBtn.onclick = async () => {
                    if (confirm(`Are you sure you want to delete faculty "${faculty.name}"?`)) {
                        await fetchData(`/api/faculties/${faculty.id}`, 'DELETE');
                        loadFaculties();
                    }
                };
                li.appendChild(deleteBtn);
                facultyList.appendChild(li);

                // Populate assign faculty dropdown
                const option = document.createElement('option');
                option.value = faculty.id;
                option.textContent = faculty.name;
                assignFacultySelect.appendChild(option);
            });
        }
    };

    addFacultyForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = facultyNameInput.value.trim();
        if (!name) return;
        await fetchData('/api/faculties', 'POST', { name });
        facultyNameInput.value = '';
        loadFaculties();
    });

    assignSubjectForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const facultyId = assignFacultySelect.value;
        const subjectId = assignSubjectSelect.value;
        if (!facultyId || !subjectId) {
            alert('Please select both a faculty and a subject.');
            return;
        }
        await fetchData(`/api/faculties/${facultyId}/subjects`, 'POST', { subject_id: subjectId });
        assignFacultySelect.value = '';
        assignSubjectSelect.value = '';
        loadFaculties(); // Reload faculties to show new assignments
    });

    // --- Initial Loads for Manage Page ---
    loadRooms();
    loadBatches();
    loadSubjects();
    loadFaculties();
}


// ======================================================================
// --- DASHBOARD PAGE LOGIC ---
// ======================================================================

function initializeDashboard() {
    const generateBtn = document.getElementById('generateBtn');
    const statusDiv = document.getElementById('status');
    const resultsContainer = document.getElementById('results-container');

    generateBtn.addEventListener('click', async () => {
        statusDiv.innerHTML = '<div class="spinner-border spinner-border-sm text-primary me-2" role="status"><span class="visually-hidden">Loading...</span></div>Generating... This may take a moment. Check the terminal for progress.';
        resultsContainer.innerHTML = ''; // Clear previous results

        const data = await fetchData('/api/generate', 'POST');

        if (!data) { // fetchData handles unauthorized, so this is for other errors
            statusDiv.textContent = 'An unexpected error occurred during generation.';
            return;
        }

        if (data.status === 'success') {
            statusDiv.textContent = `Generation complete! Found ${data.results.length} optimized options.`;
            renderResults(data.results);
        } else {
            statusDiv.textContent = `Error: ${data.message}`;
            resultsContainer.innerHTML = `<div class="alert alert-warning mt-3">Error generating timetable: ${data.message}. Please ensure you have added rooms, batches, subjects (with hours), and faculty (with assigned subjects) in the "Manage Data" section.</div>`;
        }
    });
}

function renderResults(results) {
    const container = document.getElementById('results-container');
container.innerHTML = ''; // Clear previous results
    
    if (results.length === 0) {
        container.innerHTML = '<div class="alert alert-info">No timetables could be generated with the current constraints and data. Please adjust your inputs.</div>';
        return;
    }

    results.forEach(result => {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'mb-5 card'; // Add card styling
        resultDiv.innerHTML = `
            <div class="card-header">
                <h4 class="mb-0">Option ${result.option} <span class="badge bg-secondary ms-2">Fitness Score: ${result.fitness}</span></h4>
            </div>
            <div class="card-body">
                <p>${result.fitness === 0 ? '<span class="text-success fw-bold">This is a perfect timetable with no hard conflicts.</span>' : '<span class="text-warning">This timetable has some soft conflicts. Review carefully.</span>'}</p>
                <div id="timetable-option-${result.option}"></div>
            </div>
        `;
        container.appendChild(resultDiv);
        renderTimetable(result.timetable, `timetable-option-${result.option}`);
    });
}

function renderTimetable(timetableData, containerId) {
    const container = document.getElementById(containerId);
    
    // These should ideally come from the backend's configuration
    const timeslots = ["9-10", "10-11", "11-12", "1-2", "2-3"];
    const days = ["Mon", "Tue", "Wed", "Thu", "Fri"];
    
    // Get unique batches from the generated timetable data
    const batches = [...new Set(timetableData.map(g => g.batch))].sort();

    let html = '';
    if (batches.length === 0) {
        html = '<div class="alert alert-warning">No batches found in the generated timetable.</div>';
    } else {
        batches.forEach(batch => {
            html += `<h5 class="mt-4 mb-3">Timetable for Batch: <span class="badge bg-info">${batch}</span></h5>`;
            html += '<div class="table-responsive"><table class="table table-bordered table-sm">';
            html += '<thead><tr><th>Time</th>';
            days.forEach(day => html += `<th>${day}</th>`);
            html += '</tr></thead><tbody>';

            timeslots.forEach(slot => {
                html += `<tr><td><b>${slot}</b></td>`;
                days.forEach(day => {
                    const classes = timetableData.filter(gene => gene.batch === batch && gene.day === day && gene.timeslot === slot);
                    let cellContent = classes.map(c => 
                        `<div><strong>${c.subject}</strong><br><small>${c.faculty}</small><br><small><i>${c.room}</i></small></div>`
                    ).join('<hr class="my-1">'); // Separate multiple classes in one slot
                    html += `<td>${cellContent}</td>`;
                });
                html += '</tr>';
            });
            html += '</tbody></table></div>';
        });
    }
    
    container.innerHTML = html;
}