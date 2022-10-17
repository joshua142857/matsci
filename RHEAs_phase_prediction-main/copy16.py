import update as u

x = u.run(45000)
while x != -1:
    print(x)
    x = u.run(x)
