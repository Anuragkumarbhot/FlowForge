import time

def run_worker():
    print("Worker started...")

    while True:
        print("Checking jobs...")
        time.sleep(10)

if __name__ == "__main__":
    run_worker()
