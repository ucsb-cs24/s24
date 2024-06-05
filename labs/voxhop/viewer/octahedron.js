class Octahedron {
  constructor(gl) {
    const vshader = `
    uniform mat4 uModelViewMatrix;
    uniform mat4 uProjectionMatrix;
    uniform vec3 uColor;

    attribute vec4 aVertexPosition;
    attribute vec3 aVertexNormal;

    varying vec3 normal;
    varying vec3 color;

    void main() {
      vec4 tmp = uModelViewMatrix * aVertexPosition;
      gl_Position = uProjectionMatrix * tmp;

      normal = aVertexNormal;
      color  = uColor;
    }
    `;

    const fshader = `
    varying mediump vec3 normal;
    varying mediump vec3 color;

    void main() {
      mediump vec3  lighting = vec3(1.0/1.7320508075688772, 1.0/1.7320508075688772, 1.0/1.7320508075688772);
      mediump float angle    = max(0.0, dot(normal, lighting));
      mediump vec3  ambient  = color * 0.6;
      mediump vec3  diffuse  = color * 0.4 * angle;
      // mediump vec3  specular = vec3(1.0, 1.0, 1.0) * 0.1 * pow(angle, 4.0);

      gl_FragColor = vec4(ambient + diffuse, 1.0);
    }
    `;

    this.program = initShaderProgram(gl, vshader, fshader)

    const n = 1.0 / Math.sqrt(3)

    const vertices = new Float32Array([
      // Northwest Top
      0.50, 0.50, 0.25,   -n, +n, -n,
      0.25, 0.50, 0.50,   -n, +n, -n,
      0.50, 0.75, 0.50,   -n, +n, -n,

      // Northeast Top
      0.75, 0.50, 0.50,   +n, +n, -n,
      0.50, 0.50, 0.25,   +n, +n, -n,
      0.50, 0.75, 0.50,   +n, +n, -n,

      // Southeast Top
      0.50, 0.50, 0.75,   +n, +n, +n,
      0.75, 0.50, 0.50,   +n, +n, +n,
      0.50, 0.75, 0.50,   +n, +n, +n,

      // Southwest Top
      0.25, 0.50, 0.50,   -n, +n, +n,
      0.50, 0.50, 0.75,   -n, +n, +n,
      0.50, 0.75, 0.50,   -n, +n, +n,


      // Northwest Bottom
      0.25, 0.50, 0.50,   -n, -n, -n,
      0.50, 0.50, 0.25,   -n, -n, -n,
      0.50, 0.25, 0.50,   -n, -n, -n,

      // Northeast Bottom
      0.50, 0.50, 0.25,   +n, -n, -n,
      0.75, 0.50, 0.50,   +n, -n, -n,
      0.50, 0.25, 0.50,   +n, -n, -n,

      // Southeast Bottom
      0.75, 0.50, 0.50,   +n, -n, +n,
      0.50, 0.50, 0.75,   +n, -n, +n,
      0.50, 0.25, 0.50,   +n, -n, +n,

      // Southwest Bottom
      0.50, 0.50, 0.75,   -n, -n, +n,
      0.25, 0.50, 0.50,   -n, -n, +n,
      0.50, 0.25, 0.50,   -n, -n, +n,
    ])

    this.buffer = gl.createBuffer()
    gl.bindBuffer(gl.ARRAY_BUFFER, this.buffer)
    gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW)

    this.attributes = {
      modelview:  gl.getUniformLocation(this.program, "uModelViewMatrix"),
      projection: gl.getUniformLocation(this.program, "uProjectionMatrix"),
      color:      gl.getUniformLocation(this.program, "uColor"),

      position:   gl.getAttribLocation(this.program,  "aVertexPosition"),
      normal:     gl.getAttribLocation(this.program,  "aVertexNormal"),
    }
  }

  bind(gl, projection) {
    gl.useProgram(this.program)
    gl.bindBuffer(gl.ARRAY_BUFFER, this.buffer)

    gl.vertexAttribPointer(this.attributes.position,
      3,         // three elements per vertex
      gl.FLOAT,  // elements are 32-bit floats
      false,     // don't normalize
      24,        // stride in bytes
      0          // offset in bytes
    )

    gl.vertexAttribPointer(this.attributes.normal,
      3,         // three elements per vertex
      gl.FLOAT,  // elements are 32-bit floats
      false,     // don't normalize
      24,        // stride in bytes
      12         // offset in bytes
    )

    gl.enableVertexAttribArray(this.attributes.position)
    gl.enableVertexAttribArray(this.attributes.normal)

    gl.uniformMatrix4fv(this.attributes.projection, false, projection)
  }

  render(gl, color, modelview) {
    gl.uniformMatrix4fv(this.attributes.modelview, false, modelview);
    gl.uniform3fv(this.attributes.color, color);
    gl.drawArrays(gl.TRIANGLES,
      0,  // index of first vertex
      24  // number of vertices
    )
  }
}
