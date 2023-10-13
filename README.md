# Classic Crypto

Classic Crypto is a collection of scripts and utilities designed to work with classic cryptographic schemes like Vigenere, Caesar, and Affine ciphers. In addition to foundational utility modules for text manipulation and histogram creation/display, the repository contains a series of scripts aimed at cracking, encrypting, and analyzing encrypted messages.

---

## Table of Contents

- [Scripts](#scripts)
    - [cracker.py](#crackerpy)
    - [Cipher GUI Programs](#cipher-gui-programs)
    - [compare_file_and_language_histogram.py](#compare_file_and_language_histogrampy)
    - [compare_files_histograms.py](#compare_files_histogramspy)
- [Dependencies](#dependencies)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Scripts

### cracker.py

A CLI utility designed to crack classic encrypted messages.

#### Usage

\```
usage: cracker.py [-h] --cryptoscheme {vigenere,caesar,affine} [--no-gui] [--fast] --lang {ESP,ENG} [--decrypt] filepath
\```

- `--cryptoscheme {vigenere,caesar,affine}`: Specifies the cryptoscheme to crack.
- `--no-gui`: If specified, all outputs will be in CLI, ensuring no GUI pop-ups.
- `--fast`: Crack as fast as possible, though it may be less reliable.
- `--lang {ESP,ENG}`: Specify the suspected language of the cleartext. Choose between Spanish (ESP) and English (ENG).
- `--decrypt`: If specified, the message will be decrypted with the guessed key and printed to stdout.
- `filepath`: Path to the file to decrypt.

### Cipher GUI Programs

- **affine_cipher.py**
- **caesar_cipher.py**
- **vigenere_cipher.py**

These GUI programs facilitate encryption and decryption of text messages using their respective cryptographic schemes. Users can input text and a key, then choose to either encrypt or decrypt the message. Results can be saved to a file for further use or analysis.

### compare_file_and_language_histogram.py

A GUI utility allowing users to load a text file and compare its letter frequency histogram with a standard language histogram. Users can shift the histogram and automatically determine the shift that provides the best match between the two histograms. This tool is useful for manually cracking Caesar ciphers and observing how different encryption schemes alter histograms.

### compare_files_histograms.py

A GUI utility similar to `compare_file_and_language_histogram.py` but allows users to compare the histograms of two text files instead of a text file against a language’s histogram.

---

## Dependencies

See `requirements.txt`.

---

## Getting Started

Set up a virtual environment and install the dependencies by running:
```commandline
pip install -r requirements.txt
```

After that, you may launch any of the `.py` scripts in the root directory from the command line, like:
```commandline
python vigenere_cipher.py
```

---

## Contributing

Pull requests welcome!

---

