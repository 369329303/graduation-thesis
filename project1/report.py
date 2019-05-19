import sys
import subprocess


if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} data.txt')
    sys.exit(1)

src_file = sys.argv[1]
#  radius list
radius_a = [i for i in range(10, 51, 5)]

report = open('report.txt', 'a')

print(f'{"Method":<10}{"Time/s":>10}'
      f'{"min/m":>10}{"max/m":>10}{"mean/m":>12}'
      f'{"rmse/m":>10}{"error/%":>10}')
report.write(f'{"Method":<10}{"Time/s":>10}'
             f'{"min/m":>10}{"max/m":>10}{"mean/m":>12}'
             f'{"rmse/m":>10}{"error/%":>10}\n')

for radius in radius_a:
    res1 = subprocess.run(['python3', 'methods.py', str(radius), src_file],
                          stdout=subprocess.PIPE, text=True)
    res2 = subprocess.run(['python3', 'accuracy.py', src_file,
                           'f1.txt', 'f2.txt', 'f3.txt',
                           'f4.txt', 'f5.txt', 'f6.txt'],
                          stdout=subprocess.PIPE, text=True)

    print(f'----Radius: {radius} m')
    report.write(f'----Radius: {radius} m\n')
    for line1, line2 in zip(res1.stdout.splitlines(),
                            res2.stdout.splitlines()):
        if line1.startswith('Method'):
            continue
        sline1 = line1.split()
        sline2 = line2.split()
        print(f'{sline1[0]:<10}{sline1[1]:>10}'
              f'{sline2[1]:>10}{sline2[2]:>10}{sline2[3]:>12}'
              f'{sline2[4]:>10}{sline2[5]:>10}')
        report.write(f'{sline1[0]:<10}{sline1[1]:>10}'
                     f'{sline2[1]:>10}{sline2[2]:>10}{sline2[3]:>12}'
                     f'{sline2[4]:>10}{sline2[5]:>10}\n')

report.close()
