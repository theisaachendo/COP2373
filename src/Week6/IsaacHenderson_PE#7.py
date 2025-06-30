import re

def split_paragraph(paragraph):
    # Split sentences followed by punctuation and space (handles numbers at start)
    sentences = re.split(r'(?<=[.!?])\s+', paragraph)
    # Remove any empty strings from the list
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def main():
    print("Enter your paragraph (press Enter twice to finish):")
    paragraph = []
    while True:
        line = input()
        if line == "":
            break
        paragraph.append(line)
    
    paragraph = " ".join(paragraph)
    sentences = split_paragraph(paragraph)
    
    print("\nIndividual sentences:")
    for i, sentence in enumerate(sentences, 1):
        print(f"{i}. {sentence}")
    
    print(f"\nTotal number of sentences: {len(sentences)}")

if __name__ == "__main__":
    main()