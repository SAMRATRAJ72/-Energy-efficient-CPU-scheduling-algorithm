import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import time
import random

# Function to load GitHub logo from URL
def load_github_logo():
    url = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def center_all_headers():
    st.markdown(
        """
        <style>
            /* Main background and text colors */
            .stApp {
                background-color: #f5f7fa;
                color: #333333;
            }
            
            /* Move sidebar to right */
            section[data-testid="stSidebar"] {
                position: fixed;
                right: 0;
                top: 0;
                bottom: 0;
                width: 300px;
                padding: 1rem;
                background-color: #e6f0ff;
                border-left: 1px solid #d3d3d3;
                transition: margin 200ms;
            }
            
            /* Adjust main content area */
            .main .block-container {
                padding-right: 320px;
                padding-left: 2rem;
                max-width: 1000px;
            }
            
            /* Center all header text */
            h1, h2, h3 {
                text-align: center;
                color: #2563eb !important;
                font-weight: bold;
            }
            
            /* Container styling */
            .container {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                border: 1px solid #e0e0e0;
            }
            
            /* Button styling */
            .stButton>button {
                background-color: #2563eb;
                color: white;
                border-radius: 8px;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                transition: all 0.3s;
            }
            
            .stButton>button:hover {
                background-color: #1d4ed8;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            
            /* Metric styling */
            .metric-box {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                border-left: 4px solid #2563eb;
            }
            
            /* GitHub logo positioning */
            .github-corner {
                position: fixed;
                bottom: 10px;
                left: 10px;
                z-index: 100;
            }
            
            /* Table styling */
            .dataframe {
                background-color: white !important;
                border-radius: 10px !important;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
            }
            
            /* Process input styling */
            .process-input {
                background-color: #f8fafc;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 15px;
                border: 1px solid #e2e8f0;
            }
            
            /* Animation for simulation */
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            
            .pulse-animation {
                animation: pulse 1.5s infinite;
            }
            
            /* Responsive adjustments */
            @media (max-width: 768px) {
                section[data-testid="stSidebar"] {
                    width: 250px;
                }
                .main .block-container {
                    padding-right: 270px;
                    padding-left: 1rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply custom styles
center_all_headers()

# GitHub logo and link
github_logo = load_github_logo()
st.markdown(
    f"""
    <div class="github-corner">
        <a href="https://github.com/FarazKhan001/Energy-Efficient-CPU-Scheduling-Algorithm" target="_blank">
            <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="40">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar on the right
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #2563eb;'>CPU Scheduling</h1>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=["FCFS", "SJF", "SRTF", "Round Robin", "Priority"],
        icons=["clock", "stopwatch", "hourglass", "arrow-repeat", "list-ol"],
        default_index=0,
        styles={
            "container": {"background-color": "#e6f0ff"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "8px",
                "--hover-color": "#dbeafe",
                "border-radius": "8px",
                "padding": "8px 12px"
            },
            "nav-link-selected": {
                "background-color": "#2563eb",
                "font-weight": "bold"
            },
        }
    )
    
    # Add a simulation speed control
    st.markdown("---")
    st.markdown("<h4 style='text-align: center;'>Simulation Controls</h4>", unsafe_allow_html=True)
    simulation_speed = st.slider("Animation Speed", 0.5, 5.0, 1.0, 0.5)
    
    # Add a theme selector
    theme_color = st.selectbox("Theme Color", ["Blue", "Green", "Purple", "Red"], index=0)
    
    # Add a quick guide
    with st.expander("Quick Guide"):
        st.write("""
        1. Select algorithm
        2. Enter process details
        3. Click Simulate
        4. View results & animation
        """)

