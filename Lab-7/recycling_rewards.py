def parse_collection(text):
    material, kg = text.split(':')
    return material.strip().title(), float(kg)

def weight_average(weights_csv):
    values = [int(r) for r in weights_csv.split(',')]
    return sum(values) // len(values)

def net_points(text):
    points, penalty = text.split('|')
    total = float(points) * 2 - float(penalty)
    return max(total, 0)

def main():
    print("==== Running parse_collection ====")
    user_input = input("Enter material:weight in kg (e.g. paper:12): ")
    result = parse_collection(user_input)
    print("Material and Weight:", result)

    print("\n==== Running weight_average ====")
    user_input = input("Enter weights in kg as CSV (e.g. 5,12,20): ")
    result = weight_average(user_input)
    print("Average Weight:", result)

    print("\n==== Running net_points ====")
    user_input = input("Enter points|penalty (e.g. 80|10): ")
    result = net_points(user_input)
    print("Net Points:", result)

if __name__ == "__main__":
    main()
