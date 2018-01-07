class Tools:

    @staticmethod
    def string_to_binary(input:str):
        binary = []
        for char in input:
            binary.append(bin(ord(char))[2:])

        return ''.join(binary)