import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import math

class DarkModeSchedulerApp:
    def __init__(self, root):

        
        self.root = root
        self.root.title("Real-Time Multicore Studio - Dark Mode")
        self.root.geometry("1250x750")
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bg_color = "#121212"
        self.panel_color = "#1E1E1E"
        self.input_bg = "#2C2C2C"
        self.text_color = "#E0E0E0"
        self.accent_color = "#3B82F6"
        
        self.font_main = ("Segoe UI", 10)
        self.font_bold = ("Segoe UI", 10, "bold")
        self.font_title = ("Segoe UI", 12, "bold")
        
        self.root.configure(bg=self.bg_color)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Treeview", font=self.font_main, rowheight=30, borderwidth=0, 
                        background=self.panel_color, fieldbackground=self.panel_color, foreground=self.text_color)
        style.configure("Treeview.Heading", font=self.font_bold, background="#2A2A2A", foreground="white", borderwidth=0)
        style.map("Treeview.Heading", background=[('active', '#3A3A3A')])
        style.map("Treeview", background=[('selected', self.accent_color)], foreground=[('selected', 'white')])
        
        style.configure("TEntry", fieldbackground=self.input_bg, foreground="white", borderwidth=0, padding=5)
        style.configure("TCombobox", fieldbackground=self.input_bg, foreground="white", background=self.input_bg, borderwidth=0, arrowcolor="white")

        self.left_panel = tk.Frame(root, width=380, bg=self.panel_color, padx=20, pady=20)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(20, 10), pady=20)
        
        self.right_panel = tk.Frame(root, bg=self.bg_color)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 20), pady=20)

        self.setup_input_panel()
        self.setup_result_panel()


    def on_closing(self):
        plt.close('all') 
        self.root.quit() 
        self.root.destroy()
        
    def setup_input_panel(self):
        tk.Label(self.left_panel, text="System Configuration", font=("Segoe UI", 16, "bold"), bg=self.panel_color, fg="white").pack(anchor="w", pady=(0, 20))

        tk.Label(self.left_panel, text="1. Environment", font=self.font_title, bg=self.panel_color, fg=self.accent_color).pack(anchor="w")
        env_frame = tk.Frame(self.left_panel, bg=self.panel_color)
        env_frame.pack(fill="x", pady=(5, 15))
        
        tk.Label(env_frame, text="Cores:", font=self.font_main, bg=self.panel_color, fg=self.text_color).grid(row=0, column=0, sticky="w", pady=5)
        self.cores_var = tk.StringVar(value="3")
        ttk.Entry(env_frame, textvariable=self.cores_var, width=8).grid(row=0, column=1, padx=(5, 15), sticky="w")

        tk.Label(env_frame, text="Sim Time:", font=self.font_main, bg=self.panel_color, fg=self.text_color).grid(row=0, column=2, sticky="w")
        self.sim_time_var = tk.StringVar(value="40")
        ttk.Entry(env_frame, textvariable=self.sim_time_var, width=8).grid(row=0, column=3, padx=(5, 0), sticky="w")

        tk.Label(env_frame, text="Resources:", font=self.font_main, bg=self.panel_color, fg=self.text_color).grid(row=1, column=0, sticky="w", pady=5)
        self.sys_res_var = tk.StringVar(value="A")
        ttk.Entry(env_frame, textvariable=self.sys_res_var, width=25).grid(row=1, column=1, columnspan=3, padx=5, sticky="w")

        tk.Label(self.left_panel, text="2. Tasks & Resources", font=self.font_title, bg=self.panel_color, fg=self.accent_color).pack(anchor="w")
        tasks_frame = tk.Frame(self.left_panel, bg=self.panel_color)
        tasks_frame.pack(fill="both", expand=True, pady=(5, 15))

        tk.Label(tasks_frame, text="Format: Name, Arrival, Exec(C), Period(T)", font=("Segoe UI", 8), fg="#9E9E9E", bg=self.panel_color).pack(anchor="w")
        self.text_tasks = tk.Text(tasks_frame, height=4, width=40, font=("Consolas", 10), bg=self.input_bg, fg="white", insertbackground="white", relief="flat", padx=10, pady=10)
        self.text_tasks.pack(pady=(2, 10))
        self.text_tasks.insert(tk.END, "T1, 0, 1, 3\nT2, 0, 5, 10\nT3, 0, 4, 7")

        tk.Label(tasks_frame, text="Format: Task, Resource, Start, Duration", font=("Segoe UI", 8), fg="#9E9E9E", bg=self.panel_color).pack(anchor="w")
        self.text_resources = tk.Text(tasks_frame, height=3, width=40, font=("Consolas", 10), bg=self.input_bg, fg="white", insertbackground="white", relief="flat", padx=10, pady=10)
        self.text_resources.pack(pady=(2, 10))
        self.text_resources.insert(tk.END, "T2, A, 3, 2")

        tk.Label(self.left_panel, text="3. Algorithm", font=self.font_title, bg=self.panel_color, fg=self.accent_color).pack(anchor="w")
        algo_frame = tk.Frame(self.left_panel, bg=self.panel_color)
        algo_frame.pack(fill="x", pady=(5, 20))
        
        self.algo_var = tk.StringVar(value="Combinational")
        ttk.Combobox(algo_frame, textvariable=self.algo_var, values=["RMA", "EDF", "Combinational"], width=35, font=self.font_main, state="readonly").pack(side=tk.LEFT)

        btn_generate = tk.Button(self.left_panel, text="► Run & Analyze", command=self.process_and_run, 
                                 bg=self.accent_color, fg="white", font=("Segoe UI", 12, "bold"), 
                                 relief="flat", cursor="hand2", pady=10, activebackground="#2563EB", activeforeground="white")
        btn_generate.pack(fill="x", pady=(10, 20))
        
        self.lbl_summary = tk.Label(self.left_panel, text="Ready to simulate.", bg=self.panel_color, fg="#9E9E9E", justify=tk.LEFT, font=self.font_main)
        self.lbl_summary.pack(fill="x", anchor="w")

    def setup_result_panel(self):
        table_frame = tk.Frame(self.right_panel, bg=self.panel_color, padx=15, pady=15)
        table_frame.pack(fill="x", pady=(0, 20))
        tk.Label(table_frame, text="Response Time Analysis", font=self.font_title, bg=self.panel_color, fg="white").pack(anchor="w", pady=(0, 10))

        columns = ("Task", "Execution (C)", "Period (T)", "Response Time (R)", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=4)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="x")

        graph_frame = tk.Frame(self.right_panel, bg=self.panel_color, padx=15, pady=15)
        graph_frame.pack(fill="both", expand=True)
        tk.Label(graph_frame, text="Execution Gantt Chart", font=self.font_title, bg=self.panel_color, fg="white").pack(anchor="w", pady=(0, 10))

        self.fig, self.ax = plt.subplots(figsize=(8, 4), facecolor=self.panel_color)
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def calculate_metrics(self, tasks, algo, cores):
        utilization = sum(task['C'] / task['T'] for task in tasks)
        summary_text = f"Total Utilization (U) = {utilization:.4f} / {cores}.00\n"

        if algo == "RMA":
            n = len(tasks)
            rm_bound = cores * (n * (math.pow(2, 1/n) - 1))
            summary_text += f"Scaled RM Bound = {rm_bound:.4f}\n"
        elif algo == "Combinational":
            summary_text += "Hybrid Bound = Dependent on Task Mix\n"
        
        table_data = []
        if algo == "RMA" or algo == "Combinational":
            sorted_tasks = sorted(tasks, key=lambda x: x['T'])
            for i, task in enumerate(sorted_tasks):
                R_current = task['C']
                while True:
                    total_interference = sum(math.ceil(R_current / hp_task['T']) * hp_task['C'] for hp_task in sorted_tasks[:i])
                    core_interference = math.ceil(total_interference / cores)
                    R_new = task['C'] + core_interference
                    
                    if R_new == R_current:
                        status = "✅ Pass" if R_current <= task['T'] else "❌ Fail"
                        table_data.append((task['name'], task['C'], task['T'], R_current, status))
                        break
                    if R_new > task['T']: 
                        table_data.append((task['name'], task['C'], task['T'], f"> {task['T']}", "❌ Fail"))
                        break
                    R_current = R_new
        else:
            for task in tasks:
                table_data.append((task['name'], task['C'], task['T'], "N/A", "Dynamic (EDF)"))

        return summary_text, table_data

    def simulate_cpu(self, tasks, cores, sim_time, algo):
        schedule = []  
        active_jobs = [] 
        for t in range(sim_time):
            for task in tasks:
                if t >= task['arrival'] and (t - task['arrival']) % task['T'] == 0:
                    active_jobs.append({'name': task['name'], 'remaining_C': task['C'], 'abs_deadline': t + task['T'], 'period': task['T']})
            
            if not active_jobs: continue 

            if algo == "RMA": 
                active_jobs.sort(key=lambda x: x['period'])
            elif algo == "EDF": 
                active_jobs.sort(key=lambda x: x['abs_deadline'])
            elif algo == "Combinational":
                # Primary sort by Period (RM), Secondary sort by Deadline (EDF)
                active_jobs.sort(key=lambda x: (x['period'], x['abs_deadline']))

            running_this_tick = []
            for core in range(min(cores, len(active_jobs))):
                job = active_jobs[core]
                schedule.append((t, t + 1, job['name'], core))
                running_this_tick.append(job)

            for job in running_this_tick: job['remaining_C'] -= 1
            active_jobs = [j for j in active_jobs if j['remaining_C'] > 0]
            
        return schedule

    def process_and_run(self):
        try:
            cores = int(self.cores_var.get())
            sim_time = int(self.sim_time_var.get())
            algo = self.algo_var.get()
            
            tasks = []
            for line in self.text_tasks.get("1.0", tk.END).strip().split('\n'):
                if line.strip():
                    parts = [p.strip() for p in line.split(',')]
                    tasks.append({"name": parts[0], "arrival": int(parts[1]), "C": int(parts[2]), "T": int(parts[3])})

            resources = []
            for line in self.text_resources.get("1.0", tk.END).strip().split('\n'):
                if line.strip():
                    parts = [p.strip() for p in line.split(',')]
                    resources.append({"task": parts[0], "res": parts[1], "start": int(parts[2]), "dur": int(parts[3])})

            summary, table_data = self.calculate_metrics(tasks, algo, cores)
            self.lbl_summary.config(text=summary, fg=self.accent_color, font=self.font_bold)
            
            for row in self.tree.get_children():
                self.tree.delete(row)
            for row in table_data:
                self.tree.insert("", tk.END, values=row)

            final_schedule = self.simulate_cpu(tasks, cores, sim_time, algo)
            self.draw_gantt(final_schedule, tasks, resources, cores, sim_time)

        except Exception as e:
            messagebox.showerror("Input Error", f"Please check your input format.\nDetails: {str(e)}")

    def draw_gantt(self, schedule, tasks, resources, cores, sim_time):
        self.ax.clear() 
        self.ax.set_facecolor(self.panel_color)
        
        self.ax.set_xlim(0, sim_time)
        self.ax.set_ylim(0, cores * 10)
        
        self.ax.set_xlabel("Time", fontsize=10, color=self.text_color)
        self.ax.tick_params(colors=self.text_color)
        
        yticks = [(i * 10) + 5 for i in range(cores)]
        yticklabels = [f"Core {i}" for i in range(cores)]
        self.ax.set_yticks(yticks)
        self.ax.set_yticklabels(yticklabels, fontsize=10, color=self.text_color, fontweight='bold')
        
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('#444444')
        self.ax.spines['bottom'].set_color('#444444')
        
        self.ax.grid(True, axis='x', linestyle='-', color='#333333')

        colors = {'T1': '#4DABF7', 'T2': '#FF922B', 'T3': '#51CF66', 'T4': '#F06595'}
        res_colors = {'A': '#FA5252', 'B': '#FCC419', 'C': '#BE4BDB'}
        task_periods = {task['name']: task['T'] for task in tasks}

        for tick in schedule:
            start, end, task_name, core_id = tick
            y_base = core_id * 10
            color = colors.get(task_name, '#ADB5BD')
            
            rect = Rectangle((start, y_base + 2), 1, 6, facecolor=color, edgecolor='none')
            self.ax.add_patch(rect)
            
            is_resource = False
            for res in resources:
                if res['task'] == task_name:
                    T = task_periods.get(task_name, 1)
                    if start >= res['start'] and (start - res['start']) % T < res['dur']:
                        res_color = res_colors.get(res['res'], '#FA5252')
                        res_rect = Rectangle((start, y_base + 2), 1, 6, facecolor=res_color, edgecolor='none')
                        self.ax.add_patch(res_rect)
                        self.ax.text(start + 0.5, y_base + 5, f"{res['res']}", color='black', ha='center', va='center', fontweight='bold', fontsize=9)
                        is_resource = True
                        break
            
            if not is_resource:
                self.ax.text(start + 0.5, y_base + 5, task_name, color='black', ha='center', va='center', fontsize=9, fontweight='bold')

        for task in tasks:
            arr = task['arrival']
            period = task['T']
            for t in range(arr, sim_time + 1, period):
                self.ax.annotate('', xy=(t, cores * 10), xytext=(t, (cores * 10) - 1.5), arrowprops=dict(arrowstyle="->", color=self.text_color, lw=1))
                if t + period <= sim_time:
                    self.ax.annotate('', xy=(t + period, (cores * 10) - 1.5), xytext=(t + period, cores * 10), arrowprops=dict(arrowstyle="->", color=self.text_color, lw=1))

        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = DarkModeSchedulerApp(root)
    root.mainloop()