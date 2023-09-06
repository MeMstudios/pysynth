def fib_seq(last_n, n=1, seq=None):
    if seq is None:
        seq = []
    if n < 100000:
        seq.append(n)
        fib_seq(n, n + last_n, seq)
    else:
        return seq


nums = fib_seq(0)
print(nums)