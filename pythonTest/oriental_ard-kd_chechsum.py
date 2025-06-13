data = bytes([0x01, 0x06, 0x00, 0x7D, 0x00, 0x00])


def custom_crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF

crc_result = custom_crc16(data)
print(hex(crc_result))  # 결과 확2
