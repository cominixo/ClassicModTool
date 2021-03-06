import numpy as np
from PIL import Image
from consts import *

class Cart:


    loaded_spritesheet = np.zeros((128, 128, 3), dtype=np.uint8)
    
    def __init__(self, cart_path):
        with open(cart_path, "r",encoding="utf-8") as f:
            self.cart = f.read()

        self.split_cart()
        self.load_spritesheet()
        
        self.load_extended_map()

        self.load_map()

        self.past_states = [{"gfx": self._gfx, "map": self._map}]


        
    def split_cart(self):
        self._lua = self.get_cart_section("lua")
        self._gfx = self.get_cart_section("gfx")
        self._gff = self.get_cart_section("gff")
        self._label = self.get_cart_section("label").strip() + "\n"
        self._map = self.get_cart_section("map")
        self._sfx = self.get_cart_section("sfx")
        self._music = self.get_cart_section("music")

        self._extended_map = "".join(self._gfx.split("\n")[(SPRITESHEET_SIZE//2)+1:])
        

    def get_cart_section(self, section) -> str:
        section = f"__{section}__"
        section_index = self.cart.find(section)
        return self.cart[section_index:self.cart.find("__", section_index + len(section))]

    def load_spritesheet(self):
    
        lines = self._gfx.split("\n")[1:]
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                self.loaded_spritesheet[y,x] = P8_COLORS[int(lines[y][x], 16)]

    def save(self):
        self._gfx += "\n"
        return P8_HEADER + self._lua + self._gfx + self._gff + self._label + self._map + self._sfx + self._music 

    def get_sprite(self, id) -> Image:
        y, x = divmod(id, SPRITESHEET_SIZE//SPRITE_SIZE)

        x *= 8
        y *= 8

        return Image.fromarray(self.loaded_spritesheet[y:y+SPRITE_SIZE, x:x+SPRITE_SIZE])

    def load_map(self):

        map_image = Image.new("RGBA", (128*SPRITE_SIZE, 64*SPRITE_SIZE))

        lines = self._map.split("\n")[1:-1]
        lines += self._extended_map.split("\n")
        for y in range(len(lines)):
            for x in range(0, len(lines[y]), 2):
                spriteid = int(lines[y][x] + lines[y][x+1], 16)
                map_image.paste(self.get_sprite(spriteid), ((x//2)*8, y*8))

        self.loaded_map = np.array(map_image)

    def load_extended_map(self):
        # split line every 256 characters
        self._extended_map = [self._extended_map[i:i+SPRITESHEET_SIZE*2] for i in range(0, len(self._extended_map), SPRITESHEET_SIZE*2)]


        lines = self._extended_map
        for y in range(len(lines)):
            for x in range(0, len(lines[y]), 2): 
                lines[y] = lines[y][:x] + lines[y][x+1] + lines[y][x] + lines[y][x + 2:]


        self._extended_map = "\n".join(lines)


    def get_level(self, level) -> np.ndarray:
        y, x = divmod(level, MAP_WIDTH)

        map_arr = self.loaded_map

        x *= SPRITE_SIZE * LEVEL_SIZE
        y *= SPRITE_SIZE * LEVEL_SIZE

        return map_arr[y:y+(LEVEL_SIZE*SPRITE_SIZE), x:x+(LEVEL_SIZE*SPRITE_SIZE)]

    def get_tile(self, level, tile_x, tile_y) -> str:
        if level > 15:

            level -= 16
            celeste_map = self._extended_map.split("\n")
        else:
            celeste_map = self._map.split("\n")[1:]

        level_y, level_x = divmod(level, 8)

        tile_x += (16*level_x)
        tile_y += (16*level_y)
        str_value = celeste_map[tile_y][tile_x*2:tile_x*2+2]
        if not str_value:
            return "0"
        return str_value

    def edit_sprite(self, color, sprite, x, y):

        x += (sprite%16)*8
        y += (sprite//16)*8

        color_hex = hex(color)[2:]

        lines = self._gfx.split("\n")[1:]

        lines[y] = lines[y][:x] + color_hex + lines[y][x + 1:]

        self._gfx = "__gfx__\n" + "\n".join(lines)

    def undo(self):
        if len(self.past_states) <= 0:
            return

        last_state = self.past_states[-1]

        

        self._map = last_state["map"]
        self._gfx = last_state["gfx"]

        
        self.load_spritesheet()
        self._extended_map = "".join(self._gfx.split("\n")[(SPRITESHEET_SIZE//2)+1:])
        self.load_extended_map()

        self.load_map()

        self.past_states.pop(-1)


    def edit_tile(self, sprite, level, tile_x, tile_y):
        
        
        sprite_hex = '{:02x}'.format(sprite)

        is_extended = False

        if level > 15:

            is_extended = True
            level -= 16
            celeste_map = self._extended_map.split("\n")
        else:
            celeste_map = self._map.split("\n")[1:]
            

        level_y, level_x = divmod(level, 8)

        tile_x += (16*level_x)
        tile_y += (16*level_y)
        try:
            if celeste_map[tile_y][tile_x*2:tile_x*2 + 2] == sprite_hex:
                return
        except IndexError:
            return

        if len(self.past_states) > 256:
            self.past_states.pop(0)
        self.past_states.append({"map":self._map, "gfx":self._gfx})


        celeste_map[tile_y] = celeste_map[tile_y][:tile_x*2] + sprite_hex + celeste_map[tile_y][tile_x*2 + 2:]

        if is_extended:
            flat_map = "".join(celeste_map)
            # split line every 128 characters to put back in gfx
            gfx_format = [flat_map[i:i+SPRITESHEET_SIZE] for i in range(0, len(flat_map), SPRITESHEET_SIZE)]

            for y in range(len(gfx_format)):
                for x in range(0, len(gfx_format[y]), 2): 
                    gfx_format[y] = gfx_format[y][:x] + gfx_format[y][x+1] + gfx_format[y][x] + gfx_format[y][x + 2:]


            gfx = "\n".join(self._gfx.split("\n")[:(SPRITESHEET_SIZE//2)+1])

            self._gfx = gfx + "\n" + "\n".join(gfx_format)

            self._extended_map = "\n".join(celeste_map)

        else:
            self._map = "__map__" + "\n" + "\n".join(celeste_map)

        
            
        
        

        


