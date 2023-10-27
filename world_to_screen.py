#ext
from pyMeow import r_bytes
from numpy import matmul, array, frombuffer, float32
#own
from data import Offsets

class World:

    def __init__(self, process, base_address, width, height):
        self.process = process
        self.base_address = base_address
        self.width = width
        self.height = height
        self.view_proj_matrix_offset = Offsets.view_proj_matrix

    def get_view_proj_matrix(self):
        data = r_bytes(self.process, self.base_address + self.view_proj_matrix_offset, 0x128)
        view_matrix = frombuffer(data[:64], dtype=float32).reshape(4, 4)
        proj_matrix = frombuffer(data[64:128], dtype=float32).reshape(4, 4)
        view_proj_matrix = matmul(view_matrix, proj_matrix)
        return view_proj_matrix
    
    def world_to_screen(self, view_proj_matrix, x, y, z):
        clip_coords = matmul(array([x, y, z, 1.0]), view_proj_matrix.reshape(4, 4))
        if clip_coords[3] <= 0.: clip_coords[3] = 0.1
        clip_coords /= clip_coords[3]
        return int((self.width / 2.0 * clip_coords[0]) + (clip_coords[0] + self.width / 2.0)), int(-(self.height / 2.0 * clip_coords[1]) + (clip_coords[1] + self.height / 2.0))

    def world_to_screen_limited(self, view_proj_matrix, x, y, z):
        clip_coords = matmul(array([x, y, z, 1.0]), view_proj_matrix.reshape(4, 4))
        if clip_coords[3] <= 0.: clip_coords[3] = 0.1
        clip_coords /= clip_coords[3]
        out_x, out_y =  int((self.width / 2.0 * clip_coords[0]) + (clip_coords[0] + self.width / 2.0)), int(-(self.height / 2.0 * clip_coords[1]) + (clip_coords[1] + self.height / 2.0))

        if 0 <= out_x <= self.width and 0 <= out_y <= self.height:
            return out_x, out_y
