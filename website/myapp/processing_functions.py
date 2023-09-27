import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS


def remove_stopwords(text):
    text = ' '.join([word for word in text.split() if word not in STOP_WORDS])
    return text

# remove punctuations
def remove_punctuations(text):
    text = re.sub(r'[^\w\s]', '', text)
    return text

#remove numbers both 123
def remove_numbers(text):
    text = re.sub(r'\d+', '', text)
    return text

def preprocess_text(text, remove_newline=False):
    text = remove_stopwords(text)
    text = remove_punctuations(text)
    text = remove_numbers(text)
    if remove_newline:
        text = text.replace('\n', '')
    return text

#get the unique words percentage from the column "lyrics_clean"
def get_unique_words_percentage(lyrics_list):
    '''
    @args : 
        lyrics_list: list [str] : list of lyrics
    @returns:
        percentage of unique words in the lyrics
    '''

    # get all the unique words in all the lyrics
    unique_words = set()
    total_words = 0
    for lyrics in lyrics_list:
        lyrics_processed = preprocess_text(lyrics)
        try:
            unique_words.update(lyrics_processed.split())
            total_words += len(lyrics_processed.split())
        except:
            print("Lyrics caused problem : ", lyrics_processed)

    # get the percentage of unique words
    return (len(unique_words) / total_words) * 100

def get_decades(df):
    # return a dictionary with the decades as keys and "views" from column views as values
    # get the years from the column yearx
    years = df['yearx'].tolist()
    # get the views from the column views
    views = df['views'].tolist()
    # create a dictionary with decades as keys and views as values
    decades = {}
    for i in range(len(years)):
        decade = years[i] // 10 * 10
        if decade in decades:
            decades[decade] += views[i]
        else:
            decades[decade] = views[i]

    # use the convert_to_thousands to convert the values into thousands, millions, billions, etc.
    # for key in decades:
    #     decades[key] = convert_to_thousands(decades[key])
    
    # sort the dictionary keys
    decades = dict(sorted(decades.items()))

    return decades


def convert_to_thousands(number):
    if number < 1000:
        return str(number)
    elif number < 1000000:
        return str(number // 1000) + 'K'
    elif number < 1000000000:
        return str(number // 1000000) + 'M'
    else:
        return str(number // 1000000000) + 'B'
    

def get_year_views(df):
    '''
    using "views" and "yearx" column, get how many views each year has
    return a dictionary with keys as years and values as views
    
    '''
    years = df['yearx'].tolist()
    views = df['views'].tolist()

    year_views = {}
    for i in range(len(years)):
        if years[i] in year_views:
            year_views[years[i]] += views[i]
        else:
            year_views[years[i]] = views[i]
    
    return year_views



# count the number of times curse words appear in the lyrics

def count_curse_words(lyrics):
    '''
    given a list of strings as lyrics and a list of strings for curse_words,
    return the count of every curse word which has appeared.
    return variable should be a dictionary where key will be the curse word and value will be its count    
    '''
    
    curse_words = ["fuck", "shit", "bitch", "anal", "ass", "shitbag", "asshole", "bastard", "damn", "bollocks"]
    
    curse_word_counts = {curse_word: 0 for curse_word in curse_words}

    for lyric in lyrics:
        words = lyric.split()
        
        for word in words:
            if word.lower() in curse_words:
                curse_word_counts[word.lower()] += 1
    # dont return the items which are zero
    curse_word_counts = {word: count for word, count in curse_word_counts.items() if count > 0}

    curse_word_counts = dict(sorted(curse_word_counts.items(), key=lambda item: item[1], reverse=True))

    return curse_word_counts

def get_sentiment_data(df, column_name_sentiment = "sentiment", column_name_year = "yearx"):

    '''
    returns a dataframe where each row is the year and there are 3 columns 
    positive negative and neutral and each has a count of songs in that year
    
    '''
    # Group the data by "yearx" and "sentiment" and count the occurrences of each sentiment
    sentiment_counts = df.groupby([column_name_year, column_name_sentiment]).size().unstack(fill_value=0)

    # Calculate the total number of songs for each year
    total_songs_per_year = df.groupby(column_name_year).size()

    # Calculate the percentage of each sentiment category for each year
    sentiment_percentage = sentiment_counts.divide(total_songs_per_year, axis=0) * 100

    return sentiment_percentage

def get_artist_name(df):

    # get all the unique artist names in the taylor swift df:
    artist_list = df['artist'].unique()

    # split
    artist_list = [artist.split(",") for artist in artist_list]

    # flatten the list
    artist_list = [item for sublist in artist_list for item in sublist]

    # get the most frequent artist name
    from collections import Counter
    artist_list = Counter(artist_list)
    return artist_list.most_common(1)[0][0]


