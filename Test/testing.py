import threading
import time
import sys

def operation(stop_event):
    for i in range(5):
        if stop_event.is_set():
            break
        print(f"Performing step {i + 1}")
        time.sleep(10)  # Simulating a time-consuming step

def stop_operation(stop_event):
    input("Press Enter to stop the operation.")
    stop_event.set()

def main():
    stop_event = threading.Event()

    # Create a thread for the operation
    operation_thread = threading.Thread(target=operation, args=(stop_event,))

    # Start the operation thread
    operation_thread.start()

    try:
        # Wait for user input to stop the operation
        stop_operation(stop_event)
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) to stop the operation
        stop_event.set()

    # Wait for the operation thread to finish
    operation_thread.join()

if __name__ == "__main__":
    main()
