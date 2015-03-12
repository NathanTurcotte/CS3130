import redis
import random
import time
import timeit

def ComputeSquare(r, x):
    value = r.get(str(x))
    if value is None:
        time.sleep(0.001)
        value = x * x
        r.set(str(x), value)
    return value

def StartRedis():
    r = redis.StrictRedis()
    return r
def main():
    r = StartRedis()
    def Make_Request():
        ComputeSquare(r, random.randint(0,5000))
    for i in range(1,11):
        print(timeit.timeit(Make_Request, number=2000))


if __name__ == '__main__':
    main()

