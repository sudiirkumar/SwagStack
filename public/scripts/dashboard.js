document.addEventListener("DOMContentLoaded", function() {
    const isAdmin = document.getElementById('isAdmin');
    const logoutButton = document.getElementById('logout-button');
    const inventory = document.getElementById('inventory');
    const sales = document.getElementById('sales');
    const transactions = document.getElementById('transactions');
    const summary = document.getElementById('summary');
    const reports = document.getElementById('reports');
    const users = document.getElementById('users');

    const name = localStorage.getItem('name');
    const is_admin = localStorage.getItem('isAdmin');

    if (is_admin === '1') {
        isAdmin.innerHTML = `Admin`;
        isAdmin.style.background = 'red';
        isAdmin.style.color = 'white';
        reports.classList.remove('hidden');
        users.classList.remove('hidden');

    } else {
        isAdmin.innerHTML = `User`;
    }

    inventory.addEventListener('click', function() {
        window.location.href = 'inventory.html';
    });
})