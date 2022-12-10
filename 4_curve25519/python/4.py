import unittest

# General Curve25519 paper: https://cr.yp.to/ecdh/curve25519-20060209.pdf
# (but don't use it if you know nothing about Curve25519 - try to start with something like Wikipedia)

# This paper was suggested in chat to learn Curve25519, but I almost didn't use it
# https://www.cl.cam.ac.uk/teaching/2122/Crypto/curve25519.pdf

# General Montgomery curve: B y^2 = x^3 + A * x^2 + x
# Curve25519: y^2 = x^3 + 486662 * x^2 + x
A = 486662
p = (1 << 255) - 19   # python (2 ** 255 - 19) or math (2^255 - 19)


def add_(a, b):
    return (a + b) % p


def sub_(a, b):
    return (a - b) % p


def mul_(a, b):
    return (a * b) % p


def exp_(a, b):
    bit = 1 << 255
    res = 1
    while bit > 0:
        # optimization (for func): skip first 0-s
        res = mul_(res, res)
        if bit & b:
            res = mul_(res, a)
        bit >>= 1
    return res


# Code from here: https://ru.wikipedia.org/wiki/Расширенный_алгоритм_Евклида#Псевдокод
# or here: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
# function extended_gcd(a, b)
#     (old_r, r) := (a, b)
#     (old_s, s) := (1, 0)
#     (old_t, t) := (0, 1)
#
#     while r ≠ 0 do
#         quotient := old_r div r
#         (old_r, r) := (r, old_r − quotient × r)
#         (old_s, s) := (s, old_s − quotient × s)
#         (old_t, t) := (t, old_t − quotient × t)
#
#         output "Bézout coefficients:", (old_s, old_t)
#         output "greatest common divisor:", old_r
#         output "quotients by the gcd:", (t, s)
def extended_gcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_s, old_t


def div_(a, b):
    # a / b = a * 1/b;
    # Let's find 1/b using Bézout's identity: a * s + b * t = gcd(a, b)
    # Use gcd(b, p) and get the s = 1/b in field defined by prime p. (b * s + p * t = gcd(b, p) => b * s + 0 = 1 => s = 1/b)
    s, t = extended_gcd(b, p)
    return mul_(a, s)


# Formulas for addition and doubling: https://en.wikipedia.org/wiki/Montgomery_curve#Addition
def lambda_distinct(x1, y1, x2, y2):
    # (y2 - y1) / (x2 - x1)
    return div_(sub_(y2, y1), sub_(x2, x1))


def lambda_coincident(x, y):
    # (3 * x^2 + 2 * A * x + 1) / (2 * y)
    return div_(add_(add_(mul_(3, mul_(x, x)), mul_(2, mul_(A, x))), 1), mul_(2, y))


def add(x1, y1, x2, y2):
    # addition result is only finite valid point on the curve, so no need to check (x1 == x2 and y1 == -y2)
    if (x1 == x2) and (y1 == y2):
        l = lambda_coincident(x1, y1)
    else:
        l = lambda_distinct(x1, y1, x2, y2)

    # x3 = l^2 - A - x1 - x2
    # y3 = l * (2 * x1 + x2 + A) - l^3 - y1
    x3 = sub_(sub_(sub_(mul_(l, l), A), x1), x2)
    y3 = sub_(sub_(mul_(l, add_(mul_(2, x1), add_(x2, A))), mul_(mul_(l, l), l)), y1)
    return x3, y3

# https://mailarchive.ietf.org/arch/msg/cfrg/pt2bt3fGQbNF8qdEcorp-rJSJrc/
#    x2,z2,x3,z3 = 1,0,x1,1
#    for i in reversed(range(255)):
#      bit = 1 & (n >> i)
#      x2,x3 = cswap(x2,x3,bit)
#      z2,z3 = cswap(z2,z3,bit)
#      x3,z3 = ((x2*x3-z2*z3)^2,x1*(x2*z3-z2*x3)^2)
#      x2,z2 = ((x2^2-z2^2)^2,4*x2*z2*(x2^2+A*x2*z2+z2^2))
#      x2,x3 = cswap(x2,x3,bit)
#      z2,z3 = cswap(z2,z3,bit)
#    return x2*z2^(p-2)


def swap(a, b, bit):
    return (b, a) if bit else (a, b)


def mul(x1, factor):
    x2, z2, x3, z3 = 1, 0, x1, 1
    bit = 1 << 255
    while bit > 0:
        bit_one = bit & factor
        # optimization (for func): skip first 0-s

        x2, x3 = swap(x2, x3, bit_one)
        z2, z3 = swap(z2, z3, bit_one)

        # x3, z3 = ((x2 * x3 - z2 * z3)^2, x1 * (x2 * z3 - z2 * x3)^2)
        v1 = sub_(mul_(x2, x3), mul_(z2, z3))
        v2 = sub_(mul_(x2, z3), mul_(z2, x3))
        x3, z3 = (mul_(v1, v1), mul_(x1, mul_(v2, v2)))

        # x2, z2 = ((x2^2 - z2^2)^2, 4 * x2 * z2 * (x2^2 + A * x2 * z2 + z2^2))
        v1 = sub_(mul_(x2, x2), mul_(z2, z2))
        x2, z2 = (mul_(v1, v1), mul_(mul_(mul_(4, x2), z2), add_(add_(mul_(x2, x2), mul_(A, mul_(x2, z2))), mul_(z2, z2))))
        x2, x3 = swap(x2, x3, bit_one)
        z2, z3 = swap(z2, z3, bit_one)

        bit >>= 1
    return mul_(x2, exp_(z2, p - 2))


class Test(unittest.TestCase):
    def test_add(self):
        x1 = 56391866308239752110494101482511933051315484376135027248208522567059122930692
        y1 = 17671033459111968710988296061676524036652749365424210951665329683594356030064
        x2 = 39028180402644761518992797890514644768585183933988208227318855598921766377692
        y2 = 17694324391104469229766971147677885172552105420452910290862122102896539285628
        expected_x = 7769460008531208039267550090770832052561793182665100660016059978850497673345
        expected_y = 50777594312607721283178588283812137388073334114015585272572035433724485979392
        self.assertEquals(add(x1, y1, x2, y2), (expected_x, expected_y))

    def test_mul(self):
        x = 56391866308239752110494101482511933051315484376135027248208522567059122930692
        factor = 4
        expected = 41707806908216107150933211614905026312154955484464515789593741233629885877574
        self.assertEquals(mul(x, factor), expected)
