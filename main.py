import time
from multiprocessing import Pool, cpu_count, freeze_support


# Sync
def factorize(*numbers: int) -> list:
    results = list()
    for number in numbers:
        result = list()
        for i in range(1, number + 1):
            if number % i == 0:
                result.append(i)
        results.append(result)

    return results


# Async
def factorize_parallel(number):
    result = list()
    for i in range(1, number + 1):
        if number % i == 0:
            result.append(i)
    return result


def factorize_multi(*numbers: int) -> list:
    pool_count = cpu_count() if cpu_count() > len(numbers) else len(numbers)

    with Pool(pool_count) as pool:
        results = pool.map(factorize_parallel, numbers)

    return results


if __name__ == '__main__':
    # Sync
    start = time.perf_counter()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    finish = time.perf_counter()
    print(f'Sync: {finish - start}')

    # Async
    # start = time.perf_counter()
    # a, b, c, d = factorize_multi(128, 255, 99999, 10651060)
    # finish = time.perf_counter()
    # print(f'Async: {finish - start}')

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]
