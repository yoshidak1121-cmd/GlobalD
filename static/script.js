// Search functionality
async function performSearch() {
    const searchInput = document.getElementById('searchInput');
    const query = searchInput.value.trim();
    
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<div class="loading">Searching...</div>';
    
    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.machines && data.machines.length > 0) {
            displayResults(data.machines);
        } else {
            resultsDiv.innerHTML = '<div class="no-results">No machines found</div>';
        }
    } catch (error) {
        resultsDiv.innerHTML = '<div class="no-results">Error loading results</div>';
        console.error('Search error:', error);
    }
}

function displayResults(machines) {
    const resultsDiv = document.getElementById('results');

    // Clear previous results
    resultsDiv.innerHTML = '';

    // Create table structure
    const table = document.createElement('table');
    table.className = 'results-table';

    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    const headers = [
        'Machine No',
        'Model',
        'Serial No',
        'NC Maker',
        'Contract No',
        'Dealer',
        'End User',
        'Location'
    ];

    headers.forEach(text => {
        const th = document.createElement('th');
        th.textContent = text;
        headerRow.appendChild(th);
    });

    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');

    machines.forEach(machine => {
        const tr = document.createElement('tr');

        // Machine No with link
        const tdMachineNo = document.createElement('td');
        const link = document.createElement('a');
        const idValue = machine.id != null ? String(machine.id) : '';
        link.href = '/detail/' + encodeURIComponent(idValue);
        link.className = 'machine-link';
        link.textContent = machine.machine_no || '-';
        tdMachineNo.appendChild(link);
        tr.appendChild(tdMachineNo);

        // Model
        const tdModel = document.createElement('td');
        tdModel.textContent = machine.model || '-';
        tr.appendChild(tdModel);

        // Serial No
        const tdSerial = document.createElement('td');
        tdSerial.textContent = machine.serial_no || '-';
        tr.appendChild(tdSerial);

        // NC Maker
        const tdNcMaker = document.createElement('td');
        tdNcMaker.textContent = machine.nc_maker || '-';
        tr.appendChild(tdNcMaker);

        // Contract No
        const tdContract = document.createElement('td');
        tdContract.textContent = machine.contract_no || '-';
        tr.appendChild(tdContract);

        // Dealer
        const tdDealer = document.createElement('td');
        tdDealer.textContent = machine.dealer_name || '-';
        tr.appendChild(tdDealer);

        // End User
        const tdEndUser = document.createElement('td');
        tdEndUser.textContent = machine.end_user_company || '-';
        tr.appendChild(tdEndUser);

        // Location
        const tdLocation = document.createElement('td');
        tdLocation.textContent = machine.location || '-';
        tr.appendChild(tdLocation);

        tbody.appendChild(tr);
    });

    table.appendChild(tbody);
    resultsDiv.appendChild(table);
}

// Allow search on Enter key
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
});
