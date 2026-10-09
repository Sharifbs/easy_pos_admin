import json
import os
from modules.sheet_manager import SheetManager
from modules.health_checker import HealthChecker
from modules.backup_manager import BackupManager

def load_customers(config_path="config/customers.json"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    print("#" * 60)
    print("  EASY POS CENTRAL MANAGEMENT & AUTOMATED BACKUP BOT")
    print("#" * 60)

    # 1. Initialize Google Credentials
    creds_path = os.path.join("config", "service_account.json")
    sm = SheetManager(creds_path)
    print("[INIT] Google Service Account Authentication Successful.")

    # 2. Load Customers
    customers = load_customers()
    print(f"[INIT] Loaded {len(customers)} customer profiles from configuration.")

    # 3. Health Check & Audit
    checker = HealthChecker(sm)
    checker.audit_all_customers(customers)

    # 4. Automated Daily Local Backups
    backup = BackupManager(sm)
    backup.backup_all_customers(customers)

    print("#" * 60)
    print("  ALL OPERATIONS COMPLETED!")
    print("#" * 60)

if __name__ == "__main__":
    main()