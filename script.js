// Initialize canvas and context
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Player properties
const player = {
  x: canvas.width / 2,
  y: canvas.height - 30,
  width: 50,
  height: 30,
  speed: 5,
  dx: 0,
  color: 'green',
  shielded: false,
  armor: 0
};

// Enemy properties
const enemies = [];
let enemySpeed = 1;
const enemyWidth = 40;
const enemyHeight = 20;

// Enemy shooting properties
const enemyBullets = [];
const enemyBulletSpeed = 3;

// Bullet properties
const bullets = [];
const bulletSpeed = 7;

// Power-up properties
const powerUps = [];

// Power-up types
const powerUpTypes = [
  { type: 'scoreBoost', color: 'orange', duration: 30000, effect: () => { score += 50; } },
  { type: 'speedBoost', color: 'purple', duration: 30000, effect: () => { player.speed *= 1.5; setTimeout(() => { player.speed /= 1.5; }, 30000); } },
  { type: 'shield', color: 'cyan', duration: 60000, effect: () => { player.shielded = true; setTimeout(() => { player.shielded = false; }, 60000); } },
  { type: 'armor', color: 'blue', duration: 120000, effect: () => { player.armor += 1; } }
];

// Score properties
let score = 0;

// Level properties
let currentLevel = 1;
const maxLevels = 5;

// Ship selection properties
const ships = [
  { speed: 5, color: 'green' },
  { speed: 7, color: 'blue' },
  { speed: 4, color: 'red' }
];
let selectedShip = 0;

// Diverse enemy types
const enemyTypes = [
  { type: 'normal', color: 'red', speedMultiplier: 1 },
  { type: 'fast', color: 'yellow', speedMultiplier: 1.5 },
  { type: 'strong', color: 'blue', speedMultiplier: 0.5 }
];

// Commenting out audio elements to focus on core functionality
// const shootSound = new Audio('sounds/shoot.mp3');
// const explosionSound = new Audio('sounds/explosion.mp3');
// const powerUpSound = new Audio('sounds/powerup.mp3');
// const backgroundMusic = new Audio('sounds/background.mp3');

// shootSound.onerror = () => console.error('Shoot sound cannot be played. Check file path or format.');
// explosionSound.onerror = () => console.error('Explosion sound cannot be played. Check file path or format.');
// powerUpSound.onerror = () => console.error('Power-up sound cannot be played. Check file path or format.');
// backgroundMusic.onerror = () => console.error('Background music cannot be played. Check file path or format.');

// Player movement
function movePlayer() {
  player.x += player.dx;

  // Prevent player from going out of bounds
  if (player.x < 0) {
    player.x = 0;
  } else if (player.x + player.width > canvas.width) {
    player.x = canvas.width - player.width;
  }
}

// Draw player
function drawPlayer() {
  ctx.fillStyle = player.color;
  ctx.fillRect(player.x, player.y, player.width, player.height);
}

// Create enemies with different types
function createEnemies(rows, cols) {
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      const enemyType = enemyTypes[Math.floor(Math.random() * enemyTypes.length)];
      enemies.push({
        x: col * (enemyWidth + 10),
        y: row * (enemyHeight + 10),
        width: enemyWidth,
        height: enemyHeight,
        color: enemyType.color,
        speedMultiplier: enemyType.speedMultiplier,
        type: enemyType.type
      });
    }
  }
}

// Draw enemies
function drawEnemies() {
  enemies.forEach(enemy => {
    ctx.fillStyle = enemy.color;
    ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
  });
}

// Enhanced enemy movement patterns
function updateEnemies() {
  enemies.forEach((enemy, index) => {
    // Implement zigzag movement for 'fast' enemies
    if (enemy.type === 'fast') {
      enemy.y += enemySpeed * enemy.speedMultiplier * Math.sin(Date.now() / 1000);
    }

    // Standard horizontal movement
    enemy.x += enemySpeed * enemy.speedMultiplier;

    // Reverse direction if an enemy hits the edge
    if (enemy.x + enemy.width > canvas.width || enemy.x < 0) {
      enemySpeed *= -1;
      enemies.forEach(e => e.y += enemyHeight); // Move enemies down
    }

    // Remove enemies that move off-screen
    if (enemy.y > canvas.height) {
      enemies.splice(index, 1);
    }

    // Enemies shoot back starting from level 5 with reduced frequency
    if (currentLevel >= 5 && Math.random() < 0.005) {
      enemyShoot(enemy);
    }
  });
}

// Update bullets
function updateBullets() {
  bullets.forEach((bullet, index) => {
    bullet.y -= bulletSpeed;

    // Remove bullets that go off-screen
    if (bullet.y + bullet.height < 0) {
      bullets.splice(index, 1);
    }
  });
}

// Draw bullets
function drawBullets() {
  ctx.fillStyle = 'yellow';
  bullets.forEach(bullet => {
    ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
  });
}

