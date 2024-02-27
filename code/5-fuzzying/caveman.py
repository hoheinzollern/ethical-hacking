import os, sys, random
from pexpect import run
from pipes import quote

def get_bytes(filename):
    f = open(filename, "rb").read()
    return bytearray(f)

def create_new(data):
    f = open("mutated.jpg", "wb+")
    f.write(data)
    f.close()

N = 100000

def exif(counter,data):
    command = "./exif mutated.jpg -verbose"
    out, returncode = run(command, withexitstatus=1)
    if b"ERROR" in out:
        f = open("crashes/crash.{}.jpg".format(str(counter)), "ab+")
        f.write(data)
        f.close()
    if counter % 100 == 0:
        print(counter, end="\r")
    
def fuzz(filename):
    for counter in range(N):
        data = get_bytes(filename)
        mutated = mutate(data)
        create_new(mutated)
        exif(counter,mutated)

def bit_flip(data):
    num_of_flips = int((len(data) - 4) * .01)
    indexes = range(4, (len(data) - 4))
    chosen_indexes = random.sample(indexes, num_of_flips)
    for x in chosen_indexes:
        data[x] ^= 1 << random.randint(0,7)
    return data

def magic(data):

    magic_vals = [(1, 255), (1, 255), (1, 127), (1, 0), (2, 255), (2, 0), 
                  (4, 255), (4, 0), (4, 128), (4, 64), (4, 127) ]

    (picked_size, picked_magic) = random.choice(magic_vals)

    picked_index = random.randint(4, len(data)-4)
    
    for i in range(picked_size):
        data[picked_index + i] = picked_magic

    return data

def mutate(data):
    f = random.choice([bit_flip, magic])
    return f(data)

def get_files():
    return os.listdir("crashes/")

def triage_files(files):
    for x in files:
        original_output = os.popen(f"./exif crashes/{x} -verbose 2>&1").read()
        output = original_output

        # Getting crash reason
        crash = "SEGV" if "SEGV" in output else "HBO" if "heap-buffer-overflow" in output else None

        if crash == "HBO":
            output = output.split("\n")
            counter = 0
            while counter < len(output):
                if output[counter] == "=================================================================":
                    target_line = output[counter + 1]
                    target_line2 = output[counter + 2]
                    counter += 1
                else:
                    counter += 1
            target_line = target_line.split(" ")
            address = target_line[5].replace("0x","")


            target_line2 = target_line2.split(" ")
            operation = target_line2[0]


        elif crash == "SEGV":
            output = output.split("\n")
            counter = 0
            while counter < len(output):
                if output[counter] == "=================================================================":
                    target_line = output[counter + 1]
                    target_line2 = output[counter + 2]
                    counter += 1
                else:
                    counter += 1
            if "unknown address" in target_line:
                address = "00000000"
            else:
                address = None

            if "READ" in target_line2:
                operation = "READ"
            elif "WRITE" in target_line2:
                operation = "WRITE"
            else:
                operation = None

        if crash:
            log_name = (x.replace(".jpg","") + "." + crash + "." + address + "." + operation)
            f = open(log_name,"w+")
            f.write(original_output)
            f.close()

if __name__ == '__main__':
    fuzz('input.jpg')
    files = get_files()
    triage_files(files)
