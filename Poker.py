from collections import Counter


dictionary = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
        "7": 7, "8": 8, "9": 9, "10": 10,
        "J": 11, "Q": 12, "K": 13, "A": 14
    }
def check_hand(cards):
    suits = [card[1] for card in cards]
    values = [dictionary[card[0]]  if len(card) == 2 else dictionary["10"] for card in cards]
    value_counts = Counter(values)
    suit_counts = Counter(suits)
    def find_key_by_value(d, v):
        for key, val in d.items():
            if val == v:
                return key
        return None

    results = []
    straight_flush = is_straight_flush(cards)
    straight = is_straight(cards)
    string = ["11", "12", "13", "14"]
    if len(straight_flush) > 0:
        for s in straight_flush:
            for a in string:
                if a in s:
                    s= s.replace(a, find_key_by_value(dictionary, int(a)))
            results.append(f"Longest Straight Flush: {s}")

    if len(straight) > 0:
        for s in straight:
            for a in string:
                if a in s:
                    s = s.replace(a, find_key_by_value(dictionary, int(a)))
            results.append(f"Longest Straight: {s}")

    for value in value_counts.keys():
        if value_counts[value] == 2:
            results.append(f"Pair: {find_key_by_value(dictionary, value)}")
        if value_counts[value] == 3:
            results.append(f"Three of a Kind: {find_key_by_value(dictionary, value)}")
        if value_counts[value] == 4:
            results.append(f"Four of a Kind: {find_key_by_value(dictionary, value)}")

    return "\n".join(results) if results else "Trash Hand"

def consecutive(arr):
    if not arr:
        return []

    arr = sorted(set(arr))
    result = []
    current_sequence = [arr[0]]

    for i in range(1, len(arr)):
        if arr[i] == arr[i - 1] + 1:
            current_sequence.append(arr[i])
        else:
            if len(current_sequence) >= 3:
                result.append(current_sequence)
            current_sequence = [arr[i]]

    if len(current_sequence) >= 3:
        result.append(current_sequence)

    return result


def is_straight_flush(nums):
    if not nums:
        return []
    suits = [num[1] for num in nums]
    values = [dictionary[num[0]]  if len(num) == 2 else dictionary["10"] for num in nums]
    suit_to_values = {}

    for suit, value in zip(suits, values):
        if suit not in suit_to_values:
            suit_to_values[suit] = []
        suit_to_values[suit].append(value)

    straight_flushes = []

    for suit, values in suit_to_values.items():
        sequences = consecutive(values)
        for seq in sequences:
            straight_flushes.append(" ".join(f"{v}{suit}" for v in seq))

    return straight_flushes

def is_straight(nums):
    values = [dictionary[num[0]]  if len(num) == 2 else dictionary["10"] for num in nums]
    suits = [num[1] for num in nums]
    nums_2 = consecutive(values)
    nums_1 = is_straight_flush(nums)

    straight = []
    for num in nums_2:
        cards_in_straight = [f"{v}{suits[values.index(v)]}" for v in num]
        straight_str = " ".join(cards_in_straight)
        if straight_str not in nums_1:
            straight.append(" ".join(cards_in_straight))

    return straight




if __name__ == '__main__':
    classes = ["2D", "2C", "3C", "4D", "5C", "JC", "JD", "QC", "KC", "KD", "AD"]
    print(check_hand(classes))
