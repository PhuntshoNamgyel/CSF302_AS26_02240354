
from collections import Counter
from heapq import heappush, heappop
from itertools import count


# 1. Build Huffman tree using a priority queue
def build_tree(frequencies):
    heap = []
    order = count()

    for char, frequency in frequencies.items():
        heappush(heap, (frequency, next(order), char))

    while len(heap) > 1:
        freq1, _, left = heappop(heap)
        freq2, _, right = heappop(heap)

        heappush(heap, (freq1 + freq2, next(order), (left, right)))

    return heap[0][2]


# 2. Generate Huffman codes from the tree
def make_codes(tree):
    codes = {}

    def visit(node, prefix):
        if isinstance(node, str):
            codes[node] = prefix or "0"
        else:
            visit(node[0], prefix + "0")
            visit(node[1], prefix + "1")

    visit(tree, "")
    return codes


# 3. Decode the encoded bit string
def decode(bits, tree):
    if isinstance(tree, str):
        return tree * len(bits)

    result = []
    node = tree

    for bit in bits:
        node = node[0] if bit == "0" else node[1]

        if isinstance(node, str):
            result.append(node)
            node = tree

    return "".join(result)


# 4. Process three text files and compare compression
files = ["text1.txt", "text2.txt", "text3.txt"]

for filename in files:
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    if not text:
        print(f"{filename}: Empty file, no characters to encode.")
        continue

    frequencies = Counter(text)
    tree = build_tree(frequencies)
    codes = make_codes(tree)

    encoded = "".join(codes[char] for char in text)
    decoded = decode(encoded, tree)

    original_bits = len(text) * 8
    compressed_bits = len(encoded)
    ratio = original_bits / compressed_bits

    print(f"\nFile: {filename}")
    print("Character  Frequency  Huffman Code")

    for char in sorted(codes):
        print(f"{repr(char):>9}  {frequencies[char]:>9}  {codes[char]}")

    print("\nEncoded Bit String:", encoded)
    print("Decoded Matches Original:", decoded == text)
    print("Original Bits:", original_bits)
    print("Compressed Bits:", compressed_bits)
    print(f"Compression Ratio (original/compressed): {ratio:.2f}:1")
    print(f"Space Saved: {(1 - compressed_bits / original_bits) * 100:.2f}%")
