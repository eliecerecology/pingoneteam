from scipy.integrate import odeint
from numpy.random import randn, rand, uniform
from time import time
import numpy as np
import pylab as pl
import lib
import os

# Define the values for num_i

num_e = 250
num_i = 50

sigma_e = 0.05
sigma_i = 0.00
g_hat_ee = 0
g_hat_ei = 0.25
g_hat_ie = 0.25
g_hat_ii = 0.25
p_ee = 0.5
p_ei = 0.5
p_ie = 0.5
p_ii = 0.5

v_rev_e = 0.0
v_rev_i = -75.0
tau_r_e = 0.5
tau_peak_e = 0.5
tau_d_e = 3.0
tau_r_i = 0.5
tau_peak_i = 0.5
tau_d_i = 9.0
t_final = 200.0
dt = 0.02

spikeThreshold = -20

# Process network parameters

i_ext_e = 1.4 * np.ones(num_e) * (1 + sigma_e * randn(num_e))

u_ee = rand(num_e, num_e)
u_ei = rand(num_e, num_i)
u_ie = rand(num_i, num_e)
u_ii = rand(num_i, num_i)
g_ee = (g_hat_ee * (u_ee < p_ee) / (num_e * p_ee)).T
g_ei = (g_hat_ei * (u_ei < p_ei) / (num_e * p_ei)).T
g_ie = (g_hat_ie * (u_ie < p_ie) / (num_i * p_ie)).T
g_ii = (g_hat_ii * (u_ii < p_ii) / (num_i * p_ii)).T

start = time()

# Loop through different values of num_e

initialVec = lib.splayState(i_ext_e, rand(num_e), lib.derivative)

v_e = initialVec[:, 0]
m_e = lib.m_e_inf(v_e)
h_e = initialVec[:, 1]
n_e = initialVec[:, 2]
q_e = np.zeros(num_e)
s_e = np.zeros(num_e)

v_i = -75.0 * np.ones(num_i)
m_i = lib.m_i_inf(v_i)
h_i = lib.h_i_inf(v_i)
n_i = lib.n_i_inf(v_i)
q_i = np.zeros(num_i)
s_i = np.zeros(num_i)

initialConditions = np.hstack((v_e, h_e, n_e, q_e, s_e,
                                v_i, h_i, n_i, q_i, s_i))
t = np.arange(0, t_final, dt)
sol = odeint(lib.derivativePopulation, initialConditions, t)

lfp = np.mean(sol[:, :num_e], axis=1)
if lfp.ndim != 1:
    lfp = np.squeeze(lfp)  # Ensure lfp is a 1D array

t_e_spikes = []
t_i_spikes = []
for i in range(num_e):
    ts_e = lib.spikeDetection(t, sol[:, i], spikeThreshold)
    t_e_spikes.append(ts_e)
index = 5 * num_e
for i in range(index, index + num_i):
    ts_i = lib.spikeDetection(t, sol[:, i], spikeThreshold)
    t_i_spikes.append(ts_i)

lib.display_time(time() - start)

lib.spikeToFile(t_e_spikes, f"t_e_spikes_{num_e}.txt")
lib.spikeToFile(t_i_spikes, f"t_i_spikes_{num_e}.txt")

# Save t and lfp to file
np.savetxt(f"lfp_{num_e}.txt", np.column_stack((t, lfp)), fmt="%18.6f")
