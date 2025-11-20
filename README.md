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
