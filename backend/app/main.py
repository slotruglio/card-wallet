import os

def main():
    print("Hello from backend!")
    print(os.getenv("POSTGRES_USER"))


if __name__ == "__main__":
    main()
