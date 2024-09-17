a = """This is
a multiple line string
"""

b = "\"\"\" This is a string with triple quotes"

c = "This string continues \
on the next line"

d = (1,
2,3,[4,5]     )

while True:
    # Example of an indented block
    for i in range(10):
        print(i)
        if i == 5:
            break
    break

print(a)
print(b)
print(c)
print(d)

