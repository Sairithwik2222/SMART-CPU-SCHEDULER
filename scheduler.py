from collections import deque

# -------- FCFS --------
def fcfs(processes):
    processes = sorted(processes, key=lambda x: x['arrival'])
    time = 0
    result = []

    for p in processes:
        if time < p['arrival']:
            time = p['arrival']

        start = time
        finish = start + p['burst']

        result.append({
            'id': p['id'],
            'waiting': start - p['arrival'],
            'turnaround': finish - p['arrival'],
            'start': start,
            'burst': p['burst']
        })

        time = finish
    return result


# -------- SJF --------
def sjf(processes):
    processes = processes.copy()
    time = 0
    result = []

    while processes:
        ready = [p for p in processes if p['arrival'] <= time]
        if not ready:
            time += 1
            continue

        p = min(ready, key=lambda x: x['burst'])
        processes.remove(p)

        start = time
        finish = start + p['burst']

        result.append({
            'id': p['id'],
            'waiting': start - p['arrival'],
            'turnaround': finish - p['arrival'],
            'start': start,
            'burst': p['burst']
        })

        time = finish
    return result


# -------- Priority --------
def priority_scheduling(processes):
    processes = processes.copy()
    time = 0
    result = []

    while processes:
        ready = [p for p in processes if p['arrival'] <= time]
        if not ready:
            time += 1
            continue

        p = min(ready, key=lambda x: x['priority'])
        processes.remove(p)

        start = time
        finish = start + p['burst']

        result.append({
            'id': p['id'],
            'waiting': start - p['arrival'],
            'turnaround': finish - p['arrival'],
            'start': start,
            'burst': p['burst']
        })

        time = finish
    return result


# -------- Round Robin --------
def round_robin(processes, quantum=2):
    queue = deque()
    time = 0
    processes = sorted(processes, key=lambda x: x['arrival'])
    remaining = {p['id']: p['burst'] for p in processes}
    arrival_map = {p['id']: p['arrival'] for p in processes}

    i = 0
    result = {}

    while queue or i < len(processes):
        while i < len(processes) and processes[i]['arrival'] <= time:
            queue.append(processes[i]['id'])
            i += 1

        if not queue:
            time += 1
            continue

        pid = queue.popleft()
        exec_time = min(quantum, remaining[pid])
        remaining[pid] -= exec_time
        time += exec_time

        while i < len(processes) and processes[i]['arrival'] <= time:
            queue.append(processes[i]['id'])
            i += 1

        if remaining[pid] > 0:
            queue.append(pid)
        else:
            finish = time
            turnaround = finish - arrival_map[pid]
            waiting = turnaround - next(p['burst'] for p in processes if p['id'] == pid)
            result[pid] = {
                'id': pid,
                'waiting': waiting,
                'turnaround': turnaround,
                'start': 0,
                'burst': next(p['burst'] for p in processes if p['id'] == pid)
            }

    return list(result.values())


# -------- Average --------
def avg_time(result):
    wt = sum(p['waiting'] for p in result) / len(result)
    tat = sum(p['turnaround'] for p in result) / len(result)
    return wt, tat

def generate_gantt_data(result):
    gantt = []
    for p in result:
        gantt.append({
            "Process": f"P{p['id']}",
            "Start": p['start'],
            "Duration": p['burst']
        })
    return gantt