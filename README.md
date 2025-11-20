# night-consolidator

Simple script for Scavenger mine revards consolidation


## Install

```
git clone https://github.com/andreabravetti/night_consolidator.git
cd night_consolidator
python -m venv ./venv
. ./venv/bin/activate
pip install -r requirements.txt
```


## Setup

Compile your `night-wallets.json` following `night-wallets.json.example`

Please take care of these parameters:

```
    "range_type": "address",
    "range_min": 0,
    "range_max": 10
```

Parameter `range_type` define the derivation path the software will use:

- `wallet`: Use `m/1852'/1815'/{i}'/{x}/0` to produce n different wallets with different stake key, like you can find for example in the ADA-Markets/midnight_fetcher_bot_public and other popular API miners.

- `address`: Use `m/1852'/1815'/0'/{x}/{i}` to produce n different addresses with the same stake key, like you can get generating some nre addresses in Yoroi or other Cardano wallets.

Parameters `range_min` and `range_max` define the range of wallets or addresses you need to consolidate.

To consolidate first address of 200 different wallets you can use:

```
    "range_type": "wallet",
    "range_min": 0,
    "range_max": 199
```

To consolidate first 10 addresses of the same wallet you can use:

```
    "range_type": "address",
    "range_min": 0,
    "range_max": 9
```

There are lot of possible combination in the derivation path:

This software is somewhat limited to two most common scenarios but if you know what to do you can modify DERIVATION_PATH in the code to address your use case.


## Run

```
python consolidator.py
```


## Get $NIGHT allocation

If you want to view your $NIGHT allocation you can try this experimental feature setting the environment variable GET_ALLOCATION to 1, yes or true:

```
GET_ALLOCATION=1 python consolidator.py
```

With this variable the consolidator will print yout NIGHT balance for each address, and a total in the end.


## NOTE

You need to run it only once:

Consolidation may occur at any time during mining and up to 24 hours after mining has closed.

Consolidation will apply to all claims of the original_address both past and future.
