const API_URL = 'http://localhost:8000';
let chartInstance = null;

async function fetchBudget() {
    const month = document.getElementById('budget-month').value || '2025-06';
    try {
        const response = await fetch(`${API_URL}/budgets/${month}`);
        const data = await response.json();
        document.getElementById('current-budget').textContent = `${data.amount.toFixed(2)} €`;
    } catch (error) {
        document.getElementById('current-budget').textContent = '0 €';
    }
}

async function fetchBalance() {
    const month = document.getElementById('budget-month').value || '2025-06';
    const response = await fetch(`${API_URL}/balance/${month}`);
    const data = await response.json();
    document.getElementById('balance').textContent = `${data.balance.toFixed(2)} €`;
}

async function fetchTransactions(startDate = '', endDate = '') {
    let url = `${API_URL}/transactions/`;
    if (startDate && endDate) {
        url += `?start_date=${startDate}&end_date=${endDate}`;
    }
    const response = await fetch(url);
    const transactions = await response.json();
    const list = document.getElementById('transaction-list');
    list.innerHTML = '';
    transactions.forEach(t => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="p-2">${t.type === 'income' ? 'Revenu' : 'Dépense'}</td>
            <td class="p-2">${t.amount.toFixed(2)} €</td>
            <td class="p-2">${t.category}</td>
            <td class="p-2">${t.date.split('T')[0]}</td>
            <td class="p-2">${t.tags || ''}</td>
            <td class="p-2">
                <button onclick="editTransaction(${t.id})" class="bg-blue-500 text-white p-1 rounded mr-1">Modifier</button>
                <button onclick="deleteTransaction(${t.id})" class="bg-red-500 text-white p-1 rounded">Supprimer</button>
            </td>
        `;
        list.appendChild(tr);
    });
    updateChart(transactions);
}

async function deleteTransaction(id) {
    await fetch(`${API_URL}/transactions/${id}`, { method: 'DELETE' });
    fetchBalance();
    fetchTransactions();
}

async function editTransaction(id) {
    const transaction = await (await fetch(`${API_URL}/transactions/?skip=${id - 1}&limit=1`)).json();
    if (transaction.length) {
        const t = transaction[0];
        document.getElementById('transaction-type').value = t.type;
        document.getElementById('transaction-amount').value = t.amount;
        document.getElementById('transaction-category').value = t.category;
        document.getElementById('transaction-date').value = t.date.split('T')[0];
        document.getElementById('transaction-tags').value = t.tags || '';
        document.getElementById('transaction-form').onsubmit = async (e) => {
            e.preventDefault();
            await updateTransaction(id);
        };
    }
}

async function updateTransaction(id) {
    const transaction = {
        type: document.getElementById('transaction-type').value,
        amount: parseFloat(document.getElementById('transaction-amount').value),
        category: document.getElementById('transaction-category').value,
        date: document.getElementById('transaction-date').value,
        tags: document.getElementById('transaction-tags').value
    };
    await fetch(`${API_URL}/transactions/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(transaction)
    });
    fetchBalance();
    fetchTransactions();
    document.getElementById('transaction-form').reset();
    document.getElementById('transaction-form').onsubmit = handleTransactionSubmit;
}

async function fetchReminders() {
    const response = await fetch(`${API_URL}/reminders/`);
    const reminders = await response.json();
    const list = document.getElementById('reminders-list');
    list.innerHTML = reminders.length ? '' : '<li>Aucun rappel dû.</li>';
    reminders.forEach(r => {
        const li = document.createElement('li');
        li.textContent = `${r.description}: ${r.amount.toFixed(2)} € dû le ${new Date(r.due_date).toLocaleString()}`;
        list.appendChild(li);
    });
}

function updateChart(transactions) {
    const categories = [...new Set(transactions.filter(t => t.type === 'expense').map(t => t.category))];
    const data = categories.map(cat => 
        transactions
            .filter(t => t.category === cat && t.type === 'expense')
            .reduce((sum, t) => sum + t.amount, 0)
    );

    const ctx = document.getElementById('expense-chart').getContext('2d');
    if (chartInstance) chartInstance.destroy();
    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: categories,
            datasets: [{
                label: 'Dépenses par catégorie',
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

async function handleBudgetSubmit(e) {
    e.preventDefault();
    const month = document.getElementById('budget-month').value;
    const amount = parseFloat(document.getElementById('budget-amount').value);
    await fetch(`${API_URL}/budgets/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ month, amount })
    });
    fetchBudget();
    fetchBalance();
    document.getElementById('budget-form').reset();
}

async function handleTransactionSubmit(e) {
    e.preventDefault();
    const transaction = {
        type: document.getElementById('transaction-type').value,
        amount: parseFloat(document.getElementById('transaction-amount').value),
        category: document.getElementById('transaction-category').value,
        date: document.getElementById('transaction-date').value,
        tags: document.getElementById('transaction-tags').value
    };
    await fetch(`${API_URL}/transactions/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(transaction)
    });
    fetchBalance();
    fetchTransactions();
    document.getElementById('transaction-form').reset();
}

async function handleReminderSubmit(e) {
    e.preventDefault();
    const reminder = {
        description: document.getElementById('reminder-description').value,
        amount: parseFloat(document.getElementById('reminder-amount').value),
        due_date: new Date(document.getElementById('reminder-due-date').value).toISOString()
    };
    await fetch(`${API_URL}/reminders/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(reminder)
    });
    fetchReminders();
    document.getElementById('reminder-form').reset();
}

async function handleFilterSubmit(e) {
    e.preventDefault();
    const startDate = document.getElementById('filter-start').value;
    const endDate = document.getElementById('filter-end').value;
    fetchTransactions(startDate, endDate);
}

async function handleExportPDF() {
    const month = document.getElementById('budget-month').value || '2025-06';
    const response = await fetch(`${API_URL}/report/${month}`);
    const data = await response.json();
    alert(data.message); // Note : En local, le PDF est généré côté serveur. Pour le téléchargement, il faudrait une URL publique.
}

document.getElementById('budget-form').addEventListener('submit', handleBudgetSubmit);
document.getElementById('transaction-form').addEventListener('submit', handleTransactionSubmit);
document.getElementById('reminder-form').addEventListener('submit', handleReminderSubmit);
document.getElementById('filter-form').addEventListener('submit', handleFilterSubmit);
document.getElementById('export-pdf').addEventListener('click', handleExportPDF);

document.addEventListener('DOMContentLoaded', () => {
    fetchBudget();
    fetchBalance();
    fetchTransactions();
    fetchReminders();
});