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

## NOTE

You need to run it only once:

Consolidation may occur at any time during mining and up to 24 hours after mining has closed.

Consolidation will apply to all claims of the original_address both past and future.
