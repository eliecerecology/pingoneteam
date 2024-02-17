from brian2 import *
import numpy as np
import matplotlib.pyplot as plt

start_scope()

# Function to compute PLV
def compute_plv(spiketimes, duration, frequency):
    phase_vectors = np.exp(2j * np.pi * frequency * spiketimes / duration)
    mean_phase_vector = np.mean(phase_vectors)
    plv = np.abs(mean_phase_vector)
    return plv

# Define parameters
ratios = list(range(1, 9))  # Ratios of excitatory to inhibitory neurons
duration = 20 * ms
frequency = 10 * Hz  # Frequency for PLV computation

# Lists to store PLV values
plv_values_exc = []
plv_values_inh = []

# Loop through different ratios
for ratio in ratios:
    ne = 100 * ratio  # Number of excitatory neurons
    ni = 100         # Number of inhibitory neurons

    # Define equations for the excitatory population
    eqs_exc = '''
    dv/dt = (-(Ve) - (Vi) + 5) / tau : 1
    '''

    # Define equations for the inhibitory population
    eqs_inh = '''
    dv/dt = (-(Vi) - (Ve) + 3) / tau : 1
    '''

    # Create neuron groups for excitatory and inhibitory populations
    exc = NeuronGroup(ne,
                      eqs_exc,
                      threshold='v > 0.8',
                      reset='v = 0.3',
                      refractory=1*ms,
                      method='euler')

    inh = NeuronGroup(ni,
                      eqs_inh,
                      threshold='v > 0.5',
                      reset='v = -0.3',
                      refractory=1*ms,
                      method='euler')

    # Define synaptic connections
    exc_synapse = Synapses(exc, inh, 'w : 1', on_pre='v += w')
    exc_synapse.connect(p=0.2)  # Connects each excitatory neuron to 20% of inhibitory neurons
    exc_synapse.w = 'rand() * 0.2'

    inh_synapse = Synapses(inh, exc, 'w : 1', on_pre='v -= w')
    inh_synapse.connect(p=0.2)  # Connects each inhibitory neuron to 20% of excitatory neurons
    inh_synapse.w = 'rand() * 0.2'  # Initialize random weights

    # Define monitors
    spikemon_exc = SpikeMonitor(exc)
    spikemon_inh = SpikeMonitor(inh)

    # Run simulation
    run(duration)

    # Compute PLV
    plv_exc = compute_plv(spikemon_exc.t, duration, frequency)
    plv_inh = compute_plv(spikemon_inh.t, duration, frequency)

    # Append PLV values to the lists
    plv_values_exc.append(plv_exc)
    plv_values_inh.append(plv_inh)

    # Print PLV for the current iteration
    print(f"Ratio: {ratio}, Excitatory PLV: {plv_exc}, Inhibitory PLV: {plv_inh}")

# Plot PLV values
plt.plot(ratios, plv_values_exc, label='Excitatory')
plt.plot(ratios, plv_values_inh, label='Inhibitory')
plt.xlabel('Ratio of Excitatory to Inhibitory Neurons')
plt.ylabel('PLV Value')
plt.title('PLV vs. Ratio')
plt.legend()
plt.show()
