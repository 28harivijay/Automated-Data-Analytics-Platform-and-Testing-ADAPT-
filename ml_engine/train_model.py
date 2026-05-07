import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.model_selection import train_test_split  
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, r2_score
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import joblib
import os

def load_data(input_file):
    """Load the CSV file and remove rows that do not have skills."""
    try:
        df = pd.read_csv(input_file)
        df = df.dropna(subset=['skills'])
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
    
def prepare_features(df):
    """Convert comma-separated skill text into a machine-learning feature matrix."""
    # Example: "python, sql" -> ["python", "sql"] for each row.
    Skill_List = [[s.strip().lower() for s in rows.split(',')] for rows in df['skills']]
    mlb = MultiLabelBinarizer()
    features = mlb.fit_transform(Skill_List)
    return features, mlb

def prepare_target(df):
    """Encode job titles as numeric labels for classification."""
    le = LabelEncoder()
    target = le.fit_transform(df['job_title'])
    return target, le

def split_data(features,target):
    """Split features and targets into training and testing sets (80/20)."""
    X = features
    y = target
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train):
    """Train a Random Forest classifier for job-title prediction."""
    rfc = RandomForestClassifier(n_estimators=100, random_state=42  )
    return rfc.fit(X_train, y_train)

def evaluate_model(rfc, X_test, y_test,le):
    """Print classification quality metrics and sample predicted job titles."""
    y_pred = rfc.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Sample Predictions:", le.inverse_transform(y_pred))
    return y_pred

def prepare_salary(df):
    """Create a numeric average salary target from min and max salary columns."""
    df = df.dropna(subset=['salary_min', 'salary_max'])
    df['salary_avg'] = (df['salary_min'] + df['salary_max']) / 2
    return df, df['salary_avg']

def train_regression(X_train,y_train):
    """Train a Random Forest regressor for salary prediction."""
    rfr =  RandomForestRegressor(n_estimators=100, random_state=42)
    return rfr.fit(X_train, y_train)

def evaluate_regression(rfr,X_test,y_test):
    """Print error and fit metrics for the salary model."""
    Y_pred = rfr.predict(X_test)
    print("Mean Absolute error:" , mean_absolute_error(y_test, Y_pred))
    print("R2 Score:" , r2_score(y_test, Y_pred))
    return Y_pred

def train_clustering(features, df):
    """Train KMeans with one cluster per unique job title in the dataset."""
    n_cluster = len(df['job_title'].unique())
    kmeans = KMeans(n_clusters=n_cluster, random_state=42)
    return kmeans, kmeans.fit_predict(features)

def evaluate_clustering(features, kmeans_labels):
    """Score clustering quality using silhouette score (higher is better)."""
    score = silhouette_score(features, kmeans_labels)
    print("Silhouette Score:", score)
    return score    


def main():
    """Run classification, regression, and clustering on the jobs dataset."""
    # Classification: predict job title from skill set.

    df = load_data('datasets/job_market.csv')

    if df is None:
        return
    
    features, mlb = prepare_features(df)
    target, le = prepare_target(df)
    X_train, X_test, y_train, y_test = split_data(features, target)
    rfc = train_model(X_train, y_train)

    print("\n=== Classification ===")
    evaluate_model(rfc, X_test, y_test, le)


    # Regression: estimate average salary from skill set.

    df_sal, salary = prepare_salary(df)
    features_sal, _ = prepare_features(df_sal)
    X_train_sal, X_test_sal, y_train_sal, y_test_sal = split_data(features_sal, salary)
    rfr = train_regression(X_train_sal, y_train_sal)

    print("\n=== Regression ===")
    evaluate_regression(rfr, X_test_sal, y_test_sal)


    # Clustering: group similar jobs by skills without target labels.

    print("\n=== Clustering ===")
    kmeans, kmeans_labels = train_clustering(features, df)
    evaluate_clustering(features, kmeans_labels)

    # create models folder if it doesn't exist
    os.makedirs('models', exist_ok=True)

    # save all 5 objects here
    joblib.dump(rfc, 'models/rfc.pkl')
    joblib.dump(rfr, 'models/rfr.pkl')
    joblib.dump(kmeans, 'models/kmeans.pkl')
    joblib.dump(mlb, 'models/mlb.pkl')
    joblib.dump(le, 'models/le.pkl')

    print("All models saved!")
        
if __name__ == "__main__": 
    main()
