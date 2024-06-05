// Various HTML Elements
const path_input   = document.getElementById('path')
const path_message = document.getElementById('path-message')
const map_upload   = document.getElementById('upload')
const canvas       = document.getElementById('glcanvas')

// WebGL Rendering Context
const gl = canvas.getContext('webgl')

gl.clearColor(1.0, 1.0, 1.0, 1.0)
gl.clearDepth(1.0)

gl.enable(gl.DEPTH_TEST)
gl.depthFunc(gl.LEQUAL)

gl.enable(gl.CULL_FACE)
gl.cullFace(gl.BACK)

// Renderable Objects
const VOXMAP = new VoxMap()
// const CUBE   = new Cube(gl)
const OCTA   = new Octahedron(gl)

const SLICES = new Slices(gl)
const PATH   = new Path(gl)

// Marker Locations and Colors
const MARKERS = [null, null, null]
const COLORS  = [
  vec3.fromValues(0.0, 0.0, 1.0),
  vec3.fromValues(1.0, 0.0, 0.0),
  vec3.fromValues(0.0, 0.5, 0.0)
]

const CLIPPERS = [
  vec3.fromValues(0, 0, 0),
  vec3.fromValues(0, 0, 0)
]

// Camera Controls
let dis = 5.0  // distance from the camera target
let alt = 0.0  // altitude
let azi = 0.0  // azimuth

// Performance Counters
let FRAMES = 0
let MILLIS = 0



function loadShader(gl, type, source) {
  const shader = gl.createShader(type)
  gl.shaderSource(shader, source)
  gl.compileShader(shader)

  if(!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    const error = gl.getShaderInfoLog(shader)
    gl.deleteShader(shader)
    console.log(error)
    throw Error('Error loading shader: ' + error)
  }

  return shader
}

function initShaderProgram(gl, vsource, fsource) {
  const vshader = loadShader(gl, gl.VERTEX_SHADER,   vsource)
  const fshader = loadShader(gl, gl.FRAGMENT_SHADER, fsource)

  const program = gl.createProgram()
  gl.attachShader(program, vshader)
  gl.attachShader(program, fshader)
  gl.linkProgram(program)

  if(!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    const error = gl.getProgramInfoLog(program)
    gl.deleteProgram(program)
    console.log(error)
    throw Error('Error loading program: ' + error)
  }

  return program
}

function drawScene() {
  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
  if(!VOXMAP.height) return

  const start = window.performance.now()
  // Create a perspective matrix, a special matrix that is
  // used to simulate the distortion of perspective in a camera.
  // Our field of view is 45 degrees, with a width/height
  // ratio that matches the display size of the canvas
  // and we only want to see objects between 0.1 units
  // and 100 units away from the camera.

  const fieldOfView = (45 * Math.PI) / 180; // in radians
  const aspect      = gl.canvas.clientWidth / gl.canvas.clientHeight;
  const zNear       =    0.1;
  const zFar        = 1000.0;

  const projectionMatrix = mat4.create();
  mat4.perspective(projectionMatrix,
    fieldOfView,
    aspect,
    zNear,
    zFar
  )

  const t = Math.cos(alt) * dis
  const z = Math.sin(alt) * dis
  const x = Math.sin(azi) * t
  const y = Math.cos(azi) * t

  const camera = vec3.fromValues(x, z, y)
  const target = vec3.fromValues(VOXMAP.width/2, VOXMAP.height/2, VOXMAP.depth/2)
  vec3.add(camera, camera, target)

  const lookat = mat4.create()
  mat4.lookAt(lookat, camera, target, [0, 1, 0])
  mat4.perspective(projectionMatrix, fieldOfView, aspect, zNear, zFar)
  mat4.multiply(projectionMatrix, projectionMatrix, lookat)


  // Model View Matrix
  const mv = mat4.create()

  // // Draw voxels (too slow):
  // CUBE.bind(gl, projectionMatrix)
  // let i  = 0

  // for(let z = 0; z < VOXMAP.height; ++z) {
  //   for(let y = 0; y < VOXMAP.depth; ++y) {
  //     for(let x = 0; x < VOXMAP.width; ++x) {
  //       if(VOXMAP.data[i++]) {
  //         mat4.fromTranslation(mv, [x, z, y])
  //         CUBE.render(gl, mv)
  //       }
  //     }
  //   }
  // }

  // Draw Faces:
  gl.disable(gl.CULL_FACE)
  SLICES.bind(gl, projectionMatrix)
  SLICES.render(gl, mv, camera, CLIPPERS)
  gl.enable(gl.CULL_FACE)

  // Show markers, if any:
  OCTA.bind(gl, projectionMatrix)
  for(let i = 0; i < 3; ++i) {
    if(MARKERS[i]) {
      const m = MARKERS[i] // World -> GL coordinates
      mat4.fromTranslation(mv, [m[0], m[2], m[1]])
      OCTA.render(gl, COLORS[i], mv)
    }
  }

  // Show the path, if any:
  if(PATH.nverts) {
    mat4.fromTranslation(mv, [0.5, 0.5, 0.5])
    PATH.bind(gl, projectionMatrix)
    PATH.render(gl, mv)
  }

  const stop = window.performance.now()
  MILLIS += stop - start
  FRAMES += 1

  // if(FRAMES % 200 == 0) {
  //   console.log('FPS', FRAMES / MILLIS * 1000)
  //   FRAMES = 0
  //   MILLIS = 0
  // }
}

