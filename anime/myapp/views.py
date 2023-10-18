# myapp/views.py

import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render
from django.http import HttpResponse

# Load the anime dataset
dataset_path = r'D:\Django projects\anime recommendation\anime\dataset\anime.csv'
anime_data = pd.read_csv(dataset_path)

# Data preprocessing (same as in Colab code)
selected_features = ['genre', 'type']
for feature in selected_features:
    anime_data[feature] = anime_data[feature].fillna('')

combined_features = anime_data['genre'] + ' ' + anime_data['type']
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

# Calculate cosine similarity
similarity_matrix = cosine_similarity(feature_vectors)

# Create a Django view for anime recommendations
def recommend_anime(request):
    if request.method == 'POST':
        anime_name = request.POST.get('anime_name', '')

        # Find close matches for the anime name
        find_close_match = difflib.get_close_matches(anime_name, anime_data['name'].tolist())
        
        if not find_close_match:
            response_message = "No close matches found for the given anime name,go back."
            return HttpResponse(response_message)

        close_match = find_close_match[0]
        index_of_the_anime = anime_data[anime_data['name'] == close_match].index[0]

        # Get similarity scores
        similarity_score = list(enumerate(similarity_matrix[index_of_the_anime]))

        # Sort similar animes
        sorted_similar_anime = sorted(similarity_score, key=lambda x: x[1], reverse=True)

        # Get the top 10 similar animes
        similar_anime_list = []
        for i, movie in enumerate(sorted_similar_anime):
            index = movie[0]
            title_from_index = anime_data.iloc[index]['name']
            if i < 10:
                similar_anime_list.append((i + 1, title_from_index))

        context = {'anime_name': anime_name, 'similar_anime_list': similar_anime_list}
        return render(request, 'myapp/recommendations.html', context)

    return render(request, 'myapp/anime_input.html')

   
 

