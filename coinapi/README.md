# Crypto Alert Project
API for managing cryptocurrency alerts

## Features
- Create cryptocurrency alerts
- Get cryptocurrency alerts
- Update cryptocurrency alerts
- Delete cryptocurrency alerts


## Available endpoints
Here are the entry points available for the API with a brief explanation of each:

-POST /alerts: Create a new cryptocurrency alert. Returns a confirmation message.

-GET /alerts: Get a list of all alerts. Returns a message indicating that alerts are retrieved.

-POST /alerts/<currency_id>: Update a cryptocurrency alert based on its identifier. Returns an update message.

-DELETE /alerts/<currency_id> : Delete a cryptocurrency alert by its identifier. Returns a message indicating that the alert has been deleted.

## Installation
To install the API, you first need to install Python and Flask. Then you can set up a virtual environment to isolate your project's dependencies.

```bash

# Create a virtual environment
python -m venv env

# Activate the virtual environment
source env/bin/activate # For Linux/macOS
env\Scripts\activate # For Windows

# Install Flask
pip install flask

