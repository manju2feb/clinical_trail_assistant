import requests
import csv
import os

# Save directory
os.makedirs("../data", exist_ok=True)

def fetch_trials_v2(condition="cancer", max_trials=100):
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.term": condition,
        "pageSize": max_trials
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")

    data = response.json()
    trials = []

    for trial in data.get("studies", []):
        trials.append({
            "NCTId": trial.get("protocolSection", {}).get("identificationModule", {}).get("nctId", ""),
            "Title": trial.get("protocolSection", {}).get("identificationModule", {}).get("briefTitle", ""),
            "Condition": ', '.join(trial.get("protocolSection", {}).get("conditionsModule", {}).get("conditions", [])),
            "Phase": ', '.join(trial.get("protocolSection", {}).get("designModule", {}).get("phases", [])),
            "LocationCountry": ', '.join([
                loc.get("locationCountry", "")
                for loc in trial.get("protocolSection", {}).get("contactsLocationsModule", {}).get("locations", [])
            ]),
            "Sponsor": trial.get("protocolSection", {}).get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("leadSponsorName", "")
        })

    return trials

def save_to_csv(trials, path="../data/trials.csv"):
    if not trials:
        print(" No trials found.")
        return

    keys = trials[0].keys()
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(trials)

if __name__ == "__main__":
    trials = fetch_trials_v2(condition="cancer", max_trials=100)
    save_to_csv(trials)
    print(f"Saved {len(trials)} trials to ../data/trials.csv")
