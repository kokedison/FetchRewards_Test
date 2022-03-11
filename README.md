# Fetch Rewards Coding Exercise
Basic web service that accepts HTTP requests and return responses.

## Background
---
Our users have points in their accounts. Users only see a single balance in their accounts. But for reporting purposes we actually track their points per payer/partner. In our system, each transaction record contains: ​payer​ (string), ​points​ (integer), ​timestamp​ (date).

For earning points it is easy to assign a payer, we know which actions earned the points. And thus which partner should be paying for the points.

When a user spends points, they don't know or care which payer the points come from. But, our accounting team does care how the points are spent. There are two rules for determining what points to "spend" first:
- We want the oldest points to be spent first (oldest based on transaction timestamp, not the order they’re received)
- We want no payer's points to go negative.


## Prerequisite
---
Download and install [Python 3.4+ & pip](https://cloud.google.com/python/docs/setup) and [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) depends on the OS you're running in.


## Install
---
```
# Clone Repository
$ git clone https://github.com/kokedison/FetchRewards_Test.git

# Install Required Packages
$ pip install -r FetchRewards_Test/requirements.txt

```

## Run
---
```
# Create & Initilize SQLite Database with 2 Dummy Users and print out authentication tokens to be used later testing
$ python -m FetchRewards_Test.initializeDB

# Run Server
$ python -m FetchRewards_Test.app
```
Service is now up and running at http://127.0.0.1:5000

## API Documents
---

Please find API endpoints documentation at http://127.0.0.1:5000/api/docs

## Test
---
Replace <auth_token> with tokens printed when initializing database.

### #Add Transaction
```
$ curl -d '{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }' -H 'Content-Type: application/json' -H "Authorization: Bearer <auth_token>" http://127.0.0.1:5000/transactions

$ curl -d '{ "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }' -H 'Content-Type: application/json' -H "Authorization: Bearer <auth_token>" http://127.0.0.1:5000/transactions
```
### #Spend Points
```
$ curl -d '{ "points": 5000}' -H 'Content-Type: application/json' -H "Authorization: Bearer <auth_token>" http://127.0.0.1:5000/spend
```

### #Check Balance
```
$ curl -H "Authorization: Bearer <auth_token>" http://127.0.0.1:5000/balance
```