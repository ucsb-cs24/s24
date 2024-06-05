class VoxMap {
  constructor(text) {
    if(text) {
      this.update(text)
    }
    else {
      this.clear()
    }
  }

  clear() {
    this.width  = 0
    this.depth  = 0
    this.height = 0
    this.data   = []
  }

  get(x, y, z) {
    return this.data[this.width*this.depth*z + this.width*y + x]
  }

  getv(vec) {
    return this.data[this.width*this.depth*vec[2] + this.width*vec[1] + vec[0]]
  }

  update(text) {
    const lines = text.split(/\r?\n/)
    const dims  = lines[0].split(/\s+/)
    if(dims.length !== 3) {
      throw Error('Expected three dimensions.')
    }

    const width  = parseInt(dims[0])
    const depth  = parseInt(dims[1])
    const height = parseInt(dims[2])

    if(isNaN(width))  throw Error('Width is not a number.')
    if(isNaN(depth))  throw Error('Depth is not a number.')
    if(isNaN(height)) throw Error('Height is not a number.')

    const data = new Uint8Array(width * depth * height)

    let line_index = 1
    let data_index = 0
    for(let z = 0; z < height; ++z) {
      if(lines[line_index++] !== '') {
        throw Error(`Expected an empty line on line ${line_index}.`)
      }

      for(let y = 0; y < depth; ++y) {
        const line = lines[line_index++]
        if(line.length !== width / 4) {
          throw Error(`Incorrect line length on line ${line_index}.`)
        }

        for(let i = 0; i < line.length; ++i) {
          const digit = parseInt(line[i], 16)
          if(isNaN(digit)) {
            throw Error(`Found a non-hex digit on line ${line_index}.`)
          }

          data[data_index++] = (digit & 8) >> 3
          data[data_index++] = (digit & 4) >> 2
          data[data_index++] = (digit & 2) >> 1
          data[data_index++] = (digit & 1) >> 0
        }
      }
    }

    this.width  = width
    this.depth  = depth
    this.height = height
    this.data   = data
  }

  validate_path(src, moves) {
    let error = this.validate_source(src)
    if(error) {
      return [[], error]
    }

    const point =  vec3.clone(src)
    const next  =  vec3.create()
    const path  = [vec3.clone(src)]

    for(let i = 0; i < moves.length; ++i) {
      const move = moves[i]
      if(move === 'n') {
        vec3.subtract(next, point, [0, 1, 0])
        if(next[1] < 0) {
          path.push(vec3.clone(next))
          return [path, 'Walked off the north edge.']
        }
      }
      else if(move === 'e') {
        vec3.add(next, point, [1, 0, 0])
        if(next[0] >= this.width) {
          path.push(vec3.clone(next))
          return [path, 'Walked off the east edge.']
        }
      }
      else if(move === 's') {
        vec3.add(next, point, [0, 1, 0])
        if(next[1] >= this.depth) {
          path.push(vec3.clone(next))
          return [path, 'Walked off the south edge.']
        }
      }
      else if(move === 'w') {
        vec3.subtract(next, point, [1, 0, 0])
        if(next[0] < 0) {
          path.push(vec3.clone(next))
          return [path, 'Walked off the west edge.']
        }
      }
      else {
        return [path, 'Unknown move: \'' + move + '\'']
      }

      if(this.getv(next)) {
        const pup = vec3.create()
        const nup = vec3.create()
        vec3.add(pup, point, [0, 0, 1])
        vec3.add(nup, next,  [0, 0, 1])

        if(pup[2] >= this.height) {
          path.push(vec3.clone(pup))
          return [path, 'Climbed into space.']
        }

        if(this.getv(nup)) {
          path.push(vec3.clone(next))
          return [path, 'Walked into a wall.']
        }

        path.push(vec3.clone(pup))
        if(this.getv(pup)) {
          return [path, 'Jumped into the ceiling.']
        }
        else {
          vec3.copy(point, nup)
          path.push(vec3.clone(nup))
        }
      }
      else {
        const down = vec3.create()
        while(true) {
          path.push(vec3.clone(next))
          vec3.subtract(down, next, [0, 0, 1])

          if(down[2] < 0) {
            path.push(vec3.clone(down))
            return [path, 'Fell into the water.']
          }
          else if(this.getv(down)) {
            vec3.copy(point, next)
            break
          }
          else {
            vec3.copy(next, down)
          }
        }
      }
    }

    return [path, null]
  }

  validate_point(point) {
    if(point[0] < 0 || point[0] >= this.width) {
      return 'X coordinate out of bounds.'
    }
    if(point[1] < 0 || point[1] >= this.depth) {
      return 'Y coordinate out of bounds.'
    }
    if(point[2] < 0 || point[2] >= this.height) {
      return 'Z coordinate out of bounds.'
    }
  }

  validate_source(point) {
    if(!point) {
      return 'Unknown source point.'
    }

    if(this.validate_point(point)) {
      return 'Source point is out of bounds.'
    }

    if(this.getv(point)) {
      return 'Source point is underground.'
    }

    const down = vec3.create()
    vec3.subtract(down, point, [0, 0, 1])
    if(down[0] < 0 || !this.getv(down)) {
      return 'Source point is in midair.'
    }
  }
}