# Dynamic theme color adjustment
def update_theme(color):
    color_map = {
        "Blue": "#38ACEC",
        "Green": "#95B9C7",
        "Purple": "#6960EC",
        "Red": "#F01E2C",
    }
    hex_color = color_map.get(color, "#2563eb")
    
    st.markdown(
        f"""
        <style>
            h1, h2, h3 {{ color: {hex_color} !important; }}
            .stButton>button {{ background-color: {hex_color}; }}
            .stButton>button:hover {{ background-color: {hex_color}; opacity: 0.9; }}
            .metric-box {{ border-left: 4px solid {hex_color}; }}
            .st-c7 {{ background-color: {hex_color} !important; }}
            .gantt-process {{ background-color: {hex_color} !important; }}
        </style>
        """,
        unsafe_allow_html=True
    )

update_theme(theme_color)

# Common functions
def plot_gantt_chart(timeline, algorithm, color='#2563eb'):
    fig, ax = plt.subplots(figsize=(12, 4))
    
    for i, (process_id, start, end) in enumerate(timeline):
        color_fill = color if process_id != "IDLE" else '#f0f0f0'
        ax.barh(y=0, width=end-start, left=start, color=color_fill, edgecolor='black')
        label_color = 'white' if process_id != "IDLE" else 'black'
        ax.text((start+end)/2, 0, process_id, 
                ha='center', va='center', 
                color=label_color, fontsize=12, fontweight='bold')
    
    ax.set_yticks([])
    ax.set_xticks(np.arange(0, timeline[-1][2] + 1, 1))
    ax.set_xlabel("Time Units")
    ax.set_title(f"Gantt Chart - {algorithm} Scheduling", pad=20)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    return fig

def display_metrics(results):
    avg_tat = sum(p['Turnaround Time'] for p in results) / len(results)
    avg_wt = sum(p['Waiting Time'] for p in results) / len(results)
    throughput = len(results) / max(p['Completion Time'] for p in results)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="metric-box">
                <h4>Avg Turnaround Time</h4>
                <h2>{avg_tat:.2f}</h2>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-box">
                <h4>Avg Waiting Time</h4>
                <h2>{avg_wt:.2f}</h2>
            </div>
            """, unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric-box">
                <h4>Throughput</h4>
                <h2>{throughput:.2f}</h2>
            </div>
            """, unsafe_allow_html=True
        )

def animate_gantt_chart(timeline, algorithm, color='#2563eb'):
    placeholder = st.empty()
    end_time = timeline[-1][2]
    
    for t in range(end_time + 1):
        fig, ax = plt.subplots(figsize=(12, 4))
        
        # Draw completed processes
        for process_id, start, end in timeline:
            if end <= t:
                color_fill = color if process_id != "IDLE" else '#f0f0f0'
                ax.barh(y=0, width=end-start, left=start, color=color_fill, edgecolor='black')
                label_color = 'white' if process_id != "IDLE" else 'black'
                ax.text((start+end)/2, 0, process_id, 
                        ha='center', va='center', 
                        color=label_color, fontsize=12, fontweight='bold')
        
        # Draw current process
        current_process = None
        for process_id, start, end in timeline:
            if start <= t < end:
                current_process = process_id
                ax.barh(y=0, width=t-start, left=start, color=color, edgecolor='black', alpha=0.7)
                ax.text((start+t)/2, 0, process_id, 
                        ha='center', va='center', 
                        color='white', fontsize=12, fontweight='bold')
                break
        
        ax.set_yticks([])
        ax.set_xlim(0, end_time)
        ax.set_xticks(np.arange(0, end_time + 1, 1))
        ax.set_xlabel("Time Units")
        title = f"Gantt Chart - {algorithm} Scheduling (Time: {t})"
        if current_process:
            title += f" | Running: {current_process}"
        ax.set_title(title, pad=20)
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(1/simulation_speed)

def generate_random_processes(num_processes):
    processes = []
    for i in range(num_processes):
        pid = f"P{i+1}"
        at = random.randint(0, 5)
        bt = random.randint(1, 10)
        processes.append([pid, at, bt])
    return processes

