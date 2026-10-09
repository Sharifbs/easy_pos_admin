// Accounts and Ledger Management
function addAccountEntry() {
  const type = document.getElementById('acc-type').value;
  const desc = document.getElementById('acc-desc').value.trim();
  const amount = parseFloat(document.getElementById('acc-amount').value) || 0;

  if (!desc || amount <= 0) {
    alert("Please enter a valid description and amount.");
    return;
  }

  let ledger = JSON.parse(localStorage.getItem('pos_ledger') || '[]');
  ledger.push({ type, desc, amount, date: new Date().toLocaleDateString() });
  localStorage.setItem('pos_ledger', JSON.stringify(ledger));

  alert(`${type} Entry Recorded Successfully!`);

  document.getElementById('acc-desc').value = '';
  document.getElementById('acc-amount').value = '';

  updateAccountsDashboard();
}

function updateAccountsDashboard() {
  let ledger = JSON.parse(localStorage.getItem('pos_ledger') || '[]');
  let totalReceipts = 0;
  let totalExpense = 0;

  ledger.forEach(entry => {
    if (entry.type === 'Receipt') totalReceipts += entry.amount;
    if (entry.type === 'Expense') totalExpense += entry.amount;
  });

  const receiptEl = document.getElementById('dash-receipts');
  const expenseEl = document.getElementById('dash-expense');

  if (receiptEl) receiptEl.innerText = '৳ ' + totalReceipts;
  if (expenseEl) expenseEl.innerText = '৳ ' + totalExpense;
}