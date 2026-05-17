"""Generate Root Level Diagram - Vertical Layout for IEEE Papers."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from draw_light import *

fig, ax = setup_fig(24, 34)
ax.set_xlim(-2, 22)
ax.set_ylim(-2, 32)

# ====== TITLES ======
ax.text(10, 30.5, 'PV GHI Control System - Vertical Layout', fontsize=24, color=TEXT_W,
        ha='center', fontweight='bold')
ax.text(10, 29.5, 'Two-Tier Architecture | Physical Plant vs. Advanced Control',
        fontsize=14, color=TEXT_G, ha='center')

C = COLORS

# ====== SECTIONS ======
draw_section(ax, -1, 28, 9, 21.5, 'INPUTS', '#059669')
draw_section(ax, 10, 28, 21, 15, 'CONTROL & AI', '#2563EB')
draw_section(ax, -1, 13, 21, -1, 'PHYSICAL PLANT', '#D97706')


# ====== TIER 1: INPUTS ======
ghi_labels = ['GHI Day 1', 'GHI Day 2', 'GHI Day 3']
for i, lb in enumerate(ghi_labels):
    draw_small_block(ax, 0, 26.5 - i*1.2, 2.5, 0.6, lb, C['fw'], C['fw_bg'], gid=f'v_block_ghi_{i}')

tmp_labels = ['Temp Day 1', 'Temp Day 2', 'Temp Day 3']
for i, lb in enumerate(tmp_labels):
    draw_small_block(ax, 5, 26.5 - i*1.2, 2.5, 0.6, lb, C['fw'], C['fw_bg'], gid=f'v_block_tmp_{i}')

draw_block(ax, 0.5, 22.5, 1.5, 1.5, 'Mux 1', C['mux'], C['mux_bg'], fontsize=11, gid='v_block_mux_1')
draw_block(ax, 5.5, 22.5, 1.5, 1.5, 'Mux 2', C['mux'], C['mux_bg'], fontsize=11, gid='v_block_mux_2')


# ====== TIER 2: CONTROL & AI ======
draw_small_block(ax, 11, 26.5, 1.5, 0.6, 'Day = 2', C['const'], C['const_bg'], gid='v_block_day_root')
draw_circle(ax, 18, 26.8, 0.6, r'$t$', C['clock'], fontsize=14, gid='v_block_time_root')

draw_block(ax, 10.5, 22.5, 3, 2, 'AI Block', C['ai'], C['ai_bg'],
           icon=r'$\mathcal{NN}$', fontsize=12, sublabel='Predictor', gid='v_block_ai')
draw_block(ax, 16.5, 22.5, 3, 2, 'MPC Mgr', C['mpc_mgr'], C['mpc_mgr_bg'],
           icon=r'$f_{\mathrm{ref}}$', fontsize=12, gid='v_block_mpc_mgr')
draw_block(ax, 13, 17, 3.5, 2, 'MPC Controller', C['mpc'], C['mpc_bg'],
           icon=r'$\mathbf{MPC}$', fontsize=12, gid='v_block_mpc_ctrl')

# ====== TIER 3: PHYSICAL PLANT ======
draw_block(ax, 0, 9, 3, 2, 'PV Physics', C['pv'], C['pv_bg'],
           icon=r'$f_{\mathrm{PV}}(x)$', fontsize=12, gid='v_block_pv')
draw_block(ax, 5.5, 9, 3, 2, 'FOPID', C['fopid'], C['fopid_bg'],
           icon=r'$PI^{\lambda}D^{\mu}$', fontsize=12, gid='v_block_fopid')
draw_block(ax, 11, 9, 2.5, 2, 'VFD', C['vfd'], C['vfd_bg'],
           icon=r'$\sim$', fontsize=16, gid='v_block_vfd')
draw_block(ax, 16.5, 9, 3, 2, 'Pump Drive', C['pump'], C['pump_bg'],
           icon=r'$\mathcal{M}$', fontsize=14, gid='v_block_pump')

draw_small_block(ax, 17.5, 5, 1.5, 0.6, 'Gain', C['gain'], C['gain_bg'], gid='v_block_gain_root')
draw_block(ax, 10.5, 4, 3, 2, 'Water Tank', C['tank'], C['tank_bg'],
           icon='', fontsize=12, sublabel='Mass Balance', gid='v_block_tank')
draw_block(ax, 4, 4, 2, 1.4, 'Demand', C['demand'], C['demand_bg'],
           icon=r'$f_Q(t)$', fontsize=12, gid='v_block_demand')

draw_small_block(ax, 18.5, 17.5, 1.5, 0.6, r'$z^{-1}$', C['delay'], C['clock_bg'], fontsize=12, gid='v_block_delay_root')

# ====== ROUTING ======
# Inputs to Mux
draw_ortho_arrow(ax, [(1.25, 26.5), (1.25, 24)], C['fw'], gid='v_path_in_1')
draw_ortho_arrow(ax, [(6.25, 26.5), (6.25, 24)], C['fw'], gid='v_path_in_2')

# Mux to PV
draw_ortho_arrow(ax, [(1.25, 22.5), (1.25, 11)], C['pv'], label='GHI', gid='v_path_ghi_mux')
draw_ortho_arrow(ax, [(6.25, 22.5), (6.25, 11), (2, 11), (2, 11)], C['pv'], label='Temp', gid='v_path_temp_mux')

# Power Chain
draw_ortho_arrow(ax, [(3, 10), (5.5, 10)], C['pv'], label=r'$P_{\mathrm{pv}}$', gid='v_path_pv')
draw_ortho_arrow(ax, [(8.5, 10), (11, 10)], C['fopid'], label=r'$P_{\mathrm{ctrl}}$', gid='v_path_fopid')
draw_ortho_arrow(ax, [(13.5, 10), (16.5, 10)], C['vfd'], label=r'$P_{\mathrm{pump}}$', gid='v_path_pump_in')

# Water Chain
draw_ortho_arrow(ax, [(18, 9), (18, 5.6)], C['pump'], label=r'$Q_{\mathrm{raw}}$', gid='v_path_pump')
draw_ortho_arrow(ax, [(17.5, 5.3), (13.5, 5.3)], C['gain'], label=r'$Q_{\mathrm{in}}$', gid='v_path_gain')
draw_ortho_arrow(ax, [(6, 4.7), (10.5, 4.7)], C['demand'], label=r'$Q_{\mathrm{out}}$', gid='v_path_demand')

# Control Connections
draw_ortho_arrow(ax, [(11.75, 26.5), (11.75, 24.5)], C['const'], gid='v_path_day')
draw_ortho_arrow(ax, [(13.5, 23.5), (16.5, 23.5)], C['ai'], label=r'$\mathrm{GHI}_W$', gid='v_path_ai_1')
draw_ortho_arrow(ax, [(18, 26.2), (18, 24.5)], C['clock'], gid='v_path_clock')
draw_ortho_arrow(ax, [(18, 22.5), (18, 18), (16.5, 18)], C['mpc_mgr'], label=r'$Q_{\mathrm{ref}}$', gid='v_path_mgr')

# Cross-tier
draw_ortho_arrow(ax, [(14.75, 17), (14.75, 13), (7, 13), (7, 11)], C['mpc'], label=r'$u_{\mathrm{cmd}}$', gid='v_path_mpc_cmd')
draw_ortho_arrow(ax, [(10.5, 5), (10.5, 1), (21, 1), (21, 24), (19.5, 24)], C['tank'], label=r'$H(t)$', gid='v_path_fb_tank')
draw_ortho_arrow(ax, [(18, 11), (19.25, 11), (19.25, 17.5)], C['pump'], gid='v_path_fb_flow')
draw_ortho_arrow(ax, [(18.5, 17.8), (16.5, 17.8)], C['delay'], gid='v_path_fb_flow_in')

# Save relative paths
save_fig(fig, './01_Root_Level_Vertical_Final.png', dpi=300)
save_fig(fig, './01_Root_Level_Vertical_Final.svg', dpi=300)
save_fig(fig, './01_Root_Level_Vertical_Final.pdf', dpi=600)
