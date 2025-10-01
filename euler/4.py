class Problem:
    def __init__(self):
        pass

    def is_palindrome(s, num):
        num = str(num)
        digits = len(num)
        
        # Num is odd
        if digits % 2 == 0:
            if num[:digits / 2] == 0:
                return True
        else:
            if num[0:(digits - 1) / 2] == num[(digits + 3) / 2:]:
                return True
            
        return False

    def solve(s):
        """Solves the problem"""
        pass
    
if __name__ == "__main__":
    p = Problem()
    bool = p.is_palindrome(50)
    print(bool)
