import * as THREE from 'three';

// 1. Scene setup
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();

// 2. Camera setup
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(0, 0, 5);

// 3. Renderer setup
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
container.appendChild(renderer.domElement);

// 4. Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1.2);
directionalLight.position.set(5, 5, 5);
scene.add(directionalLight);

// 5. Geometry & Material (Placeholder TorusKnot)
const geometry = new THREE.TorusKnotGeometry(1.2, 0.4, 128, 32);
const material = new THREE.MeshStandardMaterial({
  color: 0x4f46e5,
  roughness: 0.2,
  metalness: 0.8,
});
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);

// 6. Responsive resize handler
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
});

// 7. Animation loop
function animate(time) {
  requestAnimationFrame(animate);
  const t = time * 0.001;
  mesh.rotation.x = t * 0.3;
  mesh.rotation.y = t * 0.5;
  renderer.render(scene, camera);
}

requestAnimationFrame(animate);

