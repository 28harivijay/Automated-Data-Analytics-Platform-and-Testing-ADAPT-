from django.shortcuts import render
from ml_engine.recommender import recommend_jobs
import pandas as pd

def Home_Page(request):
    return render(request, 'home.html')

def Upload(request):
    return render(request, 'upload.html')

def Results(request):
    if request.method == "POST":
        user_skills = request.POST.get('skills', '')
        jobs = recommend_jobs(user_skills)
        return render(request, 'results.html', {'jobs': jobs, 'skills': user_skills})
    return render(request, 'upload.html')

def Insights(request):
    df = pd.read_csv('datasets/job_market.csv')
    df = df.dropna(subset=['skills', 'company', 'location'])

    all_skills = df['skills'].str.split(', ').explode()
    top_skills = all_skills.value_counts().head(10).to_dict()

    top_companies = df['company'].value_counts().head(10).to_dict()

    df['avg_salary'] = (df['salary_min'] + df['salary_max']) / 2
    avg_salary = df.groupby('job_title')['avg_salary'].mean().round(0).sort_values(ascending=False).head(10).to_dict()

    top_locations = df['location'].value_counts().head(5).to_dict()

    context = {
        'top_skills': top_skills,
        'top_companies': top_companies,
        'avg_salary': avg_salary,
        'top_locations': top_locations,
    }
    return render(request, 'insights.html', context)
