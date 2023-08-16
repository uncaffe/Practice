import os
from dirscanner import scanner

def main():
    initial_folder = input("Input the initial folder path: ")
    if os.path.exists(initial_folder):
        scan_results = scanner(initial_folder)
        for item in scan_results:
            print(item)
    else:
        print("Invalid folder path.")

if __name__ == "__main__":
    main()
