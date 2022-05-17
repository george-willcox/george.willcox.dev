import decimal

def get_pi(places):
    """
    Calculates pi to the number to decimal places given using an arcsine series
    """
    decimal.getcontext().prec = places

    n = 0
    last = 0

    #Set the value of the first term
    value = decimal.Decimal(1 / 2)

    while True:
        n += 1
        top = 1
        bottom = 2 ** (2 * n + 1) * (2 * n + 1) * 2
        for i in range(n):
            top *= 2 * i + 1
            if i != 0: bottom *= 2 * i + 2
            
        value += decimal.Decimal(top) / decimal.Decimal(bottom)

        #Test if the value is the same as the last value calculated
        if value == last:
            break
        else:
            last = value

    return 6 * value
