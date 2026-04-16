# app.py - Main Flask Application with 8 Team Members

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from career_engine import CareerEngine
from data_analyzer import CareerAnalyzer
import os

os.makedirs('static', exist_ok=True)
os.makedirs('static/team_photos', exist_ok=True)

app = Flask(__name__)
app.secret_key = 'career-recommender-secret-key-2026'

career_engine = CareerEngine()
career_analyzer = CareerAnalyzer(career_engine)

# 10 Team Members Data - Your Actual Team
team_members = [
    {
        'id': 1,
        'name': 'Harsh Vardhan Singh',
        'roll_number': '2420204061',
        'student_id': 'MCA2024139',
        'position': 'Leader',
        'role': 'Project Lead & AI Engineer',
        'bio': 'Leading the AI development team with expertise in Machine Learning, Deep Learning, and Career Analytics. Responsible for overall project coordination and AI model implementation.',
        'photo': 'harshu.jpeg',
        'email': 'harshaer35@gmail.com',
        'department': 'Computer Applications',
        'year': 'Final Year',
        'skills': ['Python', 'Machine Learning', 'Flask', 'AI Algorithms']
    },
    {
        'id': 2,
        'name': 'Himanshu Patel',
        'roll_number': '2420204064',
        'student_id': 'MCA2024159',
        'position': 'Co-Leader',
        'role': 'Data Scientist & Analyst',
        'bio': 'Specializes in Pandas, NumPy and Data Visualization. Expert in statistical analysis and predictive modeling. Assists in project coordination.',
        'photo': 'himanshu.jpeg',
        'email': 'himanshupatel7434@gmail.com',
        'department': 'Computer Applications',
        'year': 'Final Year',
        'skills': ['Python', 'Pandas', 'NumPy', 'Data Analysis', 'Statistics']
    },
    {
        'id': 3,
        'name': 'Piyush Singh Air',
        'roll_number': '2420204181',
        'student_id': 'MCA2024185',
        'position': 'Member',
        'role': 'Frontend Developer & UI Designer',
        'bio': 'Expert in responsive design, user experience, and modern web technologies. Creates beautiful and intuitive interfaces for the platform.',
        'photo': 'piyush.jpeg',
        'email': 'piyush.air@university.edu',
        'department': 'Computer Applications',
        'year': 'Final Year',
        'skills': ['HTML/CSS', 'JavaScript', 'React', 'UI/UX Design']
    },
    {
        'id': 4,
        'name': 'Agnesh Kumar',
        'roll_number': '2420204152',
        'student_id': 'MCA2024010',
        'position': 'Member',
        'role': 'Backend Developer',
        'bio': 'Specializes in Flask, Database Management, and API Development. Ensures robust server-side architecture and data handling.',
        'photo': 'agnesh.jpeg',
        'email': 'agnesh.kumar@university.edu',
        'department': 'Computer Applications',
        'year': 'Final Year',
        'skills': ['Flask', 'Python', 'SQL', 'Database', 'APIs']
    },
    {
        'id': 5,
        'name': 'Sanchit Saxena',
        'roll_number': '2420204130',
        'student_id': 'MCA2024171',
        'position': 'Member',
        'role': 'ML Engineer & Data Analyst',
        'bio': 'Specializes in recommendation algorithms, data processing, and career matching logic. Works on improving the AI recommendation engine.',
        'photo': 'sancheet.jpeg',
        'email': 'sanchitsaxena789@gmail.com',
        'department': 'Computer Applications',
        'year': 'Final Year',
        'skills': ['Python', 'Machine Learning', 'Data Analysis', 'Algorithms']
    },
    {
        'id': 6,
        'name': 'Abhishek Sharma',
        'roll_number': '2420204179',
        'student_id': 'MCA2024182',
        'position': 'Member',
        'role': 'Quality Assurance & Testing',
        'bio': 'Expert in testing methodologies, automation, and ensuring bug-free code delivery. Responsible for system reliability and performance.',
        'photo': 'abhishek.jpeg',
        'email': 'sharmagksj00@gmail.com',
        'department': 'Computer Applications',
        'year': 'Final Year',
        'skills': ['Testing', 'Debugging', 'Quality Assurance', 'Automation']
    },
    {
        'id': 7,
        'name': 'Om Shiv',
        'roll_number': '2420204105',
        'student_id': 'MCA2024160',
        'position': 'Member',
        'role': 'Database Administrator',
        'bio': 'Expert in database design, optimization, and data warehousing. Manages all career data efficiently and ensures data integrity.',
        'photo': 'om_shiv.jpeg',
        'email': 'omshiv9070@gmail.com',
        'department': 'Computer Applications',
        'year': 'Final Year',
        'skills': ['SQL', 'Database', 'Data Modeling', 'Data Management']
    },
    {
        'id': 8,
        'name': 'Shivam Patel',
        'roll_number': '2420204177',
        'student_id': 'MCA2024181',
        'position': 'Member',
        'role': 'Technical Writer & Documentation',
        'bio': 'Specializes in documentation, user manuals, and technical content creation. Ensures clear communication of project features and usage.',
        'photo': 'shivam.jpeg',
        'email': 'patelshivam2123@gmail.com',
        'department': 'Computer Applications',
        'year': 'Final Year',
        'skills': ['Technical Writing', 'Documentation', 'Content Creation', 'Communication']
    },
    {
        'id': 9,
        'name': 'Harsh Bardhan Maurya',
        'roll_number': '2420204057',
        'student_id': 'MCA2024158',
        'position': 'Member',
        'role': 'Data Scientist & Analyst',
        'bio': 'Specializes in Pandas, NumPy and Data Visualization.Statistical analysis and predictive modeling. Assists in project coordination.',
        'photo': 'harsh_bardhan.jpeg',
        'email': 'harshvardhanmaurya.1@gmail.com',
        'department': 'Computer Applications',
        'year': 'Final Year',
        'skills': ['Python', 'Pandas', 'NumPy', 'Data Analysis', 'Statistics']
    },
    {
        'id': 10,
        'name': 'Chetanya Raj Verma',
        'roll_number': '2420204046',
        'student_id': 'MCA2024121',
        'position': 'Member',
        'role': 'Database Administrator',
        'bio': 'Expert in database design, optimization, and data warehousing. Manages all career data efficiently and ensures data integrity.',
        'photo': 'chatanya.jpeg',
        'email': 'chetanya2123@gmail.com',
        'department': 'Computer Applications',
        'year': 'Final Year',
        'skills': ['SQL', 'Database', 'Data Modeling', 'Data Management']
    }
]

