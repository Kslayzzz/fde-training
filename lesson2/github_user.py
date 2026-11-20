import sys
import requests

def get_github_user(username):
    url = f"https://api.github.com/users/{username}"
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Network problem: {e}")
        return None, None

    if response.status_code == 404:
        print(f"No GitHub user named '{username}'.")
        return None, None
    response.raise_for_status()

    remaining = response.headers.get("x-ratelimit-remaining")
    return response.json(), remaining

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "Kslayzzz"
    user, remaining = get_github_user(username)
    if user:
        print(f"{user['login']} has {user['public_repos']} public repos.")
        print(f"Remaining requests this hour: {remaining}")