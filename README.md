# 🧠 osmo-wallet-batch

**osmo-wallet-batch** is a Python CLI utility for generating and scanning large batches of Osmosis (`osmo1...`) wallets.

The project provides two tools:

- `mnem.py` — generate wallets and mnemonics.
- `scan.py` — scan `.json` files for wallets and check their balances via the Osmosis LCD API.

---

## 🚀 Features

- ✅ Generate up to millions of Osmosis wallets with mnemonics (12–24 words)
- 📂 Save in multiple JSON files (batches)
- 🧵 Parallel wallet generation using ProcessPoolExecutor
- 🌐 Check active wallets via public LCD API
- 🧠 Store mnemonic, private key, and address

---

## 🧰 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install bip-utils mnemonic requests tqdm
```

---

## 🛠 Usage

### 🔨 Generate wallets

```bash
python3 mnem.py --count 10000 --words 24 --batch-size 10000 --threads 4
```

**Options:**

| Option         | Description                                |
|----------------|--------------------------------------------|
| `--count`      | Total number of addresses to generate      |
| `--words`      | Number of mnemonic words (12, 15, 18, 21, 24) |
| `--batch-size` | Number of wallets per JSON file            |
| `--output-dir` | Directory for output files                 |
| `--threads`    | Number of parallel processes               |

🧪 Sample result (`wallets/osmo_wallets_000.json`):

```json
[
  {
    "mnemonic": "seed phrase ...",
    "private_key": "abcdef...",
    "address": "osmo1..."
  }
]
```

---

### 🔍 Scan wallets for balance

```bash
python3 scan.py
```

**What it does:**

- Scans all `.json` files with wallets in the current directory
- Checks their balances via `https://lcd.osmosis.zone`
- Saves matched wallets with `uosmo > 0` to `found_wallets/found_from_*.json`

✅ Sample found wallet:

```json
{
  "address": "osmo1...",
  "private_key": "...",
  "mnemonic": "...",
  "uosmo": 123456
}
```

---

## 🧼 Cleanup

To remove generated files:

```bash
rm -r wallets found_wallets
```

---

## 🔒 Warning

Do NOT use generated mnemonics or keys on the mainnet.  
This tool is for research, testing, and educational purposes only.
