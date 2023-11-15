# bots.py

import threading
import time

def bot_fetcher(item_list, cart, lock):
    for item in item_list:
        if len(item) >= 3:  # Check if there's a duration in the item list
            time.sleep(item[2])  # Fix the index to get the correct sleep duration
            with lock:
                cart.append([item[0], item[1]])
        else:
            print(f"Invalid item format: {item}")

def bot_clerk(items):
    cart = []
    lock = threading.Lock()

    # Create item list with descriptions and seconds
    inventory = {
        "101": ["Notebook Paper", 2],
        "102": ["Pencils", 2],
        "103": ["Pens", 6],
        "104": ["Graph Paper", 1],
        "105": ["Paper Clips", 1],
        "106": ["Staples", 4],
        "107": ["Stapler", 7],
        "108": ["3 Ring Binder", 1],
        "109": ["Printer Paper", 1],
        "110": ["Notepad", 1]
    }

    # Map item numbers to descriptions and seconds
    items_with_details = [(item, inventory[item][0], inventory[item][1]) for item in items]

    # Separate items into robot fetcher lists
    robot_fetcher_lists = [[] for _ in range(3)]
    for i, item in enumerate(items_with_details):
        robot_fetcher_lists[i % 3].append(item)

    # Launch each robot fetcher using a new thread
    threads = []
    for i, fetcher_list in enumerate(robot_fetcher_lists):
        thread = threading.Thread(target=bot_fetcher, args=(fetcher_list, cart, lock))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Return the cart list
    return cart

# Example usage in main.py
if __name__ == "__main__":
    # Test cases
    print("INPUT  : ['106','109','102']")
    print("OUTPUT :", bot_clerk(['106', '109', '102']))
