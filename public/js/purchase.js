// Purchase Entry Management
function addPurchase() {
  const supplier = document.getElementById('pur-supplier').value.trim();
  const item = document.getElementById('pur-item').value.trim();
  const qty = parseFloat(document.getElementById('pur-qty').value) || 0;
  const cost = parseFloat(document.getElementById('pur-cost').value) || 0;

  if (!supplier || !item || qty <= 0) {
    alert("Please fill in Supplier Name, Item Name, and Quantity.");
    return;
  }

  let stock = JSON.parse(localStorage.getItem('pos_stock') || '[]');
  const existingIndex = stock.findIndex(i => i.name.toLowerCase() === item.toLowerCase());

  if (existingIndex > -1) {
    stock[existingIndex].qty += qty;
    stock[existingIndex].price = cost;
  } else {
    stock.push({ name: item, qty: qty, price: cost });
  }

  localStorage.setItem('pos_stock', JSON.stringify(stock));
  alert(`Purchase Saved successfully for ${item}! Stock updated.`);

  document.getElementById('pur-supplier').value = '';
  document.getElementById('pur-item').value = '';
  document.getElementById('pur-qty').value = '';
  document.getElementById('pur-cost').value = '';

  if (typeof renderStockTable === 'function') {
    renderStockTable();
  }
}