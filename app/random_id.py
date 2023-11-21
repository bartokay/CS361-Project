import time

def get_rand_id():
    rand_char = open('C:/Users/b/Desktop/CS361-Project/char-id-gen/random_character_gen.txt', 'w')
    rand_char.write("run")
    rand_char.close()
    time.sleep(7)

    rand_char = open('C:/Users/b/Desktop/CS361-Project//char-id-gen/random_character_gen.txt', 'r')
    id = rand_char.read()
    rand_char.close()
    

    return id
