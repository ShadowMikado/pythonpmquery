import socket
import struct
import time


class PMQueryException(Exception):
    pass


class PMQuery:
    @staticmethod
    def query(host: str, port: int, timeout: int = 4) -> dict:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(timeout)
                sock.setblocking(True)

                # hardcoded magic https://github.com/facebookarchive/RakNet/blob/1a169895a900c9fc4841c556e16514182b75faf8/Source/RakPeer.cpp#L135
                offline_message_data_id = bytes([0x00, 0xFF, 0xFF, 0x00, 0xFE, 0xFE, 0xFE, 0xFE, 0xFD, 0xFD, 0xFD, 0xFD, 0x12, 0x34, 0x56, 0x78])
                command = struct.pack('!cQ', b'\x01', int(time.time()))
                command += offline_message_data_id
                command += struct.pack('!Q', 2)

                length = len(command)

                if length != sock.sendto(command, (host, port)):
                    raise PMQueryException("Failed to write on socket.")

                data, _ = sock.recvfrom(4096)

                if not data:
                    raise PMQueryException("Server failed to respond")

                if data[0:1] != b'\x1C':
                    raise PMQueryException("First byte is not ID_UNCONNECTED_PONG.")

                if data[17:33] != offline_message_data_id:
                    raise PMQueryException("Magic bytes do not match.")

                data = data[35:]

                data = data.decode('utf-8').split(';')
                socket.close(0)
                return {
                    'GameName': data[0] if data else None,
                    'HostName': data[1] if len(data) > 1 else None,
                    'Protocol': data[2] if len(data) > 2 else None,
                    'Version': data[3] if len(data) > 3 else None,
                    'Players': int(data[4]) if len(data) > 4 else 0,
                    'MaxPlayers': int(data[5]) if len(data) > 5 else 0,
                    'ServerId': data[6] if len(data) > 6 else None,
                    'Map': data[7] if len(data) > 7 else None,
                    'GameMode': data[8] if len(data) > 8 else None,
                    'NintendoLimited': data[9] if len(data) > 9 else None,
                    'IPv4Port': int(data[10]) if len(data) > 10 else 0,
                    'IPv6Port': int(data[11]) if len(data) > 11 else 0,
                    'Extra': data[12] if len(data) > 12 else None,
                }

        except socket.error as e:
            socket.close(0)
            raise PMQueryException(str(e))
