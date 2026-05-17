"""Generate Root Level Diagram — Final Professional Version."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from draw_light import *

fig, ax = setup_fig(32, 14)
ax.set_xlim(-2, 42)
ax.set_ylim(-1, 14)

# ====== TITLES (fontweight, NOT \textbf) ======
ax.text(20, 13.5, 'PV GHI Control System', fontsize=28, color=TEXT_W,
        ha='center', fontweight='bold')
ax.text(20, 12.7, 'Two-Tier Architecture  |  Physical Plant vs. Advanced Control',
        fontsize=14, color=TEXT_G, ha='center')

# ====== SECTIONS ======
draw_section(ax, -1.5, 7.5, 42.5, 4.5, 'PHYSICAL PLANT & ACTUATION', '#059669')
draw_section(ax, 7.5, 1.5, 17, 4.5, 'ADVANCED CONTROL (AI & MPC)', '#2563EB')

C = COLORS

# ====== TOP TIER: PHYSICAL PLANT (Y ~ 9.5) ======
# 1. Input time-series — clean labels, no underscores
ghi_labels = ['GHI Day 1', 'GHI Day 2', 'GHI Day 3']
for i, lb in enumerate(ghi_labels):
    draw_small_block(ax, -0.5, 11 - i*0.6, 2.5, 0.4, lb, C['fw'], C['fw_bg'], gid=f'block_ghi_{i}')

tmp_labels = ['Temp Day 1', 'Temp Day 2', 'Temp Day 3']
for i, lb in enumerate(tmp_labels):
    draw_small_block(ax, -0.5, 9 - i*0.6, 2.5, 0.4, lb, C['fw'], C['fw_bg'], gid=f'block_tmp_{i}')

# 2. Multiport Switches
draw_block(ax, 4, 10, 1.5, 1.5, 'Mux 1', C['mux'], C['mux_bg'], fontsize=11, gid='block_mux_1')
draw_block(ax, 4, 8, 1.5, 1.5, 'Mux 2', C['mux'], C['mux_bg'], fontsize=11, gid='block_mux_2')

# 3. Power & Actuation chain — clean block names
draw_block(ax, 8, 8.5, 3, 2, 'PV Physics', C['pv'], C['pv_bg'],
           icon=r'$f_{\mathrm{PV}}(x)$', fontsize=12, sublabel='Solar Power Model', gid='block_pv')
draw_block(ax, 14, 8.5, 3, 2, 'FOPID', C['fopid'], C['fopid_bg'],
           icon=r'$PI^{\lambda}D^{\mu}$', fontsize=12, sublabel='Fractional PID', gid='block_fopid')
draw_block(ax, 20, 8.5, 2.5, 2, 'VFD', C['vfd'], C['vfd_bg'],
           icon=r'$\sim$', fontsize=16, sublabel='Inverter', gid='block_vfd')
draw_block(ax, 25.5, 8.5, 3, 2, 'Pump Drive', C['pump'], C['pump_bg'],
           icon=r'$\mathcal{M}$', fontsize=14, sublabel='Motor Model', gid='block_pump')

# 4. Water System
draw_small_block(ax, 30.5, 9.2, 1.5, 0.6, 'Gain', C['gain'], C['gain_bg'], gid='block_gain_root')
draw_block(ax, 34, 8.5, 3, 2, 'Water Tank', C['tank'], C['tank_bg'],
           icon='', fontsize=12, sublabel='Mass Balance', gid='block_tank')
draw_block(ax, 39, 8.8, 2, 1.4, 'Demand', C['demand'], C['demand_bg'],
           icon=r'$f_Q(t)$', fontsize=12, gid='block_demand')


# ====== BOTTOM TIER: CONTROL & AI (Y ~ 3.5) ======
draw_small_block(ax, 3, 3.5, 1.5, 0.5, 'Day = 2', C['const'], C['const_bg'], gid='block_day_root')
draw_circle(ax, 11.5, 2.5, 0.4, r'$t$', C['clock'], fontsize=14, gid='block_time_root')

draw_block(ax, 8, 2.5, 3, 2, 'AI Block', C['ai'], C['ai_bg'],
           icon=r'$\mathcal{NN}$', fontsize=12, sublabel='Neural Predictor', gid='block_ai')
draw_block(ax, 14, 2.5, 3, 2, 'MPC Manager', C['mpc_mgr'], C['mpc_mgr_bg'],
           icon=r'$f_{\mathrm{ref}}(x)$', fontsize=12, sublabel='Reference Gen', gid='block_mpc_mgr')
draw_block(ax, 20, 2.5, 3, 2, 'MPC Controller', C['mpc'], C['mpc_bg'],
           icon=r'$\mathbf{MPC}$', fontsize=12, gid='block_mpc_ctrl')

# Feedback Delay
draw_small_block(ax, 30.5, 3.2, 1.5, 0.6, r'$z^{-1}$', C['delay'], C['clock_bg'], fontsize=12, gid='block_delay_root')

# ====== ORTHOGONAL ROUTING — PLANT TIER ======
# Inputs -> Mux
draw_ortho_arrow(ax, [(2, 11.2), (3.3, 11.2), (3.3, 11), (4, 11)], C['fw'], gid='path_in_1')
draw_ortho_arrow(ax, [(2, 10.6), (4, 10.6)], C['fw'], gid='path_in_2')
draw_ortho_arrow(ax, [(2, 10.0), (3.3, 10.0), (3.3, 10.2), (4, 10.2)], C['fw'], gid='path_in_3')

draw_ortho_arrow(ax, [(2, 9.2), (3.3, 9.2), (3.3, 9), (4, 9)], C['fw'], gid='path_in_4')
draw_ortho_arrow(ax, [(2, 8.6), (4, 8.6)], C['fw'], gid='path_in_5')
draw_ortho_arrow(ax, [(2, 8.0), (3.3, 8.0), (3.3, 8.2), (4, 8.2)], C['fw'], gid='path_in_6')

# Mux -> PV
draw_ortho_arrow(ax, [(5.5, 10.75), (6.5, 10.75), (6.5, 10), (8, 10)],
                 C['pv'], label='GHI', label_pos=(6.5, 11.2), gid='path_ghi_mux')
draw_ortho_arrow(ax, [(5.5, 8.75), (6.5, 8.75), (6.5, 9), (8, 9)],
                 C['pv'], label='Temp', label_pos=(6.5, 8.2), gid='path_temp_mux')

# Main power line (left to right)
draw_ortho_arrow(ax, [(11, 9.5), (14, 9.5)],
                 C['pv'], label=r'$P_{\mathrm{pv}}$', gid='path_pv')
draw_ortho_arrow(ax, [(17, 9.5), (20, 9.5)],
                 C['fopid'], label=r'$P_{\mathrm{ctrl}}$', gid='path_fopid')
draw_ortho_arrow(ax, [(22.5, 10), (25.5, 10)],
                 C['vfd'], label=r'$P_{\mathrm{pump}}$', gid='path_vfd_1')
draw_ortho_arrow(ax, [(22.5, 9), (25.5, 9)],
                 C['vfd'], label=r'$F_{\mathrm{cmd}}$', gid='path_vfd_2')
draw_ortho_arrow(ax, [(28.5, 9.5), (30.5, 9.5)],
                 C['pump'], label=r'$Q_{\mathrm{raw}}$', gid='path_pump')
draw_ortho_arrow(ax, [(32, 9.5), (34, 9.5)],
                 C['gain'], label=r'$Q_{\mathrm{in}}$', gid='path_gain')
draw_ortho_arrow(ax, [(37, 9.5), (39, 9.5)],
                 C['tank'], label=r'$H(t)$', gid='path_tank_out')

# Demand -> Tank
draw_ortho_arrow(ax, [(40, 8.8), (40, 8), (35.5, 8), (35.5, 8.5)],
                 C['demand'], label=r'$Q_{\mathrm{out}}$', label_pos=(37.7, 8), gid='path_demand')


# ====== ORTHOGONAL ROUTING — CONTROL TIER ======
# Day constant -> Mux selectors (vertical bus at X=5.5)
draw_ortho_arrow(ax, [(4.5, 3.75), (5.5, 3.75), (5.5, 12.3), (4.75, 12.3), (4.75, 11.5)], C['const'], gid='path_day_1')
draw_ortho_arrow(ax, [(4.75, 12.3), (4.75, 9.5)], C['const'], gid='path_day_2')
# Day constant -> AI
draw_ortho_arrow(ax, [(4.5, 3.75), (8, 3.75)], C['const'], label='Day', label_pos=(6.2, 4.2), gid='path_day_3')

# AI -> MPC Manager
draw_ortho_arrow(ax, [(11, 4), (14, 4)],
                 C['ai'], label=r'$\mathrm{GHI}_W$', gid='path_ai_1')
draw_ortho_arrow(ax, [(11, 3), (14, 3)],
                 C['ai'], label=r'$\vec{V}_{\mathrm{fut}}$', gid='path_ai_2')
# Clock -> MPC Manager
draw_ortho_arrow(ax, [(11.9, 2.5), (14, 2.5)],
                 C['clock'], label=r'$t$', gid='path_clock')

# MPC Manager -> MPC Controller
draw_ortho_arrow(ax, [(17, 3.5), (20, 3.5)],
                 C['mpc_mgr'], label=r'$Q_{\mathrm{ref}}$', gid='path_mgr_1')

# MPC Manager feed-forward -> VFD (vertical bus at X=18.5)
draw_ortho_arrow(ax, [(18.5, 3.5), (18.5, 7.5), (21.25, 7.5), (21.25, 8.5)],
                 C['mpc_mgr'], label=r'$Q_{\mathrm{ref}}$ FF', label_pos=(18.5, 5.5), gid='path_mgr_2')


# ====== CROSS-TIER ROUTING ======
# MPC Controller -> FOPID (command bus at Y=6.5)
draw_ortho_arrow(ax, [(23, 3.5), (24.2, 3.5), (24.2, 6.5), (15.5, 6.5), (15.5, 8.5)],
                 C['mpc'], label=r'$u_{\mathrm{cmd}}$', label_pos=(19.5, 6.5), gid='path_mpc_cmd')

# Gain -> Delay -> MPC (flow feedback)
draw_ortho_arrow(ax, [(31.25, 9.2), (31.25, 3.8)], C['gain'], gid='path_fb_flow_1')
draw_ortho_arrow(ax, [(30.5, 3.5), (23, 3.5)],
                 C['delay'], label=r'$m_o$', label_pos=(26.5, 3.5), style='<-', gid='path_fb_flow_2')

# Tank Level -> MPC Manager (global feedback bus at Y=0.5)
draw_ortho_arrow(ax, [(38, 9.5), (38, 0.5), (15.5, 0.5), (15.5, 2.5)],
                 C['tank'], label=r'$H(t)$ Feedback', label_pos=(26, 0.5), gid='path_fb_tank')

save_fig(fig, r'c:\Users\Mohammed26\Desktop\مخطط سيموليشن\01_Root_Level_Final.png', dpi=300)
save_fig(fig, r'c:\Users\Mohammed26\Desktop\مخطط سيموليشن\01_Root_Level_Final.svg', dpi=300)
save_fig(fig, r'c:\Users\Mohammed26\Desktop\مخطط سيموليشن\01_Root_Level_Final.pdf', dpi=600)
