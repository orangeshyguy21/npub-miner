# from messaging import ECKey

# def generate_keys():
#     # Generate a new key pair
#     key = ECKey()
    
#     # Get the public key
#     public_key = key.get_pubkey()
    
#     # Print the public key
#     print(public_key)

# # Call the function to generate keys
# generate_keys()

from nostr.key import PrivateKey
import multiprocessing
import sys

#first_chars = sample_str[0:3]
# npub1shy

def findKey(stop_signal, match, limit, counter, p_10, p_20, p_30, p_40, p_50, p_60, p_70, p_80, p_90):
    first_chars = ""
    suffix = ""
    found = False
    stop_index = len(match)

    while ( found != True) and (counter.value < limit) and (stop_signal.value != 1):
        with counter.get_lock():
            counter.value += 1
            current_count = counter.value
        private_key = PrivateKey()
        public_key = private_key.public_key
        first_chars = public_key.bech32()[0:stop_index].lower()
        # suffix = public_key.bech32()[stop_index]
        # found = bool(first_chars[0:stop_index] == match and suffix.isnumeric() == True) 
        found = bool(first_chars[0:stop_index] == match)

        if( current_count / limit > 0.1 and p_10.value == 0 ):
            p_10.value = 1
            print(f"10% exhausted")

        if( current_count / limit > 0.2 and p_20.value == 0 ):
            p_20.value = 1
            print(f"20% exhausted")
    
        if( current_count / limit > 0.3 and p_30.value == 0 ):
            p_30.value = 1
            print(f"30% exhausted")

        if( current_count / limit > 0.4 and p_40.value == 0 ):
            p_40.value = 1
            print(f"40% exhausted")

        if( current_count / limit > 0.5 and p_50.value == 0 ):
            p_50.value = 1
            print(f"50% exhausted")

        if( current_count / limit > 0.6 and p_60.value == 0 ):
            p_60.value = 1
            print(f"60% exhausted")

        if( current_count / limit > 0.7 and p_70.value == 0 ):
            p_70.value = 1
            print(f"70% exhausted")

        if( current_count / limit > 0.8 and p_80.value == 0 ):
            p_80.value = 1
            print(f"80% exhausted")

        if( current_count / limit > 0.9 and p_90.value == 0 ):
            p_90.value = 1
            print(f"90% exhausted")

        
    if ( current_count == limit ):
        print(f"100% exhausted - no find")
    # if ( first_chars[0:stop_index] == match and suffix.isnumeric() == True ):
    if ( first_chars[0:stop_index] == match ):
        stop_signal.value = 1
        print(f"Private key: {private_key.bech32()}")
        print(f"Public key: {public_key.bech32()}")


if __name__ == "__main__":
    print("running...")
    # limit = 1000000 million
    # limit = 1000000000 billion
    # limit = 1000000000000 trillion
    match = "npub1shyguy1"
    limit = 100000000000
    p_10 = multiprocessing.Value('i', 0)
    p_20 = multiprocessing.Value('i', 0)
    p_30 = multiprocessing.Value('i', 0)
    p_40 = multiprocessing.Value('i', 0)
    p_50 = multiprocessing.Value('i', 0)
    p_60 = multiprocessing.Value('i', 0)
    p_70 = multiprocessing.Value('i', 0)
    p_80 = multiprocessing.Value('i', 0)
    p_90 = multiprocessing.Value('i', 0)
    counter = multiprocessing.Value('i', 0)
    stop_signal = multiprocessing.Value('i', 0)

    num_processes = 12
    processes = []

    for index in range(num_processes):
        p = multiprocessing.Process(target=findKey, args=(stop_signal, match, limit, counter, p_10, p_20, p_30, p_40, p_50, p_60, p_70, p_80, p_90))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
