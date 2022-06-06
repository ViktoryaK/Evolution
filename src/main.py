from map import start


def user_input():
    """
    Receives input from a user.
    """
    while True:
        try:
            cycles = int(input("Enter the number of cycles: "))
            num_of_predators = int(input("Enter the number of predators: "))
            num_of_preys = int(input("Enter the number of preys: "))
            start(cycles, num_of_predators, num_of_preys)
            break
        except ValueError:
            continue


if __name__ == '__main__':
    user_input()
