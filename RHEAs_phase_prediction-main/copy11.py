import update as u

x = u.run(64712)
while x != -1:
    print(x)
    x = u.run(x)
