import pandas as pd
import ast  
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

movie=pd.read_csv(r"D:\Datasets\tmdb_5000_movies.csv\tmdb_5000_movies.csv")
credits=pd.read_csv(r"D:\Datasets\tmdb_5000_credits.csv\tmdb_5000_credits.csv")
# print(movie.head())
# print(credits.head())

movie=movie.merge(credits,on='title')
# print(movie.head())

movie=movie[['movie_id','title','overview','genres','keywords','cast','crew']]
print(movie.head())

print(movie.isnull().sum())

movie.dropna(inplace=True)
print(movie.isnull().sum())

print(movie.duplicated().sum())

print(movie.iloc[0].genres)

def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

movie['genres']=movie['genres'].apply(convert)

movie['keywords']=movie['keywords'].apply(convert)

# print(movie.head())

def convert3(obj):
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter!=3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L

movie['cast']=movie['cast'].apply(convert3)
# print(movie.head())

def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i['name'])
            break
    return L

movie['crew']=movie['crew'].apply(fetch_director)
# print(movie.head())

movie['overview']=movie['overview'].apply(lambda x:x.split())
# print(movie.head())

movie['genres']=movie['genres'].apply(lambda x:[i.replace(" ","")for i in x])
movie['keywords']=movie['keywords'].apply(lambda x:[i.replace(" ","")for i in x])
movie['cast']=movie['cast'].apply(lambda x:[i.replace(" ","")for i in x])
movie['crew']=movie['crew'].apply(lambda x:[i.replace(" ","")for i in x])
# print(movie.head())

movie['tags']=movie['overview']+movie['cast']+movie['crew']+movie['genres']+movie['keywords']
# print(movie.head())

new_df=movie[['movie_id','title','tags']]
# print(new_df.head())

new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))
# print(new_df.head())

new_df['tags']=new_df['tags'].apply(lambda x:x.lower())
print(new_df.head())

ps=PorterStemmer()

def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new_df['tags']=new_df['tags'].apply(stem)

cv=CountVectorizer(max_features=5000,stop_words='english')

vectors=cv.fit_transform(new_df['tags']).toarray()
print(vectors)

print(cv.get_feature_names_out())

similarity=cosine_similarity(vectors)
print(similarity)

def recommend(movie):
    movie_index=new_df[new_df['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    for i in movies_list:
        print(new_df.iloc[i[0]].title)
    
recommend('Cars')



pickle.dump(new_df, open(r'D:\Python\Major_Project\Movie_recommendation_system\movie_list.pkl', 'wb'))
pickle.dump(similarity, open(r'D:\Python\Major_Project\Movie_recommendation_system\similarity.pkl', 'wb'))
