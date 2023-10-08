import math
import sys
from collections import defaultdict

import alphabet_utils
import frequency_analysis
from alphabet_utils import Language
import matplotlib.pyplot as plt


def get_divisors(n):
    if not hasattr(get_divisors, 'divisors'):
        get_divisors.divisors = dict()

    if n not in get_divisors.divisors:
        divs = set()

        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                divs.add(i)
                divs.add(n // i)

        get_divisors.divisors[n] = list(divs)

    return get_divisors.divisors[n]


def get_separation_of_3_and_4_letter_blocks(msg: str) -> dict:
    if len(msg) < 8:
        raise RuntimeError("Cannot analyse message, too short")

    latest_position = dict()
    result = defaultdict(list)

    for i in range(len(msg) - 3):
        trigram = msg[i:i + 3]
        cuatrigram = msg[i:i + 4]

        if trigram not in latest_position:
            latest_position[trigram] = i

        if cuatrigram not in latest_position:
            latest_position[cuatrigram] = i

        trigram_distance = i - latest_position[trigram]
        cuatrigram_distance = i - latest_position[cuatrigram]

        if trigram_distance != 0:
            result[trigram].append(trigram_distance)
        if cuatrigram_distance != 0:
            result[cuatrigram].append(cuatrigram_distance)

    return result


def display_histogram(data):
    # Filter out keys with zero values and then sort
    sorted_data = sorted([(k, v) for k, v in data if v > 0], key=lambda x: x[0])

    # Separate the keys and values
    keys = [item[0] for item in sorted_data]
    values = [item[1] for item in sorted_data]

    # Plot the histogram
    plt.bar(keys, values)

    # Set x-ticks to be only for keys with non-zero values
    plt.xticks(keys)

    plt.xlabel('Keys')
    plt.ylabel('Values')
    plt.title('Possible keys')
    plt.show()

def main():
    if len(sys.argv) > 2:
        print(f"Usage: {sys.argv[0]} <file_with_encrypted_text>")
        return

    if len(sys.argv) == 2:
        filepath = sys.argv[1]
    else:
        filepath = input("File with message to crack: ")

    try:
        with open(filepath, "r") as src:
            ciphertext = src.read()
    except IOError:
        print(f"Error opening {filepath}")
        return

    language = ''
    while language.upper() not in ('ESP', 'ENG'):
        language = input("Clear text suspected language [ENG: English | ESP: Spanish): ")
    language = Language.from_string(language)

    # Clean the ciphertext
    ciphertext = ''.join([c.upper() for c in ciphertext if alphabet_utils.is_in_alphabet(language, c)])

    # Find separation for all 3 and 4 letter sequences
    distance_between_occurrences = get_separation_of_3_and_4_letter_blocks(ciphertext)
    divisor_frequency = defaultdict(int)
    processed_distances = 0

    for _, distance_list in distance_between_occurrences.items():
        for distance in distance_list:
            processed_distances += 1
            for divisor in get_divisors(distance):
                divisor_frequency[divisor] += 1

    print('Here are the top 20 candidates for key length')

    def top_items(d, n=20):
        return sorted(d.items(),
                      key=lambda item: item[1],
                      reverse=True)[:n]

    display_histogram(top_items(divisor_frequency))
    #for pair in top_items(divisor_frequency):
    #    print(f"{pair[0]}: {pair[1]} / {processed_distances}")

    while True:
        try:
            key_length = int(input("Selected key length: "))
            break
        except ValueError:
            print("Invalid key.")

    guessed_key = []

    for i in range(key_length):
        every_nth_letter = ciphertext[i::key_length]
        partial_histogram = frequency_analysis.normalized_histogram(every_nth_letter, language)
        key_numeric_value = frequency_analysis.find_step_for_best_match(
            partial_histogram,
            frequency_analysis.frequency_per_language(language))
        guessed_key.append(alphabet_utils.uppercase_alphabet(language)[key_numeric_value])
    print(f"Guessed key: {''.join(guessed_key)}")


if __name__ == '__main__':
    main()
