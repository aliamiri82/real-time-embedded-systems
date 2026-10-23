import matplotlib.pyplot as plt

class Task:
    def __init__(self, name, c, p, d):
        self.name = name
        self.c = c
        self.p = p
        self.d = d

class Job:
    def __init__(self, task, arrival_time):
        self.task = task
        self.arrival = arrival_time
        self.abs_deadline = arrival_time + task.d
        self.remaining = task.c

def read_input(filename="input.txt"):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    total_time, cores = map(int, lines[0].split())
    num_tasks = int(lines[1])
    
    tasks = []
    for i in range(2, 2 + num_tasks):
        parts = lines[i].split()
        tasks.append(Task(parts[0], int(parts[1]), int(parts[2]), int(parts[3])))
        
    return total_time, cores, tasks

def simulate(total_time, cores, tasks, algo):
    active_jobs = []
    completed_count = 0
    missed_count = 0
    schedule = {c: [] for c in range(cores)}
    
    for t in range(total_time):
        for task in tasks:
            if t % task.p == 0:
                active_jobs.append(Job(task, t))
        
        for job in active_jobs[:]:
            if t >= job.abs_deadline:
                if job.remaining > 0:
                    missed_count += 1
                active_jobs.remove(job)
        
        if algo == 'RM':
            active_jobs.sort(key=lambda j: j.task.p)
        elif algo == 'DM':
            active_jobs.sort(key=lambda j: j.task.d)
        elif algo == 'EDF':
            active_jobs.sort(key=lambda j: j.abs_deadline)
            
        assigned_jobs = active_jobs[:cores]
        
        for core in range(cores):
            if core < len(assigned_jobs):
                job = assigned_jobs[core]
                schedule[core].append(job.task.name)
                job.remaining -= 1
                
                if job.remaining == 0:
                    completed_count += 1
                    active_jobs.remove(job)
            else:
                schedule[core].append("IDLE")
                
    busy_time = sum(1 for core in schedule for status in schedule[core] if status != "IDLE")
    utilization = (busy_time / (total_time * cores)) * 100
    
    return {
        'algo': algo,
        'cores': cores,
        'schedule': schedule,
        'completed': completed_count,
        'missed': missed_count,
        'utilization': utilization
    }

def write_output(filename, all_results):
    with open(filename, 'w') as f:
        for res in all_results:
            f.write("="*50 + "\n")
            f.write(f"Algorithm: {res['algo']}\n")
            f.write(f"Cores: {res['cores']}\n")
            f.write("="*50 + "\n\n")
            f.write(f"Completed Jobs: {res['completed']}\n")
            f.write(f"Deadline Misses: {res['missed']}\n")
            f.write(f"CPU Utilization: {res['utilization']:.2f}%\n\n")
            
            for core, sched in res['schedule'].items():
                f.write(f"Core {core} Schedule:\n")
                f.write(" ".join(sched) + "\n\n")

def plot_gantt(all_results, total_time, filename="gantt_charts.png"):
    fig, axes = plt.subplots(len(all_results), 1, figsize=(12, 3 * len(all_results)))
    if len(all_results) == 1:
        axes = [axes]
        
    colors = ['#ff7f0e', '#1f77b4', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    task_colors = {}
    
    for ax, res in zip(axes, all_results):
        algo = res['algo']
        cores = res['cores']
        schedule = res['schedule']
        
        ax.set_title(f"{algo} Scheduling - {cores} Core(s)")
        ax.set_xlim(0, total_time)
        ax.set_ylim(0, cores * 10)
        ax.set_xlabel("Time")
        ax.set_ylabel("Cores")
        
        y_ticks = []
        y_tick_labels = []
        
        for core in range(cores):
            y_center = (cores - core - 1) * 10 + 5
            y_ticks.append(y_center)
            y_tick_labels.append(f"Core {core}")
            
            for t in range(total_time):
                task_name = schedule[core][t]
                if task_name != "IDLE":
                    if task_name not in task_colors:
                        task_colors[task_name] = colors[len(task_colors) % len(colors)]
                    
                    ax.broken_barh([(t, 1)], (y_center - 4, 8), facecolors=task_colors[task_name], edgecolor='black', linewidth=0.5)
                    ax.text(t + 0.5, y_center, task_name, ha='center', va='center', color='white', fontsize=9)
                    
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_tick_labels)
        ax.grid(True, axis='x', linestyle='--', alpha=0.5)
        
    plt.tight_layout()
    plt.savefig(filename, dpi=300)

if __name__ == "__main__":
    total_time, cores, tasks = read_input("input.txt")
    algorithms = ['RM', 'DM', 'EDF']
    results = []
    
    for algo in algorithms:
        res = simulate(total_time, cores, tasks, algo)
        results.append(res)
        
if cores == 1:
    filename = "output.txt"
    filename_2 = "gantt_charts.png"
else:
    filename = f"output_{cores}_cores.txt"
    filename_2 = f"gantt_charts_{cores}_cores.png"


write_output(filename, results)
plot_gantt(results, total_time, filename_2)