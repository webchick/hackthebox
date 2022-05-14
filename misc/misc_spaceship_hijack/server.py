#!/usr/bin/python3
import struct
import tempfile
import signal
import sys,os
import random, itertools

def edge_exists(edges, src, dst):
    for (s,d,w) in edges:
        if src == s and dst == d:
            return True
    return False

if __name__ == "__main__":
    vertices = 0x30
    edges = []

    all = [x for x in range(0,vertices)]
    shortestpath = all[1:-1]
    random.shuffle(shortestpath)
    shortestpath = shortestpath[:10]

    # construct the shortest path
    cost = 1000
    prev = 0
    for x in shortestpath:
        ecost = random.randint(1,cost//4)
        edges.append((prev, x, ecost))
        cost -= ecost
        prev = x
    edges.append((prev, all[-1], cost))
    
    # construct random paths
    
    random_edges = []
    for i in range(0x80):
        random_src = random.choice([0,vertices-1] + shortestpath)
        random_dst = random.choice([x for x in range(vertices)])
        if random.randint(1,2) == 1:
            random_src,random_dst = random_dst,random_src
        random_edges.append((random_src,random_dst))

    for (src,dst) in random_edges:
        if not edge_exists(edges,src,dst):
            edges.append((src,dst,random.randint(200,400)))

    assert(len(edges) < 0x100)
    final = b""
    final += struct.pack("<HH", vertices, len(edges))
    for (src,dst,w) in edges:
        final += struct.pack("<HHI", src,dst,w)
    final = final.ljust(0x804,b"\x00")

    signal.alarm(50)
    os.chdir(sys.path[0])
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(final)
    os.system("./controller {}".format(f.name))
    os.unlink(f.name)

