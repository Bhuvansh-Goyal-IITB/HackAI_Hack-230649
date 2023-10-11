
# Currency Exchange Alert Agent

An AI agent that notifies you when the exchange rates go out of bounds
made using uAgents library
- This is a CLI tool
- This agent lets you enter a base currency, multiple foreign currencies, and lets you set the min and max threshold values for each foreign currency
- The agent will then notify you when the currency exchange rate  goes outside the threshold set by you.
- For example,
    - Base currency: USD
    - Foreign currency: INR
    - min = 80
    - max = 84
The agent will give you an alert when the exchange rate goes below 80, or above 84






## Project Setup

### Step-1: Prerequisites
Before starting, you'll need the following:
- Python (3.11)
- Poetry (a packaging and dependency management tool for Python)

### Step-2: Setup .env file
To run the demo, you need the following:
- Currency API key:
    - Visit [Currency API](https://currencyapi.com/) website
    - Sign up or Log in
    - Copy your API key
- User Agent Seed:
    - Create a random alphanumeric string 
- Currency Agent Seed:
    - Create a random alphanumeric string

Once you have all these then create a .env file in the root directory
```shell
CURRENCY_API_KEY={GET YOUR API KEY}
CURRENCY_AGENT_SEED={GET YOUR SEED}
USER_AGENT_SEED={GET YOUR SEED}
```
Install the project
```shell
cd src 
poetry install
```
### Step-3: Configure the user script
Run the main script using
```shell 
poetry run python main.py --address
```
You need to look for the following output in the terminal
```shell
INFO - Address of currency agent is {currency_agent_address}
```
Copy the {currency_agent_address} part and keep it somewhere safe

Now to setup the currency agent address open the user.py file in the src/agents/user directory 

```python
CURRENCY_AGENT_ADDRESS = "{currency_agent_address}"
```

In this line in place of {currency_agent_address} paste the address copied above

### Step-4: Run the main script
Open a new terminal the run these commands
```shell
cd src
poetry run python main.py
```
