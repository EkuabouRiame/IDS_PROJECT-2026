import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Column names
columns = [
    "duration","protocol_type","service","flag","src_bytes",
    "dst_bytes","land","wrong_fragment","urgent","hot",
    "num_failed_logins","logged_in","num_compromised",
    "root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files",
    "num_outbound_cmds","is_host_login","is_guest_login",
    "count","srv_count","serror_rate","srv_serror_rate",
    "rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count",
    "dst_host_srv_count","dst_host_same_srv_rate",
    "dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate",
    "dst_host_srv_rerror_rate","label","difficulty"
]

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load dataset
train = pd.read_csv(
    os.path.join(BASE_DIR, "dataset", "KDDTrain+.txt"),
    names=columns
)

print("Original Shape:", train.shape)

# Remove duplicates
train = train.drop_duplicates()

print("After Removing Duplicates:", train.shape)

# Encode categorical columns
encoder = LabelEncoder()

categorical_columns = [
    "protocol_type",
    "service",
    "flag"
]

for col in categorical_columns:
    train[col] = encoder.fit_transform(train[col])

# Convert labels
train["label"] = train["label"].apply(
    lambda x: "normal" if x == "normal" else "attack"
)

train["label"] = LabelEncoder().fit_transform(train["label"])

print("\nEncoded Data")
print(train.head())

print("\nLabel Counts")
print(train["label"].value_counts())