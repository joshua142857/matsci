import update as u

x = u.run(63500)
while x != -1:
    print(x)
    x = u.run(x)
