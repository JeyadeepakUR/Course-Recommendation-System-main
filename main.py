import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request

# <==== Code starts here ====>
app = Flask(__name__)
courses_list = pickle.load(open('courses.pkl','rb'))
courses_list2 = pickle.load(open('udem_courses.pkl','rb'))
final_courses = pd.concat([courses_list, courses_list2], ignore_index=True)

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
    # with open("similarity.pkl", "rb") as f:
    #     data1 = pickle.load(f)
    # with open("udem_similarity.pkl", "rb") as f:
    #     data2 = pickle.load(f)
    # final_data = np.vstack((data1, data2))    

    def recommend(course):
        search_terms = set(course.split())

        similarity_scores = {}
        for i,r in final_courses.iterrows():
            course_name = r['course_name']
            course_tags = set(r['tags'].split())
            similarity_scores[course_name] = len(search_terms.intersection(course_tags))

        recommended_course_names = sorted(similarity_scores, key=lambda x: similarity_scores[x], reverse=True)[:7]
        #print(recommended_course_names)
        return recommended_course_names

    course_list = final_courses['course_name'].values
    selected_course = request.form['selected_course']

    recommended_course_names = recommend(selected_course)  
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