# FCFS Scheduling
if selected == "FCFS":
    st.title("First-Come First-Served Scheduling")
    
    with st.expander("ℹ️ About FCFS", expanded=True):
        st.write("""
        **First-Come First-Served (FCFS)** is the simplest CPU scheduling algorithm:
        - Processes are executed in order of arrival (FIFO queue)
        - Non-preemptive - once started, runs to completion
        - Simple to implement but suffers from the 'convoy effect'
        - May result in poor average waiting time
        """)
    
    # Process input section
    st.subheader("Process Details")
    col1, col2 = st.columns([3,1])
    with col1:
        num_processes = st.slider("Number of processes", 1, 30, 3, key="fcfs_num")
    with col2:
        if st.button("Randomize", key="fcfs_random"):
            st.session_state.fcfs_processes = generate_random_processes(num_processes)
    
    process_list = []
    for i in range(num_processes):
        with st.container():
            cols = st.columns(3)
            with cols[0]:
                pid = st.text_input(f"Process ID", f"P{i+1}", key=f"fcfs_pid_{i}")
            with cols[1]:
                at = st.number_input(f"Arrival Time", min_value=0, value=i*2, key=f"fcfs_at_{i}")
            with cols[2]:
                bt = st.number_input(f"Burst Time", min_value=1, value=5, key=f"fcfs_bt_{i}")
            process_list.append([pid, at, bt])
    
    # Simulation controls
    col1, col2 = st.columns(2)
    with col1:
        simulate_btn = st.button("Simulate FCFS", type="primary", use_container_width=True)
    with col2:
        animate_btn = st.button("Animate FCFS", use_container_width=True)
    
    if simulate_btn or animate_btn:
        # FCFS Scheduling Logic
        processes = sorted(process_list, key=lambda x: x[1])  # Sort by arrival time
        timeline = []
        current_time = 0
        results = []
        
        for i, (pid, at, bt) in enumerate(processes):
            if current_time < at:
                timeline.append(("IDLE", current_time, at))
                current_time = at
            
            start_time = current_time
            completion_time = current_time + bt
            timeline.append((pid, start_time, completion_time))
            
            turnaround = completion_time - at
            waiting = turnaround - bt
            
            results.append({
                "Process ID": pid,
                "Arrival Time": at,
                "Burst Time": bt,
                "Start Time": start_time,
                "Completion Time": completion_time,
                "Turnaround Time": turnaround,
                "Waiting Time": waiting
            })
            current_time = completion_time
        
        # Display results
        st.subheader("Results")
        df = pd.DataFrame(results)
        st.dataframe(df.style.set_properties(**{'background-color': 'white'}), 
                      use_container_width=True,
                      hide_index=True)
        
        # Display metrics
        display_metrics(results)
        
        # Show Gantt chart
        st.subheader("Gantt Chart")
        fig = plot_gantt_chart(timeline, "FCFS", color='#2563eb')
        st.pyplot(fig)
        
        # Animation
        if animate_btn:
            st.subheader("Simulation Animation")
            animate_gantt_chart(timeline, "FCFS", color='#2563eb')

