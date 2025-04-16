
async function loadCustomer() {
  const tbody = document.getElementById('product-table-body');
  tbody.innerHTML = '';

  const name = localStorage.getItem('name');
  // if(!name){
  //     // alert("Please login first");
  //     // window.location.href = 'index.html';
  //     // return;
  // }

  try {
    const res = await fetch('http://127.0.0.1:5000/api/customer');
    if (!res.ok) throw new Error('Fetch failed');
    const customers = await res.json();

    customers.forEach(p => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${p[0]}</td><td>${p[1]}</td><td>${p[2]}</td><td>${p[3]}</td><td>${p[4]}</td>
        <td>
          <button class="edit-btn" onclick="editCustomer(${p[0]})">Edit</button>
          <button class="delete-btn" onclick="deleteCustomer(${p[0]})">Delete</button>
        </td>
      `;
      tbody.appendChild(row);
    });
  } catch (err) {
    console.error(err);
    tbody.innerHTML = '<tr><td colspan="7">Failed to load customer.</td></tr>';
  }
}

function editCustomer(id) {
  fetch(`http://127.0.0.1:5000/api/customer/${id}`)
    .then(res => res.json())
    .then(p => {
      document.getElementById('editProductId').value = p.customer_id;
      document.getElementById('editName').value = p.customer_name;
      document.getElementById('editCategory').value = p.email;
      document.getElementById('editPrice').value = p.phone;
      document.getElementById('editQuantity').value = p.address;
      document.getElementById('editModal').style.display = 'block';
    })
    .catch(() => alert('Could not load customer details.'));
}

function openAddProductModal() {
  ['editProductId','editName','editCategory','editPrice','editQuantity'].forEach(id =>
    document.getElementById(id).value = ''
  );
  document.getElementById('editModal').style.display = 'block';
}

function closeEditModal() {
  document.getElementById('editModal').style.display = 'none';
}

document.getElementById('editProductForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const id = document.getElementById('editProductId').value;
  const data = {
    customer_name: document.getElementById('editName').value,
    email: document.getElementById('editCategory').value,
    phone: parseFloat(document.getElementById('editPrice').value),
    address: parseInt(document.getElementById('editQuantity').value)
  };

  const url = id ? `http://127.0.0.1:5000/api/updateCustomer/${id}` : 'http://127.0.0.1:5000/api/addCustomer';
  const method = id ? 'PUT' : 'POST';

  fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
    .then(res => {
      if (res.ok) {
        alert(`Customer ${id ? 'updated' : 'added'} successfully!`);
        closeEditModal();
        loadCustomer();
      } else {
        alert(`Failed to ${id ? 'update' : 'add'} customer.`);
      }
    })
    .catch(err => console.error('Error:', err));
});

async function deleteCustomer(id) {
  if (confirm(`Delete customer ID ${id}?`)) {
    try {
      const res = await fetch(`http://127.0.0.1:5000/api/deleteCustomer/${id}`, { method: 'DELETE' });
      if (res.ok) {
        alert(`Customer ${id} deleted.`);
        loadCustomer();
      } else {
        alert('Delete failed.');
      }
    } catch (e) {
      console.error('Error:', e);
      alert('Error deleting customer.');
    }
  }
}

window.onload = loadCustomer;
