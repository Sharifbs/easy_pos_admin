import gspread

class SheetManager:
    def __init__(self, credentials_path):
        # Service Account scopes including Drive & Sheets
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.gc = gspread.service_account(filename=credentials_path, scopes=scopes)

    def get_sheet_by_id(self, sheet_id):
        # Direct lookup by Sheet Key (Bypasses Drive Search 404 issue)
        return self.gc.open_by_key(sheet_id)