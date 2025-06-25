import subprocess

def run_data_parsing():
    subprocess.run(["python", "dataParsing.py"], check=True)

def run_api():
    subprocess.run(["python", "api.py"], check=True)

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Ingest new data (dataParsing.py)")
    print("2. Run API (api.py)")
    choice = input("Enter a value: ")

    if choice == "1":
        run_data_parsing()
    elif choice == "2":
        run_api()
    else:
        print("Invalid choice.")
