# from pynput import mouse
# import time

# def on_move(x, y):
#     print(f'Mouse moved to ({x}, {y})')

# # Funkcja do uzyskania pozycji kursora po 5 sekundach
# def get_mouse_position():
#     print("Place the cursor at the desired location within 5 seconds...")
#     time.sleep(5)
#     with mouse.Listener(on_move=on_move) as listener:
#         listener.join()
#     print("Mouse position captured")

# get_mouse_position()

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import time
import mss

keyboard = KeyboardController()
mouse = MouseController()

def clear_field():
    time.sleep(0.5)
    for i in range(100):
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)
    time.sleep(0.5)

# Function to get the simulation result from the text area
def get_simulation_result(protocol, block_size, speed, delay):
    time.sleep(1)  # Czekaj chwilę, aby wynik został wyświetlony
    # Zrób zrzut ekranu obszaru wyników
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": 640, "height": 520}  # Dostosuj region do obszaru wyników
        screenshot = sct.grab(monitor)
        filename = f'result_{protocol}_{block_size}_{speed}_{delay}.png'
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=filename)
    return filename

# Function to simulate entering data and running the simulation
def run_simulation(protocol, block_size, speed, delay, result_file):
    # Kliknij na pole wyboru protokołu
    mouse.position = (173, 134)  # Koordynaty muszą być dostosowane
    mouse.click(Button.left, 1)
    time.sleep(0.5)
    keyboard.type(protocol)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    
    # Ustaw długość bloku
    mouse.position = (117, 216)
    mouse.click(Button.left, 1)
    time.sleep(0.5)
    clear_field()
    keyboard.type(str(block_size))
    
    # Ustaw szybkość transmisji
    mouse.position = (97, 287)
    mouse.click(Button.left, 1)
    time.sleep(0.5)
    clear_field()
    keyboard.type(str(speed))
    
    # Ustaw opóźnienie
    mouse.position = (85, 357)
    mouse.click(Button.left, 1)
    time.sleep(0.5)
    clear_field()
    keyboard.type(str(delay))
    
    # Kliknij przycisk symulacji
    mouse.position = (252, 403)
    mouse.click(Button.left, 1)

    # Czekaj na wynik (czekaj odpowiednią ilość czasu, aby symulacja się zakończyła)
    time.sleep(15)  # Dostosuj czas w zależności od czasu trwania symulacji

    # Odczytaj wynik symulacji
    screenshot_filename = get_simulation_result(protocol, block_size, speed, delay)
    
    # Zapisz informacje o symulacji i pliku zrzutu ekranu do pliku
    with open(result_file, 'a') as f:
        f.write(f"Protocol: {protocol}, Block Size: {block_size}, Speed: {speed}, Delay: {delay}\n")
        f.write(f"Screenshot: {screenshot_filename}\n\n")

# Przykładowe użycie funkcji
protocols = ['STOP-AND-WAIT', 'GO-BACK-N', 'SELECTIVE REPEAT']
block_sizes = [500, 8000]
speeds = [100, 1000, 10000]
delays = [1, 10, 100]

result_file = 'simulation_results.txt'
for protocol in protocols:
    for block_size in block_sizes:
        for speed in speeds:
            for delay in delays:
                run_simulation(protocol, block_size, speed, delay, result_file)

print("Simulation completed and results saved to", result_file)
