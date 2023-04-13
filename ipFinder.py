import ipaddress
import requests
import threading

cidr_range = input("Enter a CIDR range (e.g., 192.168.0.0/24): ")
num_threads = int(input("Enter the number of threads: "))

ips = list(ipaddress.IPv4Network(cidr_range).hosts())
total_ips = len(ips)

def send_request(ip):
    try:
        response = requests.get(f"http://{ip}/cdn-cgi/trace", timeout=5)
        if response.status_code == 200:
            print(f"Successful: {ip}")
            with open("successful_ips.txt", "a") as f:
                f.write(str(ip) + "\n")
    except:
        pass

threads = []
for i in range(num_threads):
    thread_ips = ips[i::num_threads]
    t = threading.Thread(target=lambda ips: [send_request(ip) for ip in ips], args=(thread_ips,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Done!")