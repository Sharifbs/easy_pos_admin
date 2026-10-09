// Stock Inventory List Renderer
function renderStockTable() {
  const tableBody = document.getElementById('stock-table-body');
  if (!tableBody) return;

  let stock = JSON.parse(localStorage.getItem('pos_stock') || '[]');

  if (stock.length === 0) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="3" class="p-3 text-center text-slate-500">No stock data available</td>
      </tr>`;
    return;
  }

  tableBody.innerHTML = stock.map(item => `
    <tr class="border-b hover:bg-slate-50">
      <td class="p-3 font-semibold text-slate-700">${item.name}</td>
      <td class="p-3 text-slate-600">${item.qty}</td>
      <td class="p-3 text-slate-600">৳ ${item.price}</td>
    </tr>
  `).join('');

  const dashStockCount = document.getElementById('dash-stock');
  if (dashStockCount) {
    dashStockCount.innerText = stock.length;
  }
}