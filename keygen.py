###############################################################################  

#             Introduction) This is keygen.py           

###############################################################################  

# This python program generates a vanity nostr public key and it's associated
# private key. You will be prompted to input your desired vanity npub and the
# number of worker threads you want to run. The more threads the faster the
# search will be. Your CPU will be your bottleneck in terms of thread count.
# The maximum length vanity npub this script will allow is 7. 


###############################################################################  

#  Part 1) Collect user inputs and kick off the worker threads

###############################################################################  

# Here we prompt the user for two inputs, vanity npub and worker thread count.
# After input collection the main function runs some type checking and error 
# handling on those inputs for validity. After defining variables for the
# multiprocess dispatch the threads 

from nostr.key import PrivateKey # nostr key generation package
import multiprocessing # package for multiprocessing
import re # pacakge for evaluating regex
import time

def main() : 

    # Ask the user to input their desired vanity npub 
    # and run some methods to error handle their input
    npub_selection = None
    while npub_selection is None:
        npub_selection = input("Enter your desired vanity npub: npub1")
        try:
            checkNpubSelectionLength(npub_selection) # checking valid length
            checkNpubSelectionBase58(npub_selection) # checking valid characters
        except ValueError as e:
            npub_selection = None
            print(e)

    # Ask the user to input their desired thread count
    # and then run some methods to error handle the thread selection
    thread_selection = None
    while thread_selection is None:
        thread_selection_str = input("Enter your desired number of worker threads [1-24]: ")
        try:
            thread_selection = getThreadSelectionNumber(thread_selection_str) # check if threads is a number
            checkThreadSelectionSize(thread_selection) # check if thread number is in range
        except ValueError as e:
            thread_selection = None
            print(e)

    # Assign some variables used in the worker threads 
    max_execution_limits = [100,4000,200000,11000000,700000000,40000000000,2200000000000] # execution max limiter array
    npub = "npub1" + npub_selection # concat the prefix onto the users vanity selection
    max_execution_limit = max_execution_limits[len(npub_selection)-1] # the max executions limit
    processes = [] # the container for the threaded processes

    # Assing some variables that need to be tracked between threads
    counter = multiprocessing.Value('i', 0) # total executions counter
    stop_signal = multiprocessing.Value('i', 0) # exit signal for the while loops in the threads
    best_match = multiprocessing.Array('c', 100) # best match found so far - byte array with space for npub

    # Define dict for tracking completion progress so we can update the terminal with progress updates
    progress_alerts = {}
    for i in range(10, 90 + 10, 10):
        progress_alerts[f"p_{i}"] = multiprocessing.Value('i', 0)

    # Create the desired number of worker threads and append them to the processes array
    for index in range(thread_selection):
        p = multiprocessing.Process(target=task, args=(stop_signal, npub, max_execution_limit, counter, progress_alerts, best_match))
        p.start()
        processes.append(p)

    # Alert the terminal to the running processes
    print("\nrunning...\n")

    # Wait for each worker thread to finish, catch a keyboard interrupt and terminate the threads
    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        stop_signal.value = 1
        time.sleep(0.5)
        for p in processes:
            if p.is_alive():
                p.terminate()
                p.join(timeout=1.0)
        print("All processes terminated.")
        return


###############################################################################  

#  Part 1 [error handling]) Check user inputs

###############################################################################  

# Check the size of the vanity npub (how many leading characters to match on)
# Only allow values less than 8. The work required for longer matches gets large fast.
def checkNpubSelectionLength(npub_selection : str) -> None:
    if len(npub_selection) > 7:
        raise ValueError("\nYou don't have a super computer. Try again\n")


# Check to make sure the vanity npub is valid. It must conform to bech32 rules.
# (@todo) this sould ne expanded out so it is more user friendly 
# (no [i] is allowed use one [1] instead, no [o] is allowed use zero [0] instead )
def checkNpubSelectionBase58(npub_selection : str) -> None:
    pattern = r"^[2346789a-z0-9](?!.*[1bio])[\d\w]*$"
    if not re.match(pattern, npub_selection):
        raise ValueError("\nYour npub must conform to bech32 encoding rules.\nNo special characters\nNo uppercase letters\nNone of these lowercase letters [b, i, o]\nNone of these numbers [1]\n")

