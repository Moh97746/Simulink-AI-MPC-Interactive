"""Generate AI_BLOCK + Water_Tank — Final Professional Version."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from draw_light import *

# ============================================================
#                        AI BLOCK
# ============================================================
fig, ax = setup_fig(24, 12)
ax.set_xlim(-1, 23)
ax.set_ylim(-1, 11)

ax.text(11, 10, 'AI Block  —  Neural Network GHI Prediction Subsystem',
        fontsize=22, color=COLORS['ai'], ha='center', fontweight='bold')
ax.text(11, 9.3, r'Inputs: Day Selector  |  Outputs: $\mathrm{GHI}_W$, $\vec{V}_{\mathrm{fut}}$',
        fontsize=12, color=TEXT_G, ha='center')

# Sections
draw_section(ax, -0.5, 4, 3.5, 4.5, 'DATA', COLORS['fw'])
draw_section(ax, 3.5, 1, 3.5, 7.5, 'SELECTION', COLORS['mux'])
draw_section(ax, 7.5, 3.5, 7, 5, 'PREPROCESSING', '#0E7490')
draw_section(ax, 15, 3, 6, 5.5, 'NEURAL NETWORK', COLORS['ai'])

# Inputs (X=0) — clean labels
draw_small_block(ax, 0, 7.5, 2, 0.6, 'Day Select', COLORS['fw'], COLORS['fw_bg'], gid='ai_day')
for i, lb in enumerate(['Future Day 1', 'Future Day 2', 'Future Day 3']):
    draw_small_block(ax, 0, 6.5 - i*0.8, 2, 0.5, lb, COLORS['fw'], COLORS['fw_bg'], fontsize=9, gid=f'ai_ghi_fut_{i}')
for i, lb in enumerate(['History 1', 'History 2', 'History 3']):
    draw_small_block(ax, 1, 3 - i*0.8, 1.5, 0.5, lb, COLORS['const'], COLORS['const_bg'], fontsize=9, gid=f'ai_hist_{i}')

# Muxes (X=4.5)
draw_block(ax, 4.5, 5, 2, 3, 'Mux 1', COLORS['mux'], COLORS['mux_bg'], fontsize=11, gid='ai_mux1')
draw_block(ax, 4.5, 1.5, 2, 3, 'Mux 2', COLORS['mux'], COLORS['mux_bg'], fontsize=11, gid='ai_mux2')

# Preprocessing (X=8 -> 14)
draw_block(ax, 8, 5, 1, 3, 'DEMUX\n1 : 4', '#64748B', '#F1F5F9', fontsize=10, gid='ai_demux')
draw_block(ax, 10.5, 5, 1, 3, 'MUX\n4 : 1', '#64748B', '#F1F5F9', fontsize=10, gid='ai_mux_41')
draw_small_block(ax, 12.5, 6.2, 1.5, 0.6, r"$\mathbf{X}^T$", '#0E7490', '#ECFEFF', fontsize=14, gid='ai_transpose')
draw_circle(ax, 13.5, 4, 0.4, r'$t$', COLORS['clock'], fontsize=14, gid='ai_clock')

# NN (X=16)
draw_block(ax, 16, 4, 3.5, 3.5, 'MATLAB\nFunction', COLORS['ai'], COLORS['ai_bg'],
           icon=r'$\mathcal{NN}$', fontsize=14, sublabel='PI-HybridNet', gid='ai_nn')

# Outputs (X=21)
draw_small_block(ax, 21, 6.5, 1.8, 0.6, r'$\mathrm{GHI}_{\mathrm{pred}}$', '#10B981', '#D1FAE5', gid='ai_out_ghi')
draw_small_block(ax, 21, 5, 1.8, 0.6, r'$\vec{V}_{\mathrm{fut}}$', '#10B981', '#D1FAE5', gid='ai_out_v')

# ====== Routing ======
draw_ortho_arrow(ax, [(2, 7.8), (3.5, 7.8), (3.5, 7.5), (4.5, 7.5)], COLORS['fw'], label='Day', gid='ai_path_1')
draw_ortho_arrow(ax, [(3.5, 7.5), (3.5, 4), (4.5, 4)], COLORS['fw'], gid='ai_path_2')
draw_ortho_arrow(ax, [(2, 6.75), (4.5, 6.75)], COLORS['fw'], gid='ai_path_3')
draw_ortho_arrow(ax, [(2, 5.95), (4.5, 5.95)], COLORS['fw'], gid='ai_path_4')
draw_ortho_arrow(ax, [(2, 5.15), (4.5, 5.15)], COLORS['fw'], gid='ai_path_5')
draw_ortho_arrow(ax, [(2.5, 3.25), (4.5, 3.25)], COLORS['const'], gid='ai_path_6')
draw_ortho_arrow(ax, [(2.5, 2.45), (4.5, 2.45)], COLORS['const'], gid='ai_path_7')
draw_ortho_arrow(ax, [(2.5, 1.65), (4.5, 1.65)], COLORS['const'], gid='ai_path_8')

draw_ortho_arrow(ax, [(6.5, 6.5), (8, 6.5)], COLORS['mux'], gid='ai_path_9')
for idx, yy in enumerate([5.5, 6.1, 6.7, 7.3]):
    draw_ortho_arrow(ax, [(9, yy), (10.5, yy)], '#64748B', gid=f'ai_path_10_{idx}')

draw_ortho_arrow(ax, [(11.5, 6.5), (12.5, 6.5)], '#0E7490', gid='ai_path_11')
draw_ortho_arrow(ax, [(14, 6.5), (16, 6.5)], '#0E7490',
                 label=r'$\mathrm{Row}_{\mathrm{cur}}$', gid='ai_path_12')

draw_ortho_arrow(ax, [(6.5, 3), (16, 3), (16, 4.8)], COLORS['mux'],
                 label=r'$\mathrm{Hist}_{\mathrm{init}}$', label_pos=(10.5, 3), gid='ai_path_13')
draw_ortho_arrow(ax, [(13.9, 4), (16, 4)], COLORS['clock'], label='Time', gid='ai_path_14')

draw_ortho_arrow(ax, [(19.5, 6.8), (21, 6.8)], COLORS['ai'], gid='ai_path_15')
draw_ortho_arrow(ax, [(19.5, 5.3), (21, 5.3)], COLORS['ai'], gid='ai_path_16')

save_fig(fig, r'c:\Users\Mohammed26\Desktop\مخطط سيموليشن\02_AI_BLOCK_Final.png', dpi=300)
save_fig(fig, r'c:\Users\Mohammed26\Desktop\مخطط سيموليشن\02_AI_BLOCK_Final.svg', dpi=300)
save_fig(fig, r'c:\Users\Mohammed26\Desktop\مخطط سيموليشن\02_AI_BLOCK_Final.pdf', dpi=600)


# ============================================================
#                      WATER TANK
# ============================================================
fig, ax = setup_fig(20, 8)
ax.set_xlim(-1, 19)
ax.set_ylim(-1, 7)

ax.text(9, 6.2, 'Water Tank Model  —  Mass Balance Subsystem',
        fontsize=20, color=COLORS['tank'], ha='center', fontweight='bold')
ax.text(9, 5.5, r'$\dfrac{dH}{dt} = \dfrac{Q_{\mathrm{in}} - Q_{\mathrm{out}}}{A}$'
        r'$\quad|\quad H(0) = 4\,\mathrm{m} \quad|\quad 0 \leq H \leq H_{\max}$',
        fontsize=14, color=TEXT_G, ha='center')

# Blocks
draw_block(ax, 0, 3.5, 1.5, 1, r'$Q_{\mathrm{in}}$', COLORS['fw'], COLORS['fw_bg'], fontsize=12, gid='wt_qin')
draw_block(ax, 0, 1.5, 1.5, 1, r'$Q_{\mathrm{out}}$', COLORS['fw'], COLORS['fw_bg'], fontsize=12, gid='wt_qout')

draw_circle(ax, 3.5, 3, 0.7, '', COLORS['sum'], fontsize=14, gid='wt_sum')
ax.text(3.15, 3.55, '+', fontsize=16, fontweight='bold', color='#059669')
ax.text(3.15, 2.35, r'$-$', fontsize=20, fontweight='bold', color='#DC2626')

draw_triangle(ax, 5.5, 2.2, 2.5, 1.6, r'$\dfrac{1}{A}$', COLORS['gain'], fontsize=18, gid='wt_gain')

draw_block(ax, 9.5, 2.2, 2, 1.6, r'$\dfrac{1}{s}$', COLORS['int'], COLORS['int_bg'], fontsize=20, gid='wt_int')
ax.text(10.5, 1.7, 'Integrator', fontsize=10, color=TEXT_G, ha='center')

draw_block(ax, 13, 2.2, 2, 1.6, 'Saturation', COLORS['sat'], COLORS['sat_bg'], fontsize=12, gid='wt_sat')

draw_block(ax, 16.5, 2.4, 2, 1.2, r'$H(t)$', '#059669', '#D1FAE5', fontsize=14, gid='wt_ht')

# Routing
draw_ortho_arrow(ax, [(1.5, 4), (2.8, 3.5)], COLORS['fw'], lw=2,
                 label=r'$Q_{\mathrm{in}}$', label_pos=(2.2, 4.3), gid='wt_path_1')
draw_ortho_arrow(ax, [(1.5, 2), (2.8, 2.5)], COLORS['fw'], lw=2,
                 label=r'$Q_{\mathrm{out}}$', label_pos=(2.2, 1.6), gid='wt_path_2')
draw_ortho_arrow(ax, [(4.2, 3), (5.5, 3)], COLORS['sum'], lw=2,
                 label=r'$\Delta Q$', gid='wt_path_3')
draw_ortho_arrow(ax, [(8, 3), (9.5, 3)], COLORS['gain'], lw=2, gid='wt_path_4')
draw_ortho_arrow(ax, [(11.5, 3), (13, 3)], COLORS['int'], lw=2, gid='wt_path_5')
draw_ortho_arrow(ax, [(15, 3), (16.5, 3)], COLORS['sat'], lw=2,
                 label=r'$H(t)$', gid='wt_path_6')

# Info Box
r = FancyBboxPatch((3, -0.5), 12, 1.2, boxstyle="round,pad=0.2",
                   facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.5, zorder=2)
ax.add_patch(r)
ax.text(9, 0.3, r'$(Q_{\mathrm{in}} - Q_{\mathrm{out}}) \times \frac{1}{A}'
        r' \;\rightarrow\; \int \;\rightarrow\;'
        r' \mathrm{Sat} \;\rightarrow\; H(t)$',
        fontsize=12, color=TEXT_W, ha='center', zorder=3)
ax.text(9, -0.2, r'$A$: Tank Area  |  IC: $4\,\mathrm{m}$  |  $H_{\max}$: Max Height',
        fontsize=10, color=TEXT_G, ha='center', zorder=3)

save_fig(fig, r'c:\Users\Mohammed26\Desktop\مخطط سيموليشن\03_Water_Tank_Final.png', dpi=300)
save_fig(fig, r'c:\Users\Mohammed26\Desktop\مخطط سيموليشن\03_Water_Tank_Final.svg', dpi=300)
save_fig(fig, r'c:\Users\Mohammed26\Desktop\مخطط سيموليشن\03_Water_Tank_Final.pdf', dpi=600)