let DIRTY = false
function render() {
  if(DIRTY) {
    DIRTY = false
    drawScene()
  }
}

function schedule() {
  requestAnimationFrame(render)
  DIRTY = true
}


function reset_clippers() {
  document.querySelectorAll('#controls fieldset.clip').forEach((fset, i) => {
    const div = fset.children[1]
    const x   = (i === 0)? 0 : VOXMAP.width
    const y   = (i === 0)? 0 : VOXMAP.depth
    const z   = (i === 0)? 0 : VOXMAP.height

    div.children[0].setAttribute('max', x)
    div.children[1].setAttribute('max', y)
    div.children[2].setAttribute('max', z)

    div.children[0].value = x
    div.children[1].value = y
    div.children[2].value = z

    CLIPPERS[i][0] = x
    CLIPPERS[i][1] = z
    CLIPPERS[i][2] = y
  })

  schedule()
}

function resize_canvas() {
  const viewport = document.getElementById('viewport')
  canvas.width   = viewport.clientWidth
  canvas.height  = viewport.clientHeight
  gl.viewport(0, 0, canvas.width, canvas.height)

  schedule()
}

function update_clipper(index, div) {
  let x = parseInt(div.children[0].value)
  let y = parseInt(div.children[1].value)
  let z = parseInt(div.children[2].value)

  if(isNaN(x)) x = (index === 0)? 0 : VOXMAP.width
  if(isNaN(y)) y = (index === 0)? 0 : VOXMAP.depth
  if(isNaN(z)) z = (index === 0)? 0 : VOXMAP.height

  CLIPPERS[index][0] = x
  CLIPPERS[index][1] = z
  CLIPPERS[index][2] = y

  schedule()
}

function update_map(text) {
  try {
    VOXMAP.update(text)
    dis = 2 * Math.max(VOXMAP.width, VOXMAP.depth, VOXMAP.height)
    alt = Math.PI / 8
    azi = Math.PI / 8

    FRAMES = 0
    MILLIS = 0

    SLICES.update(gl, VOXMAP)
    reset_clippers()
    update_path()
    schedule()
  }
  catch(error) {
    console.error(error)
    alert('Error reading map:\n' + error)
  }
}

function update_marker(index, div, update) {
  const x = parseInt(div.children[0].value)
  const y = parseInt(div.children[1].value)
  const z = parseInt(div.children[2].value)

  if(isNaN(x) || isNaN(y) || isNaN(z)) {
    MARKERS[index] = undefined
  }
  else {
    MARKERS[index] = vec3.fromValues(x, y, z)
  }

  if(index === 0) {
    update_path()
  }

  if(update) {
    schedule()
  }
}

function update_path() {
  const [points, error] = VOXMAP.validate_path(MARKERS[0], path_input.value)

  if(points.length === 1) {
    path_message.classList.remove('invalid')
    path_message.innerText = 'No path given.'
  }
  else if(error) {
    path_message.classList.add('invalid')
    path_message.innerText = 'Invalid: ' + error
  }
  else {
    path_message.classList.remove('invalid')
    path_message.innerText = 'Valid path.'
  }

  PATH.update(gl, points)
  schedule()
}


// File Reader for Maps
const reader = new FileReader()
reader.addEventListener('error', error => {
  alert('Error loading map: ' + reader.error)
})
reader.addEventListener('load', event => {
  if(reader.readyState === 2) {
    update_map(event.target.result)
  }
})


// Mouse-Based Camera Controls
canvas.addEventListener('mousemove', event => {
  if(event.buttons & 1) {
    alt += event.movementY / 100
    azi -= event.movementX / 100
    schedule()
  }
})

canvas.addEventListener('wheel', event => {
  dis += event.deltaY / 100
  schedule()
})

// Map Upload
map_upload.addEventListener('change', event => {
  reader.readAsText(map_upload.files[0])
})

if(map_upload.files.length) {
  reader.readAsText(map_upload.files[0])
}

// Marker Coordinate Updates
document.querySelectorAll('#controls fieldset.marker').forEach((fset, i) => {
  fset.addEventListener('change', event => {
    update_marker(i, event.target.parentElement, true)
  })

  update_marker(i, fset.children[1])
})

// Marker Coordinate Updates
document.querySelectorAll('#controls fieldset.clip').forEach((fset, i) => {
  fset.addEventListener('change', event => {
    update_clipper(i, event.target.parentElement)
  })
})

// Path Updates
path_input.addEventListener('input', event => {
  update_path(path_input.value)
})

// Resize Handler
window.addEventListener('resize', resize_canvas)

// Gooooooo!
resize_canvas();
