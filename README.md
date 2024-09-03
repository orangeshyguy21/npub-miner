<h1 align="center">Nostr Keygen</h1>

## Documentation

This script is designed to find a vanity nostr npub of your choice. 

### Usage

To run this script run in a terminal

```
python3 keygen.py
```

## Inputs

### Vanity Npub

You will be asked to enter your choice of npub. All public keys start with *npub1* 
* Valid lengths are 1 to 7.
* Vanity choices must only contain valid characters (no b,i,o,l)

```
npub1n0str
```

### Worker Trheads

You will also be asked to enter the number of worker threads to use.
This is how many "checkers" you will run at the same time. The specifications of your computer determine how many you can spawn reliably.
* Valid entries are 1-24


## Output

```
Public key: npub1n0strd57e2war80c5la62795mz0d9upeyte648jsutxdapr3zsasktl3qk
Private key: nsec....
```

