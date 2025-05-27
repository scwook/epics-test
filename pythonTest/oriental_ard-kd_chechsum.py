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

data = bytes([0x01, 0x10, 0x02,0x42,0x00,0x02,0x04,0x00,0x00,0x03,0x20])
crc_result = custom_crc16(data)
print(hex(crc_result))  # 결과 확인