import csv

with open('lyrics.txt', 'w') as outfile:
    with open('lyrics.csv', 'r') as infile:
        reader = csv.reader(infile, quotechar='"')
        next(reader)
        lines = 0
        for idx, rec in enumerate(reader):
            lyric = rec[5]
            outfile.write(lyric + '\n\n')

            lyric_lines = lyric.split('\n')
            lines += len(lyric_lines)
            if lines >= 500000: # set limit here
                break