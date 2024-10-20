from mpmath import mp, nstr

if __name__ == "__main__":
    prec = 10_000_000
    mp.prec = prec
    
    find = lambda x: x.find('060201')

    pi = mp.pi
    piStr = nstr(pi, prec)
    index = find(piStr)
    if index > -1:
        print(f"pi index: {index}")

    e = mp.e
    eStr = nstr(e, prec)
    index = find(piStr)
    if index > -1:
        print(f"e index: {index}")
    
    r = mp.sqrt(2)
    rStr = nstr(r, prec)
    index = find(rStr)
    if index > -1:
        print(f"sqrt(2) index: {index}")