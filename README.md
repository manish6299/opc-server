# OPC UA Client Data Logger  

## 📌 Introduction  
This project implements an **OPC UA Client** that connects to a simulated OPC UA server, reads dummy tags at regular intervals, and logs the values into **hourly CSV files**.  

The main objectives of this project are:  
- Learn and apply **OPC UA protocol** concepts (client-server, nodes, namespaces).  
- Connect to a simulator (Prosys OPC UA Simulation Server).  
- Continuously **read 10 dummy tags** every minute.  
- Store readings in structured **hourly log files** with timestamps.  
- Automate file rotation and logging for long-running monitoring.  

This project simulates how industrial applications monitor process variables from PLCs, sensors, or SCADA systems.  

---

## ⚙️ Technologies Used  
- **Programming Language**: Python 3.12  
- **Libraries**:  
  - [`opcua`](https://github.com/FreeOpcUa/python-opcua) – OPC UA client library.  
  - `csv`, `datetime`, `time`, `os` – Standard Python libraries for file handling and scheduling.  
- **Simulator**: [Prosys OPC UA Simulation Server](https://prosysopc.com/products/opc-ua-simulation-server/)  

---

## 🚀 Features  
- Connects automatically to the OPC UA server.  
- **Auto-discovers available tags** under the *Simulation* folder.  
- Ensures **10 tags** are always logged (repeats if fewer than 10 exist).  
- Reads **once per minute**.  
- Logs to **hourly CSV files** (`OPC_Log_YYYY-MM-DD_HH.csv`).  
- Columns include:  
  - Local timestamp (`YYYY-MM-DD HH:MM:SS`)  
  - UTC Epoch timestamp (seconds since 1970)  
  - Tag1 … Tag10 values (with real tag names in headers).  
- Runs **continuously** and switches log files on every hour change.  

---

## 🖥️ Setup Instructions  

### 1. Install Prerequisites  
- Install Python (>=3.10 recommended).  
- Install required Python packages:  
```bash
pip install opcua
```

### 2. Setup OPC UA Simulator (Prosys)  
1. Download **Prosys OPC UA Simulation Server** from:  
   👉 https://prosysopc.com/products/opc-ua-simulation-server/  
2. Install and launch the simulator.  
3. Verify the default endpoint (commonly):  
   ```
   opc.tcp://localhost:53530/OPCUA/SimulationServer
   ```
4. Expand the **Objects → Simulation** folder.  
   - By default, you will see tags like **Counter, Random, Sawtooth, Sinusoid, Square, Triangle, Constant**.  

### 3. Run the Client  
1. Place the client script (`opcua_client_logger.py`) in your project folder.  
2. Run it:  
   ```bash
   python opcua_client_logger.py
   ```
3. The client will:  
   - Connect to the simulator.  
   - Discover tags.  
   - Start logging values once per minute.  
   - Create CSV files like:  
     ```
     OPC_Log_2025-09-01_14.csv
     OPC_Log_2025-09-01_15.csv
     ...
     ```  

---

## 📂 Example Output  

**File Name:** `OPC_Log_2025-09-01_14.csv`  

```csv
Timestamp,Timestamp_UTC_Epoch,Tag1_Counter,Tag2_Random,Tag3_Sawtooth,Tag4_Sinusoid,Tag5_Square,Tag6_Triangle,Tag7_Constant,Tag8_Counter,Tag9_Random,Tag10_Sawtooth
2025-09-01 14:36:28,1756717588,9,0.212727,-0.8,-0.8134734,-2.0,-0.5333334,1.0,9,0.212727,-0.8
2025-09-01 14:37:00,1756717620,10,-0.5043247,0.0,0.0,-2.0,0.0,1.0,10,-0.5043247,0.0
2025-09-01 14:38:00,1756717680,7,1.83603,-0.4,-0.4158234,-2.0,0.0,1.0,8,-1.794179,0.0
```

---

## 📖 How It Works  
1. On start, the client connects to the OPC UA server.  
2. It scans the *Simulation* folder for available variable nodes.  
3. If fewer than 10 nodes are found, some nodes are repeated until 10 are reached.  
4. Every minute:  
   - Current local timestamp is recorded.  
   - UTC Epoch time is captured.  
   - All tag values are read and appended to the active hourly CSV file.  
5. At the start of a new hour, a new CSV file is created automatically.  

---

## ✅ Conclusion  
This project demonstrates the design and implementation of a **continuous OPC UA data logger**. It connects to a simulated server, reads real-time process variables, and stores them in a structured, timestamped log format suitable for monitoring, analysis, or further processing.  