# SJF Scheduling
elif selected == "SJF":
    st.title("⏱️ Shortest Job First (Non-Preemptive)")
    
    with st.expander("ℹ️ About SJF", expanded=True):
        st.write("""
        **Shortest Job First (SJF)** scheduling:
        - Executes processes with shortest burst time first
        - Non-preemptive version shown here
        - Minimizes average waiting time
        - Requires knowing burst times in advance
        """)
    
    # Process input section
    st.subheader("Process Details")
    col1, col2 = st.columns([3,1])
    with col1:
        num_processes = st.slider("Number of processes", 1, 30, 3, key="sjf_num")
    with col2:
        if st.button("Randomize", key="sjf_random"):
            st.session_state.sjf_processes = generate_random_processes(num_processes)
    
    process_list = []
    for i in range(num_processes):
        with st.container():
            cols = st.columns(3)
            with cols[0]:
                pid = st.text_input(f"Process ID", f"P{i+1}", key=f"sjf_pid_{i}")
            with cols[1]:
                at = st.number_input(f"Arrival Time", min_value=0, value=i*2, key=f"sjf_at_{i}")
            with cols[2]:
                bt = st.number_input(f"Burst Time", min_value=1, value=(i+1)*2, key=f"sjf_bt_{i}")
            process_list.append([pid, at, bt])
    
    # Simulation controls
    col1, col2 = st.columns(2)
    with col1:
        simulate_btn = st.button("Simulate SJF", type="primary", use_container_width=True)
    with col2:
        animate_btn = st.button("Animate SJF", use_container_width=True)
    
    if simulate_btn or animate_btn:
        # SJF Scheduling Logic
        processes = sorted(process_list, key=lambda x: x[1])  # Sort by arrival time
        n = len(processes)
        completed = [False] * n
        timeline = []
        current_time = 0
        results = []
        
        while sum(completed) < n:
            ready = [i for i in range(n) if processes[i][1] <= current_time and not completed[i]]
            
            if not ready:
                next_arrival = min([p[1] for i,p in enumerate(processes) if not completed[i]])
                timeline.append(("IDLE", current_time, next_arrival))
                current_time = next_arrival
                continue
            
            # Find process with shortest burst time
            shortest_idx = min(ready, key=lambda i: processes[i][2])
            pid, at, bt = processes[shortest_idx]
            
            start_time = current_time
            completion_time = current_time + bt
            timeline.append((pid, start_time, completion_time))
            
            turnaround = completion_time - at
            waiting = turnaround - bt
            
            results.append({
                "Process ID": pid,
                "Arrival Time": at,
                "Burst Time": bt,
                "Start Time": start_time,
                "Completion Time": completion_time,
                "Turnaround Time": turnaround,
                "Waiting Time": waiting
            })
            
            completed[shortest_idx] = True
            current_time = completion_time
        
        # Display results
        st.subheader("Results")
        df = pd.DataFrame(results)
        st.dataframe(df.sort_values("Process ID").style.set_properties(**{'background-color': 'white'}), 
                      use_container_width=True,
                      hide_index=True)
        
        # Display metrics
        display_metrics(results)
        
        # Show Gantt chart
        st.subheader("Gantt Chart")
        fig = plot_gantt_chart(timeline, "SJF", color='#2563eb')
        st.pyplot(fig)
        
        # Animation
        if animate_btn:
            st.subheader("Simulation Animation")
            animate_gantt_chart(timeline, "SJF", color='#2563eb')

