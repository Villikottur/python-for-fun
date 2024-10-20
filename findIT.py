import os

folder = r"C:\Users\Admin\Desktop\Temp"
fcerca = os.path.join(folder, 'cerca.txt')
ftrova = os.path.join(folder, 'trova.txt')

with open(fcerca, 'r') as f:
    string = f.read().strip()
    
with open(ftrova, 'w') as ris:
    
    for root, dirs, files in os.walk(folder):
        
        for filename in files:
            filepath = os.path.join(root, filename)
            
            if filename in ['cerca.txt', 'trova.txt']:
                continue
            
            with open(filepath, 'r', errors='ignore') as thefile:
                
                if string in thefile.read():
                    ris.write(filename + '\n')