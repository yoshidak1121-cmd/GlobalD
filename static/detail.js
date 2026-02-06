let currentMachine = null;

async function loadMachineDetail(machineId) {
    try {
        const response = await fetch(`/api/machines/${machineId}`);
        if (!response.ok) {
            let errorMessage;
            if (response.status === 404) {
                errorMessage = 'Machine not found (404).';
            } else if (response.status >= 500) {
                errorMessage = 'Server error while loading machine. Please try again later.';
            } else {
                errorMessage = `Error loading machine (status ${response.status} ${response.statusText || ''}).`;
            }
            document.getElementById('machineHeader').innerHTML = `<div class="no-results">${errorMessage}</div>`;
            return;
        }

        currentMachine = await response.json();
        displayMachineHeader();
        switchTab('machine');
    } catch (error) {
        let errorMessage = 'Unexpected error while loading machine.';
        if (error && (error.name === 'TypeError' || (typeof error.message === 'string' && error.message.toLowerCase().includes('network')))) {
            errorMessage = 'Network error while loading machine. Please check your connection and try again.';
        }
        document.getElementById('machineHeader').innerHTML = `<div class="no-results">${errorMessage}</div>`;
        console.error('Load error:', error);
    }
}

function createInfoItem(label, value) {
    const itemDiv = document.createElement('div');
    itemDiv.className = 'info-item';

    const labelDiv = document.createElement('div');
    labelDiv.className = 'info-label';
    labelDiv.textContent = label;

    const valueDiv = document.createElement('div');
    valueDiv.className = 'info-value';
    valueDiv.textContent = value || '-';

    itemDiv.appendChild(labelDiv);
    itemDiv.appendChild(valueDiv);

    return itemDiv;
}

function displayMachineHeader() {
    const headerDiv = document.getElementById('machineHeader');
    headerDiv.innerHTML = '';

    const heading = document.createElement('h2');
    heading.textContent = `Machine: ${currentMachine.machine_no}`;
    headerDiv.appendChild(heading);

    const infoContainer = document.createElement('div');
    infoContainer.className = 'header-info';

    infoContainer.appendChild(createInfoItem('Model', currentMachine.model));
    infoContainer.appendChild(createInfoItem('Serial No', currentMachine.serial_no));
    infoContainer.appendChild(createInfoItem('Created', currentMachine.created_at));
    infoContainer.appendChild(createInfoItem('Updated', currentMachine.updated_at));

    headerDiv.appendChild(infoContainer);
}

function switchTab(tabName) {
    // Update tab buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(button => {
        const buttonTab = button.getAttribute('data-tab');
        if (buttonTab === tabName) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });
    
    // Display content
    const contentDiv = document.getElementById('tabContent');
    
    switch(tabName) {
        case 'machine':
            displayMachineTab();
            break;
        case 'nc':
            displayNCTab();
            break;
        case 'contract':
            displayContractTab();
            break;
        case 'sales':
            displaySalesTab();
            break;
        case 'dealer':
            displayDealerTab();
            break;
        case 'ship':
            displayShipTab();
            break;
        case 'install':
            displayInstallTab();
            break;
        case 'enduser':
            displayEndUserTab();
            break;
        case 'service':
            displayServiceTab();
            break;
    }
}

function displayMachineTab() {
    const contentDiv = document.getElementById('tabContent');
    let html = '<div class="detail-grid">';
    html += `<div class="detail-item"><div class="detail-label">Machine No</div><div class="detail-value">${currentMachine.machine_no || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Model</div><div class="detail-value">${currentMachine.model || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Serial No</div><div class="detail-value">${currentMachine.serial_no || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Created At</div><div class="detail-value">${currentMachine.created_at || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Updated At</div><div class="detail-value">${currentMachine.updated_at || '-'}</div></div>`;
    html += '</div>';
    contentDiv.innerHTML = html;
}

function displayNCTab() {
    const contentDiv = document.getElementById('tabContent');
    const nc = currentMachine.nc;
    
    if (!nc) {
        contentDiv.innerHTML = '<div class="empty-state">No NC data available</div>';
        return;
    }
    
    let html = '<div class="detail-grid">';
    html += `<div class="detail-item"><div class="detail-label">NC Maker</div><div class="detail-value">${nc.nc_maker || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">NC Model</div><div class="detail-value">${nc.nc_model || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">NC Serial</div><div class="detail-value">${nc.nc_serial || '-'}</div></div>`;
    html += '</div>';
    contentDiv.innerHTML = html;
}

function displayContractTab() {
    const contentDiv = document.getElementById('tabContent');
    const contract = currentMachine.contract;
    
    if (!contract) {
        contentDiv.innerHTML = '<div class="empty-state">No contract data available</div>';
        return;
    }
    
    let html = '<div class="detail-grid">';
    html += `<div class="detail-item"><div class="detail-label">Contract No</div><div class="detail-value">${contract.contract_no || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Contract Date</div><div class="detail-value">${contract.contract_date || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Contract Type</div><div class="detail-value">${contract.contract_type || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Memo</div><div class="detail-value">${contract.memo || '-'}</div></div>`;
    html += '</div>';
    contentDiv.innerHTML = html;
}