# SRTF Scheduling
elif selected == "SRTF":
    st.title("Shortest Remaining Time First (Preemptive)")
    
    with st.expander("ℹ️ About SRTF", expanded=True):
        st.write("""
        **Shortest Remaining Time First (SRTF)**:
        - Preemptive version of SJF
        - Always executes process with shortest remaining time
        - More complex but better for responsiveness
        - Optimal for minimizing average turnaround time
        """)
    
    # Process input section
    st.subheader("Process Details")
    col1, col2 = st.columns([3,1])
    with col1:
        num_processes = st.slider("Number of processes", 1, 30, 3, key="srtf_num")
    with col2:
        if st.button("Randomize", key="srtf_random"):
            st.session_state.srtf_processes = generate_random_processes(num_processes)
    
    process_list = []
    for i in range(num_processes):
        with st.container():
            cols = st.columns(3)
            with cols[0]:
                pid = st.text_input(f"Process ID", f"P{i+1}", key=f"srtf_pid_{i}")
            with cols[1]:
                at = st.number_input(f"Arrival Time", min_value=0, value=i, key=f"srtf_at_{i}")
            with cols[2]:
                bt = st.number_input(f"Burst Time", min_value=1, value=(i+1)*2, key=f"srtf_bt_{i}")
            process_list.append([pid, at, bt])
    
    # Simulation controls
    col1, col2 = st.columns(2)
    with col1:
        simulate_btn = st.button("Simulate SRTF", type="primary", use_container_width=True)
    with col2:
        animate_btn = st.button("Animate SRTF", use_container_width=True)
    
    if simulate_btn or animate_btn:
        # SRTF Scheduling Logic
        processes = sorted(process_list, key=lambda x: x[1])  # Sort by arrival time
        n = len(processes)
        remaining_time = [p[2] for p in processes]
        timeline = []
        current_time = 0
        results = {pid: {"pid": pid, "at": at, "bt": bt, "start": None, "end": None} 
                  for pid, at, bt in processes}
        
        while True:
            ready = [i for i in range(n) if processes[i][1] <= current_time and remaining_time[i] > 0]
            
            if not ready:
                if all(rt == 0 for rt in remaining_time):
                    break
                next_arrival = min([p[1] for i,p in enumerate(processes) if remaining_time[i] > 0])
                idle_time = next_arrival - current_time
                if idle_time > 0:
                    timeline.append(("IDLE", current_time, next_arrival))
                current_time = next_arrival
                continue
            
            # Find process with shortest remaining time
            shortest_idx = min(ready, key=lambda i: remaining_time[i])
            pid = processes[shortest_idx][0]
            
            # Record start time if not already set
            if results[pid]["start"] is None:
                results[pid]["start"] = current_time
            
            # Execute for 1 time unit
            start_time = current_time
            remaining_time[shortest_idx] -= 1
            current_time += 1
            
            if timeline and timeline[-1][0] == pid:
                # Extend existing execution
                timeline[-1] = (pid, timeline[-1][1], current_time)
            else:
                timeline.append((pid, start_time, current_time))
            
            # Record completion if finished
            if remaining_time[shortest_idx] == 0:
                results[pid]["end"] = current_time
        
        # Prepare results
        final_results = []
        for pid, data in results.items():
            if data["end"] is None:
                continue
            turnaround = data["end"] - data["at"]
            waiting = turnaround - data["bt"]
            final_results.append({
                "Process ID": pid,
                "Arrival Time": data["at"],
                "Burst Time": data["bt"],
                "Start Time": data["start"],
                "Completion Time": data["end"],
                "Turnaround Time": turnaround,
                "Waiting Time": waiting
            })
        
        # Display results
        st.subheader("Results")
        df = pd.DataFrame(final_results)
        st.dataframe(df.sort_values("Process ID").style.set_properties(**{'background-color': 'white'}), 
                      use_container_width=True,
                      hide_index=True)
        
        # Display metrics
        display_metrics(final_results)
        
        # Show Gantt chart
        st.subheader("Gantt Chart")
        fig = plot_gantt_chart(timeline, "SRTF", color='#2563eb')
        st.pyplot(fig)
        
        # Animation
        if animate_btn:
            st.subheader("Simulation Animation")
            animate_gantt_chart(timeline, "SRTF", color='#2563eb')