// Function to shoot a bullet
function shootBullet() {
  bullets.push({
    x: player.x + player.width / 2,
    y: player.y,
    width: 5,
    height: 10
  });
  // shootSound.play();
}

// Function for enemies to shoot
function enemyShoot(enemy) {
  enemyBullets.push({
    x: enemy.x + enemy.width / 2,
    y: enemy.y + enemy.height,
    width: 5,
    height: 10
  });
}

// Update enemy bullets
function updateEnemyBullets() {
  enemyBullets.forEach((bullet, index) => {
    bullet.y += enemyBulletSpeed;

    // Remove bullets that go off-screen
    if (bullet.y > canvas.height) {
      enemyBullets.splice(index, 1);
    }

    // Check collision with player
    if (
      bullet.x < player.x + player.width &&
      bullet.x + bullet.width > player.x &&
      bullet.y < player.y + player.height &&
      bullet.y + bullet.height > player.y
    ) {
      if (!player.shielded) {
        endGame();
      } else {
        enemyBullets.splice(index, 1);
      }
    }
  });
}

// Draw enemy bullets
function drawEnemyBullets() {
  ctx.fillStyle = 'red';
  enemyBullets.forEach(bullet => {
    ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
  });
}

// Enhanced collision detection
function detectCollisions() {
  bullets.forEach((bullet, bulletIndex) => {
    enemies.forEach((enemy, enemyIndex) => {
      if (
        bullet.x < enemy.x + enemy.width &&
        bullet.x + bullet.width > enemy.x &&
        bullet.y < enemy.y + enemy.height &&
        bullet.y + bullet.height > enemy.y
      ) {
        // Remove bullet and enemy on collision
        bullets.splice(bulletIndex, 1);
        enemies.splice(enemyIndex, 1);
        score += 10; // Increase score when hitting an enemy
        // explosionSound.play();
        updateScore();
      }
    });

    powerUps.forEach((powerUp, powerUpIndex) => {
      if (
        bullet.x < powerUp.x + powerUp.width &&
        bullet.x + bullet.width > powerUp.x &&
        bullet.y < powerUp.y + powerUp.height &&
        bullet.y + bullet.height > powerUp.y
      ) {
        // Remove bullet and activate power-up effect
        bullets.splice(bulletIndex, 1);
        powerUps.splice(powerUpIndex, 1);
        powerUp.effect(); // Apply power-up effect
        // powerUpSound.play();
        updateScore();
      }
    });
  });

  // Check collision between player and enemies
  enemies.forEach((enemy, enemyIndex) => {
    if (
      player.x < enemy.x + enemy.width &&
      player.x + player.width > enemy.x &&
      player.y < enemy.y + enemy.height &&
      player.y + player.height > enemy.y
    ) {
      if (!player.shielded && player.armor === 0) {
        endGame();
      } else if (player.armor > 0) {
        player.armor -= 1;
        enemies.splice(enemyIndex, 1);
      } else {
        enemies.splice(enemyIndex, 1);
      }
    }
  });
}

// Function to start a new level
function startLevel(level) {
  enemies.length = 0; // Clear existing enemies
  createEnemies(level + 2, 8); // Increase rows with each level
  player.speed = ships[selectedShip].speed;
}

// Function to change ship
function changeShip() {
  selectedShip = (selectedShip + 1) % ships.length;
  player.speed = ships[selectedShip].speed;
  player.color = ships[selectedShip].color;
}

// Check if level is complete
function checkLevelComplete() {
  if (enemies.length === 0) {
    if (currentLevel < maxLevels) {
      currentLevel++;
      startLevel(currentLevel);
    } else {
      endGame();
    }
  }
}

// Function to update score display
function updateScore() {
  document.getElementById('score').textContent = `Score: ${score}`;
}

// Save score to local storage
function saveScore() {
  localStorage.setItem('highScore', score);
}

// Load score from local storage
function loadScore() {
  const savedScore = localStorage.getItem('highScore');
  if (savedScore) {
    score = parseInt(savedScore, 10);
    updateScore();
  }
}

// Function to create a random power-up
function createRandomPowerUp() {
  const x = Math.random() * (canvas.width - 20);
  const y = Math.random() * (canvas.height / 2);
  const powerUpType = powerUpTypes[Math.floor(Math.random() * powerUpTypes.length)];
  powerUps.push({
    x: x,
    y: y,
    width: 20,
    height: 20,
    active: true,
    type: powerUpType.type,
    color: powerUpType.color,
    effect: powerUpType.effect,
    duration: powerUpType.duration
  });
}

