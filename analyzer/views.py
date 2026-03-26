from django.shortcuts import render
from ml_engine.recommender import recommend_jobs

def Home_Page(request):
    return render(request, 'home.html')

def Recommend(request):
    if request.method == "POST":
        user_skills = request.POST.get('skills', '')
        jobs = recommend_jobs(user_skills)
        return render(request, 'results.html', {'jobs': jobs , 'skills': user_skills})
    return render(request, 'recommend.html')



def Insights(request):
    return render(request, 'insights.html')
