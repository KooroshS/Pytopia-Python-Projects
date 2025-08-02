from constants import ABOVE_100, TENS, UNDER_20


def num_to_word(num: int) -> str:
    """
    Convert an integer `num` into its English word representation.
    Works for numbers from 0 up to 999,999,999,999 (exclusive).

    Parameters:
    num (int): The integer to convert into words.

    Returns:
    str: The English words representing the input number.
    """
    # If the number is less than 20, directly look up in UNDER_20 table
    if num < 20:
        return UNDER_20[num]

    # If the number is between 20 and 99
    if num < 100:
        # If it's a multiple of 10, return the corresponding TENS word
        if (num % 10) == 0:
            return f"{TENS[num // 10]}"
        # Otherwise, combine the tens and units parts
        return f"{TENS[num // 10]}-{UNDER_20[num % 10]}"
    
    # For numbers 100 and above, find the highest pivot (100, 1_000, 1_000_000, etc.)
    pivot = max([key for key in ABOVE_100 if key <= num])
    
    # Recursively convert the quotient and the remainder parts
    p1 = num_to_word(num // pivot)  # Word for the quotient
    p2 = ABOVE_100[pivot]           # Word for the pivot (hundred, thousand, etc.)
    
    # If the number is an exact multiple of the pivot
    if (num % pivot) == 0:
        return f"{p1} {p2}"
    
    # Otherwise, include the remainder part in the output
    return f"{p1} {p2} {num_to_word(num % pivot)}"
    

if __name__ == "__main__":
    num = int(input("Enter a number: "))
    # Validate range: only accept positive numbers less than 1 trillion
    if num > 0 and num < 999_999_999_999:
        print(num_to_word(num))
    else:
        print("Number out of range!")
