import requests

def get_info(ip):
    resp = requests.get(f"https://ipinfo.io/{ip_address}/json")
    data = resp.json()
    return data

ip = ''  # Пример IP-адреса
ip_info = get_info(ip)
print("IP:", ip_info["ip"])
print("Location:", ip_info["city"])
print("Country:", ip_info["country"])
print("Operator:", ip_info["org"])