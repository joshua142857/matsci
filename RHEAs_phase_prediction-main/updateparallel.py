import update as u
from multiprocessing import Pool


def functionToRunParallely(i, e, s):
    return u.run(i, e, s)


xfcc = [783, 12359, 17618, 24985, 32000, 42358, 50000, 60000]
xbcc = [0, 10682, 17698, 24736, 32000, 40000, 48000, 59933]
xefcc = []
xebcc = []
for a in xfcc:
    xefcc.append(a + 10000)
for c in xbcc:
    xebcc.append(c + 10000)
y = []
noOfPools = len(xfcc) + len(xbcc)
for b in range(16):
    y.append((xfcc[b], xefcc[b], "FCC"))
    y.append((xbcc[b], xebcc[b], "BCC"))
if __name__ == "__main__":
    with Pool(noOfPools) as p:
        try:
            p.starmap(functionToRunParallely, y)
        except:
            pass
