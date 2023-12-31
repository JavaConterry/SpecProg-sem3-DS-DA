import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons, Button
import numpy as np
from scipy.signal import iirfilter, lfilter



def harmonic_with_noise(amplitude, frequency, phase, noise, show_noise):
    harmonic = amplitude * np.sin(frequency * time + phase)
    if(show_noise):
        harmonic+=noise

    return harmonic

init_amplitude = 1.0
init_frequency = 0.1
init_phase = 0
noise_mean = 0
noise_covariance = 0.1
show_noise = False
time = np.arange(0, 360)
noise = np.random.normal(noise_mean, noise_covariance, size=len(time))



fig, axs = plt.subplots(nrows=1, ncols=2)
axs[0].set_title('Harmonic Signal')
axs[1].set_title('Filtered Harmonic Signal')
plt.subplots_adjust(bottom=0.50)

harmonic = harmonic_with_noise(init_amplitude, init_frequency, init_phase, noise, show_noise)
line, = axs[0].plot(time, harmonic, color='green')

filtered_harmonic = np.copy(harmonic)
line2, = axs[1].plot(time, filtered_harmonic, color='red')

ax_amplitude = plt.axes([0.2, 0.25, 0.65, 0.03])
amplitude_slider = Slider(ax_amplitude, 'Amplitude', 0.1, 5.0)

ax_frequency = plt.axes([0.2, 0.20, 0.65, 0.03])
frequency_slider = Slider(ax_frequency, 'Frequency', 0.1, 5.0)

ax_phase = plt.axes([0.2, 0.15, 0.65, 0.03])
phase_slider = Slider(ax_phase, 'Phase', 1, 100)


ax_noise_mean = plt.axes([0.2, 0.1, 0.65, 0.03])
noise_mean_slider = Slider(ax_noise_mean, 'Noise mean', 0.1, 5.0)


ax_noise_covariance = plt.axes([0.2, 0.05, 0.65, 0.03])
noise_covariance_slider = Slider(ax_noise_covariance, 'Noise Covariance', 0.1, 5.0)

ax_show_noise = plt.axes([0.2, 0.01, 0.25, 0.04])
show_noise_checkbox = CheckButtons(ax_show_noise, ['Show noise'])

reset_button = Button(plt.axes([0.53, 0.0, 0.3, 0.04]), "Reset")
# iirf_button = Button(plt.axes([0.2, 0.04, 0.3, 0.04]), "IIR filter")

def update_graph(val):
    # global show_noise
    global harmonic
    amplitude = amplitude_slider.val
    frequency = frequency_slider.val
    phase = phase_slider.val
    show_noise = show_noise_checkbox.get_status()[0]
    harmonic = harmonic_with_noise(amplitude, frequency, phase, noise, show_noise)
    global filtered_harmonic                            #added to update the filtered graph everytime anything has been changed
    b, a = iirfilter(5, 0.5, btype='low')               #
    filtered_harmonic = lfilter(b, a, harmonic)         #
    line2.set_ydata(filtered_harmonic)                  #
    line.set_ydata(harmonic)
    fig.canvas.draw_idle()

def reset_init_vals(val):
    amplitude_slider.reset()
    frequency_slider.reset()
    phase_slider.reset()
    show_noise_checkbox.set_active(False)

def update_chbx_noise(val):
    global show_noise
    show_noise = not show_noise

def update_noise_chbx_and_graph(val):
    update_chbx_noise(val)
    update_graph(val)
    
def calculate_noise(noise_mean, noise_covariance):
    noise = np.random.normal(noise_mean, noise_covariance, size=len(time))
    return noise

def recalculate_and_update_noise_and_graph(val):
    global noise
    noise = calculate_noise(noise_mean_slider.val, noise_covariance_slider.val)
    update_graph(val)
        

amplitude_slider.on_changed(update_graph)
frequency_slider.on_changed(update_graph)
phase_slider.on_changed(update_graph)
noise_mean_slider.on_changed(recalculate_and_update_noise_and_graph)
noise_covariance_slider.on_changed(recalculate_and_update_noise_and_graph)
show_noise_checkbox.on_clicked(update_noise_chbx_and_graph)
reset_button.on_clicked(reset_init_vals)

# Display the plot
plt.legend()
plt.show()