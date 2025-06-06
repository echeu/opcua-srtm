###import sys
###sys.path.insert(0, "..")
import logging
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from opcua import Client
from opcua import ua

"""
This script connects to the SRTM via opcua. It creates a window to display some values 
as a function of time
"""

def init_socket(cl):
    
    # flag to retry connection
    iloop = 1

    # Loop until a connection is established
    while iloop > 0:  
        try:

            # start of attempt to establish a connection
            print("Connecting to SRTM...")

            # Connect to socket
            print("Connect socket")
            cl.connect_socket()
            try:
                print("Open secure channel")
                cl.open_secure_channel()
                try:
                    print("Create session")
                    cl.create_session()
                    try:
                        print("Activate session")
                        cl.activate_session(username=cl._username, password=cl._password, certificate=cl.user_certificate)
                    except Exception:
                        # clean up the session
                        print("Close session")
                        cl.close_session()
                        raise
                except Exception:
                    # clean up the secure channel
                    print("Close secure channel")
                    cl.close_secure_channel()
                    raise
            except Exception:
                print("Disconnect socket")
                cl.disconnect_socket()  # clean up open socket
                raise

            print("Connected")
            iloop = 0

        except:
            print("Error accessing data. iloop: ", iloop)
            time.sleep(1)
            iloop = iloop + 1


# main client and the default SRTM url
url = "opc.tcp://192.168.0.117:4841/"
client = Client(url)

# Create a figure and axes for display window
fig, ax = plt.subplots()
line1, = ax.plot([], [], lw=1)
line2, = ax.plot([], [], lw=1)
xlim = 50
ax.set_xlabel("Time")
ax.set_ylabel("Temp (C)")
ax.set_title("SRTM Temperatures")
ax.set_xlim(0, xlim)
ax.set_ylim(0, 50)

x_data = []
y_data1 = []
y_data2 = []

# Method to refresh the data in the frame
def update(frame):

    # Access the nodes on the SRTM
    # Need to test each time we access the data. The connection seems very fragile
    # FPGA temperatures
    try:
        var_FPGA_temp = client.get_node("ns=2;s=SRTM.FPGA_temp")
    except:
        init_socket(client)
        var_FPGA_temp = client.get_node("ns=2;s=SRTM.FPGA_temp")

    # F11 temperature. Unfortunately, one nee
    try:
        var_F11_tempC = client.get_node("ns=2;s=SRTM.F11_tempC")
    except:
        init_socket(client)
        var_F11_tempC = client.get_node("ns=2;s=SRTM.F11_tempC")

    xval = time.time() % xlim
    
    # Now try to get the actual data. Again, we need to test the connection.
    try:
        yval1 = var_FPGA_temp.get_value()
    except:
        init_socket(client)
        yval1 = var_FPGA_temp.get_value()

    try:
        yval2 = var_FF11_tempC.get_value()
    except:
        init_socket(client)
        yval2 = var_FF11_tempC.get_value()

    # set up the line data
    x_data.append(xval)
    y_data1.append(yval1)
    y_data2.append(yval2)
    line1.set_data(x_data, y_data1)
    line2.set_data(x_data, y_data2)

    # Start the trace back at the beginning.
    if xval >= xlim -0.5:
        x_data.clear()
        y_data1.clear()
        y_data2.clear()

    return line1,line2,

# Main routine is here
if __name__ == "__main__":

    # main routine for accessing SRTM sensor values
    logging.basicConfig(level=logging.WARN)

    # create connection to socket
    init_socket(client)

    # access SRTM variables
    var_FF11_cdrenable = client.get_node("ns=2;s=SRTM.FF11_cdrenable")
    print("FF11_cdrenable: ", var_FF11_cdrenable.get_value()) 
    var_FF11_cdrlol = client.get_node("ns=2;s=SRTM.FF11_cdrlol")
    print("FF11_cdrlol: ", var_FF11_cdrlol.get_value()) 
    var_FF11_cdrrate = client.get_node("ns=2;s=SRTM.FF11_cdrrate")
    print("FF11_cdrrate: ", var_FF11_cdrrate.get_value())
    var_FF11_fwversion = client.get_node("ns=2;s=SRTM.FF11_fwversion")
    print("FF11_fwversion: ", var_FF11_fwversion.get_value())
    var_FF11_id = client.get_node("ns=2;s=SRTM.FF11_id")
    print("FF11_id: ", var_FF11_id.get_value()) 
    var_FF11_los = client.get_node("ns=2;s=SRTM.FF11_los")
    print("FF11_los: ", var_FF11_los.get_value()) 
    var_FF11_model = client.get_node("ns=2;s=SRTM.FF11_model")
    print("FF11_model: ", var_FF11_model.get_value()) 
    var_FF11_powerfault = client.get_node("ns=2;s=SRTM.FF11_powerfault")
    print("FF11_powerfault: ", var_FF11_powerfault.get_value()) 
    var_FF11_present = client.get_node("ns=2;s=SRTM.FF11_present")
    print("FF11_present: ", var_FF11_present.get_value()) 
    var_FF11_rxpower_0 = client.get_node("ns=2;s=SRTM.FF11_rxpower_0")
    print("FF11_rxpower_0: ", var_FF11_rxpower_0.get_value()) 
    var_FF11_rxpower_1 = client.get_node("ns=2;s=SRTM.FF11_rxpower_1")
    print("FF11_rxpower_1: ", var_FF11_rxpower_1.get_value()) 
    var_FF11_rxpower_2 = client.get_node("ns=2;s=SRTM.FF11_rxpower_2")
    print("FF11_rxpower_2: ", var_FF11_rxpower_2.get_value()) 
    var_FF11_rxpower_3 = client.get_node("ns=2;s=SRTM.FF11_rxpower_3")
    print("FF11_rxpower_3: ", var_FF11_rxpower_3.get_value()) 
    var_FF11_serial = client.get_node("ns=2;s=SRTM.FF11_serial")
    print("FF11_serial: ", var_FF11_serial.get_value()) 
    var_FF11_status = client.get_node("ns=2;s=SRTM.FF11_status")
    print("FF11_status: ", var_FF11_status.get_value()) 
    var_FF11_tempC = client.get_node("ns=2;s=SRTM.FF11_tempC")
    print("FF11_tempC: ", var_FF11_tempC.get_value()) 
    var_FF11_tempfault = client.get_node("ns=2;s=SRTM.FF11_tempfault")
    print("FF11_tempfault: ", var_FF11_tempfault.get_value()) 
    var_FF11_txdisable = client.get_node("ns=2;s=SRTM.FF11_txdisable")
    print("FF11_txdisable: ", var_FF11_txdisable.get_value()) 
    var_FF11_txfault = client.get_node("ns=2;s=SRTM.FF11_txfault")
    print("FF11_txfault: ", var_FF11_txfault.get_value()) 
    var_FF11_uptime = client.get_node("ns=2;s=SRTM.FF11_uptime")
    print("FF11_uptime: ", var_FF11_uptime.get_value()) 
    var_FF11_voltfault = client.get_node("ns=2;s=SRTM.FF11_voltfault")
    print("FF11_voltfault: ", var_FF11_voltfault.get_value())

    # set up the animated window
    # interval: time between frames
    # frames: total number of frames
    ani = animation.FuncAnimation(fig, update, frames=xlim, interval=250, blit=True)
    handles = [line1, line2]
    labels = ['FPGA_temp', 'F11_tempC']
    plt.legend(handles, labels)
    plt.show()
    
    client.disconnect()
            

