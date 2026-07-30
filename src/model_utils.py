import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

encoders = joblib.load(os.path.join(BASE_DIR, "models", "encoders.pkl"))

def preprocess(df):
    df = df.copy()

    for col in ["protocol_type", "service", "flag"]:
        encoder = encoders[col]

        # Handle unknown values safely
        df[col] = df[col].apply(
            lambda x: x if x in encoder.classes_ else encoder.classes_[0]
        )

        df[col] = encoder.transform(df[col])

    df["label"] = df["label"].apply(
        lambda x: "normal" if x == "normal" else "attack"
    )

    y = encoders["label_encoder"].transform(df["label"])

    X = df.drop(["label", "difficulty"], axis=1)

    return X, y