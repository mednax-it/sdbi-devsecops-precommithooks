import subprocess
import json
import os
from datetime import datetime
import sys

def get_local_git_user() -> str:

    res = subprocess.run(["git", "config", "user.name"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return res.stdout.strip().decode()

def get_local_git_email() -> str:

    res = subprocess.run(["git", "config", "user.email"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return res.stdout.strip().decode()

def is_git_using_gpssign() -> bool:

    res = subprocess.run(["git", "config", "commit.gpgsign"], stdout=subprocess.PIPE, check=False)
    return res.stdout.strip().decode() == "true"

def append_new_user_record(username: str, email: str, gpgsign: bool, existing_data: dict) -> dict:

    existing_data.setdefault("users", [])
    new_entry = {
        "username": username,
        "email": email,
        "signed_commits": gpgsign,
        "last_run": datetime.now().isoformat()
    }
    existing_data["users"].append(new_entry)
    return existing_data

def update_time_on_user_record(username: str, email: str, existing_data: dict) -> bool:

    for user in existing_data.get("users", []):
        if user["username"] == username and user["email"] == email:
            user["last_run"] = datetime.now().isoformat()
            return True

    return False

def get_existing_user_records() -> dict:

    directory = ".github"
    file_path = os.path.join(directory, "precommit_user_record.json")

    if not os.path.exists(directory):
        os.makedirs(directory)

    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r") as f:
        return json.load(f)

def save_updated_user_record(data: dict):

    file_path = os.path.join(".github", "precommit_user_record.json")
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)



def main():

    try:
        username = get_local_git_user()
        email = get_local_git_email()
        gpgsign = is_git_using_gpssign()
    except subprocess.CalledProcessError as e:
        print(f"Could not retrieve git user info - this is likely due to the script being run not in a local environment. Please ignore! Error details: {e}")
        return 0

    if not username or not email:
        print("Git user.name or user.email is not configured, please set these properly.")
        return 1

    existing_data = get_existing_user_records()

    if not update_time_on_user_record(username, email, existing_data):
        updated_data = append_new_user_record(username, email, gpgsign, existing_data)
    else:
        updated_data = existing_data

    save_updated_user_record(updated_data)

    return


if __name__ == "__main__":
    if os.getenv('GITHUB_ACTIONS') == 'true':
        print("Not locally run, skipped")
        sys.exit(0)
    else:
        raise SystemExit(main())
