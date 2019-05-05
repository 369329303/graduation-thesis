import subprocess

# radius list
radius_a = [i for i in range(32, 41, 2)]

report = open('report.txt', 'a')

print(f'{"Method":<10}{"Time/s":>10}'
      f'{"min/m":>10}{"max/m":>10}{"mean/m":>12}'
      f'{"rmse/m":>10}{"error/%":>10}')
report.write(f'{"Method":<10}{"Time/s":>10}'
             f'{"min/m":>10}{"max/m":>10}{"mean/m":>12}'
             f'{"rmse/m":>10}{"error/%":>10}\n')

for radius in radius_a:
    # This statement will produce tmpfile1.txt
    subprocess.run(['python3', 'methods.py', str(radius), 'source.txt'],
                   stdout=subprocess.DEVNULL)
    # This statement will produce tmpfile2.txt
    subprocess.run(['python3', 'accuracy.py',
                    'source.txt', 'f1.txt', 'f2.txt',
                    'f3.txt', 'f4.txt', 'f5.txt'],
                   stdout=subprocess.DEVNULL)
    with open('tmpfile1.txt', 'r') as f1, \
            open('tmpfile2.txt', 'r') as f2:
        print(f'----Radius: {radius} m')
        report.write(f'----Radius: {radius} m\n')
        for line1, line2 in zip(f1, f2):
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
