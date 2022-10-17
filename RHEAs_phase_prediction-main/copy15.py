import update as u

x = u.run(42000)
while x != -1:
    print(x)
    x = u.run(x)
