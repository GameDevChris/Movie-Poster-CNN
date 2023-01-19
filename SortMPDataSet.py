import csv
from tqdm import tqdm
import mmap
from PIL import Image
import requests
from io import BytesIO
import os
import shutil

# Directories
data_dir = 'Data'
year_dir = 'Data/Year'
genre_dir = 'Data/Genre'
csv_Path = 'Data/MoviePosterInfo.csv'
movies = []

# Used For TQDM, Get CSV Line Count
def GetLinelCount(path):
    file = open(path, "r+", encoding="utf-8", errors="ignore")
    buffer = mmap.mmap(file.fileno(), 0)
    lineCount = 0
    while buffer.readline():
        lineCount += 1
    return lineCount

# Get Info From CSV
def GetMovieValue(id:str, value:str):
    file = open(csv_Path, encoding="utf-8", errors="ignore")
    movie_list = csv.DictReader(file)
    for entry in movie_list:
        if id == entry['id']:
            return entry[value]

# Movie Class
class Movie:
    def __init__(self, id:str):
        self.id = id
        self.url = GetMovieValue(id, 'Poster')

        self.title = GetMovieValue(id, 'Title')
        self.title = self.title.replace("/", "-")
        self.title = self.title.replace("|", "-")
        self.title = self.title.replace(",", "-")
        self.title = self.title.replace(":", "")
        self.title = self.title.strip()

        self.year = str(round(int(GetMovieValue(id, 'yearValue')), -1))

        self.year = self.year.strip()

        self.genre = GetMovieValue(id, 'Genre')
        self.genre = self.genre.strip()
        self.genre = self.genre.replace("/", "-")
        self.genre = self.genre.replace("|", "-")
        self.genre = self.genre.replace(" ", "")
        self.genre = self.genre.replace(",", "-")
        self.genre = self.genre.split("-")[0]

# Main Function To Create List
def CreateMovieList():
    amountOfFailed = 0

    # Delete Old Data
    if os.path.exists(year_dir):
        shutil.rmtree(year_dir)

    if os.path.exists(genre_dir):
        shutil.rmtree(genre_dir)

    # Create Folders
    os.mkdir(year_dir)
    os.mkdir(genre_dir)

    # Iterate Through CSV
    file = open(csv_Path, encoding="utf-8", errors="ignore")
    movie_list = csv.DictReader(file)
    for entry in tqdm(movie_list, total=GetLinelCount(csv_Path)):

        # For Each Entry Create Movie And Format Year
        newMovie = Movie(entry['id'])
        num = int(newMovie.year)
        count = 0
        while num != 0:
            num //= 10
            count += 1
        if not (count == 4):
            print("\rValue year not 4 digits, value is: " + newMovie.year)

        else:

            # Download Image To Correct Folder
            movieDatePath = os.path.join(year_dir, newMovie.year)
            movieGenrePath = os.path.join(genre_dir, newMovie.genre)

            if not os.path.exists(movieDatePath):
                os.mkdir(movieDatePath)
                print("\rCreated folder for year: " + newMovie.year)

            if not os.path.exists(movieGenrePath):
                os.mkdir(movieGenrePath)
                print("\rCreated folder for genre: " + newMovie.genre)

            try:
                movieRequest = requests.get(newMovie.url)
                moviePoster = Image.open(BytesIO(movieRequest.content))
                dateSavePath = os.path.join(movieDatePath, newMovie.title)
                genreSavePath = os.path.join(movieGenrePath, newMovie.title)
                moviePoster.save(dateSavePath + ".png", format="png")
                moviePoster.save(genreSavePath + ".png", format="png")
                movies.append(newMovie)

            except IOError:
                amountOfFailed+=1

CreateMovieList()
