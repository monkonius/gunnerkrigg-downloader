from bs4 import BeautifulSoup
import requests
import os

# Starting URL, the homepage
url = 'https://www.gunnerkrigg.com/'

# Store comics in ./Gunnerkrigg Court
os.makedirs('Gunnerkrigg Court', exist_ok=True)

# Iterates over each page until beginning or when up-to-date
while True:

    # Download the page
    print(f'Downloading page {url}...')
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')

    # Find the URL of the comic image
    comic = soup.select('.comic_image')
    if comic == []:
        print('Could not find comic image.')
    else:
        comic_url = f'https://gunnerkrigg.com{comic[0].get("src")}'

        # Download the image
        res = requests.get(comic_url)
        res.raise_for_status()

        # Save the image to ./Gunnerkrigg Court
        file_path = os.path.join('Gunnerkrigg Court', os.path.basename(comic_url))
        if not os.path.exists(file_path):
            print(f'Downloading image {comic_url}')
            with open(file_path, 'wb') as file:
                for chunk in res.iter_content(100000):
                    file.write(chunk)

        # Updated
        else:
            print('Page already exists...')
            break

    # Get the previous comic page's URL
    prev = soup.select('img[src="/images/prev_a.jpg"]')
    if prev:
        prev_link = prev[0].parent.get('href')
        url = f'https://www.gunnerkrigg.com/{prev_link}'

    # First comic page, no more previous pages
    else:
        break

print('Done.')