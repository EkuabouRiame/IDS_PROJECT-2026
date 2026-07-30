import os
import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Column names
columns = [
    'duration','protocol_type','service','flag','src_bytes',
    'dst_bytes','land','wrong_fragment','urgent','hot',
    'num_failed_logins','logged_in','num_compromised',
    'root_shell','su_attempted','num_root',
    'num_file_creations','num_shells','num_access_files',
    'num_outbound_cmds','is_host_login','is_guest_login',
    'count','srv_count','serror_rate','srv_serror_rate',
    'rerror_rate','srv_rerror_rate','same_srv_rate',
    'diff_srv_rate','srv_diff_host_rate','dst_host_count',
    'dst_host_srv_count','dst_host_same_srv_rate',
    'dst_host_diff_srv_rate','dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate','dst_host_serror_rate',
    'dst_host_srv_serror_rate','dst_host_rerror_rate',
    'dst_host_srv_rerror_rate','label','difficulty'
]

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load dataset
data = pd.read_csv(
    os.path.join(BASE_DIR, 'dataset', 'KDDTrain+.txt'),
    names=columns
)

# Remove duplicates
data = data.drop_duplicates()

# Encode categorical columns
encoders = {}

for col in ['protocol_type', 'service', 'flag']:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    encoders[col] = le

# Convert labels
data['label'] = data['label'].apply(
    lambda x: 'normal' if x == 'normal' else 'attack'
)

label_encoder = LabelEncoder()
data['label'] = label_encoder.fit_transform(data['label'])

# Features and target
X = data.drop(['label', 'difficulty'], axis=1)
y = data['label']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print('Training samples:', X_train.shape[0])
print('Testing samples :', X_test.shape[0])

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

print('\nTraining Random Forest model...')
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print(f'\nModel Accuracy: {accuracy:.4f}')

print('\nClassification Report:\n')
print(classification_report(y_test, y_pred))

print('\nConfusion Matrix:\n')
print(confusion_matrix(y_test, y_pred))

# Save model
model_path = os.path.join(BASE_DIR, 'models', 'random_forest.pkl')
joblib.dump(model, model_path)
# Save encoders
encoder_path = os.path.join(BASE_DIR, "models", "encoders.pkl")

joblib.dump({
    "protocol_type": encoders["protocol_type"],
    "service": encoders["service"],
    "flag": encoders["flag"],
    "label_encoder": label_encoder
}, encoder_path)

print(f"Encoders saved to: {encoder_path}")

print(f'\nModel saved to: {model_path}')