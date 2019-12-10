def legendre(a, m):
    return pow(a, (m - 1) >> 1, m)
def is_sprp(n, b=2):
    d = n - 1
    s = 0
    while d & 1 == 0:
        s += 1
        d >>= 1
    x = pow(b, d, n)
    if x == 1 or x == n - 1:
        return True
    for r in range(1, s):
        x = (x * x) % n
        if x == 1:
            return False
        elif x == n - 1:
            return True
    return False
def is_lucas_prp(n, D):
    Q = (1 - D) >> 2
    s = n + 1
    r = 0
    while s & 1 == 0:
        r += 1
        s >>= 1
    t = 0
    while s > 0:
        if s & 1:
            t += 1
            s -= 1
        else:
            t <<= 1
            s >>= 1
    U = 0
    V = 2
    q = 1
    inv_2 = (n + 1) >> 1
    while t > 0:
        if t & 1 == 1:
            U, V = ((U + V) * inv_2) % n, ((D * U + V) * inv_2) % n
            q = (q * Q) % n
            t -= 1
        else:
            U, V = (U * V) % n, (V * V - 2 * q) % n
            q = (q * q) % n
            t >>= 1
    while r > 0:
        U, V = (U * V) % n, (V * V - 2 * q) % n
        q = (q * q) % n
        r -= 1
    return U == 0
small_primes = set([
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
    127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
    179, 181, 191, 193, 197, 199, 211])
indices = [
    1, 11, 13, 17, 19, 23, 29, 31, 37, 41,
    43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
    89, 97, 101, 103, 107, 109, 113, 121, 127, 131,
    137, 139, 143, 149, 151, 157, 163, 167, 169, 173,
    179, 181, 187, 191, 193, 197, 199, 209]
offsets = [
    10, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6,
    6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4,
    2, 4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 6,
    4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 10, 2]
max_int = 2147483647
def is_prime(n):
    if n < 212:
        return n in small_primes

    for p in small_primes:
        if n % p == 0:
            return False
    if n <= max_int:
        i = 211
        while i * i < n:
            for o in offsets:
                i += o
                if n % i == 0:
                    return False
        return True
    if not is_sprp(n): return False
    a = 5
    s = 2
    while legendre(a, n) != n - 1:
        s = -s
        a = s - a
    return is_lucas_prp(n, a)
def next_prime(n):
    if n < 2:
        return 2
    n = (n + 1) | 1
    if n < 212:
        while True:
            if n in small_primes:
                return n
            n += 2
    x = int(n % 210)
    s = 0
    e = 47
    m = 24
    while m != e:
        if indices[m] < x:
            s = m
            m = (s + e + 1) >> 1
        else:
            e = m
            m = (s + e) >> 1
    i = int(n + (indices[m] - x))
    offs = offsets[m:] + offsets[:m]
    while True:
        for o in offs:
            if is_prime(i):
                return i
            i += o
