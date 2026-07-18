import socket as net
import time

# TCP Port Scanner - using socket and time only

class Scanner:
    def __init__(self, ip, start_port, end_port):
        self.host = ip
        self.start_port = start_port
        self.end_port = end_port

    def port_scanner(self):
        start = time.time()

        for port in range(self.start_port, self.end_port + 1):
            s = net.socket(net.AF_INET, net.SOCK_STREAM)
            s.settimeout(0.5)

            result = s.connect_ex((self.host, port))  # 0 = open

            if result == 0:
                print(f"[OPEN] Port {port} is open!")

            s.close()

        end = time.time()
        print(f"Scan complete in {round(end - start, 2)}s")


def get_input():
    try:
        host = input("Enter the IP address: ")

        # Empty check
        if host.strip() == "":
            print("Error: IP address cannot be empty!")
            exit()

        net.gethostbyname(host)  # Validate IP/hostname

        start_port = int(input("Enter start port: "))
        end_port   = int(input("Enter end port: "))

        # Port range validation
        if not (1 <= start_port <= 65535):
            print("Error: Start port must be between 1 and 65535!")
            exit()
        if not (1 <= end_port <= 65535):
            print("Error: End port must be between 1 and 65535!")
            exit()
        if start_port > end_port:
            print("Error: Start port cannot be greater than end port!")
            exit()

        return host, start_port, end_port

    except ValueError:
        print("Error: Port must be a number, not a string!")
        exit()
    except net.gaierror:
        print("Error: Invalid IP address or hostname!")
        exit()
    except KeyboardInterrupt:
        print("\nSuccessfully exit!")
        exit()
    except EOFError:
        print("\nSuccessfully exit!")
        exit()
    except Exception as e:
        print(f"Error: {e}")
        exit()


# ── Entry Point ────────────────────────────

host, start_port, end_port = get_input()

try:
    print(f"Scanning {host} from port {start_port} to {end_port} ...")
    scanner = Scanner(host, start_port, end_port)
    scanner.port_scanner()

except PermissionError:
    print("Error: Permission required!")
except KeyboardInterrupt:
    print("\nSuccessfully exit!")
except OSError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Error: {e}")