# Round Robin Scheduling
elif selected == "Round Robin":
    st.title("Round Robin Scheduling")
    
    with st.expander("ℹ️ About Round Robin", expanded=True):
        st.write("""
        **Round Robin** scheduling:
        - Each process gets equal time quantum
        - Preemptive - interrupts processes after quantum
        - Fair allocation of CPU time
        - Performance depends heavily on quantum size
        """)
    
    # Time quantum input
    time_quantum = st.slider("Time Quantum", 1, 10, 2, key="rr_quantum")
    
    # Process input section
    st.subheader("Process Details")
    col1, col2 = st.columns([3,1])
    with col1:
        num_processes = st.slider("Number of processes", 1, 30, 3, key="rr_num")
    with col2:
        if st.button("Randomize", key="rr_random"):
            st.session_state.rr_processes = generate_random_processes(num_processes)
    
    process_list = []
    for i in range(num_processes):
        with st.container():
            cols = st.columns(3)
            with cols[0]:
                pid = st.text_input(f"Process ID", f"P{i+1}", key=f"rr_pid_{i}")
            with cols[1]:
                at = st.number_input(f"Arrival Time", min_value=0, value=i, key=f"rr_at_{i}")
            with cols[2]:
                bt = st.number_input(f"Burst Time", min_value=1, value=(i+1)*2, key=f"rr_bt_{i}")
            process_list.append([pid, at, bt])
    
    # Simulation controls
    col1, col2 = st.columns(2)
    with col1:
        simulate_btn = st.button("Simulate Round Robin", type="primary", use_container_width=True)
    with col2:
        animate_btn = st.button("Animate Round Robin", use_container_width=True)
    
    if simulate_btn or animate_btn:
        # Round Robin Scheduling Logic
        processes = sorted(process_list, key=lambda x: x[1])  # Sort by arrival time
        n = len(processes)
        remaining_time = [p[2] for p in processes]
        timeline = []
        current_time = 0
        results = {pid: {"pid": pid, "at": at, "bt": bt, "start": None, "end": None} 
                  for pid, at, bt in processes}
        queue = []
        visited = [False] * n
        
        # Initial queue population
        for i in range(n):
            if processes[i][1] <= current_time:
                queue.append(i)
                visited[i] = True
        
        while queue:
            idx = queue.pop(0)
            pid, at, bt = processes[idx]
            
            if current_time < at:
                timeline.append(("IDLE", current_time, at))
                current_time = at
            
            # Record start time if not already set
            if results[pid]["start"] is None:
                results[pid]["start"] = current_time
            
            # Execute for time quantum or remaining time
            exec_time = min(time_quantum, remaining_time[idx])
            start_time = current_time
            current_time += exec_time
            remaining_time[idx] -= exec_time
            timeline.append((pid, start_time, current_time))
            
            # Check for new arrivals
            for i in range(n):
                if not visited[i] and processes[i][1] <= current_time:
                    queue.append(i)
                    visited[i] = True
            
            # Record completion if finished
            if remaining_time[idx] == 0:
                results[pid]["end"] = current_time
            else:
                queue.append(idx)  # Re-add to queue if not finished
        
        # Prepare results
        final_results = []
        for pid, data in results.items():
            if data["end"] is None:
                continue
            turnaround = data["end"] - data["at"]
            waiting = turnaround - data["bt"]
            final_results.append({
                "Process ID": pid,
                "Arrival Time": data["at"],
                "Burst Time": data["bt"],
                "Start Time": data["start"],
                "Completion Time": data["end"],
                "Turnaround Time": turnaround,
                "Waiting Time": waiting
            })
        
        # Display results
        st.subheader("Results")
        df = pd.DataFrame(final_results)
        st.dataframe(df.sort_values("Process ID").style.set_properties(**{'background-color': 'white'}), 
                      use_container_width=True,
                      hide_index=True)
        
        # Display metrics
        display_metrics(final_results)
        
        # Show Gantt chart
        st.subheader("Gantt Chart")
        fig = plot_gantt_chart(timeline, f"Round Robin (Quantum={time_quantum})", color='#2563eb')
        st.pyplot(fig)
        
        # Animation
        if animate_btn:
            st.subheader("Simulation Animation")
            animate_gantt_chart(timeline, f"Round Robin (Quantum={time_quantum})", color='#2563eb')

