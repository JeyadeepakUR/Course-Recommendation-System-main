import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# <==== Code starts here ====>
app = Flask(__name__)
courses_list = pickle.load(open('courses.pkl','rb'))
courses_list2 = pickle.load(open('udem_courses.pkl','rb'))
final_courses = pd.concat([courses_list, courses_list2], ignore_index=True)

# Create a CountVectorizer and fit it on all course tags
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(final_courses['tags']).toarray()

@app.route('/')
def home():
    all_courses_html = ""
    for i,r in list(final_courses.iterrows())[:15]:
        course_name = r['course_name']
        course_tags = set(r['tags'].split()[:7])
        all_courses_html += f"""
        <div class="course-card">
        <h3 class="course-title">{course_name}</h3>
        <p class="course-instructor">Tags: {course_tags}</p>
        </div>"""
    return render_template('index.html', all_courses=all_courses_html)
@app.route('/recommend', methods=['POST'])

def recommend():  
    print(final_courses.head())
    def recommend(course):        
        course_vector = cv.transform([course]).toarray()
        similarities = cosine_similarity(course_vector, vectors)
        course_indices = similarities.argsort()[0][::-1][1:8]
        recommended_course_names = final_courses.iloc[course_indices]['course_name'].tolist()
        return recommended_course_names

    course_list = final_courses['course_name'].values
    selected_course = request.form['selected_course']

    recommended_course_names = recommend(selected_course)  
    recommended_course_names = list(set(recommended_course_names)) # remove duplicates
    recommended_courses_html = ""
    for course in recommended_course_names:
        recommended_courses_html += f"""
        <div class="course-card">
        <h3 class="course-title">{course}</h3>
        </div>"""
    return render_template('explore.html', selected_course=selected_course, recommended_courses=recommended_courses_html)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')
if __name__ == '__main__':
    app.run(debug=True)