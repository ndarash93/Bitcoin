from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip39WordsNum, Bip84, Bip84Coins, Bip44Changes

# Step 1: Generate a random 12-word mnemonic
mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
print("Mnemonic:", mnemonic)

# Step 2: Generate seed from mnemonic
seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

# Step 3: Create BIP-84 master key for Bitcoin mainnet
bip84_mst_ctx = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)

# Step 4: Derive account 0 (m/84'/0'/0')
bip84_acc_ctx = bip84_mst_ctx.Purpose().Coin().Account(0)

# Step 5: Get zpub
zpub = bip84_acc_ctx.PublicKey().ToExtended()

print("zpub:", zpub)
try:
    bip84_ctx = Bip84.FromExtendedKey(zpub, Bip84Coins.BITCOIN)
    print("zpub is valid")
except Exception as e:
    print(f"Error: {e}")