from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def create_pdf(filename, total, normal, attack, accuracy):

    pdf = SimpleDocTemplate(filename)

    data = [

        ["Metric","Value"],

        ["Total Records", total],

        ["Normal Traffic", normal],

        ["Attack Traffic", attack],

        ["Accuracy", f"{accuracy}%"]

    ]

    table = Table(data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.grey),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige)

        ])

    )

    pdf.build([table])