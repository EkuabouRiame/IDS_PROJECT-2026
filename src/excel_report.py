from openpyxl import Workbook

def create_excel(filename,total,normal,attack,accuracy):

    wb = Workbook()

    ws = wb.active

    ws.title="IDS Report"

    ws.append(["Metric","Value"])

    ws.append(["Total Records",total])

    ws.append(["Normal",normal])

    ws.append(["Attack",attack])

    ws.append(["Accuracy",accuracy])

    wb.save(filename)