# Return the threads normaized to a value, throw an error if it is not an integer
def getThreadSelectionNumber(thread_selection : str) -> int:
    try:
        threads = int(thread_selection)
    except ValueError:
        raise ValueError("\nThreads must be a number between [1-24]\n")
    return threads

# Check if the thread count is within the acceptable range
# (@todo) make these values constants that can be changed at file head
def checkThreadSelectionSize(thread_selection : int ) -> None:
    if thread_selection < 1 or thread_selection > 24:
        raise ValueError("\nThreads must be a number between [1-24]\n")


###############################################################################  

#  Part 2) Generate keys until a match is found

###############################################################################  

# Dispatched tasks launched in parallel all searching for the match
# @stop_signal : exit signal for the while loops in the threads
# @match : vanity npub
# @limit : the max executions limit to prevent a runaway train
# @counter : total executions counter
# @progress_alerts : all terminal alerts for tracking progress alerts to the terminal

def task(stop_signal, match, limit, counter, progress_alerts, best_match):
    
    # leading characters to track run (same length as user selection)
    first_chars = ""

    # (depricated)
    suffix = ""

    # tracking if a match was found
    found = False

    # index at which we stop caring what the values are (not a part of the vanity choice)
    stop_index = len(match)

    # Print initial energy bar
    print("[██████████] | Best match: ", end="\r")

    # primary while loop that keeps running until
    # a) a match is found from this thread
    # b) the max limit is reached
    # c) a match is found from a child thread
    while (found != True) and (counter.value < limit) and (stop_signal.value != 1):
        try:
            # lock the global counter and update it
            with counter.get_lock():
                counter.value += 1
                current_count = counter.value
            private_key = PrivateKey() # randomly generated private key (nsec)
            public_key = private_key.public_key # randomly generated public key (npub)
            first_chars = public_key.bech32()[0:stop_index].lower() # characters to check for a match

             # was a match found on this npub?
            found = bool(first_chars[0:stop_index] == match) 

            # update the best match if the current npub is better
            current_match_length = 0
            for i in range(stop_index):
                if i >= len(first_chars) or first_chars[i] != match[i]:
                    break
                current_match_length += 1
            
            best_match_str = best_match.value.decode('utf-8').strip()
            best_match_length = 0
            
            if best_match_str:
                for i in range(stop_index):
                    if i >= len(best_match_str) or best_match_str[i] != match[i]:
                        break
                    best_match_length += 1
            
            if current_match_length > best_match_length:
                with best_match.get_lock(): 
                    best_match.value = public_key.bech32().encode('utf-8')
                progress_percent = (current_count / limit) * 100
                energy_remaining = 10 - int(progress_percent // 10)
                energy_bar = "█" * energy_remaining + "░" * (10 - energy_remaining)
                print(f"[{energy_bar}] | Best match: {public_key.bech32()}", end="\r")

            # check if any alerts need to be triggered
            for i in range(10, 90 + 10, 10):
                if( current_count / limit > (i/100) and progress_alerts[f"p_{i}"].value == 0 ):
                    with progress_alerts[f"p_{i}"].get_lock():
                        progress_alerts[f"p_{i}"].value = 1
                        # Update energy bar in place
                        energy_remaining = 10 - (i // 10)
                        energy_bar = "█" * energy_remaining + "░" * (10 - energy_remaining)
                        print(f"[{energy_bar}] | Best match: {best_match.value.decode('utf-8')}", end="\r")
            
        except KeyboardInterrupt:
            # Handle KeyboardInterrupt within the task
            return

    # check if the max limit has been reached
    if ( current_count == limit ):
        print(f"[░░░░░░░░░░] | Best match: {best_match.value.decode('utf-8')}")
        print() # Add a newline after the final status

    # check if a match was found and print to consol
    if ( first_chars[0:stop_index] == match ):
        stop_signal.value = 1
        # Calculate remaining energy when match is found
        remaining_percent = 100 - int((current_count / limit) * 100)
        energy_blocks = remaining_percent // 10
        energy_bar = "█" * energy_blocks + "░" * (10 - energy_blocks)
        print(f"[{energy_bar}] | Match Found!                                                                  ")
        print() # Add a newline after the final status
        print(f"Public key: {public_key.bech32()}")
        print(f"Private key: {private_key.bech32()}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMiner terminated.")