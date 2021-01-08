import csv, sys

ecsd_bytes = 512
if not len(sys.argv) == 2:
    print("usage: python3 emmc5_reg_reader.py ext_csd")
    exit(1)
val_ecsd = open(sys.argv[1], "r").read()
print("Reading EXT-CSD...")

f_ecsd_map = open("map/ecsd.csv", 'r')
f_result = open("result.csv", 'w')
result_writer = csv.writer(f_result)

# Parse ext-CSD. Basic unit is byte. LSB first
print("Parsing ext-CSD value...")
pos_cur = ecsd_bytes*2
result_writer.writerows(b'')
for line in f_ecsd_map:
    tokens = line[:-1].split(",")
    # One line started with "Modes Segment" does not have this field
    try:
        size_cur = int(tokens[2], 10)
        value_cur = ""
        for i in range(0, size_cur):
            pos_cur = pos_cur - 2
            value_cur = value_cur + val_ecsd[pos_cur: pos_cur + 2]
    except ValueError:
        value_cur = ""
    
    # Peel off the right number of bytes
    result_writer.writerow([tokens[0], tokens[1], tokens[2], tokens[3], tokens[4], value_cur])
