# Gunnerkrigg Downloader
Gunnerkrigg Downloader is a CLI tool for downloading pages from the webcomic [Gunnerkrigg Court](https://www.gunnerkrigg.com/) by Tom Siddell. It takes a user input to download either all pages or from a chapter range, and will automatically create a folder in which the pages will be downloaded to. If there are pages that exist already in that folder, then they will be skipped. Makes use of the Requests and Beautiful Soup libraries.

## Installation
Clone the repository to your environment and install the necessary packages from the requirements file.
```
git clone https://github.com/monkonius/gunnerkrigg-downloader
cd gunnerkrigg-downloader/
pip3 install -r requirements.txt
```

## Usage
Run the program while inside the Gunnerkrigg Downloader repository.
```
python3 gunnerkrigg.py
Do you wish to download all webcomic pages? [y/n]
Which chapters do you wish to download? [1-n]
```
The program can be quit prematurely by entering 'q' or using 'Ctrl-D' during prompts, or 'Ctrl-C' when in the middle of downloading images.

<img width="829" alt="gunnerkrigg" src="https://github.com/monkonius/gunnerkrigg-downloader/assets/65208909/0146123b-f345-49b3-9c66-131d2b17705d">