def validate_inputs(name, interests, skills_list, education, work_style, hobbies):
    errors = []
    if not name or len(name.strip()) < 2:
        errors.append("Please enter a valid name (at least 2 characters)")
    valid_interests = ['Medical', 'Education', 'Hotel', 'Government', 'Technology', 'Business', 'Arts']
    if not interests or interests not in valid_interests:
        errors.append(f"Please select an interest from: {', '.join(valid_interests)}")
    if not skills_list or len(skills_list) == 0:
        errors.append("Please enter at least one skill")
    valid_education = ['High School', 'Diploma', 'Bachelor', 'Master', 'PhD', 'MBBS', 'B.Ed']
    if education not in valid_education:
        errors.append("Please select a valid education level")
    valid_styles = ['Remote', 'Office', 'Field']
    if work_style not in valid_styles:
        errors.append("Please select a valid work style")
    if not hobbies or len(hobbies.strip()) < 2:
        errors.append("Please enter at least one hobby")
    return errors

@app.route('/')
def home():
    skill_suggestions = career_engine.get_skill_suggestions()
    hobby_suggestions = career_engine.get_hobby_suggestions()
    return render_template('index.html', skill_suggestions=skill_suggestions, hobby_suggestions=hobby_suggestions)

@app.route('/team')
def team():
    """Display team members page with all 8 members"""
    return render_template('team.html', team_members=team_members)

@app.route('/predict', methods=['POST'])
def predict():
    name = request.form.get('name', '').strip()
    interests = request.form.get('interests', '').strip()
    education = request.form.get('education', '')
    work_style = request.form.get('work_style', '')
    hobbies = request.form.get('hobbies', '').strip()
    
    skills_list = []
    for i in range(1, 7):
        skill = request.form.get(f'skill_{i}', '').strip()
        custom_skill = request.form.get(f'custom_skill_{i}', '').strip()
        if custom_skill:
            skills_list.append(custom_skill)
        elif skill and skill != 'other':
            skills_list.append(skill)
    
    skills = ', '.join(skills_list) if skills_list else ''
    errors = validate_inputs(name, interests, skills_list, education, work_style, hobbies)
    
    if errors:
        skill_suggestions = career_engine.get_skill_suggestions()
        hobby_suggestions = career_engine.get_hobby_suggestions()
        return render_template('index.html', errors=errors, form_data=request.form,
                             skill_suggestions=skill_suggestions, hobby_suggestions=hobby_suggestions)
    
    user_data = {
        'name': name, 'interests': interests, 'skills': skills,
        'education': education, 'work_style': work_style, 'hobbies': hobbies
    }
    
    recommendations = career_engine.get_recommendations(user_data, top_n=8)
    dashboard_charts = career_analyzer.generate_career_dashboard(name, user_data, recommendations)
    career_stats = career_analyzer.generate_statistics()
    
    session['recommendations'] = recommendations
    session['user_name'] = name
    session['user_data'] = user_data
    
    return render_template('result.html', recommendations=recommendations, user_name=name,
                         user_inputs=user_data, dashboard_charts=dashboard_charts, career_stats=career_stats)

@app.route('/dashboard')
def dashboard():
    if 'user_data' not in session:
        return redirect(url_for('home'))
    user_data = session.get('user_data', {})
    recommendations = session.get('recommendations', [])
    dashboard_charts = career_analyzer.generate_career_dashboard(session.get('user_name', 'User'), user_data, recommendations)
    career_stats = career_analyzer.generate_statistics()
    return render_template('dashboard.html', dashboard_charts=dashboard_charts,
                         career_stats=career_stats, user_name=session.get('user_name', 'User'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)