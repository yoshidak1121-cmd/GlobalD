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
    
    let html = '<table class="results-table">';
    html += '<thead><tr>';
    html += '<th>Machine No</th>';
    html += '<th>Model</th>';
    html += '<th>Serial No</th>';
    html += '<th>NC Maker</th>';
    html += '<th>Contract No</th>';
    html += '<th>Dealer</th>';
    html += '<th>End User</th>';
    html += '<th>Location</th>';
    html += '</tr></thead><tbody>';
    
    machines.forEach(machine => {
        html += '<tr>';
        html += `<td><a href="/detail/${machine.id}" class="machine-link">${machine.machine_no || '-'}</a></td>`;
        html += `<td>${machine.model || '-'}</td>`;
        html += `<td>${machine.serial_no || '-'}</td>`;
        html += `<td>${machine.nc_maker || '-'}</td>`;
        html += `<td>${machine.contract_no || '-'}</td>`;
        html += `<td>${machine.dealer_name || '-'}</td>`;
        html += `<td>${machine.end_user_company || '-'}</td>`;
        html += `<td>${machine.location || '-'}</td>`;
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    resultsDiv.innerHTML = html;
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
