import pandas as pd
import joblib


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
    top_jobs = df.sort_values('match_score', ascending=False).head(10)
    
    top_jobs = top_jobs[['job_title','company','location','skills','salary_min','salary_max','match_score']].to_dict(orient='records')

    for job in top_jobs:
        job['skills'] = [s.strip() for s in job['skills'].split(',')]

    """Predict job titles based on user skills using the trained model."""

    rfc = joblib.load('models/rfc.pkl')  # load the classifier model
    mlb = joblib.load('models/mlb.pkl')  # load the MultiLabelBinarizer
    le = joblib.load('models/le.pkl')    # load the LabelEncoder    
    kmeans = joblib.load('models/kmeans.pkl')  # load the KMeans model
    rfr = joblib.load('models/rfr.pkl')  # load the Random Forest Regressor

    # encode
    user_vector = mlb.transform([user_skill_list])

    # predict
    predicted_title = le.inverse_transform(rfc.predict(user_vector))[0]
    predicted_salary = round(rfr.predict(user_vector)[0], 2)
    predicted_cluster = int(kmeans.predict(user_vector)[0])

    return top_jobs, predicted_title, predicted_salary, predicted_cluster