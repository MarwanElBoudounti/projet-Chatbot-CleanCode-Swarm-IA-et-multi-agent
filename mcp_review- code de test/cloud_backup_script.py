import os
import boto3
import requests
import mysql.connector

# --- CONFIGURATION SENSIBLE (FAILLES CRITIQUES) ---

# 1. Identifiants AWS en clair (Interdit en Clean Code !)
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# 2. Connexion Base de données avec mot de passe Root
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="192.168.1.50",
            user="root",
            password="SuperSecretPassword123!",
            database="production_db"
        )
        return connection
    except Exception as e:
        print(f"Erreur de connexion : {e}")

# 3. Requête API sans vérification SSL (Faille de sécurité)
def fetch_external_config():
    url = "https://api.internal-service.com/config"
    # Le verify=False désactive la sécurité HTTPS
    response = requests.get(url, verify=False)
    return response.json()

# --- LOGIQUE DU SCRIPT ---

def upload_to_s3(file_name, bucket):
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    s3.upload_file(file_name, bucket, file_name)
    print(f"Fichier {file_name} sauvegardé sur S3.")

if __name__ == "__main__":
    print("Démarrage de la sauvegarde Cloud...")
    # Simulation d'exécution
    # upload_to_s3("backup.zip", "my-prod-bucket")