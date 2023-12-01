import countpackets

def main():
    url = input("Enter a URL to analyze (without 'https://www.'): ")
    try:
        off_packets, on_packets = countpackets.try_one_url(url)
        print(f"Results for {url}:")
        print(f"Off Packets: {off_packets}")
        print(f"On Packets: {on_packets}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
