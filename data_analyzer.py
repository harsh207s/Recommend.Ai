# data_analyzer.py - Career data analysis and visualization

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

class CareerAnalyzer:
    def __init__(self, career_engine):
        self.career_engine = career_engine
        self.df = career_engine.get_all_careers_df()
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        
    def generate_career_dashboard(self, user_name, user_inputs, recommendations):
        charts = {}
        charts['field_distribution'] = self._plot_field_distribution()
        charts['education_by_field'] = self._plot_education_by_field()
        charts['salary_distribution'] = self._plot_salary_distribution()
        charts['user_match_profile'] = self._plot_user_match_profile(recommendations)
        charts['growth_analysis'] = self._plot_growth_analysis()
        charts['top_skills'] = self._plot_top_skills()
        charts['work_styles'] = self._plot_work_styles()
        if len(recommendations) >= 3:
            charts['radar_chart'] = self._plot_radar_chart(recommendations[:3], user_inputs)
        return charts
    
    def _plot_field_distribution(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        field_counts = self.df['Field'].value_counts()
        colors = plt.cm.Set3(range(len(field_counts)))
        bars = ax.bar(field_counts.index, field_counts.values, color=colors, edgecolor='black')
        ax.set_title('Career Opportunities by Field', fontsize=16, fontweight='bold')
        ax.set_xlabel('Field', fontsize=12)
        ax.set_ylabel('Number of Careers', fontsize=12)
        for bar, value in zip(bars, field_counts.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                   str(value), ha='center', va='bottom', fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _plot_education_by_field(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        edu_order = ['Diploma', 'Bachelor', 'Master', 'MBBS']
        edu_cross = pd.crosstab(self.df['Field'], self.df['Min Education'], normalize='index') * 100
        edu_cross = edu_cross.reindex(columns=[c for c in edu_order if c in edu_cross.columns])
        edu_cross.plot(kind='bar', stacked=True, ax=ax, colormap='viridis', edgecolor='black')
        ax.set_title('Education Requirements by Field (%)', fontsize=16, fontweight='bold')
        ax.set_xlabel('Field', fontsize=12)
        ax.set_ylabel('Percentage (%)', fontsize=12)
        ax.legend(title='Education Level', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _plot_salary_distribution(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        salary_data = []
        for idx, row in self.df.iterrows():
            if row['Salary Range'] != 'Varies':
                try:
                    low, high = row['Salary Range'].replace('₹', '').replace('LPA', '').split('-')
                    avg_salary = (float(low) + float(high)) / 2
                    salary_data.append({'Field': row['Field'], 'Avg Salary': avg_salary})
                except:
                    pass
        if salary_data:
            salary_df = pd.DataFrame(salary_data)
            avg_salaries = salary_df.groupby('Field')['Avg Salary'].mean().sort_values(ascending=True)
            bars = ax.barh(avg_salaries.index, avg_salaries.values, color=plt.cm.RdYlGn(np.linspace(0.3, 0.8, len(avg_salaries))))
            ax.set_title('Average Salary by Field (Lakhs per annum)', fontsize=16, fontweight='bold')
            ax.set_xlabel('Average Salary (₹ LPA)', fontsize=12)
            for i, (bar, value) in enumerate(zip(bars, avg_salaries.values)):
                ax.text(value + 0.5, bar.get_y() + bar.get_height()/2, 
                       f'₹{value:.1f} LPA', va='center', fontweight='bold')
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _plot_user_match_profile(self, recommendations):
        fig, ax = plt.subplots(figsize=(10, 6))
        titles = [r['title'][:20] for r in recommendations[:8]]
        scores = [r['score'] for r in recommendations[:8]]
        colors = plt.cm.RdYlGn(np.array(scores) / 100)
        bars = ax.barh(range(len(titles)), scores, color=colors, edgecolor='black')
        ax.set_yticks(range(len(titles)))
        ax.set_yticklabels(titles)
        ax.set_xlabel('Match Score (%)', fontsize=12)
        ax.set_title('Your Top Career Matches', fontsize=16, fontweight='bold')
        ax.set_xlim(0, 100)
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax.text(score + 1, bar.get_y() + bar.get_height()/2, 
                   f'{score}%', va='center', fontweight='bold')
        ax.axvline(x=70, color='green', linestyle='--', alpha=0.7, label='Good Match (70%)')
        ax.legend()
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _plot_growth_analysis(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        growth_data = self.df.groupby(['Field', 'Growth Rate']).size().unstack(fill_value=0)
        growth_data.plot(kind='bar', stacked=True, ax=ax, colormap='coolwarm', edgecolor='black')
        ax.set_title('Career Growth Rate by Field', fontsize=16, fontweight='bold')
        ax.set_xlabel('Field', fontsize=12)
        ax.set_ylabel('Number of Careers', fontsize=12)
        ax.legend(title='Growth Rate', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _plot_top_skills(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        all_skills = []
        for career in self.career_engine.careers:
            all_skills.extend([s.lower() for s in career['required_skills']])
        skill_counts = pd.Series(all_skills).value_counts().head(15)
        colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(skill_counts)))
        bars = ax.barh(range(len(skill_counts)), skill_counts.values, color=colors, edgecolor='black')
        ax.set_yticks(range(len(skill_counts)))
        ax.set_yticklabels(skill_counts.index)
        ax.set_xlabel('Frequency', fontsize=12)
        ax.set_title('Top 15 Most In-Demand Skills', fontsize=16, fontweight='bold')
        for i, (bar, value) in enumerate(zip(bars, skill_counts.values)):
            ax.text(value + 0.5, bar.get_y() + bar.get_height()/2, 
                   str(value), va='center', fontweight='bold')
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _plot_work_styles(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        work_style_data = []
        for career in self.career_engine.careers:
            for style in career['work_styles']:
                work_style_data.append({'Field': career['field'], 'Work Style': style})
        ws_df = pd.DataFrame(work_style_data)
        ws_pivot = pd.crosstab(ws_df['Field'], ws_df['Work Style'], normalize='index') * 100
        ws_pivot.plot(kind='bar', stacked=True, ax=ax, colormap='Set2', edgecolor='black')
        ax.set_title('Work Style Preferences by Field (%)', fontsize=16, fontweight='bold')
        ax.set_xlabel('Field', fontsize=12)
        ax.set_ylabel('Percentage (%)', fontsize=12)
        ax.legend(title='Work Style', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _plot_radar_chart(self, top_careers, user_inputs):
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        criteria = ['Field Match', 'Skills Match', 'Education Match', 'Work Style', 'Growth Potential', 'Salary']
        num_vars = len(criteria)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        for idx, career in enumerate(top_careers):
            values = [
                self._calculate_field_score(user_inputs['interests'], career['field']),
                self._calculate_skill_score(user_inputs['skills'], career['required_skills']),
                self._calculate_education_score(user_inputs['education'], career.get('min_education', 'Bachelor')),
                self._calculate_workstyle_score(user_inputs['work_style'], career.get('work_styles', ['Office'])),
                self._calculate_growth_score(career.get('growth_rate', 'Medium')),
                self._calculate_salary_score(career.get('salary_range', '₹5-10 LPA'))
            ]
            values += values[:1]
            ax.plot(angles, values, 'o-', linewidth=2, label=career['title'][:15], color=colors[idx])
            ax.fill(angles, values, alpha=0.15, color=colors[idx])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(criteria, fontsize=10)
        ax.set_ylim(0, 100)
        ax.set_title('Career Comparison Radar Chart', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        ax.grid(True)
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _calculate_field_score(self, user_interest, career_field):
        if user_interest.lower() == career_field.lower():
            return 100
        elif career_field.lower() in user_interest.lower():
            return 70
        return 30
    
    def _calculate_skill_score(self, user_skills_str, career_skills):
        user_skills = [s.strip().lower() for s in user_skills_str.split(',')]
        career_skills_lower = [s.lower() for s in career_skills]
        matched = sum(1 for us in user_skills for cs in career_skills_lower if us in cs or cs in us)
        return min(100, (matched / max(1, len(career_skills_lower))) * 100)
    
    def _calculate_education_score(self, user_edu, career_edu):
        edu_levels = {'High School': 1, 'Diploma': 2, 'Bachelor': 3, 'Master': 4, 'PhD': 5, 'MBBS': 5}
        user_score = edu_levels.get(user_edu, 1)
        career_score = edu_levels.get(career_edu, 3)
        if user_score >= career_score:
            return 100
        elif user_score == career_score - 1:
            return 60
        return 20
    
    def _calculate_workstyle_score(self, user_style, career_styles):
        if user_style in career_styles:
            return 100
        return 40
    
    def _calculate_growth_score(self, growth_rate):
        growth_map = {'High': 100, 'Medium': 60, 'Low': 30}
        return growth_map.get(growth_rate, 50)
    
    def _calculate_salary_score(self, salary_range):
        if salary_range == 'Varies':
            return 50
        try:
            low, high = salary_range.replace('₹', '').replace('LPA', '').split('-')
            avg = (float(low) + float(high)) / 2
            return min(100, (avg / 40) * 100)
        except:
            return 50
    
    def _fig_to_base64(self, fig):
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig)
        return img_base64
    
    def generate_statistics(self):
        stats = {
            'total_careers': len(self.df),
            'fields': self.df['Field'].nunique(),
            'top_fields': self.df['Field'].value_counts().head(3).to_dict(),
            'education_distribution': self.df['Min Education'].value_counts().to_dict(),
            'high_growth_careers': len(self.df[self.df['Growth Rate'] == 'High']),
            'avg_salary_by_field': {}
        }
        for field in self.df['Field'].unique():
            field_data = self.df[self.df['Field'] == field]
            salaries = []
            for salary in field_data['Salary Range']:
                if salary != 'Varies':
                    try:
                        low, high = salary.replace('₹', '').replace('LPA', '').split('-')
                        salaries.append((float(low) + float(high)) / 2)
                    except:
                        pass
            if salaries:
                stats['avg_salary_by_field'][field] = round(np.mean(salaries), 1)
        return stats