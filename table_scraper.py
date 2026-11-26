import re, sys, requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.styles import Font

DEFAULT = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
headers = {"User-Agent": "Mozilla/5.0 (learning project)"}

res = requests.get(url, headers=headers, timeout=30)
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")
table = soup.select_one("table.wikitable")
if table is None:
    print("No table found")
    sys.exit()

def clean(text):
    text = re.sub(r"\[.*?\]", "", text)
    return " ".join(text.split())

rows = []
for tr in table.select("tr"):
    cells = [clean(c.get_text(" ")) for c in tr.find_all(["th", "td"])]
    if cells:
        rows.append(cells)

wb = Workbook()
ws = wb.active
ws.title = "Table"
for r in rows:
    ws.append(r)
for cell in ws[1]:
    cell.font = Font(bold=True)
for col in ws.columns:
    width = max(len(str(c.value or "")) for c in col)
    ws.column_dimensions[col[0].column_letter].width = min(width + 2, 50)
ws.freeze_panes = "A2"

wb.save("table.xlsx")
print(len(rows), "rows saved to table.xlsx")
