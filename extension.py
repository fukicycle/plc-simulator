def print_hex_to_console(data):
    result = "-".join(f"{byte:02X}" for byte in data)
    print(result)

def hex_to_formatted_string(data):
    return "-".join(f"{byte:02X}" for byte in data)

def hex_to_binary_string(data):
    return " ".join(f"{byte:08b}" for byte in data)