# Priority Scheduling
elif selected == "Priority":
    st.title("Priority Scheduling")
    
    with st.expander("ℹ️ About Priority Scheduling", expanded=True):
        st.write("""
        **Priority** scheduling:
        - Each process has a priority (lower number = higher priority)
        - Can be preemptive or non-preemptive
        - Higher priority processes run first
        - May cause starvation of low-priority processes
        """)
    
    # Scheduling type
    preemptive = st.radio("Scheduling Type", ["Non-Preemptive", "Preemptive"], index=0, key="priority_type") == "Preemptive"
    
    # Process input section
    st.subheader("Process Details")
    col1, col2 = st.columns([3,1])
    with col1:
        num_processes = st.slider("Number of processes", 1, 30, 3, key="priority_num")
    with col2:
        if st.button("Randomize", key="priority_random"):
            st.session_state.priority_processes = generate_random_processes(num_processes)
            for i in range(num_processes):
                st.session_state.priority_processes[i].append(random.randint(1, 5))
    
    process_list = []
    for i in range(num_processes):
        with st.container():
            cols = st.columns(4)
            with cols[0]:
                pid = st.text_input(f"Process ID", f"P{i+1}", key=f"priority_pid_{i}")
            with cols[1]:
                at = st.number_input(f"Arrival Time", min_value=0, value=i, key=f"priority_at_{i}")
            with cols[2]:
                bt = st.number_input(f"Burst Time", min_value=1, value=(i+1)*2, key=f"priority_bt_{i}")
            with cols[3]:
                priority = st.number_input(f"Priority", min_value=1, value=i+1, key=f"priority_priority_{i}")
            process_list.append([pid, at, bt, priority])
    
    # Simulation controls
    col1, col2 = st.columns(2)
    with col1:
        simulate_btn = st.button("Simulate Priority", type="primary", use_container_width=True)
    with col2:
        animate_btn = st.button("Animate Priority", use_container_width=True)
    
    if simulate_btn or animate_btn:
        # Priority Scheduling Logic
        processes = sorted(process_list, key=lambda x: (x[1], x[3]))  # Sort by arrival then priority
        n = len(processes)
        remaining_time = [p[2] for p in processes]
        timeline = []
        current_time = 0
        results = {pid: {"pid": pid, "at": at, "bt": bt, "priority": priority, "start": None, "end": None} 
                  for pid, at, bt, priority in processes}
        
        while True:
            ready = [i for i in range(n) if processes[i][1] <= current_time and remaining_time[i] > 0]
            
            if not ready:
                if all(rt == 0 for rt in remaining_time):
                    break
                next_arrival = min([p[1] for i,p in enumerate(processes) if remaining_time[i] > 0])
                timeline.append(("IDLE", current_time, next_arrival))
                current_time = next_arrival
                continue
            
            # Find process with highest priority (lowest number)
            highest_idx = min(ready, key=lambda i: processes[i][3])
            pid = processes[highest_idx][0]
            
            if preemptive:
                # Record start time if not already set
                if results[pid]["start"] is None:
                    results[pid]["start"] = current_time
                
                # Execute for 1 time unit
                start_time = current_time
                remaining_time[highest_idx] -= 1
                current_time += 1
                
                if timeline and timeline[-1][0] == pid:
                    # Extend existing execution
                    timeline[-1] = (pid, timeline[-1][1], current_time)
                else:
                    timeline.append((pid, start_time, current_time))
                
                # Record completion if finished
                if remaining_time[highest_idx] == 0:
                    results[pid]["end"] = current_time
            else:
                # Non-preemptive - execute entire burst
                if results[pid]["start"] is None:
                    results[pid]["start"] = current_time
                
                start_time = current_time
                current_time += remaining_time[highest_idx]
                remaining_time[highest_idx] = 0
                timeline.append((pid, start_time, current_time))
                results[pid]["end"] = current_time
        
        # Prepare results
        final_results = []
        for pid, data in results.items():
            if data["end"] is None:
                continue
            turnaround = data["end"] - data["at"]
            waiting = turnaround - data["bt"]
            final_results.append({
                "Process ID": pid,
                "Arrival Time": data["at"],
                "Burst Time": data["bt"],
                "Priority": data["priority"],
                "Start Time": data["start"],
                "Completion Time": data["end"],
                "Turnaround Time": turnaround,
                "Waiting Time": waiting
            })
        
        # Display results
        st.subheader("Results")
        df = pd.DataFrame(final_results)
        st.dataframe(df.sort_values("Process ID").style.set_properties(**{'background-color': 'white'}), 
                      use_container_width=True,
                      hide_index=True)
        
        # Display metrics
        display_metrics(final_results)
        
        # Show Gantt chart
        st.subheader("Gantt Chart")
        fig = plot_gantt_chart(timeline, f"Priority ({'Preemptive' if preemptive else 'Non-Preemptive'})", color='#2563eb')
        st.pyplot(fig)
        
        # Animation
        if animate_btn:
            st.subheader("Simulation Animation")
            animate_gantt_chart(timeline, f"Priority ({'Preemptive' if preemptive else 'Non-Preemptive'})", color='#2563eb')

# Footer
st.markdown("---")