objects = [1, 8, 11, 12, 18, 20, 22, 26, 28, 96, 97, 112, 113, 102, 118]

blocks = [0, 32, 33, 34, 35, 36, 37, 38, 39, 48, 49, 50, 51, 52, 
          53, 54, 55, 72, 43, 17, 27, 59, 64, 66, 67, 68, 69, 82, 83, 84, 85, 98, 99,
          100, 101, 114, 115, 116, 117, 23, -1, -2]

background = [16, 40, 41, 42, 56, 57, 58, 88, 103, 104, 44, 60, 61, 62, 63, 70, 71, 86,
              87]

misc = [i for i in range(128) if i not in background and i not in blocks and i not in objects]

all_sprites = objects + blocks + background + misc

categories_map = {0: objects, 1: blocks, 2: background, 3: misc}

"""
  1  
2   4
  8  
"""
# First element is regular blocks, second is ice
blocks_bitmasking = [
                     [32, 55, 54, 51, 
                      52, 49, 53, 50,
                      39, 48, 35, 38,
                      33, 36, 34, 37],
                     [117, 101, 116, 100,
                      114, 98, 115, 99,
                      69, 85, 68, 84,
                      66, 82, 67, 83]
                    ]


# assigning negative number so we can put it in a SpriteLabel
autotiling_sprites={-1:32, -2:117}

