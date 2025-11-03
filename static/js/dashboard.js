// Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Load statistics
    loadStats();
    
    // Auto-refresh stats every 5 minutes
    setInterval(loadStats, 300000);
});

function loadStats(period = 30) {
    fetch(`/api/stats?period=${period}`)
        .then(response => response.json())
        .then(data => {
            updateStatsDisplay(data);
        })
        .catch(error => {
            console.error('Error loading stats:', error);
        });
}

function updateStatsDisplay(data) {
    // Update any dynamic stat displays
    console.log('Stats loaded:', data);
    
    // You can add code here to update charts or other dynamic elements
    // For example, using Chart.js or Plotly
}

// Filter functionality for volunteers list
const departmentFilter = document.getElementById('department-filter');
if (departmentFilter) {
    departmentFilter.addEventListener('change', function() {
        const department = this.value;
        const status = document.getElementById('status-filter').value;
        window.location.href = `/dashboard/volunteers?department=${department}&status=${status}`;
    });
}

const statusFilter = document.getElementById('status-filter');
if (statusFilter) {
    statusFilter.addEventListener('change', function() {
        const status = this.value;
        const department = document.getElementById('department-filter').value;
        window.location.href = `/dashboard/volunteers?department=${department}&status=${status}`;
    });
}

// Sortable tables
function sortTable(table, column, asc = true) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    rows.sort((a, b) => {
        const aValue = a.children[column].textContent.trim();
        const bValue = b.children[column].textContent.trim();
        
        if (!isNaN(aValue) && !isNaN(bValue)) {
            return asc ? aValue - bValue : bValue - aValue;
        }
        
        return asc 
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
    });
    
    rows.forEach(row => tbody.appendChild(row));
}

// Add click handlers to table headers for sorting
const tableHeaders = document.querySelectorAll('.data-table th');
tableHeaders.forEach((header, index) => {
    header.style.cursor = 'pointer';
    header.addEventListener('click', function() {
        const table = this.closest('table');
        const currentAsc = this.classList.contains('asc');
        
        // Remove sort indicators from all headers
        tableHeaders.forEach(h => {
            h.classList.remove('asc', 'desc');
        });
        
        // Add sort indicator to current header
        this.classList.add(currentAsc ? 'desc' : 'asc');
        
        sortTable(table, index, !currentAsc);
    });
});
