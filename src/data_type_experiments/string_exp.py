hello_world: str = "Hello, World"

def print_hello():
    print(hello_world)

def hello_to(name: str):
    print(f"Hello, {name}!")

print_hello()

hello_to("Alice")

name="AliCe"
print(name.lower())

name="alice doe"
print(name.upper())

site="https://www.google.com"
print(site.removeprefix("https://www."))
print(site.removesuffix(".com"))
print(site.endswith(".com"))
print(site.startswith(".com"))

def check_protocol(actual_url: str):
    if actual_url.startswith("https://"):
        print(f"{actual_url} is secure")
    elif actual_url.startswith("http://"):
        print(f"{actual_url} is unsecure")
    else:
        print("Unknown protocol")

check_protocol("https://www.google.com")
check_protocol("http://www.google.com")
check_protocol("httpsS://www.google.com")