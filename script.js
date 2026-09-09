/**
 * BlockRush - Interactive Game Controller & SPA Router
 */

document.addEventListener('DOMContentLoaded', () => {
  // Screen Elements
  const screenLoader = document.getElementById('screen-loader');
  const screenMenu = document.getElementById('screen-menu');
  const screenGame = document.getElementById('screen-game');
  const screenWeekly = document.getElementById('screen-weekly-challenge');
  const screenPlayground = document.getElementById('screen-playground-select');
  const screenSupport = document.getElementById('screen-support');
  const screenTerms = document.getElementById('screen-terms');

  // Modals
  const modalVictory = document.getElementById('modal-victory');
  const modalHelp = document.getElementById('modal-help');

  // Navigation Buttons & Footer Links
  const btnStart = document.getElementById('btn-start');
  const btnChallenge = document.getElementById('btn-challenge');
  const btnPlayground = document.getElementById('btn-playground');

  const btnBackWeekly = document.getElementById('btn-back-weekly');
  const btnBackPlayground = document.getElementById('btn-back-playground');
  const btnBackSupport = document.getElementById('btn-back-support');
  const btnBackTerms = document.getElementById('btn-back-terms');
  const btnExit = document.getElementById('btn-exit');
  const btnPause = document.getElementById('btn-pause');

  const linkSupport = document.getElementById('link-support');
  const linkTerms = document.getElementById('link-terms');

  // Toolbar & Theme
  const btnTheme = document.getElementById('btn-theme');
  const btnHelp = document.getElementById('btn-help');
  const btnInfo = document.getElementById('btn-info');
  const btnCloseHelp = document.getElementById('btn-close-help');
  const btnAudio = document.getElementById('btn-audio');

  // Game UI & Board Elements
  const gameBoard = document.getElementById('game-board');
  const levelNum = document.getElementById('level-num');
  const currentLevelText = document.getElementById('current-level-text');
  const gameModeTitle = document.getElementById('game-mode-title');
  const challengeTimerContainer = document.getElementById('challenge-timer-container');
  const timerFill = document.getElementById('timer-fill');
  const timerDisplay = document.getElementById('timer-display');

  // Victory Modal Actions
  const victoryLvl = document.getElementById('victory-lvl');
  const btnRetry = document.getElementById('btn-retry');
  const btnContinue = document.getElementById('btn-continue');
  const pgBeginner = document.getElementById('pg-beginner');

  // State
  let currentScreen = 'menu';
  let gameMode = 'classic'; // 'classic', 'challenge', 'playground'
  let currentLevel = 1;
  let targetValue = 16;
  let gridRows = 2;
  let gridCols = 2;
  let board = [];
  let timerInterval = null;
  let timeLeft = 10;
  let soundEnabled = true;

  // Dual-Phase Loader Sequence (Matching Figma Loader_01 & Loader_02)
  const loaderPhase1 = document.getElementById('loader-phase-1');
  const loaderPhase2 = document.getElementById('loader-phase-2');

  // Phase 1 (Ghostofzenin Intro) -> Phase 2 (BlockRush 8-block U-Shape Animated Grid)
  setTimeout(() => {
    if (loaderPhase1) loaderPhase1.classList.remove('active');
    if (loaderPhase2) loaderPhase2.classList.add('active');
  }, 1200);

  // Phase 2 -> Main Menu
  setTimeout(() => {
    switchScreen('menu');
  }, 2800);

  // Native Web Audio API Synthesizer (Zero external file dependencies)
  class WebAudioSynthesizer {
    constructor() {
      this.ctx = null;
    }

    init() {
      if (!this.ctx) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (AudioCtx) this.ctx = new AudioCtx();
      }
      if (this.ctx && this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
    }

    playMove() {
      if (!soundEnabled) return;
      this.init();
      if (!this.ctx) return;

      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(160, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(320, this.ctx.currentTime + 0.08);

      gain.gain.setValueAtTime(0.15, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.08);

      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.08);
    }

    playMerge(value) {
      if (!soundEnabled) return;
      this.init();
      if (!this.ctx) return;

      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';

      const baseFreq = 220 * Math.pow(1.12, Math.log2(value || 2));
      osc.frequency.setValueAtTime(baseFreq, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(baseFreq * 1.4, this.ctx.currentTime + 0.15);

      gain.gain.setValueAtTime(0.25, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.18);

      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.18);
    }

    playClick() {
      if (!soundEnabled) return;
      this.init();
      if (!this.ctx) return;

      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(550, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(220, this.ctx.currentTime + 0.05);

      gain.gain.setValueAtTime(0.12, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.05);

      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.05);
    }

    playVictory() {
      if (!soundEnabled) return;
      this.init();
      if (!this.ctx) return;

      const notes = [261.63, 329.63, 392.00, 523.25];
      notes.forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime + idx * 0.08);

        gain.gain.setValueAtTime(0.2, this.ctx.currentTime + idx * 0.08);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + idx * 0.08 + 0.25);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(this.ctx.currentTime + idx * 0.08);
        osc.stop(this.ctx.currentTime + idx * 0.08 + 0.25);
      });
    }
  }

  const audioSynth = new WebAudioSynthesizer();

  // Screen Switcher Helper
  function switchScreen(target) {
    audioSynth.playClick();
    [screenLoader, screenMenu, screenGame, screenWeekly, screenPlayground, screenSupport, screenTerms].forEach(s => {
      if (s) s.classList.remove('active');
    });

    if (target === 'menu') screenMenu.classList.add('active');
    else if (target === 'game') screenGame.classList.add('active');
    else if (target === 'weekly') screenWeekly.classList.add('active');
    else if (target === 'playground') screenPlayground.classList.add('active');
    else if (target === 'support') screenSupport.classList.add('active');
    else if (target === 'terms') screenTerms.classList.add('active');

    currentScreen = target;
  }

  // Theme Toggle Handler
  btnTheme.addEventListener('click', () => {
    audioSynth.playClick();
    const html = document.documentElement;
    const isDark = html.getAttribute('data-theme') === 'dark';
    html.setAttribute('data-theme', isDark ? 'light' : 'dark');
  });

  // Help & Info Toolbar Handlers
  if (btnHelp) {
    btnHelp.addEventListener('click', () => {
      audioSynth.playClick();
      if (modalHelp) modalHelp.classList.remove('hidden');
    });
  }
  if (btnInfo) {
    btnInfo.addEventListener('click', () => {
      audioSynth.playClick();
      switchScreen('support');
    });
  }
  if (btnCloseHelp) {
    btnCloseHelp.addEventListener('click', () => {
      audioSynth.playClick();
      if (modalHelp) modalHelp.classList.add('hidden');
    });
  }

  // Footer Link Handlers
  if (linkSupport) {
    linkSupport.addEventListener('click', () => switchScreen('support'));
  }
  if (linkTerms) {
    linkTerms.addEventListener('click', () => switchScreen('terms'));
  }

  // Back Button Handlers
  if (btnBackWeekly) btnBackWeekly.addEventListener('click', () => switchScreen('menu'));
  if (btnBackPlayground) btnBackPlayground.addEventListener('click', () => switchScreen('menu'));
  if (btnBackSupport) btnBackSupport.addEventListener('click', () => switchScreen('menu'));
  if (btnBackTerms) btnBackTerms.addEventListener('click', () => switchScreen('menu'));

  // Support Sub-nav Tab Switching
  document.querySelectorAll('.subnav-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      audioSynth.playClick();
      document.querySelectorAll('.subnav-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const targetId = tab.getAttribute('data-target');
      const sec = document.getElementById(targetId);
      if (sec) sec.scrollIntoView({ behavior: 'smooth' });
    });
  });

  // Support Query Form Handler
  const supportQueryForm = document.getElementById('support-query-form');
  const queryToast = document.getElementById('query-toast');
  if (supportQueryForm) {
    supportQueryForm.addEventListener('submit', (e) => {
      e.preventDefault();
      audioSynth.playVictory();
      if (queryToast) {
        queryToast.classList.remove('hidden');
        setTimeout(() => queryToast.classList.add('hidden'), 3500);
      }
      supportQueryForm.reset();
    });
  }

  // Audio Toggle
  btnAudio.addEventListener('click', () => {
    soundEnabled = !soundEnabled;
    btnAudio.style.opacity = soundEnabled ? '1' : '0.4';
  });

  // Navigation Click Event Listeners
  btnStart.addEventListener('click', () => {
    audioSynth.playClick();
    gameMode = 'classic';
    currentLevel = 1;
    startNewGame(2, 2, 16, 'Challenge', '0/10', 'Level 1');
  });

  btnChallenge.addEventListener('click', () => {
    audioSynth.playClick();
    switchScreen('weekly');
  });

  btnPlayground.addEventListener('click', () => {
    audioSynth.playClick();
    switchScreen('playground');
  });

  // Playground Card Mode Handlers
  if (pgBeginner) {
    pgBeginner.addEventListener('click', () => {
      audioSynth.playClick();
      gameMode = 'playground';
      currentLevel = 2;
      startNewGame(3, 4, 64, 'Playground', 'Level 2', 'Beginner');
    });
  }

  const pgPro = document.getElementById('pg-pro');
  if (pgPro) {
    pgPro.addEventListener('click', () => {
      audioSynth.playClick();
      gameMode = 'playground';
      currentLevel = 5;
      startNewGame(4, 4, 128, 'Playground', 'Level 5', 'Pro');
    });
  }

  const pgMaster = document.getElementById('pg-master');
  if (pgMaster) {
    pgMaster.addEventListener('click', () => {
      audioSynth.playClick();
      gameMode = 'playground';
      currentLevel = 10;
      startNewGame(4, 4, 256, 'Playground', 'Level 10', 'Master');
    });
  }

  const btnRushLevel = document.getElementById('btn-rush-level');
  if (btnRushLevel) {
    btnRushLevel.addEventListener('click', () => {
      audioSynth.playVictory();
      gameMode = 'playground';
      currentLevel = 1;
      startNewGame(3, 3, 32, 'Playground', 'Level 1', 'Math Rush');
    });
  }

  btnExit.addEventListener('click', () => {
    audioSynth.playClick();
    clearInterval(timerInterval);
    switchScreen('menu');
  });

  btnPause.addEventListener('click', () => {
    audioSynth.playClick();
    alert('Game Paused. Click OK to resume.');
  });

  // Victory Button Listeners
  btnRetry.addEventListener('click', () => {
    audioSynth.playClick();
    modalVictory.classList.add('hidden');
    startNewGame(gridRows, gridCols, targetValue, gameModeTitle.textContent, levelNum.textContent, currentLevelText.textContent);
  });

  btnContinue.addEventListener('click', () => {
    audioSynth.playClick();
    modalVictory.classList.add('hidden');
    currentLevel++;
    if (gridRows === 2 && gridCols === 2) {
      startNewGame(3, 4, 32, 'Challenge', `${currentLevel}/10`, `Level ${currentLevel}`);
    } else {
      startNewGame(4, 4, 64, 'Challenge', `${currentLevel}/10`, `Level ${currentLevel}`);
    }
  });

  // Keybindings (Keyboard Controls)
  window.addEventListener('keydown', (e) => {
    if (!modalVictory.classList.contains('hidden')) {
      if (e.key.toLowerCase() === 'r') btnRetry.click();
      if (e.key === 'Enter') btnContinue.click();
      return;
    }

    if (currentScreen !== 'game') return;

    let res = { moved: false, merges: [] };
    if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') res = move('up');
    else if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') res = move('down');
    else if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') res = move('left');
    else if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') res = move('right');

    if (res.moved) {
      spawnRandomTile();
      renderBoard(res.merges);
      if (res.merges && res.merges.length > 0) {
        const topVal = Math.max(...res.merges.map(m => m.val));
        audioSynth.playMerge(topVal);
      } else {
        audioSynth.playMove();
      }
      checkGameState();
    }
  });

  // START GAME ENGINE LOGIC
  function startNewGame(rows, cols, target, modeLabel, levelVal, levelTag) {
    gridRows = rows;
    gridCols = cols;
    targetValue = target;

    gameModeTitle.textContent = modeLabel;
    levelNum.textContent = levelVal;
    currentLevelText.textContent = levelTag;

    // Adjust CSS Grid Class
    gameBoard.className = 'board-grid';
    if (rows === 2 && cols === 2) gameBoard.classList.add('grid-2x2');
    else if (rows === 3 && cols === 4) gameBoard.classList.add('grid-3x4');
    else gameBoard.classList.add('grid-4x4');

    // Handle Challenge Mode Timer
    clearInterval(timerInterval);
    if (modeLabel.toLowerCase().includes('challenge') || gameMode === 'challenge') {
      challengeTimerContainer.classList.remove('hidden');
      startTimer(10);
    } else {
      challengeTimerContainer.classList.add('hidden');
    }

    // Initialize Empty Board Grid
    board = Array(gridRows).fill(null).map(() => Array(gridCols).fill(0));

    // Initial Spawns
    spawnRandomTile();
    spawnRandomTile();

    renderBoard();
    switchScreen('game');
  }

  // Timer Bar Manager
  function startTimer(seconds) {
    timeLeft = seconds;
    updateTimerUI();

    timerInterval = setInterval(() => {
      timeLeft -= 0.1;
      if (timeLeft <= 0) {
        timeLeft = 0;
        clearInterval(timerInterval);
        alert('Time is up! Try again.');
        startNewGame(gridRows, gridCols, targetValue, gameModeTitle.textContent, levelNum.textContent, currentLevelText.textContent);
      }
      updateTimerUI();
    }, 100);
  }

  function updateTimerUI() {
    const pct = (timeLeft / 10) * 100;
    timerFill.style.height = `${pct}%`;
    const secs = Math.ceil(timeLeft);
    timerDisplay.textContent = `00 : ${secs < 10 ? '0' + secs : secs}`;
  }

  // Particle & Floating Score FX Manager
  function triggerMergeFX(tileElem, val) {
    if (!tileElem) return;
    const rect = tileElem.getBoundingClientRect();
    const boardRect = gameBoard.getBoundingClientRect();

    const x = rect.left - boardRect.left + rect.width / 2;
    const y = rect.top - boardRect.top + rect.height / 2;

    // 1. Floating Score Text (+X)
    const scoreElem = document.createElement('div');
    scoreElem.className = 'score-float';
    scoreElem.textContent = `+${val}`;
    scoreElem.style.left = `${x}px`;
    scoreElem.style.top = `${y}px`;
    gameBoard.appendChild(scoreElem);
    setTimeout(() => scoreElem.remove(), 850);

    // 2. Particle Burst Sparks
    const colors = ['#ffbd00', '#ff5400', '#ff0054', '#9e0059', '#390099', '#04c7fd'];
    for (let i = 0; i < 12; i++) {
      const p = document.createElement('div');
      p.className = 'fx-particle';
      const angle = (i / 12) * Math.PI * 2 + (Math.random() * 0.4 - 0.2);
      const dist = 30 + Math.random() * 40;
      const dx = Math.cos(angle) * dist;
      const dy = Math.sin(angle) * dist;

      p.style.left = `${x}px`;
      p.style.top = `${y}px`;
      p.style.setProperty('--dx', `${dx}px`);
      p.style.setProperty('--dy', `${dy}px`);
      p.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];

      gameBoard.appendChild(p);
      setTimeout(() => p.remove(), 650);
    }

    // 3. Screen Shake for High-Value Merges (>= 128)
    if (val >= 128) {
      gameBoard.classList.add('screen-shake');
      setTimeout(() => gameBoard.classList.remove('screen-shake'), 220);
    }
  }

  // Board Renderer with FX Support
  function renderBoard(mergedList = []) {
    gameBoard.innerHTML = '';
    for (let r = 0; r < gridRows; r++) {
      for (let c = 0; c < gridCols; c++) {
        const val = board[r][c];
        const tile = document.createElement('div');
        if (val > 0) {
          tile.className = `g-tile t-${val}`;
          tile.textContent = val;

          const isMerged = mergedList.find(m => m.r === r && m.c === c);
          if (isMerged) {
            tile.classList.add('tile-merged');
            setTimeout(() => triggerMergeFX(tile, isMerged.val), 20);
          }
        } else {
          tile.className = 'g-tile empty-cell';
          tile.style.background = 'rgba(255, 255, 255, 0.05)';
        }
        gameBoard.appendChild(tile);
      }
    }
  }

  // Spawn Random Tile
  function spawnRandomTile() {
    const emptyCells = [];
    for (let r = 0; r < gridRows; r++) {
      for (let c = 0; c < gridCols; c++) {
        if (board[r][c] === 0) emptyCells.push({ r, c });
      }
    }

    if (emptyCells.length > 0) {
      const idx = Math.floor(Math.random() * emptyCells.length);
      const cell = emptyCells[idx];
      board[cell.r][cell.c] = Math.random() < 0.8 ? 2 : 4;
    }
  }

  // Move & Merge Logic returning moved status and merged tiles list
  function move(direction) {
    let moved = false;
    let merges = [];

    if (direction === 'left') {
      for (let r = 0; r < gridRows; r++) {
        let row = board[r].filter(val => val !== 0);
        for (let i = 0; i < row.length - 1; i++) {
          if (row[i] === row[i + 1]) {
            row[i] *= 2;
            row[i + 1] = 0;
            merges.push({ r, c: i, val: row[i] });
            moved = true;
          }
        }
        row = row.filter(val => val !== 0);
        while (row.length < gridCols) row.push(0);
        if (JSON.stringify(board[r]) !== JSON.stringify(row)) moved = true;
        board[r] = row;
      }
    } else if (direction === 'right') {
      for (let r = 0; r < gridRows; r++) {
        let row = board[r].filter(val => val !== 0);
        for (let i = row.length - 1; i > 0; i--) {
          if (row[i] === row[i - 1]) {
            row[i] *= 2;
            row[i - 1] = 0;
            merges.push({ r, c: gridCols - 1 - (row.length - 1 - i), val: row[i] });
            moved = true;
          }
        }
        row = row.filter(val => val !== 0);
        while (row.length < gridCols) row.unshift(0);
        if (JSON.stringify(board[r]) !== JSON.stringify(row)) moved = true;
        board[r] = row;
      }
    } else if (direction === 'up') {
      for (let c = 0; c < gridCols; c++) {
        let col = [];
        for (let r = 0; r < gridRows; r++) if (board[r][c] !== 0) col.push(board[r][c]);
        for (let i = 0; i < col.length - 1; i++) {
          if (col[i] === col[i + 1]) {
            col[i] *= 2;
            col[i + 1] = 0;
            merges.push({ r: i, c, val: col[i] });
            moved = true;
          }
        }
        col = col.filter(val => val !== 0);
        while (col.length < gridRows) col.push(0);
        for (let r = 0; r < gridRows; r++) {
          if (board[r][c] !== col[r]) moved = true;
          board[r][c] = col[r];
        }
      }
    } else if (direction === 'down') {
      for (let c = 0; c < gridCols; c++) {
        let col = [];
        for (let r = 0; r < gridRows; r++) if (board[r][c] !== 0) col.push(board[r][c]);
        for (let i = col.length - 1; i > 0; i--) {
          if (col[i] === col[i - 1]) {
            col[i] *= 2;
            col[i - 1] = 0;
            merges.push({ r: gridRows - 1 - (col.length - 1 - i), c, val: col[i] });
            moved = true;
          }
        }
        col = col.filter(val => val !== 0);
        while (col.length < gridRows) col.unshift(0);
        for (let r = 0; r < gridRows; r++) {
          if (board[r][c] !== col[r]) moved = true;
          board[r][c] = col[r];
        }
      }
    }

    return { moved, merges };
  }

  // Check Game State (Victory condition)
  function checkGameState() {
    for (let r = 0; r < gridRows; r++) {
      for (let c = 0; c < gridCols; c++) {
        if (board[r][c] >= targetValue) {
          clearInterval(timerInterval);
          victoryLvl.textContent = currentLevel;
          audioSynth.playVictory();
          setTimeout(() => {
            modalVictory.classList.remove('hidden');
          }, 300);
          return;
        }
      }
    }
  }

});
