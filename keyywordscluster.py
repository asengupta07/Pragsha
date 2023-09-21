from collections import Counter
import re


def get_keywords(texts):
    combined_text = " ".join(texts)

    words = re.findall(r'\b\w+\b', combined_text.lower())

    word_count = Counter(words)

    top_keywords = word_count.most_common(10)

    return top_keywords


if __name__ == "__main__":
    user_inputs = []
    num_inputs = int(input("Enter the number of user inputs: "))

    for i in range(num_inputs):
        user_input = input(f"Enter input #{i + 1}: ")
        user_inputs.append(user_input)

    top_keywords = get_keywords(user_inputs)

    print("\nTop 10 Most Used Keywords:")
    for keyword, count in top_keywords:
        print(f"{keyword}: {count}")
