bl_info = {
    "name": "Blender Instant Denoise. By Moby Motion",
    "blender": (2, 82, 0),
    "category": "Object",
    "description": "Apply the new Intel denoiser in a single click.",
    "author": "Moby Motion",
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": ""
}

# Imports
import bpy

# Classes
class InstantDenoise(bpy.types.Operator):
    """Apply the new Intel denoiser in a single click."""
    bl_idname = "object.instantdenoise"
    bl_label = "Denoise"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Called when blender runs this operator"""

        scene = context.scene

        # Initialise important settings
        scene.use_nodes = True
        context.view_layer.cycles.denoising_store_passes = True
        context.scene.render.use_compositing = True

        # Clear any existing nodes
        tree = scene.node_tree

        for node in tree.nodes:
        	tree.nodes.remove(node)

        # Set up new nodes
        render_layers_node = tree.nodes.new(type='CompositorNodeRLayers')
        render_layers_node.location = 0, 0
        denoise_node = tree.nodes.new(type="CompositorNodeDenoise")
        denoise_node.location = 300, 0
        composite_node = tree.nodes.new(type='CompositorNodeComposite')
        composite_node.location = 600, 0

        # Link new nodes        
        tree.links.new(
        	render_layers_node.outputs['Noisy Image'], 
        	denoise_node.inputs['Image'])
        tree.links.new(
        	render_layers_node.outputs['Denoising Albedo'], 
        	denoise_node.inputs['Albedo'])
        tree.links.new(
        	render_layers_node.outputs['Denoising Normal'], 
        	denoise_node.inputs['Normal'])

        tree.links.new(
        	denoise_node.outputs['Image'], 
        	composite_node.inputs['Image'])

        return {'FINISHED'}


class InstantDenoisePanel(bpy.types.Panel):
    """The primary panel for Blender AutoFocus"""
    bl_label = "Instant AI denoise"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        
        row = layout.row()
        row.label(text="Click to apply Intel AI denoising", icon='CAMERA_DATA')

        row = layout.row()
        row.operator("object.instantdenoise")


# Register classes
classes = (
    InstantDenoisePanel,
    InstantDenoise,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

# Allows script to run directly from Blender's Text editor
if __name__ == "__main__":
    register()
    
