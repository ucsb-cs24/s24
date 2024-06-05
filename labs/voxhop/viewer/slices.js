function slice(n1, n2, n3, getter, putter) {
  let indices = [0]
  let index   =  0

  for(let i = 0; i < n1; ++i) {
    for(let j = 0; j < n2; ++j) {
      let k     = 0
      let start = null
      while(k < n3) {
        if(getter(i, j, k)) {
          if(start === null) {
            start = k
          }
        }
        else {
          if(start !== null) {
            putter(i, j, start, k)
            index += 1
          }

          start = null
        }

        k += 1
      }

      if(start !== null) {
        putter(i, j, start, n3)
      }
    }

    indices.push(index)
  }

  indices.push(index)
  return indices
}

function store(gl, vertices, buffer) {
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer)
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW)
  return vertices.length / 3
}

class Slices {
  constructor(gl, map) {
    const vshader = `
    uniform mat4 uModelViewMatrix;
    uniform mat4 uProjectionMatrix;
    uniform vec3 uNormal;
    uniform vec3 uCamera;

    attribute vec4 aVertexPosition;

    varying vec3 position;
    varying vec3 normal;

    void main() {
      vec4 vp = aVertexPosition;
      if(dot(vp.xyz, uNormal) < dot(uCamera, uNormal)) {
        vp    += vec4(uNormal, 0);
        normal = -uNormal;
      }
      else {
        normal = uNormal;
      }

      vp          = uModelViewMatrix * vp;
      gl_Position = uProjectionMatrix * vp;
      position    = vp.xyz;
    }
    `;

    const fshader = `
    uniform mediump vec3 uMinClip;
    uniform mediump vec3 uMaxClip;

    varying mediump vec3 position;
    varying mediump vec3 normal;

    void main() {
      if(any(lessThan(position, uMinClip))) {
        discard;
      }
      if(any(greaterThan(position, uMaxClip))) {
        discard;
      }

      mediump vec3  alldist = min(fract(position), 1.0 - fract(position)) + abs(normal);
      mediump float mindist = min(min(alldist.x, alldist.y), alldist.z);
      mindist = pow(mindist, 0.05);

      mediump float light = max(0.0, dot(normal, vec3(0.05, -0.15, 0.10)));
      light = min(light + 0.85, 1.0);

      mediump vec3 partial = vec3(light, light, light) * mindist - 0.1 * normal;
      // mediump vec3 partial = vec3(1.0, 1.0, 1.0) * mindist - 0.1 * normal;
      gl_FragColor = vec4(partial, 1.0);
      // gl_FragColor = vec4(normal, 1.0);
    }
    `;

    this.program = initShaderProgram(gl, vshader, fshader)
    this.attributes = {
      modelview:  gl.getUniformLocation(this.program, "uModelViewMatrix"),
      projection: gl.getUniformLocation(this.program, "uProjectionMatrix"),
      normal:     gl.getUniformLocation(this.program, "uNormal"),
      camera:     gl.getUniformLocation(this.program, "uCamera"),
      minclip:    gl.getUniformLocation(this.program, "uMinClip"),
      maxclip:    gl.getUniformLocation(this.program, "uMaxClip"),
      // axis:       gl.getUniformLocation(this.program, "uAxis"),
      position:   gl.getAttribLocation(this.program,  "aVertexPosition"),
    }

    this.xbuffer = gl.createBuffer()
    this.ybuffer = gl.createBuffer()
    this.zbuffer = gl.createBuffer()

    if(map) {
      update(map)
    }
    else {
      this.xlength = 0
      this.ylength = 0
      this.zlength = 0
    }
  }

  bind(gl, projection) {
    gl.useProgram(this.program)
    gl.enableVertexAttribArray(this.attributes.position)
    gl.uniformMatrix4fv(this.attributes.projection, false, projection)
  }

  render(gl, modelview, camera, clip) {
    const mv = mat4.create()
    // console.log(clip)

    gl.uniform3fv(this.attributes.camera,  camera)
    gl.uniform3fv(this.attributes.minclip, clip[0])
    gl.uniform3fv(this.attributes.maxclip, clip[1])
    gl.uniformMatrix4fv(this.attributes.modelview, false, modelview)

    // Draw X Planes
    gl.uniform3f(this.attributes.normal, 1, 0, 0)
    gl.bindBuffer(gl.ARRAY_BUFFER, this.xbuffer)
    gl.vertexAttribPointer(this.attributes.position,
      3,         // three elements per vertex
      gl.FLOAT,  // elements are 32-bit floats
      false,     // don't normalize
      12,        // stride in bytes
      0          // offset in bytes
    )

    // gl.uniformMatrix4fv(this.attributes.modelview, false, modelview);
    gl.drawArrays(gl.TRIANGLES,
      0,            // index of first vertex
      this.xlength  // number of vertices
    )

    // Draw Y Planes
    gl.uniform3f(this.attributes.normal, 0, 0, 1)
    gl.bindBuffer(gl.ARRAY_BUFFER, this.ybuffer)
    gl.vertexAttribPointer(this.attributes.position,
      3,         // three elements per vertex
      gl.FLOAT,  // elements are 32-bit floats
      false,     // don't normalize
      12,        // stride in bytes
      0          // offset in bytes
    )

    // gl.uniformMatrix4fv(this.attributes.modelview, false, modelview);
    gl.drawArrays(gl.TRIANGLES,
      0,            // index of first vertex
      this.ylength  // number of vertices
    )

    // Draw Z Planes
    gl.uniform3f(this.attributes.normal, 0, 1, 0)
    gl.bindBuffer(gl.ARRAY_BUFFER, this.zbuffer)
    gl.vertexAttribPointer(this.attributes.position,
      3,         // three elements per vertex
      gl.FLOAT,  // elements are 32-bit floats
      false,     // don't normalize
      12,        // stride in bytes
      0          // offset in bytes
    )

    // gl.uniformMatrix4fv(this.attributes.modelview, false, modelview);
    gl.drawArrays(gl.TRIANGLES,
      0,            // index of first vertex
      this.zlength  // number of vertices
    )
  }

  update(gl, map) {
    const xdata = []
    const xind  = slice(map.width, map.depth, map.height,
      (x, y, z1)     => map.get(x, y, z1),
      (x, y, z1, z2) => xdata.push(
        x, z1, y + 0,
        x, z1, y + 1,
        x, z2, y + 1,

        x, z2, y + 1,
        x, z2, y + 0,
        x, z1, y + 0,
      )
    )

    const ydata = []
    const yind  = slice(map.depth, map.height, map.width,
      (y, z, x1)     => map.get(x1, y, z),
      (y, z, x1, x2) => ydata.push(
        x1, z + 0, y,
        x1, z + 1, y,
        x2, z + 1, y,

        x2, z + 1, y,
        x2, z + 0, y,
        x1, z + 0, y,
      )
    )

    const zdata = []
    const zind  = slice(map.height, map.width, map.depth,
      (z, x, y1)     => map.get(x, y1, z),
      (z, x, y1, y2) => zdata.push(
        x + 0, z, y1,
        x + 1, z, y1,
        x + 1, z, y2,

        x + 1, z, y2,
        x + 0, z, y2,
        x + 0, z, y1,
      )
    )

    this.xlength = store(gl, xdata, this.xbuffer)
    this.ylength = store(gl, ydata, this.ybuffer)
    this.zlength = store(gl, zdata, this.zbuffer)

    this.xindices = xind
    this.yindices = yind
    this.zindices = zind
  }
}
