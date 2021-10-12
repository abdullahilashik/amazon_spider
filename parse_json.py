import json
from openpyxl import Workbook

w = Workbook()
sheet = w.active
sheet.append(
    [
        'Name', 'Link','Rating','Cover URL'
    ]
)

with open('amazon_authors.json','r') as f:
    items = json.load(f)
    for item in items:
        name = item['name'].strip().split(':')[0] if item['name'] else None
        link = item['link']
        rating = item['rating']
        cover = item['cover_image']

        if name and rating:
            data = [
                name,
                link,
                rating,
                cover
            ]
            
            sheet.append(data)
            print(f'Saved: {name}')

w.save('Amazon_Authors.xlsx')