import xml.etree.ElementTree as ET
import csv
import sys

xml_file_path = sys.argv[1]

# Parse the XML file
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Create a list to hold the item data
items_data = []

# Extract channel title
channel_title = root.find('channel/title').text

# Iterate through each item in the channel
for item in root.findall('channel/item'):
    title = item.find('title').text if item.find('title') is not None else ''
    link = item.find('link').text if item.find('link') is not None else ''
    pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
    creator = item.find('{http://purl.org/dc/elements/1.1/}creator').text if item.find('{http://purl.org/dc/elements/1.1/}creator') is not None else ''
    
    # Check if 'encoded' element exists
    content_element = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')
    content = content_element.text.strip() if content_element is not None and content_element.text is not None else ''

    # Append the data to the list
    items_data.append({
        'Category': xml_file_path.split('/')[-1].split('.')[0],
        # 'Channel Title': channel_title,
        'Title': title,
        'Link': link,
        'Publication Date': pub_date,
        'Creator': creator,
        'Content': content
    })

# Write the extracted data to a CSV file
csv_file_path = './output/{filename}.csv'.format(filename=xml_file_path.split('/')[-1].split('.')[0])
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Category', 'Title', 'Link', 'Publication Date', 'Creator', 'Content']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write header
    writer.writeheader()
    # Write rows
    for item in items_data:
        writer.writerow(item)

print(f"Data extracted and written to {csv_file_path}.")