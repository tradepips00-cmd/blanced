import time, threading, subprocess, os, tkinter as tk
from datetime import datetime

PROCESSES = ["AndroidEmulatorEx","aow_exe","AppMarket"]

def run_ps(cmd):
    try:
        subprocess.run(["powershell","-Command",cmd], capture_output=True)
    except:
        pass

def apply_affinity():
    mask = 0xFF0  # balanced cores
    ps = f'''
    $names=@("AndroidEmulatorEx","aow_exe","AppMarket");
    foreach($n in $names){{
        Get-Process -Name $n -ErrorAction SilentlyContinue | ForEach-Object {{
            try {{$_.PriorityClass='High'}} catch {{}}
            try {{$_.ProcessorAffinity={mask}}} catch {{}}
        }}
    }}
    '''
    run_ps(ps)

def power_mode():
    run_ps("powercfg /S SCHEME_MIN")

class App:
    def __init__(self):
        self.running=False
        self.root=tk.Tk()
        self.root.title("Panel Loop V4 Balanced")
        self.root.geometry("500x400")

        tk.Button(self.root,text="START BALANCED",command=self.start).pack(pady=20)
        tk.Button(self.root,text="STOP",command=self.stop).pack(pady=20)

        self.log=tk.Text(self.root)
        self.log.pack(fill="both",expand=True)

    def write(self,msg):
        self.log.insert("end",f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log.see("end")

    def loop(self):
        while self.running:
            apply_affinity()
            time.sleep(3)

    def start(self):
        if self.running: return
        self.running=True
        power_mode()
        self.write("Balanced Engine Started")
        threading.Thread(target=self.loop,daemon=True).start()

    def stop(self):
        self.running=False
        self.write("Stopped")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    App().run()
