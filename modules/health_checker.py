from datetime import datetime

class HealthChecker:
    def __init__(self, sheet_manager):
        self.sm = sheet_manager

    def audit_all_customers(self, customers):
        print("\n" + "=" * 60)
        print("  RUNNING SYSTEM HEALTH CHECK & AUDIT")
        print("=" * 60)

        active_count = 0
        error_count = 0

        for cust in customers:
            if not cust.get("active", True):
                print(f"[SKIPPED] {cust['name']} ({cust['id']}) - Account Inactive")
                continue

            try:
                doc = self.sm.get_sheet_by_id(cust["sheet_id"])

                # Check core worksheets: Sales, Purchase, Stock, Accounts
                sheet_stats = {}
                for sheet_name in ["Sales", "Purchase", "Stock", "Accounts"]:
                    try:
                        ws = doc.worksheet(sheet_name)
                        records = ws.get_all_records()
                        sheet_stats[sheet_name] = len(records)
                    except Exception:
                        sheet_stats[sheet_name] = "N/A"

                stats_str = ", ".join([f"{k}: {v}" for k, v in sheet_stats.items()])
                print(
                    f"[HEALTH OK]  ID: {cust['id']} | Name: {cust['name']} | [{stats_str}]"
                )
                active_count += 1

            except Exception as e:
                print(
                    f"[HEALTH ERR] ID: {cust['id']} | Name: {cust['name']} | Error: {repr(e)}"
                )
                error_count += 1

        print("-" * 60)
        print(f"Audit Summary: {active_count} Active & Accessible | {error_count} Issues Detected\n")