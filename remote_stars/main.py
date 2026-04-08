import numpy as np
import matplotlib.pyplot as plt
import socket

host = "84.237.21.36"
port = 5152

def recvall(sock, nbytes):
    data = bytearray()
    while len(data) < nbytes:
        packet = sock.recv(nbytes - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

plt.ion()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    sock.send(b"124ras1")
    print(sock.recv(10))
    beat = b"nope"

    while beat != b"yep":
        sock.send(b"get")
        bts = recvall(sock, 40002)

        height, width = bts[0], bts[1]
        im = np.frombuffer(bts[2:], dtype="uint8")

        index1 = np.argmax(im)
        pos1 = np.unravel_index(index1, (height, width))

        y, x = pos1

        upper_left = (y - 10, x - 10)
        lower_right = (y + 10, x + 10)

        for ys in range(upper_left[0], lower_right[0]+1):
            for xs in range(upper_left[1], lower_right[1]+1):
                index = ys * width + xs
                im[index] = 0

        index2 = np.argmax(im)
        pos2 = np.unravel_index(index2, (height, width))

        dist = ((pos2[1] - pos1[1]) ** 2 + (pos2[0] - pos1[0]) ** 2) ** 0.5
        result = round(dist, 1)
        sock.send(f"{result}".encode())
        print(sock.recv(10))

        sock.send(b"beat")
        beat = sock.recv(10)