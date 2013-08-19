#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Show static cube using vertex arrays.
"""

import numpy as np
from vispy import app, gl, oogl
import vispy_io as io  # Because vispy 0.1.0 lacks some data files
from transforms import translate, rotate, perspective


VERT_CODE = """
uniform   mat4 u_model;
uniform   mat4 u_view;
uniform   mat4 u_projection;

attribute vec3 a_position;
attribute vec4 a_color;

varying vec4 v_color;

void main()
{
    v_color = a_color;
    //gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
    gl_Position = vec4(a_position,1.0);
}
"""


FRAG_CODE = """
varying vec4 v_color;
void main()
{
    gl_FragColor = v_color;
}
"""


# Read cube data
positions, faces, normals, texcoords = io.read_mesh('cube.obj')
colors = np.random.uniform(0,1,positions.shape).astype('float32')
faces = faces.astype(np.uint16)


class Canvas(app.Canvas):
    
    def __init__(self):
        app.Canvas.__init__(self)
        self.geometry = 0, 0, 400, 400
        
        self.program = oogl.ShaderProgram(  oogl.VertexShader(VERT_CODE),
                                            oogl.FragmentShader(FRAG_CODE) )
        
        self.program.attributes['a_position'] = positions
        self.program.attributes['a_color'] = colors
    
    
    def on_initialize(self, event):
        gl.glClearColor(1,1,1,1)
    
    
    def on_resize(self, event):
        width, height = event.size
        gl.glViewport(0, 0, width, height)
        #self.projection = perspective( 45.0, width/float(height), 2.0, 10.0 )
        #self.program.uniforms['u_projection'] = self.projection

    
    def on_paint(self, event):
        
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        
        with self.program as prog:
            prog.draw_elements(gl.GL_TRIANGLES, faces)
        
        # Swap buffers
        self.swap_buffers()
    
    
    def init_transforms(self):
        # Ignore this for now
        self.view       = np.eye(4,dtype=np.float32)
        self.model      = np.eye(4,dtype=np.float32)
        self.projection = np.eye(4,dtype=np.float32)
        
        self.theta = 0
        self.phi = 0
        
        translate(self.view, 0,0,-5)
        self.program.uniforms['u_model'] = self.model
        self.program.uniforms['u_view'] = self.view
    
    
    def update_transforms(self,event):
        # Ignore this for now
        self.theta += .5
        self.phi += .5
        self.model = np.eye(4, dtype=np.float32)
        rotate(self.model, self.theta, 0,0,1)
        rotate(self.model, self.phi,   0,1,0)
        self.program.uniforms['u_model'] = self.model
        self.update()

if __name__ == '__main__':
    c = Canvas()
    c.show()
    app.run()
