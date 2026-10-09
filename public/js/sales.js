// Sales Calculation & COD Logic
function calcSaleTotal() {
  const qty = parseFloat(document.getElementById('sale-qty').value) || 0;
  const price = parseFloat(document.getElementById('sale-price').value) || 0;
  const advance = parseFloat(document.getElementById('sale-advance').value) || 0;
  const received = parseFloat(document.getElementById('sale-received').value) || 0;

  const totalBill = qty * price;
  const netPayable = Math.max(0, totalBill - advance);
  const currentDue = Math.max(0, netPayable - received);

  document.getElementById('sale-total-bill').innerText = totalBill + ' TK';
  document.getElementById('sale-net-payable').innerText = netPayable + ' TK';
  document.getElementById('sale-current-due').innerText = currentDue + ' TK';

  // COD Highlight
  const isCod = document.getElementById('sale-cod').checked;
  const codBadge = document.getElementById('cod-status-badge');
  if (codBadge) {
    codBadge.innerText = isCod ? 'YES (Cash on Delivery)' : 'NO';
  }
}

async function processSale() {
  const clientStore = document.getElementById('sale-client').value;
  const customer = document.getElementById('sale-customer').value;
  const phone = document.getElementById('sale-phone').value;
  const item = document.getElementById('sale-item').value;
  const qty = parseFloat(document.getElementById('sale-qty').value) || 0;
  const price = parseFloat(document.getElementById('sale-price').value) || 0;
  const advance = parseFloat(document.getElementById('sale-advance').value) || 0;
  const received = parseFloat(document.getElementById('sale-received').value) || 0;
  const isCod = document.getElementById('sale-cod').checked;

  const totalBill = qty * price;
  const netPayable = Math.max(0, totalBill - advance);
  const currentDue = Math.max(0, netPayable - received);

  if(!item || totalBill <= 0) {
    alert("Please enter a valid item, quantity, and price.");
    return;
  }

  // Create PDF Invoice using jsPDF
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  doc.setFontSize(16);
  doc.text("EASY POS - SALES INVOICE", 105, 15, null, null, "center");
  doc.setFontSize(10);
  doc.text(`Store: ${clientStore}`, 14, 25);
  doc.text(`Customer: ${customer} (${phone})`, 14, 32);
  doc.text(`Item: ${item} | Qty: ${qty} | Unit Price: ${price} TK`, 14, 39);
  doc.text(`--------------------------------------------------`, 14, 44);
  doc.text(`Total Bill: ${totalBill} TK`, 14, 50);
  doc.text(`Advance Paid: ${advance} TK`, 14, 57);
  doc.text(`Net Payable: ${netPayable} TK`, 14, 64);
  doc.text(`Received Amount: ${received} TK`, 14, 71);
  doc.text(`Current Due: ${currentDue} TK`, 14, 78);
  doc.text(`Payment Method: ${isCod ? 'Cash on Delivery (COD)' : 'Direct Payment'}`, 14, 85);

  const msg = encodeURIComponent(
    `*INVOICE DETAILS*\nStore: ${clientStore}\nCustomer: ${customer}\nItem: ${item}\nTotal: ${totalBill} TK\nNet Payable: ${netPayable} TK\nCurrent Due: ${currentDue} TK\nPayment: ${isCod ? 'Cash on Delivery (COD)' : 'Paid'}`
  );

  window.open(`https://wa.me/${phone ? '88' + phone : ''}?text=${msg}`, '_blank');
}