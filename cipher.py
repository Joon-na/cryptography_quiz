import numpy as np
import gradio as gr

# Vigenere Cipher
def vigenere_encrypt(plain_text, key):
    plain_text = plain_text.replace(" ", "").upper()
    key = key.upper()
    cipher_text = []

    for i in range(len(plain_text)):
        p = ord(plain_text[i]) - 65
        k = ord(key[i % len(key)]) - 65
        c = (p + k) % 26
        cipher_text.append(chr(c + 65))

    return ''.join(cipher_text)

def vigenere_decrypt(cipher_text, key):
    cipher_text = cipher_text.replace(" ", "").upper()
    key = key.upper()
    plain_text = []

    for i in range(len(cipher_text)):
        c = ord(cipher_text[i]) - 65
        k = ord(key[i % len(key)]) - 65
        p = (c - k + 26) % 26
        plain_text.append(chr(p + 65))

    return ''.join(plain_text)

# Playfair Cipher
def create_playfair_matrix(key):
    matrix = []
    key = key.replace("J", "I").upper()
    seen = set()
    for char in key:
        if char not in seen and char.isalpha():
            seen.add(char)
            matrix.append(char)

    for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':  # J digantikan dengan I
        if char not in seen:
            seen.add(char)
            matrix.append(char)

    matrix_5x5 = [matrix[i:i + 5] for i in range(0, 25, 5)]
    return matrix_5x5

def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None

def playfair_encrypt(plain_text, key):
    plain_text = plain_text.replace("J", "I").upper()
    plain_text = ''.join([c for c in plain_text if c.isalpha()])

    matrix = create_playfair_matrix(key)
    if len(plain_text) % 2 != 0:
        plain_text += 'X'  # Padding

    cipher_text = []

    for i in range(0, len(plain_text), 2):
        a, b = plain_text[i], plain_text[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:
            cipher_text.append(matrix[row_a][(col_a + 1) % 5])
            cipher_text.append(matrix[row_b][(col_b + 1) % 5])
        elif col_a == col_b:
            cipher_text.append(matrix[(row_a + 1) % 5][col_a])
            cipher_text.append(matrix[(row_b + 1) % 5][col_b])
        else:
            cipher_text.append(matrix[row_a][col_b])
            cipher_text.append(matrix[row_b][col_a])

    return ''.join(cipher_text)

def playfair_decrypt(cipher_text, key):
    cipher_text = cipher_text.replace("J", "I").upper()
    matrix = create_playfair_matrix(key)

    plain_text = []

    for i in range(0, len(cipher_text), 2):
        a, b = cipher_text[i], cipher_text[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:
            plain_text.append(matrix[row_a][(col_a - 1) % 5])
            plain_text.append(matrix[row_b][(col_b - 1) % 5])
        elif col_a == col_b:
            plain_text.append(matrix[(row_a - 1) % 5][col_a])
            plain_text.append(matrix[(row_b - 1) % 5][col_b])
        else:
            plain_text.append(matrix[row_a][col_b])
            plain_text.append(matrix[row_b][col_a])

    return ''.join(plain_text)

# Hill Cipher
def hill_encrypt(plain_text, key):
    plain_text = plain_text.replace(" ", "").upper()
    n = int(len(key)**0.5)  # Matrix harus berbentuk persegi
    key_matrix = np.array([ord(c) - 65 for c in key.upper()]).reshape(n, n)

    while len(plain_text) % n != 0:
        plain_text += 'X'

    cipher_text = []
    for i in range(0, len(plain_text), n):
        block = [ord(c) - 65 for c in plain_text[i:i+n]]
        cipher_block = np.dot(key_matrix, block) % 26
        cipher_text.extend([chr(c + 65) for c in cipher_block])

    return ''.join(cipher_text)

def hill_decrypt(cipher_text, key):
    cipher_text = cipher_text.replace(" ", "").upper()
    n = int(len(key)**0.5)
    key_matrix = np.array([ord(c) - 65 for c in key.upper()]).reshape(n, n)

    # Mencari invers matriks kunci di mod 26
    determinant = int(round(np.linalg.det(key_matrix)))
    determinant_inv = pow(determinant, -1, 26)
    key_matrix_inv = (
        determinant_inv * np.round(determinant * np.linalg.inv(key_matrix)).astype(int) % 26
    )

    plain_text = []
    for i in range(0, len(cipher_text), n):
        block = [ord(c) - 65 for c in cipher_text[i:i+n]]
        plain_block = np.dot(key_matrix_inv, block) % 26
        plain_text.extend([chr(int(c) + 65) for c in plain_block])

    return ''.join(plain_text)

# Fungsi untuk Gradio
def process_cipher(method, mode, text, key):
    if len(key) < 12:
        return "Kunci harus minimal 12 karakter."

    if method == "Vigenère":
        if mode == "Encrypt":
            return vigenere_encrypt(text, key)
        else:
            return vigenere_decrypt(text, key)
    elif method == "Playfair":
        if mode == "Encrypt":
            return playfair_encrypt(text, key)
        else:
            return playfair_decrypt(text, key)
    elif method == "Hill":
        if mode == "Encrypt":
            return hill_encrypt(text, key)
        else:
            return hill_decrypt(text, key)
    else:
        return "Metode cipher tidak valid."

# Gradio Interface
methods = ["Vigenère", "Playfair", "Hill"]
modes = ["Encrypt", "Decrypt"]

demo = gr.Interface(
    fn=process_cipher,
    inputs=[
        gr.Dropdown(choices=methods, label="Cipher Method"),
        gr.Dropdown(choices=modes, label="Mode"),
        gr.Textbox(label="Input Text", placeholder="Masukkan teks di sini"),
        gr.Textbox(label="Key", placeholder="Masukkan kunci (min 12 karakter)")
    ],
    outputs="text",
    title="Cipher Program",
    description="Aplikasi untuk mengenkripsi dan mendekripsi teks menggunakan Vigenère, Playfair, dan Hill Cipher.",
)

demo.launch()