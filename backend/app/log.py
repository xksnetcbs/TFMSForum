import time
def log(message):
    print(time.strftime("[%H:%M:%S] ", time.localtime()) + message)
    f = open(f"log-{time.strftime('%Y-%m-%d' , time.localtime())}.txt", "a")
    f.write(time.strftime("[%H:%M:%S] ", time.localtime()) + message + "\n")
    f.close()
    return