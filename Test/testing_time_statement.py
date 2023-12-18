from time import time,sleep

# Assuming self.volume_to_time_reagent and self.liquid_detection.is_filled() are defined elsewhere in your class

filling_time = 5
start_time = time()

while (time() - start_time < filling_time):
    # Your code here
    #print(time.time())
    sleep(0.1)
print("Done")