import screenJC as u

x = u.run("FCC", 11000)
if x >= 0:
    x = u.run("FCC", x)
print(x)