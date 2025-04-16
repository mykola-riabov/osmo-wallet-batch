#!/usr/bin/python3
import argparse
import os
import json
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
import signal
import sys

# === CLI arguments ===
parser = argparse.ArgumentParser(description="Generate Osmosis wallets with mnemonics")
parser.add_argument("--count", type=int, default=1_000_000, help="Total wallets to generate")
parser.add_argument("--words", type=int, default=24, choices=[12, 15, 18, 21, 24], help="Mnemonic word count")
parser.add_argument("--output-dir", type=str, default="wallets", help="Output directory")
parser.add_argument("--batch-size", type=int, default=100_000, help="Wallets per file")
parser.add_argument("--threads", type=int, default=os.cpu_count(), help="Number of processes")
args = parser.parse_args()

# === Settings ===
total = args.count
words = args.words
batch_size = args.batch_size
num_processes = args.threads
output_dir = Path(args.output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

strength_map = {12: 128, 15: 160, 18: 192, 21: 224, 24: 256}
strength = strength_map[words]

wallets = []
interrupted = False
start_time = time.time()

# === Graceful shutdown ===
def signal_handler(sig, frame):
    global interrupted
    interrupted = True
    print("\n🛑 Interrupted by user. Saving progress...\n")

signal.signal(signal.SIGINT, signal_handler)

# === Wallet generator ===
def generate_wallet(strength):
    mnemo = Mnemonic("english")
    mnemonic = mnemo.generate(strength=strength)
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip44 = Bip44.FromSeed(seed_bytes, Bip44Coins.OSMOSIS)
    account = bip44.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    return {
        "mnemonic": mnemonic,
        "private_key": account.PrivateKey().Raw().ToHex(),
        "address": account.PublicKey().ToAddress()
    }

# === Main loop ===
print(f"🚀 Generating {total:,} Osmosis wallets...")
print(f"🧠 Mnemonic words: {words} | ⚙️ Threads: {num_processes} | 📁 Output: {output_dir}\n")

counter = 0
batch_index = 0

while counter < total and not interrupted:
    current_batch = min(batch_size, total - counter)
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [executor.submit(generate_wallet, strength) for _ in range(current_batch)]
        for f in as_completed(futures):
            if interrupted:
                break
            wallets.append(f.result())
            counter += 1
            if counter % 10_000 == 0:
                elapsed = time.time() - start_time
                print(f"🔄 Progress: {counter:,}/{total:,} | ⏱ {elapsed:.1f}s")

    # Save current batch to file
    filename = output_dir / f"osmo_wallets_{batch_index:03}.json"
    with open(filename, "w") as f:
        json.dump(wallets, f, indent=2)
    print(f"💾 Saved batch {batch_index} ({len(wallets)} wallets) → {filename}")

    wallets.clear()
    batch_index += 1

print(f"\n✅ Done! Total: {counter:,} wallets | ⏱ {time.time() - start_time:.1f} sec")








