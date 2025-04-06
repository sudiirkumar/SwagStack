async function loadProducts() {
    const tbody = document.getElementById('product-table-body');
    tbody.innerHTML = '';
  
    try {
      const res = await fetch('http://127.0.0.1:5000/api/products');
      if (!res.ok) throw new Error('Fetch failed');
      const products = await res.json();
  
      products.forEach(p => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${p[0]}</td><td>${p[1]}</td><td>${p[2]}</td><td>₹${p[3]}</td><td>${p[4]}</td>
          <td>${formatDate(p[6])}</td>
          <td>
            <button class="edit-btn" onclick="editProduct(${p[0]})">Edit</button>
            <button class="delete-btn" onclick="deleteProduct(${p[0]})">Delete</button>
          </td>
        `;
        tbody.appendChild(row);
      });
    } catch (err) {
      console.error(err);
      tbody.innerHTML = '<tr><td colspan="7">Failed to load products.</td></tr>';
    }
  }
  
  function formatDate(str) {
    return new Date(str).toLocaleDateString('en-IN', {
      year: 'numeric', month: 'short', day: 'numeric'
    });
  }
  
  function editProduct(id) {
    fetch(`http://127.0.0.1:5000/api/product/${id}`)
      .then(res => res.json())
      .then(p => {
        document.getElementById('editProductId').value = p.product_id;
        document.getElementById('editName').value = p.product_name;
        document.getElementById('editCategory').value = p.category;
        document.getElementById('editPrice').value = p.price;
        document.getElementById('editQuantity').value = p.stock_quantity;
        document.getElementById('editModal').style.display = 'block';
      })
      .catch(() => alert('Could not load product details.'));
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
      product_name: document.getElementById('editName').value,
      category: document.getElementById('editCategory').value,
      price: parseFloat(document.getElementById('editPrice').value),
      stock_quantity: parseInt(document.getElementById('editQuantity').value)
    };
  
    const url = id ? `http://127.0.0.1:5000/api/updateProduct/${id}` : 'http://127.0.0.1:5000/api/addProduct';
    const method = id ? 'PUT' : 'POST';
  
    fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
      .then(res => {
        if (res.ok) {
          alert(`Product ${id ? 'updated' : 'added'} successfully!`);
          closeEditModal();
          loadProducts();
        } else {
          alert(`Failed to ${id ? 'update' : 'add'} product.`);
        }
      })
      .catch(err => console.error('Error:', err));
  });
  
  async function deleteProduct(id) {
    if (confirm(`Delete product ID ${id}?`)) {
      try {
        const res = await fetch(`http://127.0.0.1:5000/api/deleteProduct/${id}`, { method: 'DELETE' });
        if (res.ok) {
          alert(`Product ${id} deleted.`);
          loadProducts();
        } else {
          alert('Delete failed.');
        }
      } catch (e) {
        console.error('Error:', e);
        alert('Error deleting product.');
      }
    }
  }
  
  window.onload = loadProducts;
  