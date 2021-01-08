#!/usr/bin/python3
# coding=utf-8

# Written by Simon Reichel, 2021

import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty

bl_info = {
    "name": "Workspace Swapper",
    "blender": (2, 82, 0),
    "category": "Interface",
}

class WorkspaceSwapOperator(Operator):
    """Swap workspaces with this operator."""

    bl_idname = "workspaceswapper.swap"
    bl_label = "Swap Workspace"
    bl_options = {'REGISTER'}

    targetWorkspace: StringProperty(name='Target workspace', default="Modeling")

    def execute(self, context):
        # don't need to swap if already on there
        if context.workspace.name == self.targetWorkspace:
            return {'CANCELLED'}

        # VAR 1: import workspace from external file
        if not self.targetWorkspace in bpy.data.workspaces:
            bpy.ops.workspace.append_activate(idname=self.targetWorkspace, filepath=bpy.utils.user_resource('CONFIG', 'startup.blend'))
        else:
        # VAR2: swap workspace locally
            context.window.workspace = bpy.data.workspaces[self.targetWorkspace]

        return {'FINISHED'}


def register():
    bpy.utils.register_class(WorkspaceSwapOperator)

def unregister():
    bpy.utils.unregister_class(WorkspaceSwapOperator)

if __name__ == "__main__":
    register()
