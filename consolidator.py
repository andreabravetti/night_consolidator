import os
import sys
import json
import time
import requests

from pycardano import HDWallet, Address, PaymentVerificationKey, \
                      StakeVerificationKey, ExtendedSigningKey, \
                      PaymentKeyPair, sign

VERSION = [0, 0, 1]

BASE_URL = "https://scavenger.prod.gd.midnighttge.io"

DERIVATION_PATH = {
    "wallet": "m/1852'/1815'/{index}'/{x}/0",
    "address": "m/1852'/1815'/0'/{x}/{index}"
}

HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/142.0.0.0 Safari/537.36'
}

WALLETS = {}

def short_address(address: str) -> str:
    return f"{address[0:13]}...{address[-8:]}"


class wallet():
    def __init__(self, mnemonic: str, derivation_path: str, index: int):
        hdwallet = HDWallet.from_mnemonic(mnemonic)
        self.path = derivation_path.format(x=0, index=index)
        self.stake_path = derivation_path.format(x=2, index=index)
        self.wallet = hdwallet.derive_from_path(self.path)
        self.stake_wallet = hdwallet.derive_from_path(self.stake_path)

    def get_address(self) -> str:
        payment_public_key = self.wallet.public_key.hex()
        payment_vkey = PaymentVerificationKey(
            bytes.fromhex(payment_public_key))
        stake_public_key = self.stake_wallet.public_key.hex()
        stake_vkey = StakeVerificationKey(bytes.fromhex(stake_public_key))
        address = Address(payment_part=payment_vkey.hash(),
                          staking_part=stake_vkey.hash())
        return str(address)

    def get_signature(self, message: str) -> str:
        signing_key = ExtendedSigningKey.from_hdwallet(self.wallet)
        key_pair = PaymentKeyPair.from_signing_key(signing_key)
        return sign(message, key_pair.signing_key)


if __name__ == "__main__":
    # Test the wallets configurations
    if not os.path.isfile("night-wallets.json"):
        print("Please create a file named night-wallets.json with your mnemonic,")
        print("derivation path and a range of wallets or addresses you want to")
        print("consolidate, then run this program again.")
        sys.exit(1)
    # Read the wallets configurations
    with open("night-wallets.json", "r") as fin:
        WALLETS = json.loads(fin.read())
    # Initial print
    print(f"This is night-consolidator {'.'.join([str(v) for v in VERSION])}")
    print(
        f"Your destination address is {short_address(WALLETS['destination'])}")
    # Main loop
    for i, w in enumerate(WALLETS["sources"]):
        print(f" Elaborating source {i} ({w['comment']})")
        if not w.get("enabled", True):
            print("  This source is disabled in config, skip.")
            continue
        print(f"  Derivation type is {w['range_type']}")
        dmin = w['range_min']
        dmax = w['range_max']
        if dmin > dmax:
            print(f" ERROR: range_min can't be grater than range_max")
            sys.exit(1)
        if dmin == dmax:
            print(f"  Single addr/wallet with index equal to {dmin}")
        else:
            print(f"  Multiple addr/wallet in range {dmin}...{dmax}")
        derivation_range = list(range(dmin, dmax+1))
        # Wallet loop
        for index in derivation_range:
            print(f"  Running at index {index}")
            try:
                wd = wallet(w['mnemonic'], DERIVATION_PATH[w['range_type']], index)
                print(f"   Derivation path is {wd.path}")
            except ValueError as e:
                print(f"   ERROR: {e}")
                sys.exit(1)
            source_address = wd.get_address()
            print(f"   Source address: {short_address(source_address)}")
            try:
                session = requests.Session()
                dadd = WALLETS['destination']
                sadd = source_address
                ssig = wd.get_signature(f"Assign accumulated Scavenger rights to: {dadd}")
                durl = f"{BASE_URL}/donate_to/{dadd}/{sadd}/{ssig}"
                donation = session.post(durl, headers=HTTP_HEADERS, json={})
            except Exception as e:
                print(f"   ERROR: {e}")
                sys.exit(1)
            response = donation.json()
            not_registered = response.get('message', '').endswith("is not registered")
            already_done = response.get('error', '') == 'Conflict'
            is_success = response.get('status', '') == 'success'
            if not_registered:
                print(f"<  Response: skip, not registered")
            elif already_done:
                print(f">  Response: ok, alredy done")
            elif not is_success:
                print(f"   ERROR:\n{response}")
                sys.exit(1)
            else:
                print(f"X  Response: success")
            time.sleep(1)
