import json
from openpyxl import Workbook

w = Workbook()
sheet = w.active
sheet.append(
    [
        'Name', 'Link','Rating','Cover URL', 'Price', 'Variations', 'BSR'
    ]
)

with open('caregivers.json','r') as f:
    items = json.load(f)
    for item in items:
        name = item['name'].strip().split(':')[0] if item['name'] else None
        link = item['link']
        rating = item['rating']
        cover = item['cover_image']
        price = item['price']
        bsr = item['bsr'].replace('#','').replace(' in Books (','').replace('in Kindle Store (','').replace(',','').strip() if item['bsr'] else None
        variations = ', '.join(item['variations'])

        # if name and rating and ('dot to dot' in name.lower() or 'connect' in name.lower()):
        if name and ('caregiver' in name.lower() or 'care giver' in name.lower() or 'nursing' in name.lower()):
            data = [
                name,
                link,
                rating,
                cover,
                price,
                variations,
                int(bsr) if bsr else None
            ]
            
            sheet.append(data)
            print(f'Saved: {name}')

w.save('Caregivers_20220110_Analysis.xlsx')