function displaySalesTab() {
    const contentDiv = document.getElementById('tabContent');
    const sales = currentMachine.sales;
    
    if (!sales) {
        contentDiv.innerHTML = '<div class="empty-state">No sales data available</div>';
        return;
    }
    
    let html = '<div class="detail-grid">';
    html += `<div class="detail-item"><div class="detail-label">Sales Date</div><div class="detail-value">${sales.sales_date || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Sales Person</div><div class="detail-value">${sales.sales_person || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Sales Amount</div><div class="detail-value">${sales.sales_amount != null ? '¥' + sales.sales_amount.toLocaleString() : '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Memo</div><div class="detail-value">${sales.memo || '-'}</div></div>`;
    html += '</div>';
    contentDiv.innerHTML = html;
}

function displayDealerTab() {
    const contentDiv = document.getElementById('tabContent');
    const dealer = currentMachine.dealer;
    
    if (!dealer) {
        contentDiv.innerHTML = '<div class="empty-state">No dealer data available</div>';
        return;
    }
    
    let html = '<div class="detail-grid">';
    html += `<div class="detail-item"><div class="detail-label">Dealer Name</div><div class="detail-value">${dealer.dealer_name || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Country</div><div class="detail-value">${dealer.dealer_country || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Contact Person</div><div class="detail-value">${dealer.contact_person || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Phone</div><div class="detail-value">${dealer.phone || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Email</div><div class="detail-value">${dealer.email || '-'}</div></div>`;
    html += '</div>';
    contentDiv.innerHTML = html;
}

function displayShipTab() {
    const contentDiv = document.getElementById('tabContent');
    const ship = currentMachine.ship;
    
    if (!ship) {
        contentDiv.innerHTML = '<div class="empty-state">No shipping data available</div>';
        return;
    }
    
    let html = '<div class="detail-grid">';
    html += `<div class="detail-item"><div class="detail-label">Ship Date</div><div class="detail-value">${ship.ship_date || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Ship Method</div><div class="detail-value">${ship.ship_method || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Tracking No</div><div class="detail-value">${ship.tracking_no || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Destination</div><div class="detail-value">${ship.destination || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Memo</div><div class="detail-value">${ship.memo || '-'}</div></div>`;
    html += '</div>';
    contentDiv.innerHTML = html;
}

function displayInstallTab() {
    const contentDiv = document.getElementById('tabContent');
    const install = currentMachine.install;
    
    if (!install) {
        contentDiv.innerHTML = '<div class="empty-state">No installation data available</div>';
        return;
    }
    
    let html = '<div class="detail-grid">';
    html += `<div class="detail-item"><div class="detail-label">Install Date</div><div class="detail-value">${install.install_date || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Installer</div><div class="detail-value">${install.installer || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Location</div><div class="detail-value">${install.location || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Memo</div><div class="detail-value">${install.memo || '-'}</div></div>`;
    html += '</div>';
    contentDiv.innerHTML = html;
}

function displayEndUserTab() {
    const contentDiv = document.getElementById('tabContent');
    const endUser = currentMachine.end_user;
    
    if (!endUser) {
        contentDiv.innerHTML = '<div class="empty-state">No end user data available</div>';
        return;
    }
    
    let html = '<div class="detail-grid">';
    html += `<div class="detail-item"><div class="detail-label">Company Name</div><div class="detail-value">${endUser.company_name || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Country</div><div class="detail-value">${endUser.country || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Contact Person</div><div class="detail-value">${endUser.contact_person || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Phone</div><div class="detail-value">${endUser.phone || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Email</div><div class="detail-value">${endUser.email || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Address</div><div class="detail-value">${endUser.address || '-'}</div></div>`;
    html += '</div>';
    contentDiv.innerHTML = html;
}

function displayServiceTab() {
    const contentDiv = document.getElementById('tabContent');
    const serviceBase = currentMachine.service_base;
    
    if (!serviceBase) {
        contentDiv.innerHTML = '<div class="empty-state">No service base data available</div>';
        return;
    }
    
    let html = '<div class="detail-grid">';
    html += `<div class="detail-item"><div class="detail-label">Base Name</div><div class="detail-value">${serviceBase.base_name || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Country</div><div class="detail-value">${serviceBase.country || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Contact Person</div><div class="detail-value">${serviceBase.contact_person || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Phone</div><div class="detail-value">${serviceBase.phone || '-'}</div></div>`;
    html += `<div class="detail-item"><div class="detail-label">Email</div><div class="detail-value">${serviceBase.email || '-'}</div></div>`;
    html += '</div>';
    contentDiv.innerHTML = html;
}
