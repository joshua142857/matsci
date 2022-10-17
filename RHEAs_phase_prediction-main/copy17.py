import update as u

x = u.run(48000)
while x != -1:
    print(x)
    x = u.run(x)
