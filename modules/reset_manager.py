import os
import glob


def reset_customer_sheet(sheet_manager, cust_sheet_id):
    """Google Sheet-er shob tabs clear kore Sales, Purchase, Stock & Accounts schema setup korbe."""
    sh = sheet_manager.get_sheet_by_id(cust_sheet_id)

    tabs_schema = {
        "Sales": [
            ["Invoice No", "Date", "Customer Name", "Phone", "Item Name", "Qty", "Unit Price", "Total Bill", "Advance",
             "Received", "Due", "Status"]],
        "Purchase": [
            ["Purchase ID", "Date", "Supplier Name", "Item Name", "Qty", "Unit Cost", "Total Cost", "Paid Amount",
             "Due"]],
        "Stock": [["Item Name", "Total Purchase Qty", "Total Sales Qty", "Current Stock"]],
        "Accounts": [["Transaction ID", "Date", "Type", "Category", "Amount", "Balance", "Notes"]]
    }

    existing_worksheets = {ws.title: ws for ws in sh.worksheets()}

    for tab_name, headers in tabs_schema.items():
        if tab_name in existing_worksheets:
            ws = existing_worksheets[tab_name]
            ws.clear()
            ws.update('A1', headers)
        else:
            ws = sh.add_worksheet(title=tab_name, rows=100, cols=12)
            ws.update('A1', headers)

    for ws in sh.worksheets():
        if ws.title not in tabs_schema:
            try:
                sh.del_worksheet(ws)
            except Exception:
                pass

    print(f"[RESET OK] Google Sheet ({cust_sheet_id}) re-initialized.")


def clear_local_backups():
    """Local backups delete korbe."""
    files = glob.glob('backups/**/*.json', recursive=True) + glob.glob('backups/**/*.pdf', recursive=True)
    for f in files:
        try:
            os.remove(f)
        except Exception as e:
            print(f"Error deleting {f}: {e}")
    print("[RESET OK] All local backup files cleared.")