"""Shared drawing utilities for Light Theme Simulink-style block diagrams (MathText/LaTeX)."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Increase default font sizes
plt.rcParams.update({
    'mathtext.fontset': 'stix',
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans']
})

BG = '#FFFFFF'
TEXT_W = '#0F172A' # Darker slate for higher contrast
TEXT_G = '#475569' 
TEXT_D = '#64748B' 

# More vibrant colors
COLORS = {
    'ai': '#D97706',      'ai_bg': '#FDE68A',
    'pv': '#059669',      'pv_bg': '#A7F3D0',
    'fopid': '#DC2626',   'fopid_bg': '#FECACA',
    'vfd': '#7C3AED',     'vfd_bg': '#DDD6FE',
    'pump': '#DB2777',    'pump_bg': '#FBCFE8',
    'mpc_mgr': '#0891B2', 'mpc_mgr_bg': '#A5F3FC',
    'mpc': '#2563EB',     'mpc_bg': '#BFDBFE',
    'tank': '#0284C7',    'tank_bg': '#BAE6FD',
    'demand': '#EA580C',  'demand_bg': '#FED7AA',
    'fw': '#2563EB',      'fw_bg': '#EFF6FF',
    'scope': '#CA8A04',   'scope_bg': '#FEF08A',
    'tw': '#0369A1',      'tw_bg': '#F0F9FF',
    'gain': '#059669',    'gain_bg': '#ECFDF5',
    'const': '#DC2626',   'const_bg': '#FEF2F2',
    'clock': '#475569',   'clock_bg': '#F8FAFC',
    'mux': '#7C3AED',     'mux_bg': '#F5F3FF',
    'sum': '#059669',
    'int': '#2563EB',     'int_bg': '#EFF6FF',
    'sat': '#9333EA',     'sat_bg': '#FAF5FF',
    'delay': '#475569',   'delay_bg': '#F8FAFC',
}

def setup_fig(w=24, h=14):
    fig, ax = plt.subplots(1, 1, figsize=(w, h), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax

def draw_block(ax, x, y, w, h, label, color, bg_color=None, icon=None,
               fontsize=12, rx=0.15, border_w=2.0, sublabel=None, gid=None):
    if bg_color is None: bg_color = '#FFFFFF'
    
    shadow = FancyBboxPatch((x+0.1, y-0.1), w, h, boxstyle=f"round,pad={rx}",
                            facecolor='#94A3B8', alpha=0.3, edgecolor='none', zorder=1)
    ax.add_patch(shadow)
    
    box = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={rx}",
                         facecolor=bg_color, edgecolor=color,
                         linewidth=border_w, zorder=2, gid=gid)
    ax.add_patch(box)
    
    cy = y + h/2
    if icon:
        ax.text(x + w/2, cy + 0.35, icon, ha='center', va='center',
                fontsize=fontsize+6, color=color, fontweight='bold', zorder=3)
        ax.text(x + w/2, cy - 0.4, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=TEXT_W, zorder=3)
    else:
        ax.text(x + w/2, cy, label, ha='center', va='center',
                fontsize=fontsize+2, fontweight='bold', color=TEXT_W, zorder=3)
    
    if sublabel:
        ax.text(x + w/2, y - 0.3, sublabel, ha='center', va='top',
                fontsize=fontsize-2, color=TEXT_G, zorder=3)

def draw_small_block(ax, x, y, w, h, label, color, bg_color=None, fontsize=10, gid=None):
    if bg_color is None: bg_color = '#FFFFFF'
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                         facecolor=bg_color, edgecolor=color,
                         linewidth=1.5, zorder=2, gid=gid)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, label, ha='center', va='center',
            fontsize=fontsize, fontweight='bold', color=TEXT_W, zorder=3)

def draw_circle(ax, cx, cy, r, label, color, bg_color='#FFFFFF', fontsize=14, gid=None):
    circle = plt.Circle((cx, cy), r, facecolor=bg_color, edgecolor=color,
                        linewidth=2.0, zorder=2, gid=gid)
    ax.add_patch(circle)
    ax.text(cx, cy, label, ha='center', va='center',
            fontsize=fontsize, fontweight='bold', color=TEXT_W, zorder=3)

def draw_triangle(ax, x, y, w, h, label, color, fontsize=14, gid=None):
    tri = plt.Polygon([(x, y), (x+w, y+h/2), (x, y+h)],
                      facecolor='#FFFFFF', edgecolor=color,
                      linewidth=2.0, zorder=2, gid=gid)
    ax.add_patch(tri)
    ax.text(x + w*0.35, y + h/2, label, ha='center', va='center',
            fontsize=fontsize, fontweight='bold', color=TEXT_W, zorder=3)

def draw_ortho_arrow(ax, pts, color='#2563EB', lw=1.8, label=None, label_pos=None, style='->', zorder=4, gid=None):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    
    for i in range(len(pts)-1):
        is_last = (i == len(pts)-2)
        # Unique GID for each segment of the arrow if gid is provided
        seg_gid = f"{gid}_{i}" if gid else None
        ann = ax.annotate('', xy=(xs[i+1], ys[i+1]), xytext=(xs[i], ys[i]),
                          arrowprops=dict(arrowstyle=style if is_last else '-',
                                         color=color, lw=lw, shrinkA=0, shrinkB=0),
                          zorder=zorder)
        if seg_gid and ann.arrow_patch:
            ann.arrow_patch.set_gid(seg_gid)
    
    if label:
        if label_pos is None:
            mx, my = (xs[0]+xs[-1])/2, (ys[0]+ys[-1])/2
        else:
            mx, my = label_pos
            
        ax.text(mx, my, label, ha='center', va='center',
                fontsize=9, color=color, fontweight='bold',
                zorder=5, bbox=dict(boxstyle='round,pad=0.2',
                                   facecolor=BG, edgecolor='none', alpha=0.9))

def draw_section(ax, x, y, w, h, label, color):
    r = FancyBboxPatch((x,y), w, h, boxstyle="round,pad=0.3",
                       facecolor=color+'0F', edgecolor=color+'60', linewidth=1.5, linestyle='--', zorder=0)
    ax.add_patch(r)
    ax.text(x, y + h + 0.5, label, fontsize=11, fontweight='bold',
            color=color, zorder=1)

def save_fig(fig, path, dpi=300):
    fig.savefig(path, dpi=dpi, facecolor=BG,
                edgecolor='none', bbox_inches='tight', pad_inches=0.4)
    plt.close(fig)
    print(f"Saved: {path.split(chr(92))[-1]}")
