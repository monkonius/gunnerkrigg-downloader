from bs4 import BeautifulSoup
import requests
import os
import re
import sys


def decrement_page(page: str):
    """Decrement the string value of the webcomic page by 1."""
    return page[:3] + str(int(page[3:]) - 1)


def check(input: str):
    """Check the input of the user and either return the input value or quit the program."""
    if input == 'q':
        print('Quitting...')
        sys.exit(0)

    return input


# Starting URL, the homepage
url = 'https://www.gunnerkrigg.com/'

# Store comics in ./Gunnerkrigg Court
os.makedirs('Gunnerkrigg Court', exist_ok=True)

try:
    res = requests.get(url, timeout=5)
    res.raise_for_status()
except Exception as error:
    print(error, '\nPlease try again.')
    sys.exit(1)

soup = BeautifulSoup(res.text, 'html.parser')
latest_chapter = soup.select('.chapter_button')[-1]
alt = latest_chapter.img.get('alt')
regex_result = re.findall(r'\d+', alt)[0]
total_chapters = int(regex_result)
print(f'There are currently {total_chapters} chapters in Gunnerkrigg Court.')

# Prompt user if they want to download all pages or a chapter range
download_all = False
while True:
    yes_responses = ['y', 'Y', 'yes', 'Yes', 'YES']
    no_responses = ['n', 'N', 'no', 'No', 'NO']
    try:
        response = check(input('Do you wish to download all webcomic pages? [y/n] '))
    except EOFError:
        print('\nQuitting...')
        sys.exit(0)
    if response in yes_responses or response in no_responses: 
        if response in yes_responses:
            download_all = True
        break
    print('Invalid option...')

if not download_all:
    print(f'Which chapters do you wish to download? [1-{total_chapters}]')
    while True:
        try:
            start_chapter = int(check(input('Start: ')))
            end_chapter = int(check(input('End: ')))
        except ValueError:
            print('Invalid option...')
            continue
        except EOFError:
            print('\nQuitting...')
            sys.exit(0)

        if start_chapter < 1 or start_chapter > total_chapters:
            print('Invalid range...')
        elif end_chapter < start_chapter or end_chapter > total_chapters:
            print('Invalid range...')
        else:
            start_data = soup.find('strong', string=re.compile(f'Chapter {start_chapter}'))
            start_page = start_data.parent.get('href')
            end_data = soup.find('strong', string=re.compile(f'Chapter {end_chapter + 1}'))
            end_page = decrement_page(end_data.parent.get('href'))
            url = url + end_page
            break

# Iterates over each page until beginning or when up-to-date
if download_all:
    while True:

        try:
            # Download the page
            print(f'Downloading page {url}...')
            try:
                res = requests.get(url, timeout=5)
                res.raise_for_status()
            except Exception as error:
                print(error, '\nPlease try again.')
                sys.exit(1)

            soup = BeautifulSoup(res.text, 'html.parser')

            # Find the URL of the comic image
            comic = soup.select('.comic_image')
            if comic == []:
                print('Could not find comic image.')
            else:
                comic_url = f'https://gunnerkrigg.com{comic[0].get("src")}'

                # Download the image
                try:
                    res = requests.get(comic_url)
                    res.raise_for_status()
                except Exception as error:
                    print(error, '\nPlease try again.')
                    sys.exit(1)

                # Save the image to ./Gunnerkrigg Court
                file_path = os.path.join('Gunnerkrigg Court', os.path.basename(comic_url))
                if not os.path.exists(file_path):
                    print(f'Downloading image {comic_url}')
                    with open(file_path, 'wb') as file:
                        for chunk in res.iter_content(100000):
                            file.write(chunk)

                # Skip image download
                else:
                    print('Image already exists...')

            # Get the previous comic page's URL
            prev = soup.select('img[src="/images/prev_a.jpg"]')
            if prev:
                prev_link = prev[0].parent.get('href')
                url = f'https://www.gunnerkrigg.com/{prev_link}'

            # First comic page, no more previous pages
            else:
                break

        except KeyboardInterrupt:
            print('\nInterrupted...')
            sys.exit(0)

#  Download selected chapters
else:
    while True:

        try:
            # Download the page
            print(f'Downloading page {url}...')
            try:
                res = requests.get(url)
                res.raise_for_status()
            except Exception as error:
                print(error, '\nPlease try again.')
                sys.exit(1)

            soup = BeautifulSoup(res.text, 'html.parser')

            # Find the URL of the comic image
            comic = soup.select('.comic_image')
            if comic == []:
                print('Could not find comic image.')
            else:
                comic_url = f'https://gunnerkrigg.com{comic[0].get("src")}'

                # Download the image
                try:
                    res = requests.get(comic_url)
                    res.raise_for_status()
                except Exception as error:
                    print(error, '\nPlease try again.')
                    sys.exit(1)

                # Save the image to ./Gunnerkrigg Court
                file_path = os.path.join('Gunnerkrigg Court', os.path.basename(comic_url))
                if not os.path.exists(file_path):
                    print(f'Downloading image {comic_url}')
                    with open(file_path, 'wb') as file:
                        for chunk in res.iter_content(100000):
                            file.write(chunk)

                # Skip image download
                else:
                    print('Image already exists...')

            # Start comic page range
            if url.split('/')[-1] == start_page:
                break

            # Get the previous comic page's URL
            prev = soup.select('img[src="/images/prev_a.jpg"]')
            if prev:
                prev_link = prev[0].parent.get('href')
                url = f'https://www.gunnerkrigg.com/{prev_link}'
        
        except KeyboardInterrupt:
            print('\nInterrupted...')
            sys.exit(0)

print('Done.')