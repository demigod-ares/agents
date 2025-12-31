# LinkedIn Message Automation using https://pypi.org/project/linkedin-api/ library for python
# This version is configured to fetch a specific number of connections to avoid overwhelming the LinkedIn API.

# %%
# Step 1: Imports and LinkedIn API Client setup
import os
import time
import traceback
from typing import List, Dict
from dotenv import load_dotenv
from linkedin_api import Linkedin

load_dotenv(override=True)
username = os.getenv("LINKEDIN_USERNAME")
password = os.getenv("LINKEDIN_PASSWORD")
if not username or not password:
    print("CRITICAL: Credentials not found in .env file!")


# %% 
# Step 2: Defining the Robust Client Class
# A single connection object from LinkedIn API looks like this:
# {'urn_id': 'ACoAACDZky4B2o7MraFVl12N2otH9zi03NF_YKo', 'distance': 'DISTANCE_1', 'jobtitle': 'IT Analyst at Tata consultancy services', 'location': 'New Delhi', 'name': 'VIPUL PANWAR'}
class LinkedInClient:
    def __init__(self, username: str, password: str):
        """Initialize LinkedIn API client"""
        if not username or not password:
            raise ValueError("LinkedIn credentials (username/password) must be provided")
        self.api = Linkedin(username, password)
        print("Successfully authenticated with LinkedIn.")

    def get_connections(self, limit: int, offset: int) -> List[Dict]:
        """Get first-degree connections with a specific limit and offset"""
        print(f"Fetching first {limit} first-degree connections with offset {offset}.")
        connections = self.api.search_people(
            network_depths=["F"],
            include_private_profiles=True,
            limit=limit # should be a multiple of 10 with max value 1000
            # offset=offset
        )
        return connections

    def get_jobs(self, limit: int, offset: int) -> List[Dict]:
        """Get jobs with a specific limit and offset"""
        print(f"Fetching first {limit} jobs with offset {offset}.")
        jobs = self.api.search_jobs(
            job_title="Software Engineer",
            job_type=["F"],
            location_name="India",
            limit=limit # should be a multiple of 10 with max value 1000
            # offset=offset
        )
        return jobs

    def send_personalized_bulk_messages(self, connections: List[Dict], message_template: str, delay: int):
        """Send messages to a list of connections with personalization and error detail"""
        success_count = 0
        for i, connection in enumerate(connections, 1):
            try:
                # Extracting ID
                profile_urn = connection.get('urn_id') or connection.get('public_id')
                if not profile_urn:
                    print(f"[{i}/{len(connections)}] Skipping: No valid ID found for user.")
                    continue
                # FIX: Try to get name directly from the connection object first.
                name = connection.get('name')
                name = name or "there"
                message = message_template.format(name=name)
                
                # Attempting to send message
                print(f"[{i}/{len(connections)}] Attempting to message {name} ({profile_urn})...")
                self.api.send_message(
                    message_body=message,
                    recipients=[profile_urn]
                )
                success_count += 1
                print(f"[OK] Message sent. Success count: {success_count}")
                # Delay to be safe
                time.sleep(delay)
                
            except Exception as e:
                print(f"\n[!!!] FAILED at connection {i}:")
                print(traceback.format_exc())
                # Check if it was a rate limit
                if "429" in str(e) or "throttle" in str(e).lower():
                    print("Rate limit detected. Stopping bulk run.")
                    break
                continue
        
        return success_count


# %% 
# Step 3: Run the Automation
message_template = "Hi {name}, best wishes to you and your family on this auspicious occasion of New Year!"
if __name__ == "__main__":
    client = LinkedInClient(username, password)
    rate_limit_hit = False
    print(f"Starting bulk message campaign...")    
    # ACCOUNT BAN WARNING:Don't ever loop until no more connections or rate limit is hit
    limit = 100  # Number of connections to fetch per batch
    offset = 400   # Starting offset
    try:
        # Fetch connections
        connections = client.get_connections(limit=limit, offset=offset)
        print(f"Retrieved {len(connections)} connections.")
        # Stop if no connections retrieved
        if not connections:
            print("No more connections to process. Stopping.")
        # Send messages to this batch
        sent_count = client.send_personalized_bulk_messages(
            connections=connections,
            message_template=message_template,
            delay=5  # 5 sec delay
        )
        print(f"Total sent so far: {sent_count}")
    except Exception as e:
        print(f"\n[!!!] ERROR in sending bulk messages:")
        print(traceback.format_exc())
        # Check for rate limiting
        if "429" in str(e) or "throttle" in str(e).lower():
            print("Rate limit detected. Stopping bulk run.")
            rate_limit_hit = True
    # Final summary
    print(f"\n{'='*60}")
    print(f"Campaign Summary:")
    if rate_limit_hit:
        print(f"  Status: Stopped due to rate limit")
    else:
        print(f"  Status: Completed successfully")
    print(f"{'='*60}")

# %%
# Step 4: Fetch jobs
if __name__ == "__main__":
    client = LinkedInClient(username, password)
    limit = 15  # Number of connections to fetch per batch
    offset = 0  # Starting offset
    jobs = client.get_jobs(limit=limit, offset=offset)
    print(f"Retrieved {len(jobs)} jobs. {jobs}")
