import matplotlib.pyplot as plt


def plot_graph_time(a,b):
    plt.plot(a, b)
    plt.title("CPU Time vs. Problem Size")
    plt.xlabel('Problem Size')
    plt.ylabel("CPU Time")
    plt.show() 

def plot_graph_memory(a,b):
    plt.plot(a, b)
    plt.title("Memory Usage vs. Problem Size")
    plt.xlabel('Problem Size')
    plt.ylabel("Memory Usage")
    plt.show()   

def main():
    m_n = [132,160,608,2430,2048,2066]
    time = [0.221,0.224,0.097,1.66,0.399,0.81]
    memory = [31220,31532,2752,13156,6496,8440]
    plot_graph_time(m_n,time)
    plot_graph_memory(m_n,memory)

main()