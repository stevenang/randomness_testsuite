class Tools:

    @staticmethod
    def string_to_binary(input:str):
        binary = []
        for char in input:
            temp = bin(ord(char))[2:]
            while(len(temp) < 8):
                temp = '0' + temp
            binary.append(temp)

        return ''.join(binary)

    @staticmethod
    def string_to_binary_no_concat(input: str):
        binary = []
        for char in input:
            binary.append(bin(ord(char))[2:])

        return ''.join(binary)

    @staticmethod
    def url_to_binary(input:str):
        binary = []
        url = input.split('/')[-1].split('.')[0]

        return url

    @staticmethod
    def bytes_to_binary(input:bytes):
        binary = []
        for b in input:
            binary.append(f'{b:08b}')
        return ''.join(binary)
