objects = [1, 8, 11, 12, 18, 20, 22, 26, 28, 96, 97, 112, 113, 102, 118]

blocks = [0, 32, 33, 34, 35, 36, 37, 38, 39, 48, 49, 50, 51, 52, 
          53, 54, 55, 72, 43, 17, 27, 59, 64, 66, 67, 68, 69, 82, 83, 84, 85, 98, 99,
          100, 101, 114, 115, 116, 117, 23]

background = [16, 40, 41, 42, 56, 57, 58, 88, 103, 104, 44, 60, 61, 62, 63, 70, 71, 86,
              87]

misc = [i for i in range(128) if i not in background and i not in blocks and i not in objects]

categories_map = {0: objects, 1: blocks, 2: background, 3: misc}