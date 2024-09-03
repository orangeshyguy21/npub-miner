<h1 align="center">Nostr Keygen</h1>

## Documentation

This script is designed to find a vanity nostr npub of your choice. 

### Usage

You need to install the nostr python dependencies before running the script

```
pip install nostr
```


To generate an npub 
1. download this repository somewhere on your machine
2. make sure you are in the directory where keygen.py exists 
3. run in a terminal

```
python3 keygen.py
```

## Inputs

### Vanity Npub

You will be asked to enter your npub of choice. All public keys start with *npub1* 
* Valid lengths are 1 to 7.
* Vanity choices must only contain valid characters (no b,i,o,l)

ex.
```
npub1n0str
```

### Worker Threads

You will also be asked to enter the number of worker threads to use.
This is how many checking functions you will run simultaneously. More threads equals less waiting time. 
Don't be too greedy, especially if you have a destitute computer.
* Valid entries are 1-24

## Output

```
Public key: npub1n0strd57e2war80c5la62795mz0d9upeyte648jsutxdapr3zsasktl3qk
Private key: nsec....
```

