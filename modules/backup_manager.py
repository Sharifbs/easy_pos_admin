import json
import os
from datetime import datetime


class BackupManager:
    def __init__(self, sheet_manager, backup_dir="backups"):
        self.sm = sheet_manager
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)

    def backup_all_customers(self, customers):
        print("\n" + "=" * 60)
        print("  STARTING AUTOMATED DAILY LOCAL BACKUPS")
        print("=" * 60)

        today = datetime.now().strftime("%Y-%m-%d")

        for cust in customers:
            if not cust.get("active", True):
                continue

            cust_id = cust["id"]
            cust_name = cust["name"]

            # Directory for customer backups
            cust_dir = os.path.join(self.backup_dir, cust_id)
            os.makedirs(cust_dir, exist_ok=True)

            try:
                doc = self.sm.get_sheet_by_id(cust["sheet_id"])

                # Full multi-tab backup structure
                backup_payload = {
                    "customer_id": cust_id,
                    "customer_name": cust_name,
                    "backup_date": today,
                    "timestamp": datetime.now().isoformat(),
                    "sheets": {}
                }

                # Fetch all target worksheets
                for sheet_name in ["Sales", "Purchase", "Stock", "Accounts"]:
                    try:
                        ws = doc.worksheet(sheet_name)
                        backup_payload["sheets"][sheet_name] = ws.get_all_records()
                    except Exception:
                        backup_payload["sheets"][sheet_name] = []

                # Write JSON file
                file_path = os.path.join(cust_dir, f"{today}_backup.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(backup_payload, f, indent=4, ensure_ascii=False)

                print(f"[BACKUP SUCCESS] {cust_name} ({cust_id}) -> Saved: {file_path}")

            except Exception as e:
                print(f"[BACKUP FAILED]  {cust_name} ({cust_id}) -> Error: {repr(e)}")