import pandas as pd

def recommend_jobs(user_skills, top_n=5):
    # load dataset
    df = pd.read_csv('datasets/job_market.csv')
    df = df.dropna(subset=['skills'])
    
    # convert user skills to a list
    user_skill_list = [s.strip().lower() for s in user_skills.split(',')]
    
    # count how many skills match each job
    def count_matches(job_skills):
        job_skill_list = [s.strip().lower() for s in job_skills.split(',')]
        return len(set(user_skill_list) & set(job_skill_list))
    
    df['match_score'] = df['skills'].apply(count_matches)
    
    # sort by best match
    top_jobs = df.sort_values('match_score', ascending=False).head(top_n)
    
    return top_jobs[['job_title', 'company', 'location', 'skills', 'salary_min', 'salary_max', 'match_score']].to_dict(orient='records')