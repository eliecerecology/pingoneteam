from brian2 import *
start_scope()

# Define parameters
ratios = list(range(1, 9))  # Ratios of excitatory to inhibitory neurons

tau = 5*ms
Ve = 50   # Reversal potential for excitatory synapse
Vi = -50   # Reversal potential for inhibitory synapse

# Loop through different ratios
for ratio in ratios:
    print(ratio)
    ne = 100 * ratio  # Number of excitatory neurons
    ni = 100         # Number of inhibitory neurons

    # Define equations for the excitatory population
    eqs_exc = '''
    dv/dt = (-Ve - Vi + 5) / tau : 1
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

    # Define synaptic connections
    exc_synapse = Synapses(exc, inh, 'w : 1', on_pre='v += w')
    exc_synapse.connect(p=0.2)  # Connects each excitatory neuron to 20% of inhibitory neurons
    exc_synapse.w = 'rand() * 0.2'

    inh_synapse = Synapses(inh, exc, 'w : 1', on_pre='v -= w')
    inh_synapse.connect(p=0.2)  # Connects each inhibitory neuron to 20% of excitatory neurons
    inh_synapse.w = 'rand() * 0.2'  # Initialize random weights

    # Define monitors
    statemon_exc = StateMonitor(exc, 'v', record=0)
    spikemon_exc = SpikeMonitor(exc)

    statemon_inh = StateMonitor(inh, 'v', record=0)
    spikemon_inh = SpikeMonitor(inh)

    # Run simulation
    run(20*ms)

    # Plot results
    subplot(3, 1, 1)
    plot(statemon_exc.t/ms, statemon_exc.v[0], label=f'{ne} Excitatory Neurons')
    xlabel('Time (ms)')
    ylabel('v')
    legend()

    subplot(3, 1, 2)
    plot(statemon_inh.t/ms, statemon_inh.v[0], label=f'{ni} Inhibitory Neurons')
    xlabel('Time (ms)')
    ylabel('v')
    legend()

    subplot(3, 1, 3)
    plot(spikemon_exc.t/ms, spikemon_exc.i, '.r', label=f'{ne} Excitatory Neurons')
    plot(spikemon_inh.t/ms, spikemon_inh.i, '.k', label=f'{ni} Inhibitory Neurons')
    xlabel('Time (ms)')
    ylabel('Neuron Index')
    legend()

    show()
