from django.shortcuts import render
import pandas as pd
from .processing_functions import *

from .lyrics_generator import generate_lyrics_internal
from .sing import sing
import random, os
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from django.http import JsonResponse


from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt




# CONSTANTS



def landingpage(request):
    return render(request, 'myapp/landingpage.html', {})

def analysis_homepage(request):
    return render(request, 'myapp/analysis_homepage.html', {})

def about_page(request):
    return render(request, 'myapp/about_page.html', {})


def generate_vocals(request):
    if request.method == 'POST':
        print("Genetraing vocals")

        first_sentence = request.POST.get('first_sentence', '')
        second_sentence = request.POST.get('second_sentence', '')
        third_sentence = request.POST.get('third_sentence', '')
        fourth_sentence = request.POST.get('fourth_sentence', '')

        # generate a random number between 1 and 100
        params = {}

        random_number = random.randint(1, 100)
        randome_number_file_name = str(random_number) + ".mp3"
        static_dir = os.path.join(settings.BASE_DIR, 'myapp', 'static')
        after_static_name_path = os.path.join('myapp/music_files/' , randome_number_file_name)


        # mp3_file_path = os.path.join(static_dir, 'myapp/music_files/' , randome_number_file_name)
        mp3_file_path = os.path.join(static_dir, after_static_name_path)
        
        after_static_name_path = os.path.join('static/myapp/music_files/' , randome_number_file_name)
        
        vocal_words = first_sentence + "\n" + second_sentence + "\n" + third_sentence + "\n" + fourth_sentence

        x = sing(words = vocal_words, output_file_path=mp3_file_path)

        if x==True:
            print("File generated successfully")
            params = {"mp3_url": after_static_name_path}
        else:
            print("File generation failed")



        print("params : ", params)
        return render(request, 'myapp/generate_vocals.html', params)
        # return JsonResponse(params)
    else:
        return render(request, 'myapp/generate_vocals.html')

def generate_lyrics(request):
    if request.method == 'POST':
        CSV_FILEPATH = "static/data/data.csv"

        desc_user = request.POST.get('inputField', '')
        artist_name = request.POST.get('artist_name', '')

        df = pd.read_csv(CSV_FILEPATH)
        
        
        model_output_lyrics = generate_lyrics_internal(desc_user, df, specific_artist = artist_name)

        params = {}
        params["lyrics"] = model_output_lyrics
        # params["lyrics"] = "Lyrics will appear here \n Lyrics will appear here \n Lyrics will appear here \n Lyrics will appear here \n "
    
        return render(request, 'myapp/generate_lyrics.html', params)



    
    return render(request, 'myapp/generate_lyrics.html')


