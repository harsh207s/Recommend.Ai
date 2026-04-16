# career_engine.py - Enhanced career database with hobby matching

import pandas as pd
import numpy as np

class CareerEngine:
    def __init__(self):
        self.careers = self._initialize_careers()
        self.education_levels = {
            "High School": 1,
            "Diploma": 2,
            "Bachelor": 3,
            "Master": 4,
            "PhD": 5,
            "MBBS": 5,
            "B.Ed": 3
        }
        
        # Hobby to career mapping
        self.hobby_mapping = {
            "Reading": ["Content Writer", "Journalist", "Librarian", "Editor", "Researcher", "Teacher"],
            "Writing": ["Content Writer", "Author", "Journalist", "Copywriter", "Technical Writer", "Blogger"],
            "Drawing": ["Graphic Designer", "Animator", "Illustrator", "Architect", "Fashion Designer"],
            "Painting": ["Graphic Designer", "Interior Designer", "Art Teacher", "Illustrator", "Art Director"],
            "Photography": ["Photographer", "Journalist", "Film Maker", "Social Media Manager", "Photo Editor"],
            "Cooking": ["Chef", "Food Blogger", "Nutritionist", "Restaurant Manager", "Food Stylist"],
            "Gardening": ["Botanist", "Landscape Architect", "Farmer", "Environmental Scientist", "Horticulturist"],
            "Traveling": ["Travel Consultant", "Tour Guide", "Flight Attendant", "Travel Blogger", "Geographer"],
            "Gaming": ["Game Developer", "Game Tester", "Esports Manager", "Streamer", "Game Designer"],
            "Music": ["Music Producer", "Sound Engineer", "Music Teacher", "Singer", "DJ"],
            "Dancing": ["Dance Teacher", "Choreographer", "Fitness Instructor", "Performer", "Event Planner"],
            "Sports": ["Sports Coach", "Physical Trainer", "Sports Journalist", "Athlete", "Sports Manager"],
            "Yoga": ["Yoga Instructor", "Wellness Coach", "Physiotherapist", "Fitness Trainer", "Therapist"],
            "Programming": ["Software Developer", "Data Scientist", "Web Developer", "AI Engineer", "Game Developer"],
            "Teaching": ["Teacher", "Professor", "Trainer", "Educational Consultant", "Online Tutor"],
            "Volunteering": ["Social Worker", "NGO Manager", "Public Health Specialist", "Counselor", "Community Manager"],
            "Debating": ["Lawyer", "Politician", "Journalist", "Public Speaker", "Corporate Trainer"],
            "Singing": ["Singer", "Music Teacher", "Voice Actor", "Performer", "Music Therapist"],
            "Acting": ["Actor", "Theater Artist", "Voice Actor", "Drama Teacher", "Content Creator"],
            "Crafting": ["Craft Designer", "Artisan", "Product Designer", "Interior Designer", "E-commerce Seller"],
            "Fitness": ["Personal Trainer", "Physiotherapist", "Sports Coach", "Nutritionist", "Wellness Coach"],
            "Research": ["Scientist", "Data Analyst", "Researcher", "Professor", "Market Research Analyst"],
            "Public Speaking": ["Corporate Trainer", "Motivational Speaker", "Politician", "Lawyer", "Sales Manager"],
            "Event Planning": ["Event Manager", "Wedding Planner", "Corporate Event Coordinator", "Conference Organizer"],
            "Blogging": ["Content Creator", "Social Media Manager", "Digital Marketer", "Influencer", "Journalist"],
            "Video Editing": ["Video Editor", "Film Maker", "YouTuber", "Content Creator", "Motion Graphics Designer"],
            "Animation": ["Animator", "VFX Artist", "Game Developer", "Multimedia Designer", "3D Modeler"],
            "Psychology": ["Psychologist", "Counselor", "HR Manager", "Therapist", "Career Coach"],
            "Business": ["Entrepreneur", "Business Analyst", "Marketing Manager", "Sales Manager", "Consultant"],
            "Healthcare": ["Doctor", "Nurse", "Pharmacist", "Physiotherapist", "Medical Researcher"]
        }
    
    def calculate_match_score(self, user_inputs, career):
        """Calculate detailed match score between user and career (0-100)"""
        score = 0
        max_possible = 0
        
        # 1. Interest/Field match (25 points)
        max_possible += 25
        user_interest = user_inputs['interests'].lower()
        career_field = career['field'].lower()
        
        if user_interest == career_field:
            score += 25
        elif user_interest in career_field or career_field in user_interest:
            score += 17
        elif any(word in career_field for word in user_interest.split()):
            score += 10
        
        # 2. Skills match (30 points)
        max_possible += 30
        user_skills = [s.strip().lower() for s in user_inputs['skills'].split(',')]
        career_skills = [s.lower() for s in career['required_skills']]
        
        matched_skills = 0
        for skill in user_skills:
            for career_skill in career_skills:
                if skill in career_skill or career_skill in skill:
                    matched_skills += 1
                    break
        
        skill_match_ratio = min(1.0, matched_skills / max(1, len(career_skills)))
        score += skill_match_ratio * 30
        
        # 3. Hobby match (20 points)
        max_possible += 20
        user_hobbies = [h.strip().lower() for h in user_inputs['hobbies'].split(',')]
        hobby_score = self._calculate_hobby_match(user_hobbies, career['title'])
        score += hobby_score
        
        # 4. Education match (15 points)
        max_possible += 15
        user_edu_score = self.education_levels.get(user_inputs['education'], 1)
        career_edu_score = self.education_levels.get(career['min_education'], 1)
        
        if user_edu_score >= career_edu_score:
            score += 15
        elif user_edu_score == career_edu_score - 1:
            score += 8
        elif user_edu_score == career_edu_score - 2:
            score += 4
        
        # 5. Work style match (10 points)
        max_possible += 10
        if user_inputs['work_style'] in career['work_styles']:
            score += 10
        elif 'Remote' in career['work_styles'] and user_inputs['work_style'] == 'Office':
            score += 5
        elif 'Office' in career['work_styles'] and user_inputs['work_style'] == 'Remote':
            score += 5
        
        # Calculate percentage
        final_score = (score / max_possible) * 100 if max_possible > 0 else 0
        return round(final_score, 1)
    
    def _calculate_hobby_match(self, user_hobbies, career_title):
        """Calculate match score based on hobbies (0-20 points)"""
        hobby_score = 0
        
        for hobby in user_hobbies:
            if hobby in self.hobby_mapping:
                related_careers = [c.lower() for c in self.hobby_mapping[hobby]]
                if career_title.lower() in related_careers:
                    hobby_score += 10
                else:
                    for career_list in self.hobby_mapping.values():
                        if career_title.lower() in [c.lower() for c in career_list]:
                            hobby_score += 5
                            break
        
        return min(20, hobby_score)
    
    def get_recommendations(self, user_inputs, top_n=8):
        """Get top N career recommendations with scores and details"""
        recommendations = []
        
        for career in self.careers:
            score = self.calculate_match_score(user_inputs, career)
            recommendations.append({
                'title': career['title'],
                'score': score,
                'description': career['description'],
                'field': career['field'],
                'required_skills': ', '.join(career['required_skills'][:4]),
                'salary_range': career.get('salary_range', 'Varies'),
                'growth_rate': career.get('growth_rate', 'Medium'),
                'match_details': self._get_match_details(user_inputs, career)
            })
        
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:top_n]
    
    def _get_match_details(self, user_inputs, career):
        """Get detailed match breakdown"""
        details = {}
        
        if user_inputs['interests'].lower() == career['field'].lower():
            details['field'] = 'Excellent match'
        elif career['field'].lower() in user_inputs['interests'].lower():
            details['field'] = 'Good match'
        else:
            details['field'] = 'Related field'
        
        user_skills = [s.strip().lower() for s in user_inputs['skills'].split(',')]
        career_skills = [s.lower() for s in career['required_skills']]
        matched = sum(1 for us in user_skills for cs in career_skills if us in cs or cs in us)
        details['skills_matched'] = f"{matched}/{len(career_skills)} skills"
        
        user_hobbies = [h.strip().lower() for h in user_inputs['hobbies'].split(',')]
        hobby_related = []
        for hobby in user_hobbies:
            if hobby in self.hobby_mapping:
                if career['title'].lower() in [c.lower() for c in self.hobby_mapping[hobby]]:
                    hobby_related.append(hobby)
        if hobby_related:
            details['hobbies'] = f"Matches: {', '.join(hobby_related[:2])}"
        else:
            details['hobbies'] = "No direct match"
        
        user_edu = self.education_levels.get(user_inputs['education'], 1)
        career_edu = self.education_levels.get(career['min_education'], 1)
        if user_edu >= career_edu:
            details['education'] = 'Meets requirement'
        else:
            details['education'] = f"Needs {career['min_education']}"
        
        return details
    
    def get_all_careers_df(self):
        """Get all careers as pandas DataFrame for analysis"""
        data = []
        for career in self.careers:
            data.append({
                'Title': career['title'],
                'Field': career['field'],
                'Min Education': career['min_education'],
                'Work Styles': ', '.join(career['work_styles']),
                'Salary Range': career.get('salary_range', 'Varies'),
                'Growth Rate': career.get('growth_rate', 'Medium')
            })
        return pd.DataFrame(data)
    
    def get_skill_suggestions(self):
        """Get all skill suggestions grouped by category"""
        return {
            "Technical": ["Python", "Java", "JavaScript", "SQL", "C++", "HTML/CSS", "React", "Node.js", "AWS", "Docker", "Git", "Linux", "Machine Learning", "Data Analysis", "Cloud Computing"],
            "Medical": ["Patient Care", "Diagnosis", "Medical Knowledge", "Emergency Response", "Surgery", "Anatomy", "Pharmacology", "Lab Skills", "Radiology", "First Aid"],
            "Education": ["Teaching", "Lesson Planning", "Classroom Management", "Curriculum Design", "Student Assessment", "Mentoring", "Educational Technology"],
            "Business": ["Communication", "Leadership", "Project Management", "Marketing", "Sales", "Negotiation", "Financial Analysis", "Strategic Planning", "Team Management"],
            "Creative": ["Design", "Creativity", "Photoshop", "Illustrator", "Video Editing", "Content Writing", "Photography", "Animation", "Typography"],
            "Hospitality": ["Customer Service", "Cooking", "Food Safety", "Event Planning", "Inventory Management", "Bartending", "Housekeeping"],
            "Government": ["Administration", "Law Knowledge", "Public Speaking", "Policy Making", "Crisis Management", "Record Keeping", "Public Relations"]
        }
    
    def get_hobby_suggestions(self):
        """Get all hobby suggestions"""
        return list(self.hobby_mapping.keys())
    
    def _initialize_careers(self):
        """Initialize comprehensive career database"""
        return [
            # MEDICAL DOMAIN
            {
                "title": "Doctor (MBBS)",
                "field": "Medical",
                "required_skills": ["Patient Care", "Diagnosis", "Medical Knowledge", "Communication", "Emergency Response"],
                "min_education": "MBBS",
                "work_styles": ["Field", "Office"],
                "salary_range": "₹8-25 LPA",
                "growth_rate": "High",
                "description": "Diagnose and treat medical conditions, perform surgeries, and provide healthcare to patients."
            },
            {
                "title": "Nurse",
                "field": "Medical",
                "required_skills": ["Patient Care", "Communication", "Medical Knowledge", "Emergency Response", "Compassion"],
                "min_education": "Bachelor",
                "work_styles": ["Field", "Office"],
                "salary_range": "₹3-8 LPA",
                "growth_rate": "High",
                "description": "Provide patient care, assist doctors, and administer medications in hospitals and clinics."
            },
            {
                "title": "Pharmacist",
                "field": "Medical",
                "required_skills": ["Medical Knowledge", "Attention to Detail", "Customer Service", "Inventory Management", "Communication"],
                "min_education": "Bachelor",
                "work_styles": ["Office"],
                "salary_range": "₹3-6 LPA",
                "growth_rate": "Medium",
                "description": "Dispense medications, counsel patients on drug interactions, and manage pharmacy inventory."
            },
            {
                "title": "Physiotherapist",
                "field": "Medical",
                "required_skills": ["Patient Care", "Exercise Prescription", "Anatomy Knowledge", "Communication", "Manual Therapy"],
                "min_education": "Bachelor",
                "work_styles": ["Office", "Field"],
                "salary_range": "₹4-10 LPA",
                "growth_rate": "High",
                "description": "Help patients recover from injuries through exercise, massage, and rehabilitation techniques."
            },
            {
                "title": "Dentist",
                "field": "Medical",
                "required_skills": ["Patient Care", "Manual Dexterity", "Medical Knowledge", "Communication", "Problem Solving"],
                "min_education": "Bachelor",
                "work_styles": ["Office"],
                "salary_range": "₹5-15 LPA",
                "growth_rate": "Medium",
                "description": "Diagnose and treat dental issues, perform procedures like fillings, extractions, and root canals."
            },
            {
                "title": "Psychologist",
                "field": "Medical",
                "required_skills": ["Counseling", "Psychology", "Communication", "Empathy", "Active Listening"],
                "min_education": "Master",
                "work_styles": ["Office", "Remote"],
                "salary_range": "₹5-12 LPA",
                "growth_rate": "High",
                "description": "Help people manage mental health issues, provide therapy and counseling sessions."
            },
            {
                "title": "Medical Lab Technician",
                "field": "Medical",
                "required_skills": ["Lab Equipment", "Attention to Detail", "Sample Analysis", "Medical Knowledge", "Data Recording"],
                "min_education": "Diploma",
                "work_styles": ["Office"],
                "salary_range": "₹2-5 LPA",
                "growth_rate": "Medium",
                "description": "Perform laboratory tests, analyze blood/tissue samples, and maintain lab equipment."
            },
            
            # TECHNOLOGY DOMAIN
            {
                "title": "Software Developer",
                "field": "Technology",
                "required_skills": ["Python", "Java", "JavaScript", "Problem Solving", "Databases"],
                "min_education": "Bachelor",
                "work_styles": ["Remote", "Office"],
                "salary_range": "₹5-25 LPA",
                "growth_rate": "High",
                "description": "Design, code, and maintain software applications and systems."
            },
            {
                "title": "Data Scientist",
                "field": "Technology",
                "required_skills": ["Python", "Machine Learning", "Statistics", "SQL", "Data Analysis"],
                "min_education": "Master",
                "work_styles": ["Remote", "Office"],
                "salary_range": "₹8-30 LPA",
                "growth_rate": "High",
                "description": "Analyze complex data, build predictive models, drive business decisions."
            },
            {
                "title": "Game Developer",
                "field": "Technology",
                "required_skills": ["C#", "Unity", "Game Design", "Problem Solving", "Creativity"],
                "min_education": "Bachelor",
                "work_styles": ["Office", "Remote"],
                "salary_range": "₹5-20 LPA",
                "growth_rate": "High",
                "description": "Create video games for consoles, PC, and mobile devices."
            },
            {
                "title": "Cybersecurity Analyst",
                "field": "Technology",
                "required_skills": ["Network Security", "Risk Assessment", "Ethical Hacking", "Security Tools", "Problem Solving"],
                "min_education": "Bachelor",
                "work_styles": ["Office", "Remote"],
                "salary_range": "₹6-20 LPA",
                "growth_rate": "High",
                "description": "Protect systems from cyber threats, conduct security audits, respond to incidents."
            },
            {
                "title": "AI/ML Engineer",
                "field": "Technology",
                "required_skills": ["Python", "TensorFlow", "Deep Learning", "Mathematics", "Problem Solving"],
                "min_education": "Master",
                "work_styles": ["Remote", "Office"],
                "salary_range": "₹10-35 LPA",
                "growth_rate": "High",
                "description": "Build AI models, implement machine learning algorithms, create intelligent systems."
            },
            {
                "title": "Web Developer",
                "field": "Technology",
                "required_skills": ["HTML/CSS", "JavaScript", "React", "Node.js", "Databases"],
                "min_education": "Bachelor",
                "work_styles": ["Remote", "Office"],
                "salary_range": "₹4-18 LPA",
                "growth_rate": "High",
                "description": "Build and maintain websites and web applications for clients and companies."
            },
            
            # EDUCATION DOMAIN
            {
                "title": "School Teacher",
                "field": "Education",
                "required_skills": ["Communication", "Patience", "Lesson Planning", "Classroom Management", "Subject Knowledge"],
                "min_education": "Bachelor",
                "work_styles": ["Office"],
                "salary_range": "₹3-8 LPA",
                "growth_rate": "Medium",
                "description": "Educate students in primary or secondary schools, create engaging lessons."
            },
            {
                "title": "University Professor",
                "field": "Education",
                "required_skills": ["Research", "Teaching", "Subject Expertise", "Communication", "Mentoring"],
                "min_education": "Master",
                "work_styles": ["Office"],
                "salary_range": "₹6-20 LPA",
                "growth_rate": "Medium",
                "description": "Teach at colleges/universities, conduct research, publish papers, mentor students."
            },
            {
                "title": "Educational Counselor",
                "field": "Education",
                "required_skills": ["Communication", "Psychology", "Problem Solving", "Listening", "Career Guidance"],
                "min_education": "Bachelor",
                "work_styles": ["Office", "Remote"],
                "salary_range": "₹3-8 LPA",
                "growth_rate": "High",
                "description": "Help students with career choices, academic issues, and personal development."
            },
            {
                "title": "Online Tutor",
                "field": "Education",
                "required_skills": ["Subject Knowledge", "Communication", "Tech Skills", "Patience", "Lesson Planning"],
                "min_education": "Bachelor",
                "work_styles": ["Remote"],
                "salary_range": "₹3-10 LPA",
                "growth_rate": "High",
                "description": "Provide personalized teaching through online platforms to students worldwide."
            },
            
            # HOTEL/HOSPITALITY DOMAIN
            {
                "title": "Hotel Manager",
                "field": "Hotel",
                "required_skills": ["Leadership", "Customer Service", "Management", "Communication", "Problem Solving"],
                "min_education": "Bachelor",
                "work_styles": ["Office", "Field"],
                "salary_range": "₹5-20 LPA",
                "growth_rate": "Medium",
                "description": "Oversee hotel operations, manage staff, ensure guest satisfaction and profitability."
            },
            {
                "title": "Chef",
                "field": "Hotel",
                "required_skills": ["Cooking", "Creativity", "Kitchen Management", "Food Safety", "Team Leadership"],
                "min_education": "Diploma",
                "work_styles": ["Office"],
                "salary_range": "₹3-15 LPA",
                "growth_rate": "Medium",
                "description": "Prepare high-quality meals, manage kitchen staff, create menus, ensure food quality."
            },
            {
                "title": "Event Planner",
                "field": "Hotel",
                "required_skills": ["Organization", "Communication", "Creativity", "Budgeting", "Problem Solving"],
                "min_education": "Bachelor",
                "work_styles": ["Field", "Office"],
                "salary_range": "₹4-12 LPA",
                "growth_rate": "High",
                "description": "Plan and coordinate weddings, conferences, parties, and corporate events."
            },
            {
                "title": "Travel Consultant",
                "field": "Hotel",
                "required_skills": ["Communication", "Planning", "Customer Service", "Geography Knowledge", "Sales"],
                "min_education": "Bachelor",
                "work_styles": ["Office", "Remote"],
                "salary_range": "₹3-8 LPA",
                "growth_rate": "Medium",
                "description": "Help clients plan trips, book flights/hotels, provide travel advice and itineraries."
            },
            
            # GOVERNMENT DOMAIN
            {
                "title": "IAS Officer",
                "field": "Government",
                "required_skills": ["Leadership", "Administration", "Communication", "Problem Solving", "Public Service"],
                "min_education": "Bachelor",
                "work_styles": ["Field", "Office"],
                "salary_range": "₹10-25 LPA",
                "growth_rate": "High",
                "description": "Top civil servant, implement government policies, administer districts/departments."
            },
            {
                "title": "Police Officer",
                "field": "Government",
                "required_skills": ["Leadership", "Physical Fitness", "Law Knowledge", "Communication", "Crisis Management"],
                "min_education": "Bachelor",
                "work_styles": ["Field", "Office"],
                "salary_range": "₹5-12 LPA",
                "growth_rate": "Medium",
                "description": "Maintain law and order, investigate crimes, protect citizens and property."
            },
            {
                "title": "Lawyer",
                "field": "Government",
                "required_skills": ["Legal Knowledge", "Argumentation", "Research", "Communication", "Analytical Thinking"],
                "min_education": "Bachelor",
                "work_styles": ["Office", "Field"],
                "salary_range": "₹5-25 LPA",
                "growth_rate": "High",
                "description": "Represent clients in legal matters, provide legal advice, argue cases in court."
            },
            {
                "title": "Bank PO",
                "field": "Government",
                "required_skills": ["Numerical Ability", "Customer Service", "Communication", "Financial Knowledge", "Management"],
                "min_education": "Bachelor",
                "work_styles": ["Office"],
                "salary_range": "₹6-12 LPA",
                "growth_rate": "Medium",
                "description": "Manage banking operations, handle customer accounts, oversee branch activities."
            },
            
            # BUSINESS DOMAIN
            {
                "title": "Business Analyst",
                "field": "Business",
                "required_skills": ["Data Analysis", "Communication", "Problem Solving", "SQL", "Documentation"],
                "min_education": "Bachelor",
                "work_styles": ["Office", "Remote"],
                "salary_range": "₹6-18 LPA",
                "growth_rate": "High",
                "description": "Analyze business processes, gather requirements, recommend solutions."
            },
            {
                "title": "Marketing Manager",
                "field": "Business",
                "required_skills": ["Marketing Strategy", "Digital Marketing", "Analytics", "Leadership", "Creativity"],
                "min_education": "Bachelor",
                "work_styles": ["Office", "Remote"],
                "salary_range": "₹8-25 LPA",
                "growth_rate": "High",
                "description": "Develop marketing campaigns, manage brand, drive customer acquisition."
            },
            {
                "title": "Entrepreneur",
                "field": "Business",
                "required_skills": ["Leadership", "Risk Taking", "Innovation", "Business Planning", "Problem Solving"],
                "min_education": "Bachelor",
                "work_styles": ["Remote", "Field", "Office"],
                "salary_range": "₹5-100 LPA",
                "growth_rate": "High",
                "description": "Start and run your own business, create innovative products/services."
            },
            {
                "title": "HR Manager",
                "field": "Business",
                "required_skills": ["Communication", "Recruitment", "Employee Relations", "Leadership", "Organization"],
                "min_education": "Bachelor",
                "work_styles": ["Office", "Remote"],
                "salary_range": "₹6-18 LPA",
                "growth_rate": "Medium",
                "description": "Manage hiring, employee benefits, training, and workplace culture."
            },
            
            # ARTS DOMAIN
            {
                "title": "Graphic Designer",
                "field": "Arts",
                "required_skills": ["Design", "Photoshop", "Illustrator", "Creativity", "Typography"],
                "min_education": "Diploma",
                "work_styles": ["Remote", "Office"],
                "salary_range": "₹3-12 LPA",
                "growth_rate": "Medium",
                "description": "Create visual content for brands, websites, and marketing materials."
            },
            {
                "title": "Content Writer",
                "field": "Arts",
                "required_skills": ["Writing", "Research", "Creativity", "SEO", "Communication"],
                "min_education": "Bachelor",
                "work_styles": ["Remote", "Office"],
                "salary_range": "₹3-10 LPA",
                "growth_rate": "High",
                "description": "Create engaging content for blogs, websites, social media, and marketing."
            },
            {
                "title": "Photographer",
                "field": "Arts",
                "required_skills": ["Photography", "Editing", "Creativity", "Lighting", "Composition"],
                "min_education": "Diploma",
                "work_styles": ["Field", "Remote"],
                "salary_range": "₹3-15 LPA",
                "growth_rate": "Medium",
                "description": "Capture professional photos for events, products, portraits, and commercial use."
            },
            {
                "title": "Video Editor",
                "field": "Arts",
                "required_skills": ["Video Editing", "Premiere Pro", "Creativity", "Storytelling", "Color Grading"],
                "min_education": "Diploma",
                "work_styles": ["Remote", "Office"],
                "salary_range": "₹3-12 LPA",
                "growth_rate": "High",
                "description": "Edit video content for YouTube, films, commercials, and social media."
            },
            {
                "title": "Animator",
                "field": "Arts",
                "required_skills": ["Animation", "Creativity", "2D/3D Software", "Storyboarding", "Patience"],
                "min_education": "Bachelor",
                "work_styles": ["Office", "Remote"],
                "salary_range": "₹4-15 LPA",
                "growth_rate": "High",
                "description": "Create animated characters, scenes, and visual effects for media."
            }
        ]