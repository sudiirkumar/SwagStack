document.addEventListener("DOMContentLoaded", function() {
    const isAdmin = document.getElementById('isAdmin');
    const logoutButton = document.getElementById('logout_btn');
    const inventory = document.getElementById('inventory');
    const sales = document.getElementById('sales');
    const transactions = document.getElementById('transactions');
    const users = document.getElementById('users');
    const customer = document.getElementById('customer');
    const transactions_div = document.getElementById('transactions_div');
    const users_div = document.getElementById('users_div');

    const name = localStorage.getItem('name');
    if(!name){
        alert("Please login first");
        window.location.href = 'index.html';
        return;
    }
    const is_admin = localStorage.getItem('isAdmin');

    if (is_admin === '1') {
        isAdmin.innerHTML = `Admin`;
        isAdmin.style.background = 'red';
        isAdmin.style.color = 'white';
        users_div.classList.remove('hidden');
        transactions_div.classList.remove('hidden');

    } else {
        isAdmin.innerHTML = `User`;
    }

    inventory.addEventListener('click', function() {
        window.location.href = 'inventory.html';
    });
    logoutButton.addEventListener('click', function() {
        localStorage.removeItem('name');
        localStorage.removeItem('isAdmin');
        window.location.href = 'index.html';
    }
    );
    sales.addEventListener('click', function() {
        window.location.href = 'manage_orders.html';
    });
    transactions.addEventListener('click', function() {
        window.location.href = 'transaction-log.html';
    });
    users.addEventListener('click', function() {
        window.location.href = 'manage_users.html';
    });
    customer.addEventListener('click', function() {
        window.location.href = 'manage-customer.html';
    });

})