def analysis(request, artist_name):

    if artist_name == "Taylor Swift":
        CSV_FILE_PATH = "static/data/taylorSwift_data.csv"
        # CSV_FILE_PATH = "/Users/umer/Desktop/a .nosync/Masters /UdS summer 23/DL for literary texts/website/myapp/static/data/taylorSwift_data.csv"
        # use static files storage to get csv file
        # CSV_FILE_PATH = staticfiles_storage.url('data/taylorSwift_data.csv')

    elif artist_name == "Eminem":
        CSV_FILE_PATH = "static/data/eminem_data.csv"
        # CSV_FILE_PATH = "/Users/umer/Desktop/a .nosync/Masters /UdS summer 23/DL for literary texts/website/myapp/static/data/eminem_data.csv"                
        # CSV_FILE_PATH = staticfiles_storage.url('data/eminem_data.csv')

    print("CSV_FILE_PATH : ", CSV_FILE_PATH)

    # ARTISTS_CSV_FILE_PATH = "/Users/umer/Desktop/a .nosync/Masters /UdS summer 23/DL for literary texts/website/myapp/static/data/artists_info.csv"    
    # ARTISTS_CSV_FILE_PATH = staticfiles_storage.url('data/artists_info.csv')
    
    ARTISTS_CSV_FILE_PATH = "static/data/artists_info.csv"


    LYRICS_COLUMN_TO_USE = "lyrics_clean_with_newline"


    artists_df = pd.read_csv(ARTISTS_CSV_FILE_PATH)

    # read the csv file from CSV_FILE_PATH using pd
    df = pd.read_csv(CSV_FILE_PATH)


    df = df[(df['yearx'] >= 1900) & (df['yearx'] <= 2024)] 


    params = {}

    #For Tile 1
    artist_name = get_artist_name(df)
    artist_intro = artists_df[artists_df['name'] == artist_name]['intro'].tolist()[0]
    artist_instagram = artists_df[artists_df['name'] == artist_name]['instagram'].tolist()[0]
    artist_twitter = artists_df[artists_df['name'] == artist_name]['twitter'].tolist()[0]
    artist_spotify = artists_df[artists_df['name'] == artist_name]['spotify'].tolist()[0]
    artist_youtube = artists_df[artists_df['name'] == artist_name]['youtube'].tolist()[0]

    artist_most_viewed_song_name = artists_df[artists_df['name'] == artist_name]['most_viewed_song_name'].tolist()[0]
    artist_most_viewed_song_link = artists_df[artists_df['name'] == artist_name]['most_viewed_song_link'].tolist()[0]


    temp_artist_name = artist_name.replace(" ","").lower()
    image_url = staticfiles_storage.url('images/' + temp_artist_name + '.png')
    print("image_url : ", image_url)

    params["artist_name"] = artist_name

    params["artist_image_path"] = image_url


    params["artist_intro"] = artist_intro
    params["artist_instagram_link"] = artist_instagram
    params["artist_twitter_link"] = artist_twitter
    params["artist_spotify_link"] = artist_spotify
    params["artist_youtube_link"] = artist_youtube
    params["artist_most_viewed_song_name"] = artist_most_viewed_song_name
    params["artist_most_viewed_song_link"] = artist_most_viewed_song_link

    
    # For tile 2
    unique_word_percentage = get_unique_words_percentage(df[LYRICS_COLUMN_TO_USE])
    # round to 2 decimal places
    unique_word_percentage = round(unique_word_percentage, 2)
    print("unique_word_percentage : ", unique_word_percentage)

    params["unique_word_percentage"] = unique_word_percentage

    #calculate the genre counts. information in tag column
    genre_counts = df['tag'].value_counts()

    # Prepare data for the chart
    labels = genre_counts.index.tolist()
    data = genre_counts.tolist()

    params["genre_labels"] = labels
    params["genre_counts"] = data
    
    decade_views = get_decades(df) # returns a dictionary with keys as decades and values as views

    params["decade_views_labels"] = list(decade_views.keys())
    params["decade_views_views"] = list(decade_views.values())

    # For tile 3
    year_views = get_year_views (df)
    params["year_views_labels"] = list(year_views.keys())
    params["year_views_views"] = list(year_views.values())
    
    
    # For tile 6
    curse_words_counts = count_curse_words(df['lyrics_clean'].tolist())
    params["curse_words_labels"] = list(curse_words_counts.keys())
    params["curse_words_counts"] = list(curse_words_counts.values())


    # For tile 7: pass the following variables
    # total_songs , total_views, earliest_year, earliest_song, latest_year, latest_song
    total_songs = len(df)
    total_views = df['views'].sum()
    total_views = convert_to_thousands(total_views)
    earliest_year = df['yearx'].min()
    earliest_song = df[df['yearx'] == earliest_year]['title'].tolist()[0]
    latest_year = df['yearx'].max()
    latest_song = df[df['yearx'] == latest_year]['title'].tolist()[0]

    params["total_songs"] = total_songs
    params["total_views"] = total_views
    params["earliest_year"] = earliest_year
    params["earliest_song"] = earliest_song
    params["latest_year"] = latest_year
    params["latest_song"] = latest_song

    # For tile 8: pass the following variables
    # use get_sentiment_data to get the sentiment data
    sentiment_data = get_sentiment_data(df)

    params["sentiment_labels"] = sentiment_data.index.tolist()
    params["sentiment_positive"] = sentiment_data['Positive'].tolist()
    params["sentiment_negative"] = sentiment_data['Negative'].tolist()
    params["sentiment_neutral"] = sentiment_data['Neutral'].tolist()



    # return render(request, 'myapp/homepage.html', {"genre_counts":genre_counts})
    return render(request, 'myapp/analysis.html', params)



