import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request

# <==== Code starts here ====>
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    courses_list = pickle.load(open('courses.pkl','rb'))
    courses_list2 = pickle.load(open('udem_courses.pkl','rb'))
    final_courses = pd.concat([courses_list, courses_list2], ignore_index=True)
    with open("similarity.pkl", "rb") as f:
        data1 = pickle.load(f)
    with open("udem_similarity.pkl", "rb") as f:
        data2 = pickle.load(f)
    final_data = np.vstack((data1, data2))    
    def recommend(course):
        index = final_courses[final_courses['course_name'] == course].index[0]
        distances = sorted(list(enumerate(final_data[index])), reverse=True, key=lambda x: x[1])
        recommended_course_names = []
        for i in distances[1:7]:
            course_name = final_courses.iloc[i[0]].course_name
            recommended_course_names.append(course_name)

        return recommended_course_names

    course_list = final_courses['course_name'].values
    selected_course = request.form['selected_course']

    recommended_course_names = recommend(selected_course)  
    recommended_courses_html = ""
    for course in recommended_course_names:
        recommended_courses_html += f"<li>{{course}}</li>"

    return render_template('index.html', selected_course=selected_course, recommended_courses=recommended_courses_html)

if __name__ == '__main__':
    app.run(debug=True)