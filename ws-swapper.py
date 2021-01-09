#!/usr/bin/python3
# coding=utf-8

# Written by Simon Reichel, 2021

import bpy
from pathlib import Path
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty

bl_info = {
    "name": "Workspace Swapper",
    "blender": (2, 82, 0),
    "description": "A utility operator to switch to a different workspace.",
    "author": "Simon Reichel, Sebastian König, Robert Gützkow",
    "version": (0, 0, 1),
    "support": "COMMUNITY",
    "tracker_url": "https://github.com/Amudtogal/blender-workspace-swapper/issues",
    "category": "Interface",
}

class WorkspaceSwapOperator(Operator):
    """Swap workspaces with this operator."""

    bl_idname = "workspaceswapper.swap"
    bl_label = "Swap Workspace"
    bl_options = {'REGISTER'}

    targetWorkspace: StringProperty(name='Target workspace', default="Motion Tracking")

    def execute(self, context):
        # don't need to swap if already on there
        if context.workspace.name == self.targetWorkspace:
            return {'CANCELLED'}

        # Try local workspace swapping first
        if self.targetWorkspace in bpy.data.workspaces:
            context.window.workspace = bpy.data.workspaces[self.targetWorkspace]
            return {'FINISHED'}

        # Try importing from startup blend (this allows user workspaces to be included)
        success = bpy.ops.workspace.append_activate(
            idname=self.targetWorkspace,
            filepath=bpy.utils.user_resource('CONFIG', 'startup.blend'))
        if success == {'FINISHED'}:
            return success

        # Last resort: try to import from the blender templates
        for p in Path(next(bpy.utils.app_template_paths())).rglob("startup.blend"):
            success = bpy.ops.workspace.append_activate(
                idname=self.targetWorkspace,
                filepath=str(p))

            if success == {'FINISHED'}:
                return success
        else:
            print('Workspace Swapper: Could not find the requested workspace "{}"'.format(
                self.targetWorkspace))
        return {'CANCELLED'}


def register():
    bpy.utils.register_class(WorkspaceSwapOperator)

def unregister():
    bpy.utils.unregister_class(WorkspaceSwapOperator)

if __name__ == "__main__":
    register()