// Update power-ups to fall down the screen
function updatePowerUps() {
  powerUps.forEach((powerUp, index) => {
    if (powerUp.active) {
      // Move power-up down the screen
      powerUp.y += 1;

      // Check collision with player
      if (
        player.x < powerUp.x + powerUp.width &&
        player.x + player.width > powerUp.x &&
        player.y < powerUp.y + powerUp.height &&
        player.y + player.height > powerUp.y
      ) {
        powerUp.active = false;
        powerUps.splice(index, 1);
        powerUp.effect(); // Apply power-up effect
        // powerUpSound.play();
        updateScore();
      }

      // Remove power-ups that go off-screen
      if (powerUp.y > canvas.height) {
        powerUps.splice(index, 1);
      }
    }
  });
}

// Display power-up type
function drawPowerUps() {
  powerUps.forEach(powerUp => {
    if (powerUp.active) {
      ctx.fillStyle = powerUp.color;
      ctx.fillRect(powerUp.x, powerUp.y, powerUp.width, powerUp.height);

      // Display power-up type
      ctx.fillStyle = 'white';
      ctx.font = '10px Arial';
      ctx.fillText(powerUp.type, powerUp.x, powerUp.y - 5);
    }
  });
}

// Responsive canvas scaling
function resizeCanvas() {
  const scale = Math.min(window.innerWidth / canvas.width, window.innerHeight / canvas.height);
  canvas.style.transform = `scale(${scale})`;
  canvas.style.transformOrigin = 'top left';
}

// Event listener for window resize
window.addEventListener('resize', resizeCanvas);

// Function to start the game
function startGame() {
  document.getElementById('startScreen').style.display = 'none';
  document.getElementById('gameScreen').style.display = 'block';
  gameState = 'playing';
  // playBackgroundMusic();
  update();
}

// Function to end the game
function endGame() {
  document.getElementById('gameScreen').style.display = 'none';
  document.getElementById('gameOverScreen').style.display = 'block';
  document.getElementById('finalScore').textContent = score;
  saveScore();
  gameState = 'over';
}

// Restart game without server reset
function restartGame() {
  gameState = 'playing';
  document.getElementById('gameOverScreen').style.display = 'none';
  document.getElementById('gameScreen').style.display = 'block';
  score = 0;
  updateScore();
  currentLevel = 1;
  player.x = canvas.width / 2;
  player.y = canvas.height - 30;
  player.shielded = false;
  player.armor = 0;
  enemies.length = 0;
  bullets.length = 0;
  enemyBullets.length = 0;
  powerUps.length = 0;
  startLevel(currentLevel);
  requestAnimationFrame(update);
}

// Pause game
function pauseGame() {
  if (gameState === 'playing') {
    gameState = 'paused';
    // backgroundMusic.pause();
  } else if (gameState === 'paused') {
    gameState = 'playing';
    // backgroundMusic.play();
    update();
  }
}

// Save game state
function saveGame() {
  try {
    localStorage.setItem('savedScore', score);
    localStorage.setItem('savedLevel', currentLevel);
    alert('Game saved!');
  } catch (e) {
    console.error('Failed to save game:', e);
  }
}

// Quit game
function quitGame() {
  gameState = 'over';
  document.getElementById('gameScreen').style.display = 'none';
  document.getElementById('startScreen').style.display = 'block';
  // Reset game state
  score = 0;
  currentLevel = 1;
  updateScore();
  enemies.length = 0;
  bullets.length = 0;
  enemyBullets.length = 0;
  powerUps.length = 0;
}

// Event listeners for buttons
document.getElementById('playButton').addEventListener('click', startGame);
document.getElementById('restartButton').addEventListener('click', restartGame);
document.getElementById('pauseButton').addEventListener('click', pauseGame);
document.getElementById('saveButton').addEventListener('click', saveGame);
document.getElementById('quitButton').addEventListener('click', quitGame);

// Update game objects
function update() {
  if (gameState !== 'playing') return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  movePlayer();
  updateEnemies();
  updateBullets();
  updateEnemyBullets();
  detectCollisions();
  updatePowerUps();
  drawPlayer();
  drawEnemies();
  drawBullets();
  drawEnemyBullets();
  drawPowerUps();
  checkLevelComplete();

  requestAnimationFrame(update);
}

// Play background music
function playBackgroundMusic() {
  // backgroundMusic.play();
}

// Keydown event
function keyDown(e) {
  if (e.key === 'ArrowRight') {
    player.dx = player.speed;
  } else if (e.key === 'ArrowLeft') {
    player.dx = -player.speed;
  } else if (e.key === ' ') {
    shootBullet();
  } else if (e.key === 'c') {
    changeShip();
  }
}

// Keyup event
function keyUp(e) {
  if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
    player.dx = 0;
  }
}

// Event listeners
window.addEventListener('keydown', keyDown);
window.addEventListener('keyup', keyUp);

// Initialize game
loadScore();
setInterval(createRandomPowerUp, 10000); // Create a power-up every 10 seconds
player.color = ships[selectedShip].color;
startLevel(currentLevel);
resizeCanvas();