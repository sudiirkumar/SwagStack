document.addEventListener('DOMContentLoaded', () => {
    const name = localStorage.getItem('name');
    if(!name){
        alert("Please login first");
        window.location.href = 'index.html';
        return;
    }
    fetch('http://127.0.0.1:5000/api/transaction_log')
      .then(response => response.json())
      .then(data => {
        const tbody = document.getElementById('log-table-body');
        tbody.innerHTML = '';
  
        data.forEach(log => {
            console.log("Row data:", log);
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${log[0]}</td>
            <td>${log[1] ?? '-'}</td>
            <td>${log[2]}</td>
            <td>${log[3]}</td>
            <td>${log[4] ?? '-'}</td>
            <td>${log[5] ?? '-'}</td>
            <td>${new Date(log[6]).toLocaleString()}</td>
          `;
          tbody.appendChild(row);
        });
      })
      .catch(error => {
        console.error('Error fetching logs:', error);
      });
  });