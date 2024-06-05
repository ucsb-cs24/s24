class Path {
  constructor(gl, points=[]) {
    const vshader = `
    uniform mat4 uModelViewMatrix;
    uniform mat4 uProjectionMatrix;

    attribute vec4  aVertexPosition;
    attribute float aVertexProgress;

    varying float progress;

    void main() {
      vec4 tmp = uModelViewMatrix * aVertexPosition;
      gl_Position = uProjectionMatrix * tmp;
      progress = aVertexProgress;
    }
    `;

    const fshader = `
    varying mediump float progress;

    void main() {
      gl_FragColor = vec4(progress, 0.0, 1.0 - progress, 1.0);
    }
    `;

    this.program = initShaderProgram(gl, vshader, fshader)
    this.attributes = {
      modelview:  gl.getUniformLocation(this.program, "uModelViewMatrix"),
      projection: gl.getUniformLocation(this.program, "uProjectionMatrix"),
      position:   gl.getAttribLocation(this.program,  "aVertexPosition"),
      progress:   gl.getAttribLocation(this.program,  "aVertexProgress"),
    }

    this.buffer = gl.createBuffer()
    this.update(gl, points)
  }

  bind(gl, projection) {
    gl.useProgram(this.program)
    gl.bindBuffer(gl.ARRAY_BUFFER, this.buffer)

    gl.vertexAttribPointer(this.attributes.position,
      3,         // three elements per vertex
      gl.FLOAT,  // elements are 32-bit floats
      false,     // don't normalize
      16,        // stride in bytes
      0          // offset in bytes
    )

    gl.vertexAttribPointer(this.attributes.progress,
      1,         // one element per vertex
      gl.FLOAT,  // elements are 32-bit floats
      false,     // don't normalize
      16,        // stride in bytes
      12         // offset in bytes
    )

    gl.enableVertexAttribArray(this.attributes.position)
    gl.enableVertexAttribArray(this.attributes.progress)

    gl.uniformMatrix4fv(this.attributes.projection, false, projection)
  }

  render(gl, modelview) {
    gl.uniformMatrix4fv(this.attributes.modelview, false, modelview)
    gl.drawArrays(gl.LINE_STRIP,
      0,           // index of first vertex
      this.nverts  // number of vertices
    )
  }

  update(gl, points) {
    this.nverts  = points.length

    const vertices = new Float32Array(4 * points.length)
    points.forEach((point, i) => {
      vertices[4*i + 3] = i / (points.length - 1),
      vertices[4*i + 2] = point[1],
      vertices[4*i + 1] = point[2],
      vertices[4*i + 0] = point[0]
    })

    gl.bindBuffer(gl.ARRAY_BUFFER, this.buffer)
    gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.DYNAMIC_DRAW)
  }
}
