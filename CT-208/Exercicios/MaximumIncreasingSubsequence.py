import math

X = [5,2,7,1,3,6,7,8,10,2,4,10,15,12,6,20]

N = len(X)
P = list(range(N))
M = [0] + list(range(N))

L = 0
for i in range(N):
    # Binary search for the largest positive j ≤ L
    # such that X[M[j]] < X[i]
    lo = 1
    hi = L
    while lo <= hi:
        mid = math.ceil((lo+hi)/2)
        if X[M[mid]] < X[i]:
            lo = mid+1
        else:
            hi = mid-1

    # After searching, lo is 1 greater than the
    # length of the longest prefix of X[i]
    newL = lo

    # The predecessor of X[i] is the last index of 
    # the subsequence of length newL-1
    P[i] = M[newL-1]
    M[newL] = i
    print(M)
    if newL > L:
        # If we found a subsequence longer than any we've
        # found yet, update L
        L = newL

# Reconstruct the longest increasing subsequence
S = [0] * L
k = M[L]
for i in range(L):
    S[L-i-1] = X[k]
    k = P[k]


print(S)

# Erdos-Szekeres Theorem: Any sequence with n²+1 integers has a subsequence 
# (decreasing or increasing) with n+1 elements. So the expected value of L
# with be 2*sqrt(n)