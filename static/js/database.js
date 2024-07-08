// Function to update records
function updateRecord(table, id) {
    const row = event.target.closest('tr');
    const data = {};
    row.querySelectorAll('td[contenteditable="true"]').forEach((cell) => {
        data[cell.getAttribute('data-name')] = cell.innerText;
    });

    fetch(`/update_record/${table}/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        const queryResult = document.getElementById('query-result');
        if (result.success) {
            queryResult.innerText = `Record with ID ${id} updated successfully.`;
        } else {
            queryResult.innerText = `Failed to update record with ID ${id}. Error: ${result.error}`;
        }
    })
    .catch(error => {
        console.error('Error updating record:', error);
        const queryResult = document.getElementById('query-result');
        queryResult.innerText = `An error occurred while updating record with ID ${id}.`;
    });
}

// Function to delete records
function deleteRecord(table, recordId) {
    fetch(`/delete_record/${table}/${recordId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Record deleted successfully.');
            // Optionally refresh or update the page to reflect changes
            location.reload();
        } else {
            alert('Failed to delete record: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to execute SQL queries
function executeQuery(queryKey) {
    console.log('Executing query:', queryKey);
    fetch('/execute-query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query_name: queryKey })
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Query result:', data);
        const resultContainer = document.getElementById('query-result');
        if (data.success) {
            resultContainer.innerHTML = '<pre>' + JSON.stringify(data.rows, null, 2) + '</pre>';
        } else {
            resultContainer.innerHTML = '<pre>Error: ' + data.error + '</pre>';
        }
    })
    .catch(error => {
        console.error('Error executing query:', error);
        const resultContainer = document.getElementById('query-result');
        resultContainer.innerHTML = '<pre>Error: ' + error + '</pre>';
    });
}

// Function to display query results on the webpage
function displayResults(results) {
    const resultContainer = document.getElementById('query-result');
    resultContainer.innerHTML = ''; // Clear previous results

    if (!results.success) {
        resultContainer.innerHTML = `<p>Error: ${results.error}</p>`;
        return;
    }

    if (results.data.length === 0) {
        resultContainer.innerHTML = '<p>No results found.</p>';
        return;
    }

    // Build HTML for displaying results dynamically based on the first row's keys
    let html = '<table>';
    html += '<tr>';
    Object.keys(results.data[0]).forEach(key => {
        html += `<th>${key}</th>`;
    });
    html += '</tr>';

    results.data.forEach(row => {
        html += '<tr>';
        Object.values(row).forEach(value => {
            html += `<td>${value}</td>`;
        });
        html += '</tr>';
    });

    html += '</table>';

    resultContainer.innerHTML = html;
}