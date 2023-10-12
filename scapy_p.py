from scapy.all import sniff

# Функция для обработки сетевых пакетов
def packet_callback(packet):
    if packet.haslayer("IP"):
        # Выводим информацию о принятых пакетах
        print(f"Исходный IP: {packet[IP].src} -> Целевой IP: {packet[IP].dst}")

# Захватываем и анализируем сетевой трафик (например, первые 10 пакетов)
sniff(prn=packet_callback, count=10)