from brian2 import *
start_scope()

# Define parameters
ratios = list(range(1, 9))  # Ratios of excitatory to inhibitory neurons

tau = 10*ms  # Increase synaptic time constant
Ve = 65     # Adjust reversal potential for excitatory synapse
Vi = -65    # Adjust reversal potential for inhibitory synapse

# Define lists to store monitor data
statemon_exc_list = []
spikemon_exc_list = []
statemon_inh_list = []
spikemon_inh_list = []

# Function to initialize membrane potentials randomly
def initialize_membrane_potentials(group, low, high):
    group.v = 'rand() * (high - low) + low'

# Loop through different ratios
for ratio in ratios:
    print(ratio)
    ne = 100 * ratio  # Number of excitatory neurons
    ni = 100         # Number of inhibitory neurons

    # Define equations for the excitatory population
    eqs_exc = '''
    dv/dt = (-Ve - Vi + 8) / tau : 1
    '''

    
    # Define equations for the inhibitory population
    eqs_inh = '''
    dv/dt = (-Vi - Ve + 3) / tau : 1
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

    # Initialize membrane potentials randomly
    initialize_membrane_potentials(exc, 0, 1)
    initialize_membrane_potentials(inh, -1, 0)

    # Define synaptic connections
    exc_synapse = Synapses(exc, inh, 'w : 1', on_pre='v += w')
    exc_synapse.connect(p=0.1)  # Decrease connectivity to promote desynchronization
    exc_synapse.w = 'rand() * 0.1'  # Decrease synaptic weights to promote desynchronization

    inh_synapse = Synapses(inh, exc, 'w : 1', on_pre='v -= w')
    inh_synapse.connect(p=0.1)  # Decrease connectivity to promote desynchronization
    inh_synapse.w = 'rand() * 0.1'  # Decrease synaptic weights to promote desynchronization

    # Define monitors
    statemon_exc = StateMonitor(exc, 'v', record=0)
    spikemon_exc = SpikeMonitor(exc)

    statemon_inh = StateMonitor(inh, 'v', record=0)
    spikemon_inh = SpikeMonitor(inh)
    
    # Store monitors for later use
    statemon_exc_list.append(statemon_exc)
    spikemon_exc_list.append(spikemon_exc)
    statemon_inh_list.append(statemon_inh)
    spikemon_inh_list.append(spikemon_inh)

    # Run simulation
    run(20*ms)

# Plot results
for i, ratio in enumerate(ratios):
    ne = 100 * ratio
    ni = 100

    statemon_exc = statemon_exc_list[i]
    spikemon_exc = spikemon_exc_list[i]
    statemon_inh = statemon_inh_list[i]
    spikemon_inh = spikemon_inh_list[i]

    subplot(3, len(ratios), i+1)
    plot(statemon_exc.t/ms, statemon_exc.v[0], label=f'{ne} Excitatory Neurons')
    xlabel('Time (ms)')
    ylabel('v')
    legend()

    subplot(3, len(ratios), len(ratios) + i+1)
    plot(statemon_inh.t/ms, statemon_inh.v[0], label=f'{ni} Inhibitory Neurons')
    xlabel('Time (ms)')
    ylabel('v')
    legend()

    subplot(3, len(ratios), 2*len(ratios) + i+1)
    plot(spikemon_exc.t/ms, spikemon_exc.i, '.r', label=f'{ne} Excitatory Neurons')
    plot(spikemon_inh.t/ms, spikemon_inh.i, '.k', label=f'{ni} Inhibitory Neurons')
    xlabel('Time (ms)')
    ylabel('Neuron Index')
    legend()

show()
