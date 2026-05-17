"""Auto-generated Layout from PV_GHI_System_Mezoo_3.slx"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from draw_light import *

fig, ax = setup_fig(24, 14)
ax.set_xlim(-2, 30)
ax.set_ylim(-2, 20)

C = COLORS

# ====== BLOCKS ======
draw_block(ax, 0, 15, 2.5, 1.5, ' Demand', C['fw'], C['fw'_bg], fontsize=10, gid='b_212')
draw_block(ax, 4, 15, 2.5, 1.5, 'AI_BLOCK', C['fw'], C['fw'_bg], fontsize=10, gid='b_89')
draw_block(ax, 8, 15, 2.5, 1.5, 'Clock', C['fw'], C['fw'_bg], fontsize=10, gid='b_84')
draw_block(ax, 12, 15, 2.5, 1.5, 'Clock1', C['fw'], C['fw'_bg], fontsize=10, gid='b_139')
draw_block(ax, 16, 15, 2.5, 1.5, 'Clock2', C['fw'], C['fw'_bg], fontsize=10, gid='b_157')
draw_block(ax, 20, 15, 2.5, 1.5, 'Clock3', C['fw'], C['fw'_bg], fontsize=10, gid='b_213')
draw_block(ax, 0, 12, 2.5, 1.5, 'Clock4', C['fw'], C['fw'_bg], fontsize=10, gid='b_148')
draw_block(ax, 4, 12, 2.5, 1.5, 'Clock5', C['fw'], C['fw'_bg], fontsize=10, gid='b_154')
draw_block(ax, 8, 12, 2.5, 1.5, 'Clock6', C['fw'], C['fw'_bg], fontsize=10, gid='b_163')
draw_block(ax, 12, 12, 2.5, 1.5, 'Clock7', C['fw'], C['fw'_bg], fontsize=10, gid='b_166')
draw_block(ax, 16, 12, 2.5, 1.5, 'Constant1', C['fw'], C['fw'_bg], fontsize=10, gid='b_202')
draw_block(ax, 20, 12, 2.5, 1.5, 'FOPID_Control', C['fw'], C['fw'_bg], fontsize=10, gid='b_4')
draw_block(ax, 0, 9, 2.5, 1.5, 'Flow', C['fw'], C['fw'_bg], fontsize=10, gid='b_150')
draw_block(ax, 4, 9, 2.5, 1.5, 'Flow_Calc', C['gain'], C['gain'_bg], fontsize=10, gid='b_7')
draw_block(ax, 8, 9, 2.5, 1.5, 'From Workspace', C['fw'], C['fw'_bg], fontsize=10, gid='b_197')
draw_block(ax, 12, 9, 2.5, 1.5, 'From Workspace1', C['fw'], C['fw'_bg], fontsize=10, gid='b_198')
draw_block(ax, 16, 9, 2.5, 1.5, 'From Workspace2', C['fw'], C['fw'_bg], fontsize=10, gid='b_199')
draw_block(ax, 20, 9, 2.5, 1.5, 'From Workspace3', C['fw'], C['fw'_bg], fontsize=10, gid='b_292')
draw_block(ax, 0, 6, 2.5, 1.5, 'From Workspace4', C['fw'], C['fw'_bg], fontsize=10, gid='b_290')
draw_block(ax, 4, 6, 2.5, 1.5, 'From Workspace5', C['fw'], C['fw'_bg], fontsize=10, gid='b_291')
draw_block(ax, 8, 6, 2.5, 1.5, 'GH', C['gain'], C['gain'_bg], fontsize=10, gid='b_167')
draw_block(ax, 12, 6, 2.5, 1.5, 'GHI', C['fw'], C['fw'_bg], fontsize=10, gid='b_169')
draw_block(ax, 16, 6, 2.5, 1.5, 'MPC Controller', C['fw'], C['fw'_bg], fontsize=10, gid='b_224')
draw_block(ax, 20, 6, 2.5, 1.5, 'MPC_Manager', C['fw'], C['fw'_bg], fontsize=10, gid='b_49')
draw_block(ax, 0, 3, 2.5, 1.5, 'Moto', C['gain'], C['gain'_bg], fontsize=10, gid='b_158')
draw_block(ax, 4, 3, 2.5, 1.5, 'Motor Speed', C['fw'], C['fw'_bg], fontsize=10, gid='b_159')
draw_block(ax, 8, 3, 2.5, 1.5, 'Multiport Switch', C['fw'], C['fw'_bg], fontsize=10, gid='b_201')
draw_block(ax, 12, 3, 2.5, 1.5, 'Multiport Switch1', C['fw'], C['fw'_bg], fontsize=10, gid='b_293')
draw_block(ax, 16, 3, 2.5, 1.5, 'PV_Physics', C['fw'], C['fw'_bg], fontsize=10, gid='b_200')
draw_block(ax, 20, 3, 2.5, 1.5, 'Power Consumed', C['fw'], C['fw'_bg], fontsize=10, gid='b_165')
draw_block(ax, 0, 0, 2.5, 1.5, 'Power1', C['fw'], C['fw'_bg], fontsize=10, gid='b_172')
draw_block(ax, 4, 0, 2.5, 1.5, 'Pump_Drive', C['fw'], C['fw'_bg], fontsize=10, gid='b_54')
draw_block(ax, 8, 0, 2.5, 1.5, 'Tank Level', C['fw'], C['fw'_bg], fontsize=10, gid='b_171')
draw_block(ax, 12, 0, 2.5, 1.5, 'To Workspace', C['fw'], C['fw'_bg], fontsize=10, gid='b_215')
draw_block(ax, 16, 0, 2.5, 1.5, 'To Workspace1', C['fw'], C['fw'_bg], fontsize=10, gid='b_216')
draw_block(ax, 20, 0, 2.5, 1.5, 'To Workspace2', C['fw'], C['fw'_bg], fontsize=10, gid='b_217')
draw_block(ax, 0, -3, 2.5, 1.5, 'To Workspace3', C['fw'], C['fw'_bg], fontsize=10, gid='b_218')
draw_block(ax, 4, -3, 2.5, 1.5, 'To Workspace4', C['fw'], C['fw'_bg], fontsize=10, gid='b_219')
draw_block(ax, 8, -3, 2.5, 1.5, 'Unit Delay', C['fw'], C['fw'_bg], fontsize=10, gid='b_226')
draw_block(ax, 12, -3, 2.5, 1.5, 'VFD', C['fw'], C['fw'_bg], fontsize=10, gid='b_214')
draw_block(ax, 16, -3, 2.5, 1.5, 'Water_Tank_Model', C['fw'], C['fw'_bg], fontsize=10, gid='b_185')
draw_block(ax, 20, -3, 2.5, 1.5, 'flo', C['gain'], C['gain'_bg], fontsize=10, gid='b_149')
draw_block(ax, 0, -6, 2.5, 1.5, 'pc', C['gain'], C['gain'_bg], fontsize=10, gid='b_164')
draw_block(ax, 4, -6, 2.5, 1.5, 'po', C['gain'], C['gain'_bg], fontsize=10, gid='b_140')
draw_block(ax, 8, -6, 2.5, 1.5, 'tan', C['gain'], C['gain'_bg], fontsize=10, gid='b_155')

# ====== WIRES ======
# Wire from Water_Tank_Model to To Workspace3
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Water_Tank_Model to To Workspace3
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Water_Tank_Model to To Workspace3
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Water_Tank_Model to MPC_Manager
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Water_Tank_Model to MPC_Manager
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Water_Tank_Model to  Demand
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Water_Tank_Model to Tank Level
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Flow_Calc to Unit Delay
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Flow_Calc to Unit Delay
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Flow_Calc to Flow
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Flow_Calc to Flow
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Flow_Calc to Water_Tank_Model
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Pump_Drive to Flow_Calc
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Pump_Drive to To Workspace4
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Pump_Drive to To Workspace4
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Pump_Drive to Power Consumed
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Pump_Drive to To Workspace2
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Pump_Drive to To Workspace2
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Pump_Drive to Motor Speed
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Clock1 to po
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from po to Power1
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from flo to Flow
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Clock4 to flo
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Clock5 to tan
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from tan to Tank Level
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Clock2 to Moto
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Moto to Motor Speed
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Clock6 to pc
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from pc to Power Consumed
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Clock7 to GH
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from GH to GHI
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from PV_Physics to To Workspace1
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from PV_Physics to To Workspace1
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from PV_Physics to To Workspace1
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from PV_Physics to Power1
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from PV_Physics to FOPID_Control
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Multiport Switch to To Workspace
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Multiport Switch to To Workspace
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Multiport Switch to To Workspace
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Multiport Switch to GHI
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Multiport Switch to PV_Physics
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Constant1 to Multiport Switch1
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Constant1 to Multiport Switch1
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Constant1 to Multiport Switch1
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Constant1 to AI_BLOCK
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Constant1 to Multiport Switch
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from From Workspace to Multiport Switch
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from From Workspace1 to Multiport Switch
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from From Workspace2 to Multiport Switch
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from  Demand to Water_Tank_Model
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Clock3 to  Demand
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from FOPID_Control to VFD
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from VFD to Pump_Drive
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from VFD to Pump_Drive
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from MPC_Manager to VFD
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from MPC_Manager to VFD
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from MPC_Manager to MPC Controller
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from MPC Controller to FOPID_Control
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Unit Delay to MPC Controller
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Clock to MPC_Manager
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from AI_BLOCK to MPC_Manager
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from From Workspace4 to Multiport Switch1
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from From Workspace3 to Multiport Switch1
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from From Workspace5 to Multiport Switch1
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from Multiport Switch1 to PV_Physics
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])
# Wire from AI_BLOCK to MPC_Manager
# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])

save_fig(fig, "./PV_GHI_System_Mezoo_3_Generated.png", dpi=300)
