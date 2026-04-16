import random
import timeit


def original():
    base_vel = 70
    vel_rand = 20
    for _ in range(1000):
        _velocity = max(
            0,
            min(
                127,
                base_vel
                + random.randint(  # nosec
                    -vel_rand // 2,
                    max(1, vel_rand // 2),
                ),
            ),
        )


def optimized():
    base_vel = 70
    vel_rand = 20
    vel_rand_min = -vel_rand // 2
    vel_rand_max = max(1, vel_rand // 2)
    for _ in range(1000):
        _velocity = max(
            0,
            min(
                127,
                base_vel
                + random.randint(  # nosec
                    vel_rand_min,
                    vel_rand_max,
                ),
            ),
        )


if __name__ == "__main__":
    t1 = timeit.timeit(original, number=10000)
    t2 = timeit.timeit(optimized, number=10000)
    print(f"Original: {t1:.4f}s")
    print(f"Optimized: {t2:.4f}s")
    if t1 > t2:
        print(f"Improvement: {(t1 - t2) / t1 * 100:.2f}%")
