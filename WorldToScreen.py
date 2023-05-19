#ext
from numpy import array, frombuffer, float32
from pyMeow import r_bytes

#own
from Data import Offsets

class World:

    def __init__(self, process, base_address, width, height):
        self.process = process
        self.base_address = base_address
        self.width = width
        self.height = height

    def _list_to_matrix(self, floats):
        return array(floats).reshape(4,4)
    
    def get_view_proj_matrix(self):
        data = r_bytes(self.process, self.base_address + Offsets.oViewProjMatrix, 0x128)
        view_matrix = self._list_to_matrix(frombuffer(data[:64], dtype=float32))
        proj_matrix = self._list_to_matrix(frombuffer(data[64:128], dtype=float32))
        view_proj_matrix = view_matrix @ proj_matrix
        return view_proj_matrix.reshape(16)
    
    def world_to_screen(self, view_proj_matrix, x, y, z):
        clip_coords_x = x * view_proj_matrix[0] + y * view_proj_matrix[4] + z * view_proj_matrix[8] + view_proj_matrix[12]
        clip_coords_y = x * view_proj_matrix[1] + y * view_proj_matrix[5] + z * view_proj_matrix[9] + view_proj_matrix[13]
        clip_coords_w = x * view_proj_matrix[3] + y * view_proj_matrix[7] + z * view_proj_matrix[11] + view_proj_matrix[15]

        if clip_coords_w <= 0.:
            clip_coords_w = .1

        M_x, M_y = clip_coords_x / clip_coords_w, clip_coords_y / clip_coords_w
        out_x, out_y = (self.width / 2. * M_x) + (M_x + self.width / 2.), -(self.height / 2. * M_y) + (M_y + self.height / 2.) 

        return out_x, out_y

    def world_to_screen_restricted(self, view_proj_matrix, x, y, z):
        clip_coords_x = x * view_proj_matrix[0] + y * view_proj_matrix[4] + z * view_proj_matrix[8] + view_proj_matrix[12]
        clip_coords_y = x * view_proj_matrix[1] + y * view_proj_matrix[5] + z * view_proj_matrix[9] + view_proj_matrix[13]
        clip_coords_w = x * view_proj_matrix[3] + y * view_proj_matrix[7] + z * view_proj_matrix[11] + view_proj_matrix[15]

        if clip_coords_w <= 0.:
            clip_coords_w = .1

        M_x, M_y = clip_coords_x / clip_coords_w, clip_coords_y / clip_coords_w
        out_x, out_y = (self.width / 2. * M_x) + (M_x + self.width / 2.), -(self.height / 2. * M_y) + (M_y + self.height / 2.)

        if 0 <= out_x <= self.width and 0 <= out_y <= self.height:
            return out_x, out_y
        
