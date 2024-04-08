import numpy
# bit-size of p
n = 512

# p determines the field
p = next_prime(2^(n-1))

# number of MSBs
k = ceil(sqrt(n)) + ceil(log(n, 2))

def msb(k, x):
    """
        Randomised/non-randomised MSBs that returns k bits of x
        p is global. Do not use the randomised version for large p
    """
    """
    while True:
        z = ZZ.random_element(1, p-1) #randint(1, p-1)
        answer = abs(x - z)
        if answer < p / 2^(k+1):
            print(answer)
            break
    """
    xbin = x.digits(2)
    n = len(xbin)
    z = sum([2^i*xbin[i] for i in range(n-k-1,n)])
    #assert abs(x-z)<p / 2^(k+1)
    print(abs(x-z))

    return z, abs(x-z)

def create_oracle(alpha, k):
    """
        The Hidden Number Problem oracle for alpha and k MSBs
    """
    alpha = alpha
    def oracle():
        random_t = ZZ.random_element(1, p-1)#randint(1, p-1)
        ret = msb(k, (alpha * random_t) % p)
        return random_t, ret[0], ret[1]
    return oracle

# Example
alpha = ZZ.random_element(1, p-1)
print('alpha:', alpha)
oracle = create_oracle(alpha, k)

# write secrete alpha to file
file_alpha = open("alpha.txt", 'w')
file_alpha.write(str(alpha)+'\n')
file_alpha.close()

# write known values to file
file = open("hidden.txt", 'w')
file.write(str(p)+'\n')
d = ceil(2*sqrt(n)+2)
t = [0]*d
msbs = [0]*d
lsbs = [0]*d
for i in range(d):
    t[i], msbs[i], lsbs[i] = oracle()
    file.write(str(t[i])+ ' ' + str(msbs[i])+'\n')
