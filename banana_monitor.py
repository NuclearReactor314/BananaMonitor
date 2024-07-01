import requests
import json

# Load API credentials from config file
def load_config():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config

# Get activities from Strava
def get_strava_activities(access_token):
    url = f"https://www.strava.com/api/v3/athlete/activities"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    activities = response.json()
    return activities

# Calculate the total calories burned
def calculate_calories(activities):
    total_calories = 0
    for activity in activities:
        if 'calories' in activity:
            total_calories += activity['calories']
    return total_calories

# Calculate the number of bananas needed
def calculate_bananas(calories_burned):
    CALORIES_PER_BANANA = 105
    bananas_needed = calories_burned / CALORIES_PER_BANANA
    return bananas_needed

# Update Strava activity description
def update_activity_description(activity_id, access_token, bananas_needed, website_url):
    url = f"https://www.strava.com/api/v3/activities/{activity_id}"
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    description = f"Burned enough calories for {bananas_needed:.2f} bananas. Check out more details at {website_url}."
    data = {'description': description}
    response = requests.put(url, headers=headers, data=json.dumps(data))
    return response.json()

# Main function
def main():
    config = load_config()
    activities = get_strava_activities(config['access_token'])
    total_calories = calculate_calories(activities)
    bananas_needed = calculate_bananas(total_calories)
    website_url = config['website_url']
    
    print(f"Total calories burned: {total_calories}")
    print(f"Bananas needed: {bananas_needed}")

    # Update each activity description
    for activity in activities:
        activity_id = activity['id']
        update_activity_description(activity_id, config['access_token'], bananas_needed, website_url)
        print(f"Updated activity {activity_id} with bananas needed.")

if __name__ == "__main__":
    main()
